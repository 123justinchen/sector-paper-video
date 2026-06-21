# Sector-Paper-Video

从 A 股最热板块出发，用 AI 全自动生成"硬核科技三分钟"深度科普视频。不讲股票、不念影响因子、只讲技术突破和产业逻辑。

## 工作流

```
同花顺问财（最热板块，选题锚点）
       ↓
OpenAlex（1 篇中国论文，近一年内）
       ↓
OA 论文优先取全文 → 提取 Results/Methods 数据
       ↓
深度科普文案（1800-2500 字，3 分钟口播）
       ↓
剪映 AI文字成片（自动填入文案，生成视频）
```

全程自动化：从选题 → 论文检索 → 文案撰写 → 视频生成，一条命令完成。

## 项目结构

```
sector-paper-video/
├── README.md
├── sector-paper-video/           # 主 Skill
│   ├── SKILL.md                  # Skill 定义 & 完整工作流
│   ├── references/
│   │   └── sector-keyword-map.md # 板块→学术关键词映射表
│   └── scripts/
│       └── jianying_ai_video.py  # 剪映自动化脚本
└── hithink-sector-selector/      # 依赖 Skill
    ├── LICENSE.txt
    ├── SKILL.md                  # 同花顺问财 API 封装
    └── scripts/
        └── cli.py                # 问财 CLI
```

## 安装

### 1. 安装 Skill

将 `sector-paper-video/` 和 `hithink-sector-selector/` 复制到 Claude Code 的 skills 目录：

```bash
# macOS / Linux
~/.claude/skills/

# Windows
C:\Users\<用户名>\.claude\skills\
```

### 2. 配置 API Key

```bash
export IWENCAI_API_KEY="your-key"  # 同花顺问财
```

获取方式：浏览器打开 https://www.iwencai.com/skillhub → 登录 → 点击具体 Skill → 安装方式 → Agent 用户 → 复制 API Key

### 3. 安装 Python 依赖

```bash
pip install uiautomation
```

### 4. 安装剪映专业版

从 https://www.capcut.cn/ 下载安装。脚本自动按以下顺序探测安装路径：

1. 注册表 `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` 中搜索"剪映"
2. 默认路径 `%LOCALAPPDATA%\JianyingPro\Apps\<版本号>\JianyingPro.exe`（覆盖绝大多数安装）
3. 兜底全盘扫描

验证安装：打开一次剪映确认正常启动即可，脚本后续会自行调起。

## 使用

在 Claude Code 中输入：

```
/sector-paper-video 排名第三的板块
```

或：

```
sector-paper-video 排名第一的板块
```

- `排名第N的板块` — 取 A 股涨幅第 N 名板块作为选题
- 不指定排名默认取第 1 名

AI 会自动完成全文书流程，最终在剪映中生成视频。

## 写作铁律

文案严格遵循以下规则：

1. **不讲股票** — 不出现涨跌幅、主力资金等术语
2. **不讲 IF** — 不出现影响因子、JCR 分区
3. **不数引用** — 不出现被引次数
4. **一定有震撼数字** — 找论文里最震撼的数量级
5. **一定有背景科普** — 假设观众零基础
6. **一定有产业落地** — 至少 2 个产业赛道
7. **一定有国家站位** — 强调中国团队、自主专利
8. **一定有风控** — 结尾必须带"不构成投资建议"

## 论文选择铁律

- 时效第一、期刊第二 — 近一年内、中国团队主导、摘要能读懂即可
- 不追顶刊、不数 IF — 好期刊是加分项，不是准入门槛
- Nature 系列摘要缺失普遍 — 三处 API 都无摘要则直接跳过
- OA 论文优先取全文 — 全文数据充实文案细节；读不到则退回摘要，不卡流程

## 依赖

| 依赖 | 说明 |
|------|------|
| hithink-sector-selector | 同花顺问财 API（查板块排名） |
| OpenAlex / Semantic Scholar / Crossref | 学术论文检索（裸 API，无需安装） |
| 剪映专业版 | 视频生成 |
| Python 3 + uiautomation | 剪映自动化 |

## License

MIT
