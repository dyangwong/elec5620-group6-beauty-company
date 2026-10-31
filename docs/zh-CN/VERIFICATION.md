# 本地验证记录

## 本地 MC／AP 核心边界修复 · 2026-10-31

KAN-9-mc-ap-core-boundaries 基于 d30dc019，Mac Python3.9.6 全量
**319项／37.185秒通过**（307+12）。MC 新测试覆盖 mock／受控 fake-live 来源事实及元数据矛盾、
不调用生成器／不新建 review／effect、失败修订历史与纠正后新 review、合法有香精产品、
重启恢复拦截旧暂存矛盾而不推理／渲染。AP 覆盖未知／额外／畸形动作、服务端类别审计、
相同回执复用与不同证据拒绝、CS 目标／策略／ref 不匹配、未知保存动作在意图／恢复时拦截、
意图／恢复／投递时策略变化、保存证据不可替换、重投递拒绝后保留已提交决策。
原有 BA／CS／MC／CO、HTTP 身份验证和一次 effect 回归均通过。

首次 MC 专项测试发现3处旧 revise 的保存顺序兼容问题，以及新测试错误期待故意最终保存失败时返回结果；
现修正同一事务内保存顺序及测试的真实异常预期，全量通过，保留首次失败日志。
本地日志／hash证据在 output/core-boundaries-20261031/。
[证据索引](EVIDENCE_INDEX.md)区分本机文件／CI、Windows 执行回执和待补人工记录。
本轮没有新增真实推理／Windows／网页／Canvas 验收或独立人工认可；
来源／JS／空白检查随本地交接记录，41组状态不变。

## 合并后返回一致性修复 · 2026-10-31

PR #20 的必需检查41093217688 在 d88bb48 通过，并正常以本人 PR 例外 squash 为5b83cda。
随后 main 检查41093577366：Python3.13通过，3.9在新结构化权限回归的整条记录比较中失败；返回的
CLARIFYING 记录 updated 比实际保存值早，业务范围未变。失败日志124193419028 已保留；不重跑掩盖失败。
KAN-10-saved-record-response 补准备/低层成功结果/共享最终记录的 Store.get 返回。新增递增时钟测试：
澄清、完成、替换、取消、低层 submit 返回均须等于存储；独立复制原5b83cda稳定失败，修复后通过，原断言保留。
Mac Python3.9.6 全量306项/36.240秒通过；来源133文件/41组、已装Node JS/空白通过。
日志见 output/ba-mc-fix-20261031/response-regression-before-fix.txt 与 full-tests-response-fix.txt。
只是返回一致性修复，无新增权限/状态/schema/模型/UI 功能；PR/CI/合并/Jira 回执随后记录。

## KAN-10 / KAN-12 修复验证 · 2026-10-31

Danny 授权从 main e6bd1b4 在 KAN-10-KAN-12-ba-mc-failure-lifecycle 修复并提交 PR、检查后合并。
两任务实查 Verification 后转 In Progress；保留 Danyang Wang / ZHENGDU WEI 负责人及原成果。
Mac Python3.9.6 全量 305 项/36.000 秒通过（原286+新增19：BA15、MC4）。受限运行9项仅因回环绑定
禁止；允许本机测试端口后重跑。一次新取消测试发现返回更新时间未刷新，已改为返回实际保存记录，最终全套通过。
BA 验证同 ID 续办/重启/新库存、全量替换不继承旧约束、低层兼容、旧预算单位、身份/归属/修订/额外字段、
推理中取消/修改抑制晚到结果、取消后新建；模拟和真实 SQLite 写入失败、双方快照不泄露暂存建议、重启/并发
只记录一次且不重调模型、未知库存拒绝旧建议、无暂存/取消写入失败、角色撤销和实际 HTTP 会话撤销。
MC 验证空/缺失/错误结构/空白事实停止生成并保留 INCOMPLETE，无脚本/媒体/AP；失败修订历史与旧审批取代、
修正后新修订审批；Company mock/受控 fake-live 原模式保留；真实 SQLite 审计失败回滚。
来源检查133文件/41组及哈希通过，已装 Node JS 语法及空白检查通过；核对参考 PDF 第48/49/51/52物理页状态图。
无新结构化生命周期 HTTP/UI 按钮或结构化 AP；无新增真实模型、Windows/视频/ZIP/Canvas/现场验收。
仍为37 PARTIAL /4 NOT_STARTED；详细本地日志 output/ba-mc-fix-20261031/full-tests-final.txt。

