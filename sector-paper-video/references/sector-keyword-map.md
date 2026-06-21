# 板块→学术关键词映射表

单篇文案只需 **1 篇论文**，用此表将板块名转为学术搜索关键词。优先英文关键词（OpenAlex 覆盖广），中文关键词作为知网兜底。

| 板块 | 英文关键词（优先） | 中文关键词（兜底） | 学科路由 |
|------|-------------------|-------------------|---------|
| 钨 | tungsten, tungsten alloy, WS2, tungsten oxide, POM tungsten | 钨合金, 氧化钨, 碳化钨 | chemistry-materials |
| 稀土 | rare earth, lanthanide, neodymium magnet, rare earth doping | 稀土, 镧系, 钕铁硼, 稀土催化 | chemistry-materials |
| 半导体 | silicon photonics, semiconductor chip, GaN, SiC, advanced packaging | 半导体, 芯片, 硅光, 氮化镓 | physics-math |
| 人工智能 | large language model, deep learning, AI agent, multimodal | 大模型, 深度学习, 人工智能 | computer-science |
| 新能源 | lithium battery, perovskite solar, solid-state battery, electrocatalysis | 锂电池, 钙钛矿, 固态电池 | chemistry-materials |
| 机器人 | humanoid robot, embodied AI, tactile sensor, soft robotics | 人形机器人, 具身智能 | computer-science |
| 创新药 | CRISPR, mRNA vaccine, gene therapy, ADC drug, PROTAC | 基因编辑, 基因治疗, 免疫治疗 | biomedicine |
| 低空经济 | eVTOL, drone delivery, urban air mobility, flight control | 无人机, 飞行汽车, 低空 | physics-math |
| 量子计算 | quantum computing, superconducting qubit, quantum error correction | 量子计算, 超导量子比特 | physics-math |
| 商业航天 | reusable rocket, satellite constellation, LEO satellite, propulsion | 可回收火箭, 卫星互联网 | physics-math |
| 磁性材料 | magnetic materials, ferrite, permanent magnet, spin, spintronics | 磁性材料, 永磁, 铁氧体, 自旋电子 | chemistry-materials |
| 磨具磨料 | diamond, superhard material, abrasive, grinding, CBN | 金刚石, 超硬材料, 立方氮化硼, 磨料 | chemistry-materials |
| 非金属材料 | ceramic, composite, carbon fiber, boron nitride, advanced ceramic | 陶瓷, 复合材料, 碳纤维, 氮化硼 | chemistry-materials |

## 搜索策略（单论文模式）

1. 先用英文关键词 1（最核心的）在 OpenAlex 标题搜索，`sort=cited_by_count:desc`
2. 取第 1 条结果（最高引 = 最可能是顶刊）
3. 如果无结果，换关键词 2、3 依次试
4. 如果仍无，放宽到全文搜索（`search=` 代替 `title.search`）
5. 映射表未覆盖的板块：用板块名英文翻译 + 常识推断

## 单篇筛选优先级

只取 1 篇，按此顺序选：
1. Nature / Science / Cell 系列 → 直接锁定
2. IF>20（EES、ACS Nano、Adv. Mater.、Angew. Chem.、JACS、Nature Comms 等）
3. 学科顶刊 + 引用≥30
4. 引用最高的那篇（兜底）
