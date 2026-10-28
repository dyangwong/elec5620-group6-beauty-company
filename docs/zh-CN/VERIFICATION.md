# 本地验证记录

中文阅读副本，依据 2026-10-29 英文主版同步。以[英文主版](../VERIFICATION.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

## MC 有界真实文字检查点 · 2026-10-29

本次是**本地 MC 文字**新证据，区别于历史 BA／ZIP 检查点。分支 KAN-15-mc-live-text，
从干净 4f43f38a89637248874f4ed308441a5502e464ff 开始；获取远程后 origin/main 仍为
515bfa537e31a01b9e9a24400a7112f8103babb3。Danny / M1 明确授权共享文件例外，AI 辅助，
任务归属不变。

| 本次检查 | 实际结果 |
|---|---|
| Windows Verify | **181 项全部通过，49.886 秒**，原 169 + 新 MC 12；来源 114 文件／41 组、来源哈希及交接检查通过。JS 语法通过，审批标签修正后再查通过；MC 单独 28 项通过。 |
| 离线边界／失败 | 显式开启／默认兼容、最小 DTO 严格传输、无效方案无回退、实际脚本／字幕／方向／时长篡改、独立证据、身份权限／CSRF／精确字段、审批／修订、并发过期结果、目录变化、最终保存回滚及不可用／超时／无效结果留存。这些是测试替身，不算真实推理。 |
| 实际 mock 网页／新库 5710 | MC-b3315edc057a 修订 1 APPROVED，文字／媒体均模拟，原审批及投递通过。 |
| 真实模型／新库 5711 | MC-931edb7409b9 修订 1 CALM，重点 Fragrance-free，仍选择三个目录事实。brief 要求仅 Fragrance-free，但模型保留其他授权事实；此创意不符显示给 Founder，不能宣称语义遵循通过。Founder REQUEST_REVISION 已投递。 |
| 真实新修订及审批 | 同 MC 修订 2 ENERGETIC，factRefs=[50 ml]，重点字幕 50 ml；脚本变为 “Meet Daily Hydration Cream. 50 ml. Explore the product details.” AP-31e86c3715fa APPROVED/DELIVERED；旧 AP-d0e8fc30ccdd SUPERSEDED，保留修改要求决策。 |
| 独立数据库核验 | 使用当前 P-101:v1 原目录重建实际脚本／声明／三分镜，文字非模拟、媒体模拟。审批绑定准确草稿／修订／真实文字／mock 媒体；两条不同决策，业务效果 0，库存 12/8/0 不变。 |
| 停止准确所启模型后新网页创建 | 应用健康、配置 LIVE_TEXT_WITH_MOCK_MEDIA，8080 关闭；MC-de418646a5b9 GENERATION_FAILED / LLM_UNAVAILABLE / textSimulated=false，无脚本／声明／媒体／审批，不回退 mock。 |
| 环境和清理 | Windows 11 Pro 25H2 build 26200.9711、应用 Python 3.14.5；Strata 0.2.1、Terminal 0.1.46.1、engine 0.1.46 CUDA 13／Python 3.12.15，qwen3.8-flash-next-gyro-gyro-s。复用 8192 context、单请求、关闭 vision/MTP、1536 MiB reserve、route-tail-skip 7、120 秒／512 输出 token；无安装／下载／新依赖／配置改写。仅停止本轮 5710／5711 和准确模型实例。原配置／数据库哈希和 56 模型文件大小／mtime 匹配；无捕获的浏览器警告／错误。 |

引擎两次 MC 生成记录 prompt 326／332 token、输出 53／41 token，prompt/decode 时间为
6135+2062 毫秒和 1803+1260 毫秒，是引擎测量，不是完整网页耗时。适配器核对精确配置模型与
完整 JSON；实际保存内容和模型停机失败另行核验，区别于替身／仅健康检查。初次测试发现漏导入
text_value，修正后全通过；创建／修订字段和真实审批标题也在最终网页验收前修正。

原始日志、测试库、实例回执、前后哈希、引擎日志和 evidence-summary.json 在忽略目录
var/mc-live-20261029，截图在本地 outputs。未跟踪会话／密钥／模型。复现见 WINDOWS_LLM.md。
未生成新 ZIP／校验值，旧 f7bb141 包早于 BA／MC 增量。

**未验证／未完成：**自由创作文案、一般／多语言 brief 语义、医疗安全、真实视频／媒体质量、MC
取消和生成保存的持久恢复／完整生命周期、完整 MC／Stage 2 验收、新增量 ZIP／其他电脑／现场
验收。最终保存回滚可能保留无输出／审批的 DRAFTING，已有 AP 恢复不能称为 MC 生成恢复按钮。
未接入真实 CS 意图／交接。Jira 未核实／更新待办（本轮不访问／修改），未推送／PR／合并／
上传 Canvas。


## BA 生命周期检查点 · 2026-10-29

动工前复核第一轮：本地 478d522694ca381b2ba3c3c5e3711a77fb04133a 干净，147 项通过，
应用/模型有主动正常停止回执（模型退出 0）。未见项目闪退证据，但这些记录不能证明 Codex 窗口稳定性。
随后获取 main 515bfa537e31a01b9e9a24400a7112f8103babb3，从 478d522 建立
KAN-15-ba-lifecycle-recovery，保留早先本地工作。

| 本次第二轮检查 | 实测结果 |
|---|---|
| 仓库 Windows Verify，Python 3.14.5 | **169 项通过，46.561 秒**：旧 147 + 新 22；来源 113 文件/41 组及 JS 通过 |
| 新离线生命周期/失败用例 | 同 ID 完整替换/历史、完成后拒绝取消、提取/推荐中取消、修订竞态、归属/会话/CSRF/输入、重复/并发恢复、模式保留、暂存/最终/失败状态/取消写入失败、无草稿显式重试及无效/不支持的持久证据 |
| 独立单测库的真实 SQLite 触发器中止最终建议审计 | 建议 UPDATE 与审计一起回滚，持久草稿保留，无 COMPLETED/当前结果；移除测试触发器后仅恢复保存一次、不推理 |
| 实际 mock 网页，新数据库/5700 | 修订 2 为 P-101 -> 修订 3 替换 Gentle cleansing. 后无当前旧建议、重问缺失条件 -> 修订 4 回答 -> 新确认后修订 5/P-102，历史保留 P-101 |
| 实际 mock 取消与恢复 | 另一咨询 CANCELLED/修订 2，无继续控件；声明的 Founder 保存故障 -> INCOMPLETE/隐藏草稿 -> 同库重启应用 -> 网页同修订恢复 COMPLETED |
| 实际模型推理中取消，新数据库/5701 | 刷新显示 ACTIVE/修订 1，取消仍可用；取消保存修订 2，原受理晚到 HTTP 409；事件仅创建/取消，无解释或推荐结果 |
| 真实模型最终保存模拟及持久恢复 | 新咨询真实提取/推荐；故障保留 live 草稿，无当前结果。精确停止本轮模型、同库重启应用、8080 关闭后，网页在原修订 2 恢复 COMPLETED/simulated=false/P-101 |
| 独立 SQLite/HTTP 校验 | 校验目录 ID/版本/价格/条件/原因；真实结果价格 4800 澳分、预算 6000；每模式再恢复 3 次仍一条建议事件；审批/效果为零；库存 P-101=12、P-102=8、P-103=0 |
| 停模型后另发新真实请求 | 应用健康 ok、配置仍 LIVE；保存 INCOMPLETE/LLM_UNAVAILABLE/simulated=false，无推荐或 mock 回退 |
| 网页控制台/收尾 | 未捕获警告/错误；原配置/数据库哈希及 56 文件模型大小/mtime 清单保留；只停止本轮 5700/5701 应用和精确模型实例 |

复用 Windows 11 Pro 25H2/26200.9711、Strata 0.2.1、Terminal 0.1.46.1、engine 0.1.46 CUDA 13、
模型 Python 3.12.15、精确模型 qwen3.8-flash-next-gyro-gyro-s；保存的 8192 上下文、单请求、
vision/MTP 关闭、1536 MiB 预留、route-tail-skip 7。没有升级、下载、复制权重/配置或新增依赖。
引擎生成记录及精确模型包校验支持真实推理证据；停模型后恢复是在保存早先真实输出，不是新的推理，
也不证明此时模型就绪。

中间观察：一项旧保存失败测试最初仍期待原始异常/ACTIVE 缺口，已改为要求安全 503、持久草稿、
INCOMPLETE 及只保存恢复成功。首次定时取消时提取已完成，未算推理中取消；第二次同批网页提交/
刷新/取消产生已核实的晚到 409。网页保存故障明确为模拟；真正 SQLite 写入/审计失败由独立测试
验证，没有破坏磁盘制造故障。

原始日志、进程回执、前后哈希、引擎日志、记录快照、evidence-summary.json 均在忽略目录
var/ba-lifecycle-20261029/，截图为本地输出；仓库只加入脱敏摘要。共享变更仅 BA 服务、HTTP、
门面草稿投影/故障选项、网页并发刷新/取消；无表结构/供应方/队友业务模块变化，评审待办。

尚未证明：旧结构化入口完整生命周期、BA 审批、完整目录/库存故障、任意语言/医疗安全、物理 GPU
中断、自动恢复/重试、磁盘完全故障时的持久保证、跨电脑或新功能 ZIP/Canvas 验收。现有 CS/AP/MC
离线全过，本轮未重跑其网页链路。各 BA 组按实际仍部分完成；BA-START-01/任务归属未改；
Jira 未核实／更新待办，未访问或对外发布，不代表 Stage 2 完成。

## 较早的第一轮 · BA 需求检查点 · 2026-10-29

本轮是本地 KAN-15 切片，不代表 BA-START-01 或 Stage 2 完成。分支
KAN-15-ba-needs-clarification，起点 a577c98c010142882abc22b552c73de92e3d51d0，
基于本轮获取的 main 515bfa537e31a01b9e9a24400a7112f8103babb3。包含本检查点的本地
代码提交标识实际交付版本；以下旧 ZIP 不含新功能。本轮没有 Jira 访问/更新及对外发布。

| 本次新检查 | 实测结果 |
|---|---|
| Windows 11 Pro 25H2 / 26200.9711，应用 Python 3.14.5 | 全量 147 项通过，27.301 秒；旧 123 项保留、新增 BA 24 项 |
| scripts/check_repository.py；node --check beauty_company/web/app.js | 113 源文件、41 用例组、来源指纹/交接检查通过；JS 通过，包括最终确认标签调整 |
| 实际 mock 网页、5690、新忽略数据库 | 干皮原文 -> 两条追问 -> 回答后同 ID 修订 2 -> 明确确认前无商品 -> 修订 3 COMPLETED/P-101/simulated=true |
| 实际 Strata 网页、5691、另一新忽略数据库 | 相同流程；两次真实提取、一次推荐；保存原文引用及 needsConfirmed，修订 3 COMPLETED/simulated=false |
| 两条主线后独立只读 SQLite 检查 | 预算 6000 澳分、P-101 4800 澳分、catalogue:P-101:v1、AVAILABLE/库存 12；原因均为目录字面事实；审批/效果均为零，库存未变 |
| 按本轮精确实例 ID 停模型、保留应用 | 应用健康仍 ok、配置 LIVE；网页保存 INCOMPLETE/LLM_UNAVAILABLE/simulated=false，无结果或 mock 回退 |
| 已操作网页控制台 | 未捕获警告/错误 |
| 原数据保护与收尾 | 原有配置/数据库哈希及 56 文件权重大小/mtime 清单保留；只停止本轮两个应用及模型 |

复用 Strata 0.2.1、Terminal 0.1.46.1、engine 0.1.46 CUDA 13、模型 Python 3.12.15、
qwen3.8-flash-next-gyro-gyro-s；保存的 8192 上下文/单请求/vision 与 MTP 关闭/
1536 MiB 预留/route-tail-skip 7。没有安装、升级、下载或复制模型目录。
网页操作期间引擎日志有实际生成记录，严格 adapter 响应包核对精确模型 ID。
这是有限英文证据，不是通用模型质量或中文真实模型评估。

新增离线覆盖：缺失字段、信息齐全仍未确认、中英文 mock、歧义预算、句末标点、
客户更正字段、重启后同 ID 恢复、归属/会话/CSRF、额外/无效输入及长度、两类并发旧结果、
当前目录变化、无效/虚构引用、缺失能力/模型失败、不回退及最终保存失败不得虚报成功。
传输测试用严格响应包 fake，与上述真实模型网页证据分开。

已定位并修复：歧义预算正则一度拒绝数字后句号，中间 146 项运行出现 5 个 failure、
5 个 error；修正边界并加入句号/部分小数回归后，全量通过。验收助手还曾使用不存在的
来源检查文件名、误读 health 顶层字段；改用 check_repository.py 与实际 capabilities
包后重验通过。未将应用失败伪装成功。

原始日志、数据库、前后清单、模型日志、网页记录快照保留在忽略目录
var/ba-needs-20261029/，截图为本地输出；仓库只保留必要源码、文档和本脱敏摘要。

尚未新验证/完成：完整取消/已完成记录修改、BA 审批生命周期、任意语言或医疗范围检测、
完整模型/目录/库存故障矩阵、可选替代品、BA 自动存储恢复（最终保存回滚可留 ACTIVE）、
macOS/另一电脑验收及包含本功能的新 ZIP/Canvas 演练。现有 CS/AP/MC 离线用例全量通过，
本轮未重跑其网页链路。MC 仍 mock，CS 意图未连接、真实 CS 交接受限。
共享文件评审/发布待办，Jira 未核实／更新待办。

以下为按日期保留的历史记录；后续发布更新覆盖早期“无远端/字节一致打包”的现状描述。

2026 年 10 月 16 日。初始实现阶段证据，不代表老师/团队认可或完整 Stage 2 完成。

## 初始阶段实际检查

| 检查 | 观察结果 |
|---|---|
| Python 3.9.6：`python3 -m unittest discover -s tests` | 29 项通过 |
| Python 3.12.14 同一套 | 29 项通过 |
| `node --check beauty_company/web/app.js` | 通过 |
| `python3 scripts/check_repository.py` | 来源哈希、41 组追踪、有限运行数据/凭据排除检查通过 |
| 临时源码包解压到独立目录 | 29 项通过，无原课程目录仍能载入新数据库和网页资源 |
| 真实浏览器、本地服务 | 客户受理 → Founder 转交 → 客户确认 → AP 提交/投递 → 客户再确认 → 保存模拟结果 |
| 真实浏览器 MC | 标 mock 的脚本/分镜创建，精确版本待审 PENDING |
| Founder 1280×900 与 390×844 | 无横向溢出，已审截图 |
| 所测流程浏览器警告/错误 | 捕获控制台未见 |
| Git 边界 | 本地 main 已初始化，无提交/远端/推送，数据库/预览被忽略 |

29 项测的是多个验收组部分条件，不是原 41 组里 29 组全部通过。
追踪表有意保留 PARTIAL/NOT_STARTED 和缺口。未测真实 LLM、视频、外部商业服务、Jira。
独立源码检查用现有本地 Python，不是教学现场机器或 Canvas 下载测试；临时包未上传/标最终。
浏览器在忽略的数据库里产生一次虚构换货与一份待审 mock 营销活动，属于实际本地测试，
不是真公司活动、团队决定或人工贡献证据。

## 已准备但未对外执行

CI 配置参考官方 [checkout](https://github.com/actions/checkout)、
[setup-python](https://github.com/actions/setup-python)、[setup-node](https://github.com/actions/setup-node)
接口；没有 GitHub CI 运行。Jira、外部模型/媒体、托管、Canvas 均未连接/改动。
预览在被忽略的 `output/previews/`，不是运行依赖/源码交付内容。启动与虚构凭据见主 README，
没有复制旧私钥、证书、运行数据。

## 开工交接更新 · 2026-10-16

- 未改 29 项应用测试，新增 7 项交接工具测试，合计 36 项通过。
- 五个完整姓名的 CLI 均对应本人任务和实际文件；拒绝未知/部分身份、跨人任务、旧来源指纹、冲突认领。
- 干跑不写档案或共享认领；本地保存只在临时目录测试，不改 tasks.json。
- 姓名/模块与原报告提取名册对照，能发现故意交换姓名或主文件冲突。
- 完整参考 PDF 与本地正式原件逐字节相同。此次交接不改原报告、应用实现、演示数据。
- 五份任务仍 READY/UNCLAIMED，Jira/PR/账号为空，不证明个人接受或工作完成。
- 文本读取明确 UTF-8，已写 Windows 命令变体，但未测原生 Windows。

交接只准备本地工作，不做外部认领或首批任务实现。真实/本地模型仍暂缓，未做初始提交、
GitHub 仓库/邀请、Jira 任务、源码发布。

## 文档语言更新 · 2026-10-16

- 已形成 21 对英文主版/中文阅读副本，涵盖成员入口、Agent 规则、共享指南、五个模块与五份任务书。
  英文保留原路径和工具默认阅读顺序。
- 检查上述指南 94 处本地 Markdown 链接及主副版互链。原始证据和共用 JSON/CSV 未翻译、未改动，
  应用界面语言未改变。
- 仓库检查通过，共 79 个源码文件，来源指纹与 41 组验收追踪有效；Python 3.9.6 下原有 36 项测试通过。
  没有新增应用行为或执行外部操作。

## 公开源码准备 · 2026-10-16

- 可发布报告换为明确标识的隐私副本：保留 63 页/模型，去除 11 页上 25 处学号及元数据，
  已目视检查封面、名册、贡献表、模型页。
- 正式原 PDF 本地保持不变并明确忽略，原摘录留忽略的 var/private-reference/，公开摘录用脱敏标记。
  分别记录原件/派生哈希，新增篡改和来源关联回归。
- 84 文件源码集合通过学号/明显 token/运行数据检查，本地 Markdown 链接全部有效；这是有限检查。
- Python 3.9.6 下 37 项测试、来源与 41 组追踪检查通过。
- 已准备 main 保护配置与对应 CI 名：必须 PR、检查通过后可自行合并，0 个外部强制批准。
  提交配置文件本身不代表已启用 GitHub 设置。
- 实际发布、CI、规则结果在执行后另记。Jira、真实模型、首批认领未变。

## 实际 GitHub 发布 · 2026-10-16

- 已发布公开 `dyangwong/elec5620-group6-beauty-company`，初始提交
  `570ebc3adc948ff54523920cb93b5092a2013956`，84 个源码文件，不含未脱敏原件、运行数据、预览、凭据。
- [首次 CI](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/38865450983)
  在 Python 3.9/3.13 成功：37 项测试、来源/41 组追踪、JS 语法。
- 已应用并经 GitHub API 读回 main 保护：必须 PR，0 个外部批准，两项实际 github-actions 检查、
  更新到 main、讨论处理、管理员也遵守、禁强推/删除、线性历史；仅 squash，合并后删任务分支。
- 公开源码包独立解压，不用原课程目录仍通过来源检查、37 项测试、CS 身份入口；不含原件/运行数据/预览。
- 保护启用后的发布交接走 PR，实际检查/合并结果保存在 GitHub，不在此编造。
- 未做 Jira、首批认领、真实模型或队友邀请，邀请待核实 GitHub 用户名。

## Jira 配置与映射 · 2026-10-17

- 通过已登录 UI 配置现有 team-managed KAN：In Review 改 Verification，启用 Backlog，添加 Bug。
  保留 KAN-1/2、Story/Subtask 和原截止日，未启动 Sprint。
- 建立六个 Epic KAN-4..9、五份任务 KAN-10..14，刷新后核实 To Do、Medium、正确父项和分配。
  BA/CS/MC 匹配现有显示名；AP/CO 完整姓名未匹配现有账号，暂未分配，未发猜测邀请。
- 每份保留原任务书来源/验收、文件、条件、中英文链接和服务范围边界。计划分配不记为本人认领或完成。
- 空间自动化 Flows 显示 No flows created yet，未加自动 Done、Agent 委派、截止日、提醒、估计或迭代历史。
- 真实编号/链接/父项/建议分支写回版本化任务表；工具打印但不假称实时同步。
  新回归防跨成员重复 Jira key 和错误任务 URL；Python 3.9.6 下 38 项通过，来源/41 组/本地链接检查通过。
- 使用 KAN-9 维护 PR 测 GitHub-for-Jira，实际开发面板/CI/合并结果观察后另记，不从安装 app 推断成功。

- 仅将选中的五份首批任务移入 Board，观察到 Board 7 / Backlog 0，五项仍为 To Do；
  看板四列正确，父项和分配正确，原 KAN-1/2 保留。
- KAN-9 Development 实际显示 1 commit、1 OPEN PR；打开详情看到正确仓库、
  PR #2、KAN-9-jira-onboarding → main 和 GitHub 链接。开发链接不代表功能已完成。
- PR #2 初次 CI [39032162481](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/39032162481)
  与 [39032164622](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/39032164622)
  的 Python 3.9/3.13 均通过；最终检查和合并凭据以 PR 记录为准。

## Jira 进度节点规范 · 2026-10-17

- JIRA、Agent／开工／Git 指南和 PR 模板明确开工、验证、合并验收、阻塞／重开节点，
  同步中文副本。Jira 管实时工作流，设置字段保留历史，不暗示自动同步或已改状态。
- 清理建立 Jira 前的过时文字和旧分支示例；STATUS 记录所在版本的实现，认领字段是记录。
- 调整原开工回归，先给其他成员任务设置已有认领，再验证准备／保存 CS 包保留该认领
  及任务表原字节；不再要求全员永远 UNCLAIMED，允许后续真实认领。
- Python 3.9.6 下 38 项测试通过，来源／41 组追踪检查通过。未实现或认领任何成员首批功能。

## 成员确认与协作透明度 · 2026-10-17

- AGENTS／START_HERE 及中文副本加入仅补缺失信息的确认规则、简短开工／进度／交接汇报、
  任务边界检查；复用明确身份／授权，无法核实的 Jira 状态不冒充已核实。
- PR 须解释改动与本任务的对应、已授权偏离和受影响成员；共享文件指南采用真实 Jira 号分支。
- Python 3.9.6 下原有 38 项测试及来源／41 组追踪检查通过；未改应用、未新增成员认领或功能完成。

## 共享 LLM 分工与接口预留 · 2026-10-18

- Danny 明确保留共享 GR-INT-02，独立于 BA 首批。已创建并核对 KAN-15、父 KAN-9、
  分配 Danyang Wang、To Do；未选供应商／模型，未安装或开始真实实现。
- 检查现有构造／调用，记录 BA／MC 真实注入签名和单位；CS 尚无独立意图 port，明确为后续缺口。
  模式标识及事务／网络问题列未来验收，不冒称当前 live 能力。
- 中英文接口／游戏本交接、入口／任务书／PR、共享工作预留和 helper 阅读顺序同步，首批认领未变。
- Python 3.9.6 下 38 项及 90 源码文件／来源／41 组检查通过；CS 工具含新指南，仍只选 CS-START-01／KAN-11。

## 队友批准规则执行 · 2026-10-18

- 读回 main 保护及实际协作者：dyangwong admin，slei0644／ZhengduWei write；未改账号权限。
- 建立并读回 main 生效规则集 25333272：一次批准、新提交撤旧批准、处理讨论、squash；
  仅 dyangwong 用户 226655466 有 PR 场景审阅层例外，规范限自己 PR，GitHub 技术上按操作账号。
- 原基础保护读回不变：当前 main 的 Python 3.9／3.13 github-actions 检查、管理员遵守、
  处理讨论、禁强推／删除；审阅层例外不移除基础保护。
- 同步中英文 Agent／开工／Jira／Git、默认 CODEOWNERS 及 PR 审阅字段，替代队友零批准政策。
- 这是配置读回，不是使用队友凭据测试，不证明已发生队友审阅；Danny 选择保留维护 PR #6 等队友 Approve，不使用本人例外合并。

## KAN-15 Windows 检查 · 客户端工作日期 2026-10-21

e51dfc4 基线首次 38 项测试因临时目录权限失败，工作区 TEMP/TMP 重跑全部通过。
来源检查首次因 Git CRLF 失败；恢复 Git 原始字节、不改哈希后通过。新增七项集成测试，
共 45 项在 Windows Python 3.14.5 通过；来源／JS 语法检查通过。
Setup/Start/mock HTTP 探针/重复 Start/Stop 已测，保留配置、不建重复启动的另一数据库。
无模型时实际 live 配置 HTTP 咨询约 2.1 秒后保存 INCOMPLETE/LLM_TIMEOUT，探针退出 1。
Terminal 哈希和签名 feed 检查通过，引擎／模型安装受限目录权限失败，沙箱外执行被审批策略拒绝。
不宣称真实推理成功。实测规格、版本、命令、脱敏失败、剩余验收和待填 Jira 内容见 WINDOWS_LLM.md。
原始主机证据时间为 10 月 20 日 UTC，客户端日期为 10 月 21 日，均不是 Jira 状态观察。

补充：Terminal 自带 Python 3.12.15 的 45 项测试和来源检查也通过；这是本地检查，不是 GitHub CI。
实际浏览器确认 mock 成功与模型超时 INCOMPLETE 记录及分项配置标签；Windows 原生拓扑接口确认
24 物理核心 / 24 逻辑处理器。

## runtime ACL 修复与真实 BA · 2026-10-21

取代此前安装受阻／真实成功未验证快照。迁移继承 D 盘权限导致失败，已备份并通过官方私有 ACL
修复检查。脚本新增 RepairModel，复用保存的 profile，不重复下载／启动或覆盖配置。
Strata 0.1.46 CUDA 13／Gyro-S，8192 上下文、单并发、无 MTP／图像、显存预留 1536 MiB。
精确 ID 和证据见 [WINDOWS_LLM_RUNTIME.md](WINDOWS_LLM_RUNTIME.md)。实际登录后 BA HTTP
咨询通过（6.804 秒、COMPLETED、simulated:false、P-101 支持事实），随后再次通过；效果／审批均 0。
45 项离线测试、来源／JS／差异检查通过；重复修复保留配置和 profile 哈希，重复启动保留同一进程。
MC 仍 mock，CS intent／live 转交及更广验收／审阅待完成；没有 Jira、提交、推送、PR 或合并动作。

## BA 阶段提交前本地审查 · 2026-10-21

已对照 fetch 后 origin/main e51dfc4 审查 KAN-15 差异，没有引入更新 main 或队友实现。
两个新增回归先复现失败：chunked 模型响应截断会变成 HTTP 500，HTTPError 响应流未关闭。
现已分别修复为安全保存 INCOMPLETE/LLM_INVALID_OUTPUT 和及时关闭响应，不暴露供应商原文。
还复现仓库外调用 Windows Setup 时配置路径解析错误，已改为相对仓库根解析 LlmConfig，
并在报告就绪前检查环境解释器。由 work/ 连跑两次，只生成 var/setup-path-review.json，哈希不变。
本地 Python 3.14.5 和 3.12.15 各通过 47 项测试，来源／JS 检查通过。
这是本地验证；远程 CI、受影响负责人批准和 Jira 认领／状态仍未核实。
差异准备作本地阶段提交及 PR 描述草稿，不代表发布或合并。

## AP 保存恢复切片 · 2026-10-24

- 新增 `tests/test_ap.py`（15 例），并适配 `tests/test_workflows.py` 既有的 AP 原子审计失败回归。
  合并后本地 Python 3.13.3 通过 53 项测试；`python3 scripts/check_repository.py` 通过，93 个源码文件、
  41 组验收保持不变；`node --check beauty_company/web/app.js` 通过。Python 3.9／3.13 的 CI 结果记在 PR 上，
  不在此断言。
- 在临时 SQLite 库上核实：注入决定保存失败后，审批处于 RECORDING_FAILED，没有 decisionId、决定、理由和 Founder，
  没有已投递批准、没有业务效果、没有 DECISION_COMMITTED 审计；预期的 Founder、种类、理由和精确范围仍可从存储读取。
- 核实同一数据库上新建服务实例恰好一次恢复同一预期决定：一个权威决定、一条决定审计、一次投递，
  Customer 再次确认时不重复业务效果。
- 核实冲突种类或理由被拒绝、过期版本或已被替代的请求被拒绝、非 Founder 和其他 Founder 被拒绝，
  请求回执或待存意图都不会被读成批准。
- 核实恢复后投递失败保留已提交决定，重投复用同一 decisionId。
- 此处未核实：真实外部存储故障（保存失败是本地注入的模拟）、HTTP/UI 恢复控制与演示故障下拉项
  （GR-INT-01 共享集成）、过期、通知／队列失败和风险路由。因此 AP-T-05 仍记 PARTIAL，不记 PASSED。
- 在 PR 上观察到：[PR #9](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/9) 的
  “Local prototype checks” 工作流在 push 事件与 pull request 事件下都于提交 `c433ef0` 成功完成
  （Python 3.9 与 3.13 作业）。分支保护要求有写权限者的非作者批准，故 PR 保持开启未合并；开启时未观察到批准。


## 受保护合并与组合集成 · 2026-10-25

Danny 明确要求后，PR #7 保留有效非作者批准并通过必需检查，正常合并为 `6e505f0`。
AP PR #9 在 `a1ae058` 纳入该 main：本地 75 项离线测试与来源检查通过，新的 Python
3.9／3.13 CI 通过后，经授权的 AI 辅助审阅批准，正常 squash 合并为 `840ac70`。
两次合并均未使用审阅／管理员绕过。

PR #8 集成候选保留 CS／AP 代码、测试与认领凭据，六个文档冲突保留双方相关变化。
Python 3.9.6 通过 84 项测试；来源检查通过（107 个源码文件、41 组验收）；内置 Node
通过 `--check beauty_company/web/app.js`；暂存差异空白检查通过。
本次不推断 Windows／模型当前执行、完整验收、MC #11 已修复或未观察到的队友批准。
发布后的远程检查和剩余审阅在 PR #8 单独记录，不与本地验证混淆。

## Windows 合入 CS/AP 后回归 · 2026-10-25

Danny / M1 仅继续 KAN-15 / GR-INT-02。本地干净，从 bd63c08 快进到
**966dae4fd1c8afcaeb60b8af84289ae5b6edaa60**，纳入 main
**840ac7004723c62995a427191eda4f0cd4151917**。以下应用验证对应此准确提交；
本次更新另包含下述停止脚本局部修复及双语证据。未领取 BA starter、未扩展 CS/MC 真实模型，
未处理 PR #11。

- Windows Verify：Python 3.14.5 的 **84 项测试**全部通过（24.250 秒；停止修复后最终复跑 24.422 秒）；
  来源检查通过（107 个源码文件、41 组原始验收），Node 22.19.0 的 JS 语法通过。
  配套 Python 3.12.15 独立通过 84 项（22.052 秒）。构成为 workflows 29、
  onboarding 9、LLM 9、CS 22、AP 15；原 47 加 CS/AP 37，没有凑数或修改测试。
- 新建独立库和本机端口：5635 mock、5636 Strata、5637 模型无法连接、5638 AP 网页失败、
  5639 正常停止验证。原始证据及测试库位于忽略的 var/regression-20261025-966dae4/。
- 实际浏览器登录及 BA 提交在默认 mock 和 Strata 均通过。真实记录 BA-b7e1e655e3cf
  保存 COMPLETED/simulated:false，页面显示 Live BA recommendation。独立读取 SQLite
  核对 P-101、整数分价格和预算、无香条件、当前库存与版本、catalogue:P-101:v1，
  两条理由都逐字属于目录事实。BA 未产生审批或交易效果。引擎记录读取 297 个 prompt
  tokens 用 6201 ms，生成 25 tokens 用 1042 ms；单样例不代表一般性能。
- 无模型端口配 0.5 秒连接预算的网页提交保存 INCOMPLETE/LLM_TIMEOUT/simulated:false，
  页面明确显示 The model timed out，没有商品和 mock 成功。Windows 在返回拒绝连接前先超时；
  另用 5 秒预算实际连接该空端口，服务层保存 INCOMPLETE/LLM_UNAVAILABLE。没有停止真实模型制造故障。
- 实际 CS/AP HTTP 流程：待审批时执行和客户自批被拒绝，错误版本返回 STALE_SCOPE。
  精确范围批准及投递后仍为零效果；客户之后连续确认三次，同一 actionRef 仅一个效果，
  库存仅从 12 减至 11，最终 RESOLVED。
- 注入 AP 决定保存失败后为 RECORDING_FAILED，无 decisionId、无投递和业务效果。
  同库新建 Company 服务实例恢复存储中的同一精确意图；重复恢复仍只有一个决定／审计，
  恢复自身不执行，后续客户确认才产生一次效果。HTTP 保存失败也已验证；
  /api/approvals/{id}/recover 实际返回 404。
- AP 网页正确显示 recording failed、无已提交决定，且没有恢复按钮。
  **发现展示缺口：**兜底文案错误声称 review 因上下文变化被 superseded。
  这是 AP／共享网页集成限制；本轮没有扩展 AP 业务或界面，也没有声称网页恢复已实现。
- Strata 模式的 CS coordinate/revise 均保持 503/LIVE_HANDOFF_NOT_CONNECTED。
  health 的 MC:MOCK、csIntent:NOT_CONNECTED 保持准确；真实配置应用中创建的营销草稿
  仍为 simulated:true/REVIEW_PENDING，媒体保持 mock。

复用已有 Terminal 0.1.46.1／Strata v0.2.1／engine 0.1.46 CUDA 13 与
qwen3.8-flash-next-gyro-gyro-s：127.0.0.1:8080，8192 上下文、单并发、vision/MTP 关闭、
1536 MiB 显存预留、上游 route-tail-skip 7。没有安装、升级或下载。原有本地配置／profile／
数据库 SHA-256 全部保持，56 个既有模型文件的大小与修改时间清单不变；未重新计算整份权重哈希。

执行权限切换期间测试监听已消失，没有杀死身份不明的 PID。停止脚本遇到一个仍存在但无法读取
StartTime 的已记录 PID 时出现空值错误。局部修复要求开始时间和可执行文件均可读，才能比较原凭据。
验证该不可核实 PID 被保留；另启动 5639 的身份匹配应用，正常停止且保留数据库。
最终六个测试端口（含模型 8080）均无监听。

诊断中还遇到探针过窄地期待 LLM_UNAVAILABLE、实际 Windows 先连接超时，以及复用已完成订单触发
既有 DUPLICATE_REQUEST。均通过校正探针或另建测试库解决，没有修改测试数量或队友业务规则。

未验证真实外部存储故障、AP 网页恢复、CS 失败 intake 保留界面、真实 CS/MC、跨机网络、一般模型质量
或完整 41 组验收。GitHub CLI 返回 401，改用已连接 GitHub 工具读取 PR #8 及准确 head。
PR 正文记有此前经 Jira UI 更新 Verification；回归验证未独立核实 Jira，也未写入 Jira/PR。
随后 Danny 授权将这些证据与停止修复发布到 PR #8。新的 CI 和实际评审须针对发布提交；
本地自检不代表 Approve，发布不包含合并、绕过审批或 Jira 写入。

## 本地模型稳定性与重启恢复 · 2026-10-25

Danny / M1 在准确提交 `dbb6662fc1f71db9d40657bfa959cb712364b7bd` 上继续
KAN-15 / GR-INT-02。使用全新数据库和本机 5641 端口，复用 8080 的 Strata/Gyro-S profile。
未改模型／配置／代码、未装依赖、未领取 BA starter，也未扩展 CS/MC。

- 连续 20 次实际登录后的 HTTP BA 请求（保湿／洁面各 10 次），实测空闲 180 秒后 3 次，
  模型停启后 3 次，合计 **26 次**全部保存 COMPLETED/simulated:false。
  独立读取 SQLite 校验商品、逐字事实、整数分价格／预算、无香、库存和版本。
- 连续调用最短／中位／最长为 1.292/1.385/15.203 秒；空闲后为 1.277/1.321/2.802 秒；
  重启后为 1.994/2.421/7.386 秒。包含本机 HTTP／保存校验，仅为样例耗时。
- 首次模型就绪 18.816 秒，停止后再就绪 20.017 秒；重复 StartModel 复用同一实例／监听 PID，
  空闲后原实例仍就绪，重启后同一 profile 产生不同的新实例。
- 模型确实停止时，2.109 秒内保存 INCOMPLETE/LLM_UNAVAILABLE/simulated:false，
  未回退为 mock；此时 84 项离线测试全部通过（23.512 秒）。应用和数据库贯穿模型重启保留。
- 最终库为 26 条 COMPLETED、1 条预期 INCOMPLETE，零审批／交易效果，库存仍为 12/8/0。
  捕获的模型日志没有 OOM、fatal CUDA 错误、traceback 或崩溃标记。
- 已加载／请求／空闲采样的可用显存为 1957–2023 MiB，可用系统内存为 2.35–11.16 GiB。
  系统内存余量有限；没有调参或清理缓存。
- 所记录原有配置／profile／数据库哈希及 56 个模型文件大小／修改时间清单不变。
  两轮尝试启动的服务均按本轮凭据／实例身份停止，测试端口无监听。

首轮控制器因 Windows 子进程继承输出管道，在应用就绪后仍等待，尚未发出任何咨询。
只停止它自己的应用／模型后改为文件日志，另起全新数据库完整重跑；首轮不算成功测试。

成功测试窗口共 319.467 秒（约 5.3 分钟）、单并发、短小结构化样例；不代表过夜运行、
Windows 重启／睡眠唤醒、长输入、多人并发、一般建议质量、远程 Mac／Windows 或真实 CS/MC。
不能据此保证无内存泄漏。本轮为实际 HTTP 自动化，没有重新声称手动网页验收。
原始证据留在忽略目录 `var/stability-20261025-dbb6662-20261025T053019994156Z/`。
稳定性测试期间只准备本地双语记录，没有远程写入；随后 Danny 授权将这四份双语证据文档
发布到 PR #8。实际测试的应用仍为上述准确提交，新的 CI 须针对文档发布提交。
本次发布不包含模型／配置／代码、SSH／防火墙或 Jira 变更，也不包含合并或绕过审批。

## AP HTTP/UI 保存恢复 · 2026-10-26

**范围与授权：** Danny 明确授权 KAN-9 / GR-INT-01 的三个 AP 共享接口／界面缺口：准确保存失败文案、
恢复接口和恢复按钮。分支 KAN-9-ap-web-recovery 基于 main
`e141427c393df6515ad8091f035e1c2f81cba65d`，不领取 Jiaxuan 的 AP starter，
未改 approval.py、schema、CS/MC 模块、模型部署或 PR #11。

**接口：** 原 Founder 的登录会话只向 `/api/approvals/{id}/recover` 提交所显示的正整数 contextRevision。
即便已提交后重复调用，仍检查当前来源、版本和审阅关联；原服务在提交前复核持久意图的精确动作／actionRef。
拒绝覆盖决定、理由、身份和动作；保留原双参数服务调用。恢复同一已存意图只提交一次，再单独尝试投递；
投递失败须显式重投同一决定 ID。恢复／投递均不执行业务。失败卡片将已存种类／理由标作无权威意图，
仅原 Founder 对当前来源可见恢复按钮。decide／recover 失败立即刷新已存状态；
approval_recording 下拉项是本地注入样例。

**自动检查：** Mac Python 3.9.6 的 **96 项测试在 12.810 秒全部通过**，含原 84 项和 12 项新增
AP HTTP／会话／SQLite 检查：重启／重复恢复、后续仅客户确认才恰好一次执行、保留 REJECT／REQUEST_REVISION、
未登录／错误 CSRF／Customer／其他 Founder 被拒、缺失／非法／额外／覆盖输入、旧显示版本、
被替代来源、动作范围改变、提交后旧范围重复恢复、无意图／不存在审批、再次保存失败，
以及投递失败后显式重投同一 ID。Node 语法与空白检查通过，未启动或调用真实模型。

**实际网页：** 使用全新忽略数据库、本机 5661 端口，通过原服务创建 mock CS 待审批记录。
浏览器登录虚构 Founder，在 Activity trail 选 Decision recording failure (no approval) 并应用，
填写理由后点 Approve exact scope。HTTP 409 后立即刷新为 recording failed，展示非已提交决定的已存意图、
理由、No applicable committed decision 和 Recover saved decision；不再误说 superseded。
点恢复后显示 APPROVED、决定 ID、DELIVERED，恢复按钮消失，再刷新仍为同一决定。
独立读库：审批 AP-d53f12341a0d，决定 DEC-6349abf72f19，一条 DECISION_COMMITTED 审计、零业务效果，
P-101 库存仍为 12，CS 仍 AWAITING_CONFIRMATION。原始库／截图位于忽略的
var/ap-web-20261026-first.sqlite3、output/previews/。业务效果及故障为 mock／注入，不代表真实存储故障验收。

**交接：** 完整 AP-T-05／GR 验收保留 PARTIAL；队列／通知、过期、完整风险路由、CS 失败受理界面、
MC PR #11 仍为独立事项。10 月 26 日读到 Jira KAN-9 为 Integration & Verification、To Do、Unassigned；
子项只有 KAN-15，未显示单独 GR-INT-01 子项。核对 GitHub 重叠工作时仅 MC PR #11 开放。
本次未执行 Jira 认领、状态／评论、远程发布或队友审阅，不声称远程 CI；按 Danny 要求由 AI 协助完成。

**Jira update pending：** 将本次有限 GR-INT-01 AP 网页恢复记录在 KAN-9，获授权发布后补 PR 链接，
请 Jiaxuan 审阅共享 AP 边界；附 96 项检查、网页／不执行业务的证据及剩余条件。
不因本地实现将整个集成 epic 标 Done，也不改 KAN-13／KAN-15／队友认领。

## MC 修复验收 · 2026-10-27

保留 Zhengdu Wei 原 KAN-12 实现；按 Danny 明确要求，由 AI 协助将原 PR #11 同步到 main dc1b60b（含 AP #12）并修复，不重新分配 starter，不声称队友已认可。

失败修订现可在 Content studio 显示失败原因，不伪造商品、媒体或审批，并用 productId 保留更正表单选择。审批队列也处理当前失败数据，明确旧 SUPERSEDED 审阅不能批准不同的当前版本。HTTP 创建仍调用 submit，submit_draft 仍是服务入口；未新增真实模型或视频。

传给模型的证据、传给媒体适配器的输入均独立深拷贝；实际媒体帧与另一份已验证分镜快照比较，避免共享可变引用绕过验证。shot／duration 元数据和 mock 标签限定为已声明样例。适配器修改输入不能将无依据字幕带入审批，也不能替换已保存脚本／声明。这仍是确定性 mock 验证，不代表任意自然语言事实校验。

集成后的 112 项测试全部通过，含原 11 项 MC 检查和 5 项新增的适配器／证据变更、元数据、实际 HTTP 失败修订回归。实际浏览器创建后以纯空格修订，保存 INCOMPLETE／revision 2；Content studio 和旧 SUPERSEDED 审批均正常显示，保留历史。远程 CI、实际审阅／合并在 PR #11 单独记录。

## CS 失败受理网页验收 · 2026-10-27

Danny 授权 GR-INT-01，基于已合并 AP 的 main dc1b60b；MC PR #11 为单独修复分支。
HTTP 受理提交 assess 结果，界面展示证据失败／重评并在错误后刷新，未改 CS 模块／schema／模型。
107 项完整离线检查通过，含新增 11 项 CS HTTP。隔离 5663 网页验证缺政策保存、证据更正后版本 2 重评，
以及后续确认错误立即刷新。负例中的 Founder 交接使用原服务，政策变化由受控测试样例设置，不是新增政策编辑功能。
独立读库：一条 CS、零审批／效果、库存仍为 12。完整 CS／GR 保留部分验收。
远程 CI、负责人审阅、Jira 发布回执另记 PR，不推断整个模块完成。

## MC／CS 组合集成检查点 · 2026-10-27

PR #11 经 Danny 明确授权、由 dyangwong 提交标明 AI 辅助的审阅，且必需检查通过后，
已合并为 8bcc329。PR #13 的任务分支已合入该 main，保留 MC、CS 双方实现与中英文证据。
组合代码在 Mac Python 3.9.6 上 **123／123 项离线检查通过（15.884 秒）**；
来源核验（110 个源文件／41 个追踪用例）、JavaScript 语法与空白检查通过。
上文 112／107 项是此前各自基线的历史结果，不是组合后的数量。网页验证沿用上文记录，
本检查点不声称新增组合网页验证。

Danny 本次明确要求合并 #11 和 #13；自己的 #13 在最新 main 的新 CI 通过后，
可使用已有的本人 PR 审阅层例外。自检不是自我 Approve，也不是独立人工审阅，
没有将此前仅限 #12 的授权套用到 #13。#13 的远程提交、新 CI、实际合并和 Jira 回执
在发生后记于 GitHub／Jira。完整 MC、CS、GR 验收及真实 CS／MC 模型集成仍未完成。

## GR-INT-03 源码 ZIP／全新目录 Windows 演练 · 2026-10-28

Danny / M1 授权本地部署验证与本地提交。GR-INT-03 为内部标签，不是 Jira key；仓库未映射
部署子任务编号。Jira 未核实／更新待办，按要求本轮不查询或修改外部 Jira。不领取 BA
starter、不改队友归属、不新增业务／真实 CS/MC、不上传 Canvas、不推送或合并。
原干净 main e141427 已快进到最新远程 **515bfa537e31a01b9e9a24400a7112f8103babb3**，
获取时没有更新 main。独立分支 GR-INT-03-zip-windows。

本轮环境：Windows 11 Pro 25H2／26200.9711 x64；系统／新环境 Python 3.14.5；Windows
PowerShell 5.1；Git 2.51.0.windows.1；Node 22.19.0；RTX 5070 Ti Laptop 12227 MiB，
驱动 617.42，初始 D 盘剩余 210.60 GiB。未发现既有项目／模型进程或所选端口监听。
Windows 基线 **123 项测试，36.202 秒**，来源 **110 文件／41 用例组** 和 JS 检查通过。
数量为此前 84 项加 12 AP HTTP、11 CS HTTP、16 MC，未改测试；Mac 耗时不冒充本机结果。

现有打包器在干净源码上生成 5,565,726 字节／110 文件的 ZIP，SHA-256 为
`6d6517d837137db65def0223db449f8e0a8dd5c3943e1ecd15be1fb1fa040fb0`。
文件名与追踪清单完全一致，成员字节与源码一致；无 .git／.venv／var／数据库／密钥／模型／
旧输出／未脱敏报告。同名再打包退出 2 且原哈希不变。解压到全新含空格目录
`D:\elec5620_project\rehearsals\20261028-515bfa5\fresh source retry`，两次 Setup
成功且配置哈希不变，Python 可执行文件与模块均来自该新目录，移除了继承的 Python／
BEAUTY 路径覆盖。无 .git 的新目录完整核验 **123 项测试，40.384 秒**，来源和 JS 均通过。
首次外部控制器把 Git 末尾空项计入清单，尚未解压／启动即停止；保留空目录与 ZIP，过滤
空项后修正的是控制器，不是项目代码。浏览器沙箱另拒绝向 D 写截图，改存已授权 C 输出
目录；这不是应用失败，也未将这些尝试计为成功部署证据。

实际网页 mock 主线：新 5670 应用／mock-browser.sqlite3，Customer 登录／ORD-1001 ->
Founder 发起 CS/CO→BA -> Mock recommendation -> Customer 当前提案确认 -> AP 精确
范围审核。已有 approval_recording 注入令决定 RECORDING_FAILED；SQLite 确认无决定 ID、
无提交审计／效果，库存 12。只停启本轮新应用并保留同一库，失败状态仍在；网页恢复后
APPROVED／DELIVERED，一条决定审计、零效果、库存 12；另 3 次 HTTP 恢复保持同一决定。
后续 Customer 网页确认才 RESOLVED，产生一条 actionRef 模拟效果；再 3 次确认仍一条
效果，库存 **12→11**。独立核对 action／revision／actionRef、商品事实／整数分价格预算／
无香／库存版本。本轮已实际验证当前 AP 网页恢复，25 日“无按钮”为历史限制。

真实 BA：原模型 runtime 已停止，核验 owner-private profile 后用原环境 StartModel 复用
安装，在 20.535 秒内就绪（含检查），无重装／下载／权重迁移。官方 runtime 和 /v1/models
确认 exact ID qwen3.8-flash-next-gyro-gyro-s。Strata 0.2.1／Terminal 0.1.46.1／其 Python
3.12.15／engine 0.1.46 CUDA 13，8192 上下文、单请求、vision/MTP off、1536 MiB reserve
不变。新 5671 应用／live-browser.sqlite3 最初只做健康检查时使用旧配置绝对路径；任何
真实 BA 调用前已用新目录自己创建的 llm.rehearsal.json 重启，120 秒／512 tokens／
loopback8080／准确 ID，Setup 也保留该文件哈希。此后应用不需要旧应用配置。

实际 Customer 网页咨询保存 **COMPLETED／simulated:false／P-101**，显示 **Live BA
recommendation**；SQLite 独立校验事实、价格预算、无香、库存／版本，零审批／效果。
本次引擎日志为 297 输入 tokens／7496 ms、25 输出 tokens／1223 ms，不推广为基准性能。
加载后的单次资源快照为可用显存 1967 MiB、可用系统 RAM 约 4.0 GiB。MC 仍 MOCK、
csIntent 为 NOT_CONNECTED，新应用实际 live CS coordinate 返回 503／
LIVE_HANDOFF_NOT_CONNECTED；未扩展真实 CS/MC。

依赖：mock 只需新包代码／静态资源、Python 和全新本地状态，Node 只核验、Git 只打包。
live 另外依赖旧模型环境的安装、86.39 GiB 权重、profile／私有 runtime、驱动及本机服务；
不依赖旧应用导入路径或旧应用配置。无需修部署脚本或业务代码，仅更新现有双语说明／
状态／证据。网页检查点时原配置／数据库哈希与 56 个模型文件大小／修改时间清单不变。
原始证据在忽略目录 var/rehearsal-20261028-515bfa5/ 和新目录 var 中。

41 个用例组保留原状态，不因演练通过提升整个模块。实际 Canvas 上传／下载、最终包
冻结／重新解压、全新电脑／网络、教学团队预装软件／缓存模型许可、长期／睡眠／重启／
长上下文／多人、真实 CS/MC 和完整 Stage 2 仍分别待验。后续仅文档更新的源码包也必须
在 ZIP 外记录自己的准确提交／SHA-256／新目录复验回执，不能沿用本包哈希冒充。

## 冻结演练包回执 · 2026-10-28

包含新部署说明的最终 ZIP 源码冻结在本地提交
`f7bb141f6e35c7846989adccf58841b9e128a978`，分支 GR-INT-03-zip-windows；
110 文件／**5,579,703 字节**，SHA-256 为
`5be88639cdd33415dadc77c0e6bfdc286b34b50e4635be2568ee01f4543e6ba3`。
非文档文件与已验证 main 515bfa5 字节一致。本回执为之后的仅文档提交，不改变冻结 ZIP，
也不把包的源码提交冒充为之后回执提交 HEAD。

第二个全新目录 `D:\elec5620_project\rehearsals\20261028-f7bb141\final fresh source`
两次 Setup 保留配置，导入路径独立；新环境完整 **123 项测试／36.100 秒**、来源
110 文件／41 用例组与 JS 检查通过，无 .git 或旧应用导入依赖。

最终包从 5680/mock、5681/live 执行实际认证 HTTP 复验：CS→BA→客户确认→AP→模拟效果。
AP 保存失败时无有效决定／效果；应用重启后恢复，另 3 次重复恢复仍一条决定／零效果；
Customer 确认并另重复 3 次后仍只有一次效果、同一 actionRef，库存 12→11。此前 515bfa5
包的流程为实际网页；此次最终包为真实 HTTP 自动化复验，不冒充另一轮网页验收。

最终包一次真实 BA 在 **2.780 秒**内保存 COMPLETED／simulated:false／P-101，复用同一
已安装模型实例和新目录独立配置；SQLite 逐项校验保存内容／事实／库存／价格预算／无香／
版本，零审批／效果。按实例身份停止本轮模型后，应用仍健康，新咨询如实保存
**INCOMPLETE／LLM_UNAVAILABLE／simulated:false**，无商品、未回退 mock。
最终两个应用和本轮模型均停止；原配置／数据库哈希及 56 个模型大小／修改时间清单不变。
无需修改业务／部署脚本／模型／依赖。

原始最终报告／日志／数据库保留忽略目录，ZIP 与机器可读版本／哈希／结果回执已复制到
本地交接输出目录。未读写 Jira、未推送／发起／合并 PR、未上传 Canvas。GR-INT-03 仍为
内部演练标签；正式 Canvas 下载、现场条件／许可、全新电脑／网络、真实 CS/MC 和完整
Stage 2 仍未验收。
