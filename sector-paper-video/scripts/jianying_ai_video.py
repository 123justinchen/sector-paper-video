"""
剪映 AI文字成片 —— 自动输入文案并生成视频

用法:
  python jianying_ai_video.py "文案内容..."
  python jianying_ai_video.py --file C:/E/coding/influencer/content/xxx.md
"""
import sys, time, argparse, os, subprocess, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
import uiautomation as auto

# ============================================================
# 坐标表（相对窗口）—— 窗口尺寸不同时用比例计算
# ============================================================
# 首页 (HomePage_QMLTYPE_183, 1168x780)
COORDS_HOME = {
    "popup_cancel":     (660, 550),   # 启动弹窗取消按钮（旧版）
    "popup_cancel_v2":  (870, 163),   # 启动弹窗取消按钮（新版）
    "ai_text_btn":      (320, 230),   # AI文字成片 入口
}
# AI文字成片页 (WebArticleVideoWindow_QMLTYPE_481, 1440x812)
COORDS_AI = {
    "text_input":   (220, 85),    # 文案输入框
    "btn_generate": (1230, 200),  # 生成按钮
    "btn_export":   (1240, 760),  # 导出/下一步
}

# ============================================================
# 自动探测 & 启动剪映
# ============================================================
def detect_jy_exe():
    """探测最新版剪映 exe，优先级: 注册表 > 默认安装路径 > 扫描"""
    # 1) 从注册表找卸载信息（最准确）
    try:
        cmd = 'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall" /s /f "剪映" 2>nul'
        out = subprocess.check_output(cmd, shell=True, text=True, errors='ignore')
        for line in out.splitlines():
            m = re.match(r'\s*DisplayIcon\s+REG_SZ\s+(.+)', line)
            if m and 'JianyingPro' in m.group(1):
                return Path(m.group(1))
    except:
        pass

    # 2) 默认安装路径
    defaults = [
        Path.home() / 'AppData/Local/JianyingPro/Apps',
        Path('C:/Program Files/JianyingPro/Apps'),
        Path('C:/Program Files (x86)/JianyingPro/Apps'),
    ]
    for apps_dir in defaults:
        if apps_dir.exists():
            # 取版本号最新的
            versions = []
            for d in apps_dir.iterdir():
                if d.is_dir() and re.match(r'^\d', d.name):
                    exe = d / 'JianyingPro.exe'
                    if exe.exists():
                        versions.append((d.name, exe))
            if versions:
                versions.sort(key=lambda v: [int(x) for x in v[0].split('.')], reverse=True)
                return versions[0][1]

    # 3) 全盘扫描（慢，兜底）
    for root in [Path.home(), Path('C:/')]:
        try:
            for p in root.rglob('JianyingPro.exe'):
                if 'Apps' in str(p):
                    return p
        except:
            continue
    return None

def launch_jy():
    """启动剪映，等待窗口出现"""
    exe = detect_jy_exe()
    if not exe:
        print("[错误] 找不到剪映安装路径，请手动启动")
        return None

    print(f"[启动] {exe}")
    subprocess.Popen([str(exe)], shell=True)

    # 等待窗口出现（最多 30s）
    for i in range(30):
        time.sleep(1)
        win = find_jy()
        if win:
            print(f"[就绪] 窗口出现，等待初始化...")
            time.sleep(3)  # 等首页加载完
            return find_jy()
        if i % 5 == 4:
            print(f"  等待中... ({i+1}s)")

    print("[错误] 启动超时，请手动检查")
    return None

# ============================================================
def find_jy():
    """找剪映窗口，兼容首页和 AI文字成片两种状态"""
    for w in auto.GetRootControl().GetChildren():
        n = w.Name or ""
        c = w.ClassName or ""
        if ("剪映" in n or "JianyingPro" in n) and "QMLTYPE" in c:
            return w
    return None

def click_rel(win, rel_x, rel_y):
    """按相对坐标点击"""
    r = win.BoundingRectangle
    ax, ay = r.left + rel_x, r.top + rel_y
    auto.Click(ax, ay)
    return ax, ay

