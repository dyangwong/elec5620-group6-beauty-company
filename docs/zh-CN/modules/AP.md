# AP 模块交接

## 登记动作／策略边界 · 2026-10-31

Danny 授权 KAN-9 修复，不重新认领 KAN-13 starter。新增 AP 本地 approval_policy.py
登记既有 BA 重新评估、CS 争议换货、MC 草稿审阅字段，三类均须 Founder review。
未知动作／调用方 risk 字段在回执前拒绝，审计记录服务端类别／版本；
重复回执须保持证据／ref 一致，意图恢复绑定证据。
回执／新意图／未提交决策恢复／投递前复核当前 CS 订单和策略。
新增8项 AP 测试，全量319项通过。不增加免审普通 CS、通用风险评分／expiry／队列／通知、
schema／模型／业务执行。见[契约](../CONTRACTS.md)和[证据索引](../EVIDENCE_INDEX.md)。
保留 Jiaxuan Ren 归属，负责人审阅待完成。

中文阅读副本，依据 2026-10-26 英文主版同步。以[英文主版](../../modules/AP.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求默认由 Jiaxuan Ren 延续，不代表共享认领。
从 [AP-START-01](../tasks/AP-START-01.md) 及窄范围共享例外、[开工入口](../../../START_HERE.zh-CN.md)开始。

Stage 1：Jiaxuan Ren；AP-M-01 / AP-UC-01 / AP-F-01..03。
代码 `beauty_company/modules/approval.py`，以及 `beauty_company/application.py` 决定/投递边界；
新测试 `tests/test_ap.py`，既有 `test_ap_t_*`。AP 是共享控制，不是 AI 业务 Agent。

已有：CS/MC 精确动作/版本证据；持久 PENDING 回执；仅 Founder 以理由 APPROVE/REJECT/REQUEST_REVISION；
决定/请求/审计一次提交，投递另做。重复投递同 decisionId；旧范围不能改当前工作，接收服务独立复核。

## BA conditional review checkpoint · 30 October 2026

Danny授权KAN-15最小共享接入，保留Jiaxuan Ren／M4的AP贡献及KAN-13／starter归属。
新增BA REASSESS_ADVICE来源，沿用现有表／意图／决定／恢复／投递；BA本地接收器核实同意与准确范围／证据，
不调用模型或业务效果。批准返回客户确认和重新验证，拒绝保持未完成，要求修改需更正。
CS／MC映射和AP保存恢复保持，完整281项通过。相关负责人真人评审待办，不能由授权／CI推断Approve。
见CONTRACTS／VERIFICATION／BA指南；未知风险、过期、队列／通知和AP完整验收仍另行处理。

## 保存失败与恢复 · KAN-13 / AP-START-01 · 2026-10-24

**决定意图**是持久、可辨识的决定提议，保存 Founder、精确范围（来源、版本、动作、actionRef）、种类和理由。
它不是已提交决定：不授权、不投递、不调度业务。它在决定提交之前的独立已提交事务中写入，
因此提交失败后仍可从存储恢复。

- **提交失败 → `RECORDING_FAILED`。** 审批记录没有 decisionId、决定、理由和 Founder，因此不是批准；
  没有投递、没有业务效果。预期身份保留在意图中。
- **仅从存储恢复。** `Company.recover_decision` 从数据库读取意图，重新校验 Founder 与当前范围，
  再原子提交决定/请求/审计，之后才投递。同一数据库上重启的进程恰好一次恢复同一预期决定。
- **每个请求只有一个权威决定。** 冲突的种类或理由被拒绝（`DECISION_CONFLICT`），不替换首个意图或提交；
  过期动作/版本或已被替代的请求被拒绝（`STALE_SCOPE` / `REVIEW_CLOSED`），恢复时不会被静默替换。
- **回执、意图、批准三者不同。** `PENDING` 回执、拟议意图和已提交批准是三件事，只有已提交信封有 decisionId。

本切片使用的共享文件例外：`beauty_company/store.py` 增量的 `approval_intents` 表；
`beauty_company/application.py` 的决定/恢复 facade 与意图字段；
`tests/test_workflows.py` 既有的 AP 原子审计失败回归。

剩余：完整风险/权限分类、BA/CO 本地适配、未知风险、过期、通知、取消、队列失败和可选关联重提。
原服务切片将 HTTP/UI 恢复留给 GR-INT-01；下面 10 月 26 日的有限集成补齐该接口／界面缺口。
保存失败仍是本地注入的模拟，不是真实供应商故障。
审批代码永不执行换货、结算或发布。

## HTTP/UI 保存恢复 · KAN-9 / GR-INT-01 · 2026-10-26

Danny 单独授权本次共享集成，不领取 Jiaxuan 的 AP starter。
`POST /api/approvals/{id}/recover` 只接受所显示的 contextRevision，复查当前范围后调用已有的存储恢复 facade。
仍检查原 Founder／登录会话／CSRF，调用方不能传入决定、理由、身份或动作。
facade 的可选 data 参数保留原来的双参数服务调用；没有改 schema 或 approval 模块。

失败卡片现准确说明保存失败，将已存种类／理由标作无权威的意图，仅为原 Founder 与当前关联来源
显示 Recover saved decision。decide／recover 失败会刷新已存状态，立即显示失败卡片。
Founder 模拟菜单增加 approval_recording。恢复后显示实际决定 ID 与投递状态；投递失败仍用独立重投按钮。
恢复不调度换货、结算或发布。

新增 tests/test_ap_http.py 的 12 项 Router／会话／SQLite 检查，覆盖权限、CSRF、篡改输入、
当前／过期／动作范围、再次保存失败、重启、三种已存决定、仅一次提交和独立投递。
实际网页保存失败／恢复通过；独立读库为一次决定审计、零业务效果、库存不变，详见 VERIFICATION.md。
AP-T-05 保留 PARTIAL：队列／通知、过期、完整风险路由及真实存储故障验收仍待完成。
发布、相关负责人审阅和 Jira 进度更新待进行，不代表整个 AP 或 epic 验收完成。
