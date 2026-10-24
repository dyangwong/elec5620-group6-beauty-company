# AP 模块交接

中文阅读副本，依据 2026-10-24 英文主版同步。以[英文主版](../../modules/AP.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求默认由 Jiaxuan Ren 延续，不代表共享认领。
从 [AP-START-01](../tasks/AP-START-01.md) 及窄范围共享例外、[开工入口](../../../START_HERE.zh-CN.md)开始。

Stage 1：Jiaxuan Ren；AP-M-01 / AP-UC-01 / AP-F-01..03。
代码 `beauty_company/modules/approval.py`，以及 `beauty_company/application.py` 决定/投递边界；
新测试 `tests/test_ap.py`，既有 `test_ap_t_*`。AP 是共享控制，不是 AI 业务 Agent。

已有：CS/MC 精确动作/版本证据；持久 PENDING 回执；仅 Founder 以理由 APPROVE/REJECT/REQUEST_REVISION；
决定/请求/审计一次提交，投递另做。重复投递同 decisionId；旧范围不能改当前工作，接收服务独立复核。

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
HTTP/UI 恢复控制与保存失败演示开关属 GR-INT-01 共享集成，不在本切片内。已观察到的待办：后端已接受
`approval_recording` 故障值，但演示下拉尚未提供该选项；审阅卡片对 `RECORDING_FAILED` 请求没有恢复按钮；
其非 PENDING 的兜底文案（"This review was superseded by a changed context."）对保存失败并不准确，
不过卡片仍如实显示 "No applicable committed decision" 并渲染失败徽标。保存失败是本地注入的模拟，不是真实供应商故障。
审批代码永不执行换货、结算或发布。