def type_text(win, text):
    """在剪映窗口中输入文本（先点一下输入框确保焦点）"""
    r = win.BoundingRectangle
    # 基于当前窗口尺寸，按比例计算输入框位置
    scale_x = r.width() / 1440   # AI文字成片基准宽度
    scale_y = r.height() / 812   # AI文字成片基准高度
    ix = r.left + int(220 * scale_x)
    iy = r.top  + int(85  * scale_y)
    auto.Click(ix, iy)
    time.sleep(0.2)
    auto.SendKeys(text)

def ensure_window_ready():
    """确保剪映在首页、弹窗已关"""
    win = find_jy()
    if win is None:
        print("[提示] 未找到剪映窗口，尝试自动启动...")
        win = launch_jy()
    if win is None:
        print("[错误] 无法启动剪映，请手动启动后重试")
        sys.exit(1)

    r = win.BoundingRectangle
    if r.width() == 0:
        win.ShowWindow(auto.SW_SHOWNORMAL)
        time.sleep(1)

    win.SetFocus()
    time.sleep(0.3)
    return win

def goto_ai_text(win):
    """从首页进入 AI文字成片"""
    r = win.BoundingRectangle
    # 判断是否已在 AI文字成片页
    if "WebArticleVideoWindow" in win.ClassName:
        print("[已是AI文字成片页]")
        return win

    print("[首页] 关闭弹窗...")
    # 先试旧版坐标，不行再试新版
    for label, coord in [("旧版", COORDS_HOME["popup_cancel"]), ("新版", COORDS_HOME["popup_cancel_v2"])]:
        click_rel(win, *coord)
        time.sleep(1.0)
        # 检查弹窗是否还在
        still_there = False
        for child in win.GetChildren():
            if "StartUpFeatureIntroductionDialog" in (child.ClassName or ""):
                still_there = True
                break
        if not still_there:
            print(f"  [{label}] 弹窗已关闭")
            break
        else:
            print(f"  [{label}] 弹窗未关闭，换下一组坐标...")

    time.sleep(0.8)

    print("[首页] 点击 AI文字成片...")
    click_rel(win, *COORDS_HOME["ai_text_btn"])
    time.sleep(1.5)

    # 重新找窗口（进入后类名会变）
    win2 = find_jy()
    if win2:
        win2.SetFocus()
        time.sleep(0.3)
        return win2
    return win

def run_ai_text(text: str):
    """完整流程：打开剪映 → AI文字成片 → 输入文案 → 点击生成"""
    print(f"文案长度: {len(text)} 字")
    print(f"预览: {text[:80]}...\n")

    win = ensure_window_ready()
    win = goto_ai_text(win)

    r = win.BoundingRectangle
    print(f"[AI文字成片] 窗口 {r.width()}x{r.height()}")

    # 输入文案
    print("[输入] 填入文案...")
    type_text(win, text)
    time.sleep(0.3)

    # 点击生成按钮
    print("[点击] 生成按钮...")
    scale_x = r.width() / 1440
    scale_y = r.height() / 812
    click_rel(win, int(1230 * scale_x), int(200 * scale_y))
    time.sleep(0.5)

    # 点击导出/下一步
    print("[点击] 下一步...")
    click_rel(win, int(1240 * scale_x), int(760 * scale_y))

    print("完成 —— 请检查剪映窗口。")

# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="剪映 AI文字成片自动化")
    parser.add_argument("text", nargs="?", help="文案内容（直接输入）")
    parser.add_argument("--file", "-f", help="从文件读取文案（MD 文件会自动提取正文）")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        # 如果是 MD 文件，提取 ## 文案 和 ## 口播文案 之后的内容
        import re
        m = re.search(r'##\s*(口播)?文案\s*\n+(.+)', content, re.DOTALL)
        if m:
            content = m.group(2).strip()
            # 去掉末尾的元数据行（--- 之后的内容）
            content = re.split(r'\n---', content)[0].strip()
        print(f"[文件] {args.file}")
        args.text = content

    if not args.text:
        print("用法: python jianying_ai_video.py '文案内容'")
        print("      python jianying_ai_video.py --file script.md")
        sys.exit(1)

    run_ai_text(args.text)
