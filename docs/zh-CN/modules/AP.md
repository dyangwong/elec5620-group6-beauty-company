# AP 模块交接

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](../../modules/AP.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求默认由 Jiaxuan Ren 延续，不代表共享认领。
从 [AP-START-01](../tasks/AP-START-01.md) 及窄范围共享例外、[开工入口](../../../START_HERE.zh-CN.md)开始。

Stage 1：Jiaxuan Ren；AP-M-01 / AP-UC-01 / AP-F-01..03。
代码 `beauty_company/modules/approval.py`，以及 `beauty_company/application.py` 决定/投递边界；
新测试 `tests/test_ap.py`，既有 `test_ap_t_*`。AP 是共享控制，不是 AI 业务 Agent。

已有：CS/MC 精确动作/版本证据；持久 PENDING 回执；仅 Founder 以理由 APPROVE/REJECT/REQUEST_REVISION；
决定/请求/审计一次提交，投递另做。重复投递同 decisionId；旧范围不能改当前工作，接收服务独立复核。

剩余：完整风险/权限分类、BA/CO 本地适配、未知风险、过期、通知、取消、RECORDING_FAILED
生命周期、持久同一决定意图的保存重试、可选关联重提。原子回滚只测保存失败部分，不是全部 AP-T-05。
审批代码永不执行换货、结算或发布。
