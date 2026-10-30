# 共享接口约定与实现映射

## BA/MC 有界失败修复 · 2026-10-31

KAN-10 结构化字段为 message/concern/budget（澳元）/fragranceFree。续办用显式字段子集和正整数
contextRevision；全量替换丢弃遗漏的旧约束。保留同一归属 ID，修订递增，旧建议仅作历史；取消抑制晚到结果。
Company.consult 增加可选 rid 用于续办；revise_consultation、cancel_consultation、recover_consultation
及 BeautyAdvisor 的对应操作仅服务层。低层方法仍使用调用方事务；Company 复用 BaIntake ADVICE 暂存/恢复、
当前证据校验。所有 BA 快照隐藏 pendingOutcome.value。已有结构化 HTTP 创建推理后复核会话；无新增路由、
结构化卡片按钮或结构化 AP 审批。
KAN-12 在生成和已存文本校验前要求非空事实字符串列表；无效来源返回 DomainError INCOMPLETE，现有保留型
草稿/修订/Company 流程在存储可用时保存安全失败。无 schema、模型接口、媒体格式或 AP 权限规则变化。

中文阅读副本，依据 2026-10-29 英文主版同步。以[英文主版](../CONTRACTS.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

## 广告模板渲染 · 2026-10-30

可选渲染器使用源码自带PNG包装示意（另有SVG源文件）、固定影棚构图及有界
CALM／ENERGETIC／INFORMATIVE动效／点缀色。已验证字幕走textfile，不作为滤镜表达式；包装明确虚构。
不接受用户资产路径／URL，不新增模型、音频或功效事实。缺素材为MEDIA_UNAVAILABLE，不造备用成功／审批。
格式、标签、kind、元数据、文件／脚本哈希及AP范围不变；旧媒体按原字节读取／恢复。
素材更新只影响新渲染，恢复不重新生成或替换原文件。


## BA conditional review checkpoint · 30 October 2026

新增自然语言 BA-UC-01 E4 契约，无 schema／provider 变更：

POST /api/consultations/{id}/request-review 只接受
{contextRevision:正整数, consent:true, issue:1–1000字符产品问题}。
要求客户会话／CSRF／所有权及数据库当前客户角色；只接受确认需求后的自然语言 INCOMPLETE 建议，
不能带待恢复草稿或医疗停止。相同范围重复返回同一回执，变更问题须新版本；不接受自带 action／角色／
证据／决定／输出或审批ID。

服务端 action={type:REASSESS_ADVICE, consultationId, contextRevision}、actionRef=null。
最小证据={needs:{concern,budget,fragranceFree},issue,outcomeCode,adviceSimulated}，预算整数分。
失败分类受限，不传原始聊天／错误输出／订单／档案／凭证／会话。客户同意绑定当前版本。
AP回执、BA REVIEW_PENDING与审计原子提交；不可用／无回执／保存失败为BA_REVIEW_UNAVAILABLE，
不算成功或已提交。本地SQLite ReviewPort并非新增远程服务。

AP增加BA来源，沿用Founder决定意图／原子提交／存储恢复／投递；BA重查当前action／版本／同意／
确认约束／证据，恢复时也校验意图证据。APPROVE投递仅进入CLARIFYING／needsReady，旧失败建议仍未完成；
客户经原confirm-needs进入新版本重新评估。REJECT→INCOMPLETE，REQUEST_REVISION→CLARIFYING且needsReady:false，
均不能直接确认。普通有效建议不需复核；决定不能越过医疗／商品／事实／库存验证，不执行业务、
不直接调用模型、不自动重试。

自然confirm-needs接受Router可信会话复查回调，推理前关闭快照连接，暂存前核实当前客户／会话、
所有权、来源payload和版本；保留最终证据校验与草稿恢复。更正／重试／再确认／取消使旧复核失效并保存历史，
旧投递／恢复不能赋予新版本权限。旧结构化consult签名不变，本切片未给它接入条件复核。

## CS 意图v1与分阶段真实交接 · 2026-10-29

新增共享`interpret_service_request(message: str) -> dict`复用StrataLlm._complete／配置／错误。
精确字段：intent=EXCHANGE|CLARIFY|UNSUPPORTED，intentSource=原文引文|null，
needs={concern,budget,fragranceFree,sources}；沿用需求提取格式（AUD元、明确null、各字段原文证据）。
不传或接受可信身份／订单／政策／库存／商品／权限。独立有界词法核验需求／无香，混合需求／预算
不猜测，额外权限字段拒绝。否定／混合／退款／退货／取消／医疗请求澄清或转人工，非通用语义验证器。

POST /api/after-sales/intake仅orderId／message（Customer，201）；
POST /api/after-sales/{id}/revise-intent仅message／contextRevision（owner）。先验关联／政策，
保存INTERPRETING元数据，释放DB连接再推理，保存前复核当前会话／角色／来源／归属／版本／政策，
记录READY／CLARIFICATION_REQUIRED／UNSUPPORTED／FAILED。CS仍ASSESSING／NEEDS_INFORMATION／
UNRESOLVED。READY是待客户检查的解释，非审批；显示约束供更正。同样入口复用记录，更改需明确新版本。

Founder POST /api/after-sales/{id}/coordinate仅contextRevision，真实模式必填，旧mock空体兼容。
真实需当前READY意图和政策；CO.prepare_external提交一次SENT只读尝试，释放连接后以目录快照调用
BA.recommend_from_catalogue，再验会话／角色／来源／归属／版本／政策及当前商品／事实／库存，
CO.finish_external与CS结果原子保存。SENT仅待处理尝试证据，不是接收结果或效果；SENT／终态重复不
重发。客户新版本作废旧待回交接及精确审批，旧响应／确认不可重开；旧CustomerService.coordinate
真实入口返回CS_STAGED_HANDOFF_REQUIRED。

未改结构／依赖／提供方／客户端／配置或AP／效果合约，默认结构化／mock保留。
能力标记LIVE／MOCK／NOT_CONNECTED，intent.simulated／advice.simulated分别保留起源；
payload.simulated仍指模拟交易。模型不可用／超时／无效如实失败、不回退；SQLite写错误503
CS_STORAGE_UNAVAILABLE，不伪称痕迹已存。中断／最终保存失败保留INTERPRETING／SENT，需明确新版本
更正，未实现通用自动／仅保存CO恢复。确认→精确AP→客户再确认→一次模拟效果沿用原CS／AP服务。
本新验证路径取代下方历史禁用说明。

## CO 只读建议失败边界 · 2026-10-29

`Coordination.advice_handoff(db, rid, needs, advisor)` 签名及调用方事务不变。
要求当前同归属 CS 关联；新调用需 ASSESSING。仅转 message／concern／budget／fragranceFree，
预算已是整数 AUD 分。有效范围与当前已存范围不同返回 409 STALE_SCOPE；同来源／修订复用已存
结果，不新增调用／事件；再次尝试必须明确修订 CS。未改 HTTP／数据库结构。

payload.handoffs 保存 handoffId／fromRole／toRole／originId／contextRevision／handoffTime／
operation／authorisedContext／status／dispatched／result；payload.originRevision 和 CO 版本跟随 CS。
operation=READ_ONLY_ADVICE。上下文无效→安全 INCOMPLETE／CO_INVALID_CONTEXT，CO
CLARIFICATION_REQUIRED，dispatched=false。缺失／无效目标、超时、不可用／异常、无依据／未完成
结果→安全 INCOMPLETE、交接 FAILED、CO ESCALATED，保存白名单原因／恢复、businessExecution=false。
只保留安全上游代码，不保存异常原文或任意目标说明。既有 CS 保存 UNRESOLVED，无 actionRef／客户
确认／AP 审批；保留有效原始模式，不回退。

成功需商品与当前目录一致、库存可用、明确需求／预算／事实有据、证据引用／约束正确、观测时间带时区。
目标自由说明替换为安全 CO 文案。仅只读建议交接 COMPLETED；CO PENDING_VALIDATION 仍等 CS 结果。
HANDOFF_SENT 在调用前写，HANDOFF_FAILED／ADVICE_RESULT_RECORDED 保存结果；随既有 CS 事务
提交，非外部效果独立日志。SQLite 保存失败→503 CO_STORAGE_UNAVAILABLE、回滚且不声称证据已存。
不代表新增持久分阶段 CO 恢复／通用调度／自动重试，详见 VERIFICATION.md。

## MC 生成恢复检查点 · 2026-10-29

依据 MC-ACT-01／MC-STM-01（公开 PDF 第 39、51–52 页）及 MC-T-06，Danny 授权共享例外。
所有 HTTP 模式（含默认 mock）统一使用 Company.campaign 分阶段流程；既有注入式 MC
submit／submit_draft／revise 服务接口兼容保留，不因此自动具有 HTTP 持久恢复能力。

| POST `/api/campaigns/{id}/…` | 精确请求体 | 行为 |
|---|---|---|
| recover | 正整数 contextRevision | 同一已存结果／修订，不调用生成器；复核当前目录、实际文字／分镜、原模式和精确媒体 manifest／文件哈希后仅恢复一个待审。已保存则返回当前状态，保留后续决策。 |
| retry | 正整数 contextRevision | 仅无待保存结果／审批／决策的中断或失败生成；同 ID、修订 +1，按当前配置显式重新生成。有草稿返回 409 RECOVERY_AVAILABLE，生成重试不能替换既有审批权限。 |
| cancel | 正整数 contextRevision | 仅活动草稿；修订 +1、CANCELLED，保留历史、旧审批失效。同一已取消当前修订重复调用幂等；不追溯取消已决终态。取消后需新建 campaign。 |

均验证 Founder 会话、owner 和 CSRF，拒绝额外结果／模式或非法修订。revise 仍接收
brief／productId／contextRevision，更换范围并重新待审，拒绝已取消记录。默认 mock 保留空白修订
INCOMPLETE 行为；模型失败保留原模式。

GENERATING 在无写锁推理前保存范围。现有 JSON payload.pendingGeneration 保存修订／状态／结果／模式，
无需 schema 迁移；快照及操作返回只展示元数据，历史中也不暴露未最终保存文字／媒体／审批。
验证后的草稿、待审回执及审计同一事务提交。最终事务失败返回 503 MC_STORAGE_UNAVAILABLE，
可写时记录 RECORDING_FAILED；完全写故障可能留下 GENERATING 与已存草稿。阶段保存失败则无草稿，
不伪造可恢复结果；初始范围保存失败可能没有新记录。GENERATION_FAILED、CONTENT_REJECTED、
INCOMPLETE 保持区别。

Founder 专用一次性 mc_recording 是显式本地最终保存演练：503 MC_RECORDING_FAILED，草稿保留、
无待审；与真实 SQLite 失败测试区分。取消保存失败返回 503 MC_CANCELLATION_NOT_RECORDED。
原模板媒体配置未启用返回 503 MC_MEDIA_RECOVERY_UNAVAILABLE，保留待恢复结果；无效／已变化证据
或文件被扣留，不进入待审，需要修正后新生成。恢复不批准、不发布、不执行。

生成恢复与 AP 决策持久化／投递恢复分开。未添加物理中止、部分模型／渲染断点续作、孤立文件清理、
完整 MC 决策／本地保存恢复、自动重试或通用语义校验器。


## MC 模板 MP4 检查点 · 2026-10-29

Company(path, llm=None, media=None) 新可选注入保留默认 MockMedia。模板模式（含 mock
文字）走写事务外的 Company.campaign；仅真实文字／默认 mock 路径兼容。媒体增加
kind=TEMPLATE_VIDEO、simulated=false、modelGenerated=false、精确 frames、不透明 artifactId、
bytes／MIME、sha256、scriptSha256 和固定规格。textSimulated/mediaSimulated 分开，旧记录
simulated 表示文字。能力标签 TEMPLATE_VIDEO、健康 TEXT_WITH_TEMPLATE_VIDEO 只表示配置。

既有审批 action 增加 mediaKind=TEMPLATE_VIDEO、textMode、mediaSha256、scriptSha256，并
绑定草稿 ID／修订，AP 实现不变。只有校验的文件／清单可进入保存／审批事务。失败／超时／格式
异常保存 GENERATION_FAILED 及明确 MEDIA_* 代码，无输出／审批、不回退或自动重试。

GET /api/campaigns/{id}/media/{revision} 要求所属 Founder 会话、当前版本和已保存模板文件；
待审草稿允许内部预览，返回 video/mp4、no-store 及单范围字节响应 200/206/416。未登录 401、
角色／owner 不符 403、过期链接 409、缺少记录／媒体 404、文件丢失／变化 503。调用方不能指定
文件路径；下载重查清单／大小／哈希，不用新文件替换旧版本。预览／下载不代表发布。旧版、失败
或未提交文件可保留在忽略目录供诊断；本轮没有孤立文件清理、历史下载或持久媒体保存恢复。
文件缺失时拒绝访问，不倒改历史审批决策。


## MC 有界真实文字检查点 · 2026-10-29

这是显式开启的 MC 真实文字增量；默认 mock 保留原路径。要求 Founder 会话／CSRF，修改时
校验 owner。

| POST | 精确请求体 | 结果 |
|---|---|---|
| `/api/campaigns` | brief、productId | 201，保存的 MC 草稿或失败记录 |
| `/api/campaigns/{id}/revise` | brief、productId、正整数 contextRevision | 200，同 ID 新版本；旧审批被取代、保留历史；过期范围 409 |

拒绝调用方提供模式、结果、审批等额外字段。成功载荷包含 script／claims／product／evidence、
textPlan、simulated=false、textSimulated=false、mediaSimulated=true 和标注 mock 的媒体。
三镜头规则见 LLM_INTEGRATION.md；最终保存／提交前重查目录、版本和状态。真实审批 action 为
REVIEW_TEXT_DRAFT，绑定 draftId／draftRevision，含 textMode=LIVE、mediaKind=MOCK_STORYBOARD。
待审不等于批准，批准文字／模拟预览不等于生成视频或允许发布。

已知模型失败保存 GENERATION_FAILED 或 CONTENT_REJECTED；缺少／变化证据可为 INCOMPLETE。
失败不捏造输出或审批。最终结果事务回滚留下此前 DRAFTING 范围，无成功内容或审批；通用 HTTP
500 后应刷新查看记录。本轮不提供取消、结果持久暂存／恢复或自动重试。默认 mock 可保持原失败
契约。每条记录保留自身模式，当前能力配置不会重新标记历史结果。


## BA 生命周期检查点 · 2026-10-29

仅为所属 Customer 的**自然语言 BA 记录**新增操作；仍要求会话、CSRF 和正整数 contextRevision。
原结构化咨询及 CS/CO 调用契约保留。

| POST `/api/consultations/{id}/…` | 精确 JSON 字段 | 守卫及结果 |
|---|---|---|
| revise | contextRevision、message | ACTIVE/CLARIFYING/INCOMPLETE/COMPLETED；同 ID、修订 +1，完整替换当前原文，重新提取并要求新确认 |
| cancel | contextRevision | 仅 ACTIVE/CLARIFYING/INCOMPLETE；修订 +1、CANCELLED；按取消后的当前修订重复返回原状态 |
| recover | contextRevision | ACTIVE/INCOMPLETE 的当前持久草稿；只做最终保存、不推理；已保存的当前修订重复返回原结果 |
| retry | contextRevision | ACTIVE/INCOMPLETE 且无草稿；新修订、显式重新提取、再次客户确认；有草稿则 409 RECOVERY_AVAILABLE |

遵循 BA-STM-01 B 面板（PDF 第 49 页）：COMPLETED 可修改恢复，但不可取消；CANCELLED 必须新建。
取消抑制晚到输出，不中断已发出的 GPU 请求，也不撤销既有交付。替换原文不会暗中继承旧约束；
历史保留旧输入、核定条件、已适用结果及模式，明确标为历史。旧/取消修订返回 409，不能暂存或交付结果。

推理在写事务外完成，先将服务端 pendingOutcome 草稿提交至既有 payload，再重查当前修订/状态/
确认范围/目录/事实/库存，将最终结果与审计一起提交；无新表或模型接口。快照仅暴露草稿类型/修订/模式，
不返回未最终保存的建议内容。拒绝客户端提供结果、模式或额外字段。恢复保留原 mock/live 标签，即使配置
切换也不改变来源；首次恢复更新库存观察时间。重复恢复返回已保存结果/观察时间，不是新的库存检查。

最终保存失败返回 503 BA_STORAGE_UNAVAILABLE，存储允许时保存 INCOMPLETE/BA_RECORDING_FAILED；
连失败状态也无法写入时，可能留 ACTIVE 加草稿。草稿暂存也失败时不编造草稿，恢复返回 NO_PENDING_RESULT，
显式重试才新推理。ACTIVE 不证明进程崩溃；重试会明确取代可能仍运行的工作。
取消保存失败返回 503 BA_CANCELLATION_NOT_RECORDED，不宣称已停止。没有自动重试或交易效果。

Founder 专用 ba_recording 是声明的一次性最终建议保存失败模拟，保留草稿，不损坏存储、不影响 AP/CS。
推理中网页仍可刷新/取消，响应顺序校验拒绝旧快照覆盖较新刷新。共享文件评审待办。

## 较早的第一轮 · BA 需求检查点 · 2026-10-29

新增独立 BA 自然语言入口，要求 Customer 会话、CSRF 及记录归属校验。
原有结构化 `/api/consultations` 与 CS/CO 调用契约保留。

| POST 路径 | 精确 JSON 字段 | 保存行为 |
|---|---|---|
| `/api/consultations/intake` | `message` | 201；推理时 ACTIVE，随后 CLARIFYING 或 INCOMPLETE |
| `/api/consultations/{id}/clarify` | `message`, `contextRevision` | 同 ID、修订加一、旧结果失效、重新提取 |
| `/api/consultations/{id}/confirm-needs` | `contextRevision`, `concern`, `budget`, `fragranceFree` | 客户显式核对/更正并确认，修订加一，随后独立校验推荐 |

单条消息 1–2,000 字符，最多八条、合计 8,000 字符。仅自然语言记录的
ACTIVE/CLARIFYING/INCOMPLETE 状态允许补充。确认必须 CLARIFYING 且 needsReady=true；
字段齐全也不会自动推荐。contextRevision 为正整数，不能是布尔值。过期修订返回
409 STALE_SCOPE，其他客户 404、Founder 403；拒绝额外字段。已完成咨询须新建，
本轮没有取消或已完成记录修订接口。

payload.messages 保留原文；proposedNeeds 含有限字面引用，仍是未确认假设。
网页先显示固定缺失字段问题，再显示可编辑确认表单；确认后先保存 needsConfirmed
和客户核定的 needs。请求/提取预算为澳元，确认保存与目录为澳分。
推理在写事务之外执行，保存前重查修订/状态及当前目录，拒绝旧结果覆盖。
不可用、超时、无效输出保存 INCOMPLETE，不回退为 mock 成功。最终数据库写入失败
会回滚，记录可能停留 ACTIVE，不能虚报 COMPLETED；本轮 BA 尚无自动存储恢复或专用按钮。
实际检查见 VERIFICATION.md，不代表所有 BA 验收完成。

读 Stage 1 第 8.2 节与 `docs/reference/stage1-baseline.txt` 的原状态词汇。
Python 边界用 snake_case，需要明确契约字段的 JSON 用 camelCase。
当前只实现部分类/端口模型，不是一一完成每个参与者；领域对象是持久化记录。

| Stage 1 接收方 | 当前接收方 | 边界 |
|---|---|---|
| BeautyAdvisorService.submit; LlmPort.propose | `BeautyAdvisor.submit`; `MockLlm.propose` | 只读商品/库存，只写咨询 |
| CustomerServiceAgent.submitRequest/confirmResolution | `CustomerService.submit/confirm` | 自己的订单、当前证据、确认、AP |
| AfterSalesPort.executeResolution/lookupOutcome | `MockAfterSales.execute_resolution/lookup_outcome` | 唯一 actionRef，独立提交模拟效果 |
| CoordinationService.handoff/recordResult/reconcile | `Coordination.advice_handoff/state`; CS reconcile | Founder 发起 CS→BA，不是通用调度 |
| FounderApprovalService.receiveRequest/processDecision | `Approval.submit/decide` | 保存收据，提交精确决定/审计 |
| ReviewGateway.routeRecordedDecision | `Approval.deliver` | 独立投递，不执行业务 |
| MarketingContentService.submitCampaign/requestRevision | `Marketing.submit/revise` | mock 脚本/分镜；新版本重新审 |

## 身份与请求

HTTP 仅绑定 127.0.0.1，无 CORS。Host/origin 检查拒绝跨站和非本机 host。
修改需要 JSON，登录后还要 CSRF token。不透明 HttpOnly SameSite=Strict cookie 映射服务端用户；
`Authorization: userId`、请求 role/customerId 不能决定权限。共享演示密码用 PBKDF2 保存，
不是生产凭据。会话响应只返回 actor/CSRF，不返回密码/会话哈希。

错误使用相应 400/401/403/404/409/413/415 与
`{"error":{"code":"...","message":"..."}}`。他人订单/记录只返回通用不可访问/不存在，
客户不能看到全体记录。输入和数据库证据进入浏览器标记前转义。

## 初始同源 JSON 入口

| 方法/路径 | 角色 | 含义 |
|---|---|---|
| GET `/api/health` | 公开 | 仅模拟状态 |
| POST `/api/login` | 公开 | username/password 换会话和 CSRF |
| GET `/api/session` | 已登录 | 当前 actor/CSRF |
| POST `/api/logout` | 登录 + CSRF | 作废本会话 |
| GET `/api/snapshot` | 已登录 | 按角色/归属过滤 |
| POST `/api/consultations` | Customer | message、concern、budget（AUD）、fragranceFree |
| POST `/api/after-sales` | Customer | orderId／需求 → 已存评估；201 可为 ASSESSING、NEEDS_INFORMATION、UNRESOLVED，不代表换货成功 |
| POST `/api/after-sales/{id}/coordinate` | Founder | 主动发起 GR-S-01 建议转交 |
| POST `/api/after-sales/{id}/confirm` | 所属 Customer | 当前 contextRevision；首次送审，后续当前确认才可能执行 |
| POST `/api/after-sales/{id}/revise` | 所属 Customer | 当前版本和更正需求，作废旧范围 |
| POST `/api/after-sales/{id}/reconcile` | 所属 Customer | 查询同一 actionRef 并保存结果，不重复执行 |
| POST `/api/approvals/{id}/decide` | Founder | decision、reason、contextRevision |
| POST `/api/approvals/{id}/deliver` | Founder | 重投同一已提交决定 |
| POST `/api/approvals/{id}/recover` | 原 Founder | 仅 contextRevision；恢复所显示当前范围的已保存决定意图 |
| POST `/api/campaigns` | Founder | brief、授权 productId 得 mock 草稿/审批 |
| POST `/api/campaigns/{id}/revise` | Founder | 当前版本、brief、productId，创建新范围审批 |
| POST `/api/demo/fault` | Founder | 一次下一操作故障样例 |

## 证据、审批、执行关联

送审保留 origin_role/origin_id、精确动作、版本、证据、适用的 action_ref。
PENDING 是请求状态，不是 DecisionKind。DecisionKind 为 APPROVE、REJECT、REQUEST_REVISION。
已提交决定有 decision_id、actor、reason、精确范围；决定/请求/审计同时更新。
投递独立事务/状态且幂等，旧范围不能修改当前来源。批准本身无业务效果。

保存恢复需要原 Founder 的登录会话、CSRF，且请求只含
`{"contextRevision": <正整数>}`。所显示版本仍须匹配审阅、当前来源和 approvalId；
提交前重新校验已存意图的精确动作及 actionRef。拒绝调用方传入决定、理由、身份或动作，
仅复用持久化的种类和理由，恰好一次提交后单独尝试投递，不执行交易或发布。
已提交后重复恢复仅返回同一决定，不重新投递；投递失败须显式调用 `/deliver`。
重复恢复也拒绝旧范围。失败卡片明确已存意图并非权威决定，只有原 Founder 对当前关联来源可见恢复按钮。
决定/恢复失败后先刷新已存状态再展示错误。Founder 演示控件已提供 `approval_recording` 选项。

CS 重查订单归属、当前政策、库存、确认、精确 action/ref/revision、已投递且已提交的批准。
先保存 EXECUTING/意图，模拟外部适配器在另一事务原子条件扣库存并插入唯一 actionRef 效果，
之后 CS 保存结果和 CO 完成。响应超时进入 RECONCILING；结果保存失败进入 RECORDING_FAILED。
恢复只查效果表并保存同一收据，不调用 execute。

这只是外部契约的本地事务模拟，真实供应商的查询/幂等保证未核实。
进程崩溃留下 EXECUTING 时可查询；仍未确定则升级，不重试。

## 已实现状态子集

- BA：自然语言入口 ACTIVE → CLARIFYING（追问或显式确认关卡）→ ACTIVE → COMPLETED/INCOMPLETE；完整生命周期待做。
- CS：ASSESSING → AWAITING_CONFIRMATION → REVIEW_PENDING → 当前批准 →
  AWAITING_CONFIRMATION → EXECUTING → RESOLVED；失败有 RECONCILING、RECORDING_FAILED、
  UNRESOLVED；审阅结果有 REJECTED/NEEDS_INFORMATION。
- AP：PENDING → APPROVED/REJECTED/REVISION_REQUESTED；旧范围 SUPERSEDED。
  收据不是批准；投递失败保留已提交状态。
  决定未保存成功时为 RECORDING_FAILED：没有 decisionId、没有投递、没有业务效果。
  另有独立的持久决定意图（PROPOSED → COMMITTED，或 RECORDING_FAILED）保存预期的 Founder、种类、
  理由和精确范围；它不授权，是仅从存储恢复的唯一输入。每个请求最多一个已提交决定。
- MC：DRAFTING → REVIEW_PENDING → APPROVED/REJECTED/REVISION_REQUIRED；
  修改创建新数据/历史/审批，旧范围被替代。
- CO：PENDING_VALIDATION、HANDOFF_SENT、AWAITING_APPROVAL、EXECUTING、RECONCILING、
  RECORDING_FAILED、CLARIFICATION_REQUIRED、ESCALATED、CANCELLED、COMPLETED。
  当前持久化转交只是窄范围同步流程。

新增状态须记录 event/guard/effect，同步调用方、测试、模型偏差记录。
真实脚本/分镜检查必须检查实际输出，不能信模型自列的声明清单。

## 共享 LLM 边界与负责人

[LLM_INTEGRATION.md](LLM_INTEGRATION.md) 规定现有 v1 Python 调用、字段单位、模块样例、
错误／模式边界与真实验收。共享集成由 Danyang Wang 负责，默认仍 mock；可选独立 BA 传输和
分能力模式／错误映射见 [WINDOWS_LLM.md](WINDOWS_LLM.md)；一条真实 BA 路径已验证，见 [运行证据](WINDOWS_LLM_RUNTIME.md)；
CS 意图提取是后续共同定义的接口，尚未实现。

## CS HTTP 保留评估 · 2026-10-27

HTTP 受理现明确在原事务调用 CustomerService.assess，原服务 submit 不变。
初始订单归属不可访问／不可验证时只返回通用错误，不保存记录或受保护上下文。
归属验证后，政策缺失／冲突／不支持／不可读会保留 NEEDS_INFORMATION／UNRESOLVED、允许的原因／引用，
不产生建议、审批或效果。写入失败不声称已保存；请求传入的政策／身份不能覆盖服务端证据或登录身份。

卡片根据 evidenceOutcome 展示，不假设 policy／advice 存在，证据受阻时隐藏旧建议，并提供原 revision 重评入口。
权威证据更新后用当前需求重评会产生新的 ASSESSING 版本，须重新 Founder 交接、客户确认、精确审批；
表单不能编辑政策。仍缺证据则保留原失败记录，不伪造新提案。coordinate／revise／confirm 错误后刷新已存快照，
包括通过 HTTP 错误返回但已保存的受阻结果。提示准确称为评估保存，不暗示换货成功。
保留真实 CS 交接／revise 防护及效果核对；未新增政策修改接口或真实 CS 模型。
