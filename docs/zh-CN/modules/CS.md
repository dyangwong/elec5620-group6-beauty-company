# CS 模块交接

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](../../modules/CS.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求默认由 Siyuan Lei 延续，不代表共享认领。
从 [CS-START-01](../tasks/CS-START-01.md) 和[开工入口](../../../START_HERE.zh-CN.md)开始，先做声明范围。

Stage 1：Siyuan Lei；CS-M-01 / CS-UC-01 / CS-F-01..03。
代码 `beauty_company/modules/customer_service.py`、`beauty_company/adapters/after_sales.py`；
新测试 `tests/test_cs.py`，既有 `test_cs_t_*` / `test_gr_t_*`。
保留原文 8.2.2 节请求状态。

已有：本人订单换货、明确政策样例、Founder 经 CO 发起 BA 建议、Customer 确认精确版本、AP 审批、
客户再确认后只执行一次。效果先提交，后存本地收据。未知结果查 actionRef，恢复保存不执行。
批准不能创造资格/库存。所有结果均模拟且列剩余实际义务，每演示订单至多一笔活跃/完成换货。

剩余：常规退货/退款、完整政策冲突/澄清、取消、可选授权通知、全部保存/供应方失败、
真实商业契约、完整模型一致性。未明确批准范围与合适控制前，不接真实金融服务。
