# 共享接口约定与实现映射

中文阅读副本，依据 2026-10-26 英文主版同步。以[英文主版](../CONTRACTS.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

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

- BA：CLARIFYING、COMPLETED、INCOMPLETE；完整生命周期待做。
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
