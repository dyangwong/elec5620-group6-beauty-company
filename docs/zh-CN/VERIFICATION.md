# 本地验证记录

中文阅读副本，依据 2026-10-25 英文主版同步。以[英文主版](../VERIFICATION.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

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
