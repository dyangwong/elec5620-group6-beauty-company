# BA 模块交接

中文阅读副本，依据 2026-10-21 英文主版同步。以[英文主版](../../modules/BA.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求默认由 Danyang Wang 延续 Stage 2，不代表共享认领。
从 [BA-START-01](../tasks/BA-START-01.md) 和[开工入口](../../../START_HERE.zh-CN.md)开始，先只完成声明范围。

Stage 1：Danyang Wang；BA-M-01 / BA-UC-01 / BA-F-01..03。
代码 `beauty_company/modules/beauty_advisor.py`；供应方契约在
`beauty_company/contracts.py`、`beauty_company/adapters/mock.py`。
新测试 `tests/test_ba.py`，既有 `test_ba_t_*`。原文第 4–6、8.2、13.3.1 节，缺口见追踪表。

已有：明确需求/预算/无香约束；mock 提名商品；独立检查 ID、事实、库存、约束；保存咨询证据。
不改订单、库存、价格、付款或公开内容。CO 只获许可的建议上下文，模型输入无订单身份/凭据。

剩余：真实 LLM 需求提取、澄清/恢复，完整结构/事实验证，异步修改/取消/旧输出抑制，BA 审批、
全部供应方失败、可选已验证替代品。医疗关键词拦截只是有限样例，不是完整临床范围检测；
模型自列的声明不足以验证任意生成文字。

## 共享 KAN-15 边界更新 · 2026-10-21

本次未认领 BA-START-01。共享集成新增可选独立 BA 传输、模式／错误映射及 Company.consult
保存前证据复核；没有实现首批澄清／恢复／修改／取消生命周期。tests/test_llm.py 覆盖窄范围
传输和 HTTP 切片；一条实际 BA 模型路径现已通过，见 ../WINDOWS_LLM_RUNTIME.md。
完整 BA 生命周期／理解验收和独立 starter 仍未完成。