中文阅读副本，依据 2026-10-29 英文主版同步。以[英文主版](../VERIFICATION.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

## 审阅集成收口 · 2026-10-30

- Danny授权实际小修／复核／合并／发布。PR #17保留GuiyuLiu0035作者；合入当前main并修复后，
  c41a76e通过Mac284项／34.173秒、来源126／41、JS／链接／空白及Python3.9／3.13
  PR CI41045067082。dyangwong新非作者审阅5711332295绑定准确提交，正常squash合入91281dc。
- 只读GitHub核实PR作者GuiyuLiu0035／316942998与审阅者dyangwong／226655466不同。
  授权审阅如实标注AI辅助，不声称人类认可；未用owner bypass、管理员合并、伪造人类审阅或改保护规则。
- 视频分支基于main91281dc，组合 **286项／34.446秒通过**；来源133文件／41组、JS／空白／链接检查。
  CO测试／指南与已合并main完全一致；MC渲染器／素材与已测8f39046字节一致。
  下方实际成片／网页／恢复证据仍对应原准确版本，不冒充本轮新LLM／Windows运行。
- 读回活动审阅规则：一项Approve、推新提交撤旧审阅、讨论须解决、仅squash，last-push审批关闭。
  连接器读旧式分支保护返回403，本轮未改设置；使用正常保护合并及必需检查。
  集成最终提交／CI／打包启动／合并及Jira收据在集成PR记录。

未提升用例状态、改分工或自动Done。当前Windows／真实模型／FFmpeg9.0.2、双机隧道、
实际Canvas下载／现场及人工确认贡献仍未在本轮验收。


## MC 广告模板打磨 · 2026-10-30

基线main1ad1101，Danny授权AI辅助KAN-9／GR-INT-03，独立分支
KAN-9-mc-advert-template；未认领队友任务、未虚构认可。

- Mac Python3.9.6完整 **283项／33.771秒通过**；新增素材缺失、分镜时序／布尔编号拒绝检查。
  来源133文件／41组、JS、空白检查通过，宽泛用例仍PARTIAL。
- 仅在忽略的var/media-tools使用原生FFmpeg／ffprobe6.1.1；ffmpeg-static b6.1.1
  ARM64压缩包匹配GitHub资产SHA-256。未装系统软件、升级Windows工具或增加应用库。
  使用已有DejaVuSans；Windows配置字体／工具仍需复验。
- 源码包含原创SVG／PNG影棚、罐、泵瓶，运行只用PNG。CALM／P-101实际mock文本片、
  INFORMATIVE／P-102与ENERGETIC／P-103受控已验证计划片，均通过H.264／720×1280／24fps／
  360帧／15秒、静音、全解码、大小和文件／脚本哈希检查。后两者是确定性测试计划，
  **不是真实LLM调用**。抽查三段字幕与两种包装，非通用画质验收。
- 新隔离DB／本机5790实际网页：MC-a91aa5c8133f r1、AP-a2dec0aafa17待审。
  播放器readyState4，720×1280，最终currentTime15／ended=true／error=null。
  实际下载哈希与保存及审批范围一致：
  ce4c13c4eecd50eb2af6b222f2a39946ce7e4d3bac1a5d6df4dd68a7068b82b2。
- P-102最终保存失败：MC-65cdca3d844b r1 RECORDING_FAILED，该来源无预览／审批。
  仅重启本轮应用、保留同DB／配置，网页恢复至REVIEW_PENDING／AP-09c1344feaa2。
  同版本、媒体元数据相同，五份MP4清单／字节未变；仅一次TEXT_GENERATION_STARTED、一个对应审批。
  恢复文件哈希为f65a3666e0c97bd254e716da4905850f7c8647a8f5501f3e71037b3227f9f673。
  独立只读SQLite核对审批文件／脚本哈希、0效果、库存12／8／0；未审批或发布，恢复未重生成。
- 首次实际渲染发现FFmpeg6不接受fade时长`.4`，改为`0.4`后实际成片通过。
  初始诊断脚本用了错误审批表名，依据真实approvals表修正后只读核对；没有改schema／审批迁就诊断。

原始配置／DB／工具／日志／预览片仍忽略；源码发布／PR／Jira收据发生后另记。
未新增真实模型、Windows9.0.2渲染、新源码ZIP／Canvas下载／现场验收；
无任意摄影／音频／扩散视频，不代表完整MC／Stage2完成。


## BA conditional review checkpoint · 30 October 2026

本次新验证（不复用 PR #8／#14／#15 为新证据）：

- 基线 b5f496ea7e1f9ad46a3afff7e995bb86e56f536b；独立 KAN-15-ba-conditional-review。
  实现与记录构成本次 PR 源码树，发布提交／树及 CI 在创建后记入 PR。
- Windows 11 Pro 10.0.26200，应用 Python 3.14.5、Node 22.19.0；复用 Strata 0.2.1、
  terminal/build 0.1.46.1、模型 Python 3.12.15、qwen3.8-flash-next-gyro-gyro-s。
  原 8080 本地配置超时120秒／输出512 tokens，不安装、下载或升级，不启用 MC 真实／媒体。
- 改动前完整 Verify：264／85.362秒；实现后模型确实关闭时281／93.948秒，来源124文件／41组、
  来源哈希／成员交接和 JS 通过。17项新增为受控夹具，不能当真实模型证据。
  初次聚焦运行9个失败来自同一新增助手把原订单 P-103 误写为 P-102；核实种子后仅修正该期待，
  随后63项 BA 测试／10.275秒通过。
- mock 5770 独立 mock.sqlite3：真实客户网页 BA-81d4bb03d2a4 r2，AUD10 无匹配后同意复核，
  AP-5d21cf1b60cc；Founder REQUEST_REVISION／DEC-f9f2a1951307 DELIVERED，咨询 CLARIFYING，
  没有成功建议或业务效果。
- live 5771 独立 strata.sqlite3：真实网页 BA-87b0434b3bd5 r1 完成模型需求解释。仅停止本轮
  70118e93fb34491faa5f521618baacd9 实例；客户确认保存 r2 INCOMPLETE／LLM_UNAVAILABLE／simulated:false。
  同意后生成 AP-124e20c5ffa0 r2，Founder APPROVE 为 DEC-a26f82afb678／DELIVERED。
  模型仍停机时独立数据库读取为 CLARIFYING，旧结果仍 INCOMPLETE，没有直接成功。
- 恢复原模型为本轮 c6618103cad34cd099eca0c74d4881d8；客户网页再确认后真实推理，r3 COMPLETED／
  simulated:false：P-101／AUD48，Moisturises dry skin、Fragrance-free，catalogue:P-101:v1／AVAILABLE。
  独立只读 SQLite 核对 ID／名称／价格／版本／tone／事实／无香和约束；库存仍12，ORD-1001仍P-103，
  一个决定、零效果。3次旧r2确认返回STALE_SCOPE，旧决定重送STALE，无第二次推理或效果。
- 受控测试覆盖无同意／越权／CSRF／会话／缺需求／医疗／草稿、无回执／不可用和原子回滚、
  待定／拒绝／要求修改、变化的身份／来源／版本／库存／无效输出、推理无数据库连接、取消／并发重复，
  以及AP保存失败后的重启恢复／重复重送。它们不是每一分支的真实模型验收。
- 仅停本轮5770／5771应用与准确模型实例，端口关闭；原配置／数据库SHA-256及56个模型文件元数据一致。
  原始日志、测试库和捕获在忽略目录 var/ba-review-20261030，不进入公开仓库。

视觉核对PDF物理页28／36／42／48的 ReviewPort、回执、精确决定和复核不能直接成功；不是完整UML审计。
未新验证：一般医疗／中文／语义质量、分布式复核服务真实故障或整盘丢失、队列／通知／过期、
长期多人GPU、Mac真实调用、旧结构化BA复核及最新版ZIP／Canvas／现场。
本次涉及的大验收组保持PARTIAL，未涉及的NOT_STARTED行保留；AP负责人评审待办；自测／CI不等于人工Approve。

## 真实 CS 换货集成 · 2026-10-29 — 本次新证据

Danny／M1 明确授权 KAN-15／GR-INT-02 本切片，AI 辅助。从已获取的干净 main
c276fc35f600edf060e9d75e6833c4e22ef2015f（PR14）建立 KAN-15-cs-live-handoff；保留旧游戏本
分支／历史及原队友贡献，不认领／重分配 starter。2026-10-29 实际 Jira 为 Verification／Danyang Wang，
保持该状态，不标 Done；发布／CI／合入收据见本轮 PR。

本次目视 CS-CL／ACT／SEQ／STM 的公开 PDF 实际页24／37／43／50；此前 CO 页27／47／48／53属历史
设计证据，非完整 UML 审计。

| 检查 | 实际结果 |
|---|---|
| 修改前 | 干净 main c276fc3，**237项／78.055秒**；来源120文件／41组、哈希／成员交接／JS通过。 |
| 最终源码 | 模型已实际关闭，**264项／84.530秒**通过；test_cs_live.py 新增27项，来源123文件／41组及JS通过。旧CS／CO业务测试未改。三处旧预期按新接口更正：Strata CS未连接→LIVE、继承mock的MC替身CS→MOCK、旧真实交接禁用→Founder角色拒绝；未删安全测试凑数量。 |
| 合约／失败 | 精确意图／需求字段及原文证据，无权限字段，保守需求／无香核验、混合需求／预算、模糊／不支持／否定、会话／CSRF／角色／归属／政策、缺失能力、不可用／超时／无效输出／不回退。两段推理均释放DB连接，目标回调中并发写库测试通过。 |
| 旧版本／重复／保存 | 旧意图／建议／确认不能跨版本，更正作废旧审批；并发／重复入口／交接只一次模型尝试。真实SQLite审计ABORT：派发意图写失败阻止推理；最终意图保存失败留INTERPRETING；交接结果保存失败保留已提交SENT，不重新推理或生成审批。503 CS_STORAGE_UNAVAILABLE不声称已存完成。旧真实服务入口拒绝写事务内推理；既有一次性／AP恢复仍通过。 |
| 实际网页5761 | 新忽略live.sqlite3；CS-7b9121eb3bc0 r1：真实意图READY／simulated:false，预算6000分、无香必需；Founder通过CO调用真实BA→P-101 AUD48、两条原文事实、catalogue:P-101:v1、AVAILABLE。客户确认→AP-cceab8a5fb31 r1；Founder批准ORD-1001→P-101精确范围→DEC-6ad2d0800f42 DELIVERED；客户最终确认→RESOLVED／CO COMPLETED。无真实交易／发货。 |
| 独立读回／重放 | 直接数据库核验商品ID／名称／价格／版本／tone／无香／原文事实／需求证据；建议时库存12，当前11对应一次效果。再三次认证确认／交接仍**一个审批／已提交决定／效果**，终态重放不重新推理。 |
| 真实澄清／不支持 | customer-2／ORD-2001、CS-b91669cdd7a9：r1只有换货→NEEDS_INFORMATION；r2退款→UNSUPPORTED／UNRESOLVED；r3完整更正→READY。均实际模型HTTP调用，与上述网页主线区分。 |
| 实际停机 | 仅用--if-instance-id停止本轮新实例2973d663358f4500a58de13d1c8ac5f7，8080关闭；本轮应用同库重启。r3 Founder BA交接→UNRESOLVED、CO_TARGET_UNAVAILABLE／上游LLM_UNAVAILABLE、simulated:false；客户r4明确新解释→FAILED／LLM_UNAVAILABLE／false。网页显示模型解释失败，无确认／审批。库中仍只有此前授权测试的一次效果／决定。应用健康ok／配置LIVE与模型就绪不同。 |
| 默认mock5760 | 模型关闭时实际网页CS-a4a745e083c5 r1自然入口→READY，Founder交接→AWAITING_CONFIRMATION／P-101；意图及建议均明确simulated:true。此库无审批／效果，旧结构化换货由完整回归覆盖。 |
| 环境 | 仅停本轮5760／5761，原配置／数据库SHA-256及56模型文件大小／时间清单一致。保留原分支，无模型／工具安装下载升级、配置覆盖、结构／依赖或其他进程更改。 |

同一游戏本Windows11 Pro build26200，Python3.14.5、Node22.19.0；复用Strata0.2.1／
Terminal0.1.46.1／CUDA13 engine0.1.46／模型Python3.12.15／qwen3.8-flash-next-gyro-gyro-s。
既有8K／单请求／1536MiB余量／vision-MTP和120秒／512输出配置不变。引擎日志有实际prompt／decode，
原始尾部私留；其中90／59 token完成并stop仅是请求证据，不代表吞吐／延迟基准或长期稳定性。

开发中纠正：新测试误用kind而非已有decision；新词法检查变量覆盖意图引文；完整回归揭示旧MC替身
CS标记预期。不改AP／MC逻辑。受控HTTP辅助工具误期望200而非自然创建201，复用已存请求，未删库重建。
前一263项记录被新增分阶段意图审计回滚和旧结构化记录入口后的264项取代。

原日志／库／读回／引擎／保护清单在忽略var/cs-live-20261029，截图仅本地；密钥／会话／库／模型／ZIP
不发布。未实现通用语义／医疗验证、多轮记忆、退款／通知／可选项、通用异步CO队列／保存恢复或物理取消。
中断INTERPRETING／SENT需客户明确新版本更正，不自动重发推理。完整CS／CO、41组／NFR、BA条件审批、
新冻结包／Canvas／现场、Mac真实路径、远程访问及更广稳定性待验。测试绿不代表Stage2完成。
Jira实际Verification／Danyang；合入后短评链接PR，不将任务／epic标Done；远程CI／合入收据见PR。

## Mac 集成复核 · 2026-10-29

从已校验独立交接 bundle 恢复 5073dbb，比已获取 main 515bfa5 多十个提交。六项交接文件哈希、
120 个源码文件大小／SHA-256、完整 bundle 和 git fsck 均通过。Danny 明确要求发布；这是 AI 辅助
复核／自检，不冒充队友认可。

Mac 原始完整运行有一处断言失败：VideoConfig 会解析 /var→/private/var 别名，而测试预期路径未解析。
不改源码、改用规范 TMPDIR 后验证了原因。本次将测试预期输出路径 resolve，不改变运行行为。
使用正常 Mac 临时目录，Python 3.9.6 的 **237 项全部通过（29.466 秒）**；来源核验
（120 文件／41 组）、JS 语法和空白检查通过。

隔离 5760 mock 网页：BA 缺预算／香精要求→同 ID 澄清→客户明确确认→r3 COMPLETED／P-101。
MC 保存失败样例→RECORDING_FAILED，不显示未提交生成内容／审批；应用重启保留草稿，
Recover saved generation 后仍为 r1，进入 REVIEW_PENDING。独立读库：两条记录、一条待审 MC、
零业务效果、库存 12／8／0。本轮未运行模型、FFmpeg 渲染、真实交易或新 Canvas 演练。
下方 191 项冻结包真实 BA／MC／MP4 演练属于 eb8f0de；237 项 Windows 交接证据不是本轮 Mac 真实运行。

新增历史的 152 个 blob 未发现禁入运行文件路径、私钥／GitHub token 特征；只是有界检查，不代表全面密钥审计。
新远程 CI／准确 head／本人 PR 审阅层例外／合并回执记录在 PR，Jira 只补简短最终节点；
完整任务验收前保持 Verification。

## CO 交接失败保留 · 2026-10-29 — 本次新证据

分支 KAN-15-co-handoff-failures；干净起点 d8d1826cd8e0edbe3899f9d68a4da6b90b2c5987；
获取后 main 仍 515bfa537e31a01b9e9a24400a7112f8103babb3。包含本节的提交标识最终源码；
这是本地证据，非远程 CI／评审。Danny／M1 授权 KAN-15 共享例外、AI 辅助，Guiyu Liu 归属及认领不变。
本次目视核对 CO-CL／ACT／SEQ／STM 的 PDF 实际页 27／47／48／53；旧选页盘点属历史，非完整 UML 审计。

| 本次检查 | 实际结果 |
|---|---|
| 修改前 | Windows Verify **210 项／66.927 秒**通过。 |
| 最终源码 | **237 项／82.653 秒**通过；新增 tests/test_co.py **27 项**，CO 单测 27／11.444 秒；既有流程子集 29／4.786 秒。未改／删旧测试。来源 **120 文件／41 组**、哈希／五人交接及 JS 语法通过。 |
| 上下文／来源 | 缺失／非对象／无效字段、错误预算类型不派发；保留整数 AUD 分，仅转四个需求字段。覆盖已存 CS 关联／归属／版本、过期范围、输入输出变异与无效重放。 |
| 目标／结果 | 无目标／不可调用／属性异常／模式错误、超时／不可用／异常、畸形／失败／未完成结果均覆盖。保留有效原始模式，不回退、不泄漏异常原文。商品／版本／可用性／预算／需求／事实／当前证据独立校验；目标自由说明替换为安全控制文案。 |
| 重复／保存 | 重复／并发保留一次尝试和一次目标调用，更正版本保留历史。真实 SQLite audit ABORT 分别作用于派发前、成功结果后、失败结果后，另验 query_only；原子回滚并返回 503 CO_STORAGE_UNAVAILABLE，不声称痕迹已存。既有换货／AP／一次性／核对／保存恢复回归仍通过。 |
| 实际网页／5750 | 新 browser.sqlite3，实际当前 Company／HTTP／UI，使用明确的仅本地 scratch mock 目标替身。CS-e6a20b8dc2e0／CO-a5e41e057102：r1 超时→UNRESOLVED／ESCALATED，重启仍保留；再三次认证 coordinate 调用仍一次尝试。r2 不可用→CO_TARGET_UNAVAILABLE；r3 畸形→CO_INVALID_RESULT；均 UNRESOLVED／ESCALATED。失败时无确认或审批入口。 |
| 空上下文／网页 | 仅本轮一次性测试库 CS r4 needs 被设为 null；网页仍可用，保留 CO_INVALID_CONTEXT／CLARIFICATION_REQUIRED、dispatched=false，CS UNRESOLVED。未操作原数据库；这是受控损坏测试，非产品开关。 |
| 明确更正／网页 | 客户更正 r5，Founder 新交接→P-101 AUD48、catalogue:P-101:v1、AVAILABLE、mock 标签。客户确认→CS REVIEW_PENDING、CO AWAITING_APPROVAL，一项 AP-700222059d80 PENDING。保留四次失败与一次完成的只读建议。未点击 Founder 批准、未执行换货。 |
| 效果／环境 | 测试库提交决定／效果均零，库存 12／8／0 不变。仅重启／停止本轮服务。原配置／数据库 SHA-256 及 56 个模型文件大小／时间清单一致。8080 模型未启动，未结束原服务、安装／下载／升级、增加依赖／结构或读取凭证。 |

同一游戏本：Windows 11 Pro build 26200，应用 Python3.14.5，Node v22.19.0。
Strata0.2.1／engine0.1.46 CUDA13／模型 Python3.12.15／qwen3.8-flash-next-gyro-gyro-s
为历史安装版本证据，不代表本轮推理或模型就绪。BA／MC 默认 MOCK，交易模拟，CS 意图 NOT_CONNECTED，
产品真实 CS 交接仍阻止。

仓库根目录复现自动检查：
`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/windows.ps1 -Action Verify`，不需模型。
网页故障替身和 null 注入仅为 scratch 验收工具，非应用支持开关；单测独立复现目标和真实 SQLite 故障。
正常 mock 更正沿用客户 **Correct the needs and request a new proposal**，再由 Founder
**Start advice handoff**；未增加盲重试入口。

原始日志／读回／测试库／进程收据留在忽略目录 var/co-handoff-20261029，截图留本地 outputs。
会话／配置／库／模型／故障替身不入 Git。边界：同步只读调用在**调用方既有 SQLite 事务内**先写意图再
调用，未为外部效果独立提交持久意图。未增加异步回调／提供方取消保证、通用调度、队列、完整 CO
取消／升级／恢复或可选重试。审计保存失败有真实回滚／错误证据，未新实现通用 CO 仅保存恢复。
用例仍 PARTIAL，CO-T-02／03 从 NOT_STARTED 改 PARTIAL，不能据此声称 Stage2 完成。
冻结 eb8f0de ZIP 早于本源码，当前新包／真实模型／其他电脑／现场回归待验。Jira 未核实／更新待办，
未读写／推送／PR／合并／Canvas；相关负责人评审待办。

## MC 生成恢复检查点 · 2026-10-29

本轮为 MC 生成持久化新证据，下方历史 ZIP／媒体／AP 证据保持原范围。Danny / M1、AI 辅助，
分支 KAN-15-mc-save-recovery，干净基线 ca1737b9e3264f0d93c8e41516a2c15cd39c02f7，
获取后 main 仍为 515bfa537e31a01b9e9a24400a7112f8103babb3，任务及队友归属不变。

| 本次检查 | 实际结果 |
|---|---|
| 修改前 | Windows Verify 191 项通过，57.685 秒。 |
| 最终完整测试 | **210 项通过，66.961 秒**，含 MC 57 项（新 19 项）。来源 117 文件／41 组、指纹／交接和 JS 通过。最终审批权限保护测试前的 MC 专项为 56 项／9.797 秒；未删除测试。一个旧最终保存断言改为持久 RECORDING_FAILED／503，不再预期原始 SQLite 异常／DRAFTING。 |
| 存储边界 | 真实 SQLite 审计 ABORT 在插入待审后回滚草稿／待审／审计整个事务，保留草稿。完整最终写故障留下 GENERATING／pending，不伪称失败已存。阶段失败无草稿；明确重试新修订。并发／重复恢复仅一个待审／事件；生成重试不能替换既有审批／决策。 |
| 默认 mock 网页／5740 | MC-5f929d55f172 r1，一次最终保存演练故障→RECORDING_FAILED／无待审→实际重启→网页恢复 AP-c85f47d8de10 PENDING；再三次已认证恢复保持同 ID。 |
| 真实 SQLite 失败／5740 | MC-596579a178a6 r1，测试库触发器使最终 GENERATION_RECORDED 审计失败，HTTP503 MC_STORAGE_UNAVAILABLE、无待审。移除触发器、重启后网页恢复 AP-084a5a2f9a55；网页取消到 r2 CANCELLED，旧待审 SUPERSEDED，原历史保留。 |
| 无草稿／5740 | MC-95429dbd1fb8 r1，真实阶段更新触发器失败，GENERATING／无 pending／无待审。移除触发器、重启后网页明确重试 r2，AP-c7f4c29db6d1 PENDING；再三次恢复不重复。两个触发器均已移除，未作用于旧数据库。 |
| 真实 MC／5741 | MC-7dbc0096d878 r1，energetic／factRefs=[50 ml]；按当前目录独立重构实际字面脚本／三帧。真实文字及模板 MP4→显式最终保存失败、无待审，复用既有 Strata／工具。 |
| 模型停止＋应用重启＋实际网页恢复 | 以实例保护仅停止本轮 1340b2d713ce4100ad47c3abc53ceb6c，8080关闭，同 DB／媒体配置重启应用。Recover→AP-802103339dca PENDING，无已提交决策；textSimulated=false／mediaSimulated=false／videoModelUsed=false，三次重复恢复同一待审。 |
| 同一真实文件 | 新忽略目录 media-output 的 artifact dfad0c0d2bc74ce68419de2f3bf92981，63,274 字节，SHA-256 e838d2915c120ddc4a0c249c658b8dcbe81ebdef2025ea9306d8fa23a615c39d，恢复前后相同，脚本／分镜／manifest 同样相同。网页 readyState=4、15 秒，实际播放到7.550395秒、无错误；实际浏览器下载哈希一致。恢复不需推理／渲染，单测也将任何生成器调用视为失败。静音720x1280／24fps模板，无AI场景／音频。 |
| 模型关闭后新请求和重试 | MC-ed37efde1777 r1及网页明确重试r2均 GENERATION_FAILED／LLM_UNAVAILABLE，原真实标签，无脚本／媒体／待审／回退；应用健康仍ok。 |
| 范围／安全／迟到结果 | 单测覆盖 owner／Founder／会话／CSRF／精确字段、已存文字／帧／模式篡改、目录改变、缺配置／文件、pending历史隐藏、取消保存失败及迟到结果抑制。运行中取消使用离线阻塞provider替身，不作为物理GPU中止证据。 |
| 效果／环境 | 两库零业务效果、零已提交决策，库存12/8/0不变。仅停止本轮5740／5741及精确模型实例，原配置／数据库哈希和56项模型文件大小／mtime一致。无模型／工具下载、升级、新依赖、schema变更、真实支付／发货／发布。 |

同一游戏本 Windows 11 Pro build26200、应用 Python3.14.5、Node v22.19.0；既有
Strata0.2.1／Terminal0.1.46.1／engine0.1.46 CUDA13／模型Python3.12.15，
qwen3.8-flash-next-gyro-gyro-s；8192 context、单请求、1536MiB reserve、route-tail-skip7，
已存 vision／MTP 设置未改，120秒／512输出token。复用 FFmpeg／ffprobe9.0.2及Windows Arial。
引擎实际MC请求330prompt／49生成token，prompt／decode7702+2136ms，不是浏览器端到端耗时。

本轮发现并修正：抽出校验块时遗漏claims局部引用；共享HTTP初版改变空白mock修订失败分类；
已取消／已失败界面沿用含糊的生成提示。既有检查发现问题，最终测试及网页检查通过。
浏览器下载验证等待约192秒后完成且哈希正确，这是本地自动化观察，不是已确定的应用延迟上限。

原始日志／读回／触发器清单／引擎副本在忽略目录var/mc-recovery-20261029，本地outputs保存截图／视频，
只提交脱敏摘要。未生成新ZIP，冻结eb8f0de包早于本代码。Jira未核实／更新待办，按要求不读写；
未推送／PR／合并／Canvas。**剩余：**部分生成／渲染断点续作、provider物理中止保证、完整MC已提交决策／
本地保存恢复矩阵、孤立文件清理、自由文案／AI场景／音频／一般质量、新包／其他电脑／现场及完整MC／
Stage2验收。MC-T-06仍PARTIAL。


## 冻结源码 ZIP 彩排 · 2026-10-29

本地部署新证据，与下方历史记录区分。Danny / M1、AI 辅助 KAN-15 共享范围；GR-INT-03 是内部标签，
不是 Jira key。分支 KAN-15-zip-rehearsal-eb8f0de，干净冻结源码
**eb8f0de8d412344e828daf9032898c2dbb6155ee**，获取后 main 为
515bfa537e31a01b9e9a24400a7112f8103babb3。本轮未改应用代码。

| 本次检查 | 实际证据 |
|---|---|
| 压缩包 | elec5620-source-eb8f0de.zip，5,658,127 字节，116 文件；SHA-256 **bf7d8b0324c9797e2adb03d0727a89aa31325ebb5a22223fd7a528760d25bba4**。逐文件匹配干净已提交源码；不含 .git/venv/var/数据库/凭证/权重/二进制/媒体/旧输出，保留公开脱敏参考文件。同路径重复打包被拒绝，哈希不变。 |
| 新目录执行来源 | `D:\elec5620_project\rehearsals\20261029-eb8f0de\fresh source`，独立 venv／配置／mock 与 live 数据库／media-output。实际解释器、模块及服务器执行路径均在新目录，Python 导入路径无旧仓库。重复 Setup 保留配置；解压源码哈希不变。 |
| 新目录完整 Windows Verify | **191 项通过，56.564 秒**；来源 116 文件／41 组、来源指纹／交接和 JS 语法通过。未改测试，数量与冻结媒体检查点一致。 |
| mock 网页／5730 | CS-6a4c29fa9998 r1，AP-c326a7d02bb7，DEC-ea6386a58ce9 APPROVED/DELIVERED，精确 ORD-1001→P-101。客户最终确认前 effects=0／stock=12；确认后 RESOLVED、SIMULATED_EXCHANGE_REQUEST_ACCEPTED、effects=1／stock=11。再重复三次已认证确认，仍一个效果、stock=11。 |
| 真实 BA 网页／5731 | BA-e753089f2935 r2 COMPLETED、simulated=false；自然需求提取后客户显式确认。P-101／AUD48；独立检查目录版本、库存、条件、价格和字面事实。 |
| 真实 MC／5731 | MC-9a09e9cd654b r1，energetic 需求，factRefs=[50 ml]；textSimulated=false、mediaSimulated=false、videoModelUsed=false。新 artifact 292986dbf7ec491888c42998a6de9a57 在新目录 var/media-output 生成，未复制旧媒体。 |
| MP4 与审批 | 63,274 字节，SHA-256 **e838d2915c120ddc4a0c249c658b8dcbe81ebdef2025ea9306d8fa23a615c39d**；15 秒、720x1280、24 fps、H.264/yuv420p、静音。probe／完整解码／三帧检查通过；浏览器到 15 秒、ended=true／readyState=4。实际浏览器及已认证 HTTP 下载哈希相符。AP-eb1cb4015f7c／DEC-1c3f48eabe4c APPROVED/DELIVERED，绑定精确修订／文件／脚本哈希。确定性模板字节与历史样本一致，但文件／UUID／目录是新生成。 |
| 授权与效果 | Danny 在网页操作前明确授权两项具体测试审批及客户模拟确认。无发布、支付、发货；live 数据库 effects=0，库存=12/8/0。 |
| 模型关闭失败 | 仅以实例保护停止本轮模型 6a7bb9a13bae4235a54b2ef260b7a2b8。应用仍健康／配置 LIVE，模型端口关闭。新网页请求 BA-6a52c5553047 r1 保存 INCOMPLETE／LLM_UNAVAILABLE、simulated=false，无结果／推荐／回退。既有成功及已认证 MP4 访问保留。 |
| 既有 CS 限制 | 意图 NOT_CONNECTED；真实 coordinate 探测返回 503 LIVE_HANDOFF_NOT_CONNECTED，不产生记录。未扩展真实 CS／交易。 |
| 清理 | 仅停止本轮 5730／5731 应用及精确模型实例。原配置／数据库 SHA-256、56 项模型文件大小／mtime 一致；冻结包及解压源码哈希不变。 |

环境：本次检测 Windows 11 Pro 10.0.26200／build 26200，新 venv Python 3.14.5、Node v22.19.0；
复用 FFmpeg／ffprobe 9.0.2、Windows Arial。既有模型安装 Strata 0.2.1／Terminal 0.1.46.1／
engine 0.1.46 CUDA13，模型 Python 3.12.15、qwen3.8-flash-next-gyro-gyro-s；
已存 8192 context、单请求、vision／MTP 关闭、1536 MiB reserve、route-tail-skip7，120 秒／512 输出 token。
本轮未重新安装、升级、下载工具／模型或复制权重目录。
引擎记录 BA 提取 prompt285／生成85 token（6684+4927 ms）、BA 推荐295／25（3050+895 ms）、
MC330／50（2408+1442 ms）。这些不是浏览器端到端耗时，不以配置／健康代替实际推理证据。

原始日志、数据库读回、清单留在忽略目录 var/rehearsal-20261029-eb8f0de；独立数据库／配置／媒体
留在新目录，仅提交脱敏摘要。冻结包源码是 eb8f0de，后续仅文档提交／回执不在该 ZIP 内。
Jira 未核实／更新待办，按要求不读写；未推送／PR／合并／上传 Canvas。

**本轮未新验证：**AP 保存失败恢复（保留历史证据）、全部 BA／MC 生命周期／失败组合、MC 完整恢复、
自由创意语义、AI 场景／音频、其他电脑／系统／浏览器、现场网络、Canvas 下载、全新电脑／首次离线安装
或完整 Stage 2 验收。本次保留失败场景是模型不可用，不是存储恢复。


## MC 模板 MP4 验证证据 · 2026-10-29

这是本轮本地媒体新证据，不将历史占位分镜重新算成视频。Danny / M1 授权 KAN-15 有界增量，
干净基线 950ad9205d0a4522d7dc775fb2d049fc3ef9c5d9，分支 KAN-15-mc-template-video；
获取后 main 仍为 515bfa537e31a01b9e9a24400a7112f8103babb3。AI 辅助，保留原归属／任务登记。
Jira 未核实／更新待办，按要求不访问／修改；未推送、PR、合并或上传 Canvas。

| 本次检查 | 实际结果 |
|---|---|
| 修改前 | Windows Python 3.14.5，181 项通过，31.465 秒 |
| 最终 Windows Verify | **191 项通过，53.115 秒**（原 181 + 新媒体 10）；来源 116 文件／41 组、来源哈希／交接及 JS 语法通过；MC 单独 38 项通过。双语文档后重查来源／JS／差异。 |
| 新离线测试 | 精确视频哈希审批、工具不可用／超时／进程失败无回退、文件篡改／路径标识拒绝、分镜篡改拒绝、过期链接／失败修改、会话／Founder／范围响应、配置／超时边界、mock 文字制作和错误格式拒绝。测试替身字节明确不是可播放证据。 |
| 实际 mock 文字／模板文件，新库 5720 | MC-ea97fa92b3ee 修订 1 APPROVED/DELIVERED；文字模拟、媒体真实制作、无视频模型。62392 字节，SHA-256 4973c74e7bcf4f690583034481e2ac4236a773164ce5851408719c8ee254cdce。浏览器时长 15 秒、720x1280，播放推进至 8.833 秒；实际浏览器下载哈希匹配，抽查三镜头。 |
| 实际本地模型／模板文件，新库 5721 | MC-24849de55d1e 修订 1 CALM／Fragrance-free，REQUEST_REVISION 已投递；修订 2 ENERGETIC／50 ml，新文件／哈希／审批；修订 3 同一有据内容、修正 LF 排版，再建新文件／审批，前两审批 SUPERSEDED。独立核对模型输出、保存目录、脚本和分镜。 |
| 最终 MP4 及网页批准 | 修订 3，63274 字节，SHA-256 **e838d2915c120ddc4a0c249c658b8dcbe81ebdef2025ea9306d8fa23a615c39d**；15 秒、720x1280、24 fps、H.264/yuv420p、无音频。FFprobe／完整解码通过；三镜头视觉检查，浏览器 currentTime=15、ended=true、readyState=4。AP-b460e73848cc APPROVED/DELIVERED、DEC-76662eeae6e9，绑定精确修订／视频／脚本哈希，SQLite 另行确认。 |
| 下载及旧链接 | 最终真实 HTTP 下载哈希与当前保存文件匹配；修订 1／2 链接返回 409，不替换为新文件。此前 mock 成片也实际通过浏览器下载并核对哈希。 |
| 实际编码器缺失 | 不改已安装工具／原配置，只以独立配置指向故意不存在的工具重启本轮 mock。网页保存 MC-b6c143192c82 GENERATION_FAILED / MEDIA_UNAVAILABLE，无脚本／媒体／审批、不回退；保留原已批准文件和记录。 |
| 停模型及清理 | 停止本轮准确模型实例后，保存视频仍可网页访问／播放，无新推理。仅停本轮 5720／5721 及准确模型实例；原配置／数据库哈希、56 个模型文件大小／mtime 匹配；两个测试库业务效果 0，库存 12/8/0 不变。 |

可选 FFmpeg/ffprobe 9.0.2 下载 114768076 字节（约 109.45 MiB），解压目录 329221735 字节
（约 313.97 MiB），首次保留包和目录约需 424 MiB，加媒体输出。包 SHA-256
60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba，核对发行方
GitHub digest。仅本地使用系统 Arial，源码不分发字体／工具；重复 Setup 保留配置哈希、无重复
下载或覆盖，未增加 Python 依赖或修改 PATH。

复用 Windows 11 Pro 25H2 build 26200.9711、应用 Python 3.14.5、模型 Python 3.12.15、
Strata 0.2.1／Terminal 0.1.46.1／engine 0.1.46 CUDA 13、qwen3.8-flash-next-gyro-gyro-s。
保持 8192 context、单请求、关闭 vision/MTP、1536 MiB reserve、route-tail-skip 7、模型超时
120 秒／512 输出 token；无模型下载／升级／复制或配置变更。三次 MC 引擎输出 61/40/40 token，
prompt/decode 耗时 6906+2383、1939+1016、328+844 毫秒，不是完整网页耗时。

发现并修正：新增测试误用了未定义账户；版本诊断经 Select-Object 提前关闭输出管道造成假失败；
实际抽帧发现 Windows CRLF 使行距翻倍，改为明确 UTF-8 LF 并回归校验，最终修订 3 为修正版本。
恢复中断后会话失效导致一次决策 401，未计入批准；刷新重登确认仍待审。自动审批审核随后要求对
精确测试修订明确确认，Danny 回答后才成功点击，未用其他入口绕过。同一主机不同数据库端口共享
浏览器 cookie 名，切换时应重登，不能认为端口隔离会话；这是测试环境条件，不是模型故障。

原日志在忽略的 var/mc-video-20261029，成片／清单／作业在 var/mc-media，工具在
var/media-tools，本地 outputs 有最终 MP4／截图，仓库仅保存脱敏摘要。安装／启动／停止及许可
前置见 WINDOWS_LLM.md；源码 ZIP 排除工具／字体／模型／配置／数据库／媒体／日志。没有新 ZIP
校验或验收，旧 f7bb141 包早于本增量。

**待办：**仅文字卡模板，不实际执行相机动作，无商品图像／视频模型场景／音频、一般创作／医疗
语义或媒体质量验证、MC 取消和生成／最终保存持久恢复、孤立文件清理／历史下载、更广浏览器／
OS／新 ZIP／现场验收。最终保存可能留下无输出／审批的 DRAFTING；技术检查和测试通过不代表
MC-T-04/05/06 或 Stage 2 完成，这些仍 PARTIAL。


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
