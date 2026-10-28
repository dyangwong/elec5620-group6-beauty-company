# BA 模块交接

中文阅读副本，依据 2026-10-29 英文主版同步。以[英文主版](../../modules/BA.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

## BA 需求检查点 · 2026-10-29

当前 Danny 授权的 KAN-15 工作增加 modules/ba_intake.py、adapters/needs.py 的有限提取、
共享 adapter 能力、三个 HTTP 路由和独立客户网页。覆盖 BA-T-01 及 BA-T-02/03/04/05/07
部分条件，不代表自动领取/完成 BA-START-01；未修改 starter 记录或队友归属。

按 WINDOWS_LLM.md 准备 Windows 环境，使用新数据库启动：
`scripts/windows.ps1 -Action Start -Mode mock -Port 5690 -Database var/ba-demo-new.sqlite3`。
登录虚构 Customer，进入 Product advice，输入 `A moisturiser for dry skin.`；
收到预算/无香问题后回答 `My budget is AUD 60 and fragrance-free is required.`。
核对咨询 ID 不变而修订增加，核对/更正条件，点击 **Confirm needs & find a match**，
随后才应显示 P-101；mock 明确标记。原结构化表单保留于
**Use explicit structured fields (existing mode)**。

真实模式先按 WINDOWS_LLM.md 检查/复用已有模型；在另一空闲端口、新数据库使用
`-Mode strata -LlmConfig var/llm.strata.json`。不要重下模型或将私有配置加入源码。
只用匹配端口的脚本停止自己启动的应用，仅管理自己启动的模型。本轮实测隔离
5690/5691 数据库，随后停止两个应用和本轮模型实例，原数据库/配置/权重保留。

剩余：已完成记录的完整修改/取消、BA 审批/升级及审批失败、完整模型/目录/库存故障矩阵、
通用语言/医疗理解和可选已核实替代品。结果保存失败可安全停留已存 ACTIVE；尚无 BA
自动存储恢复。本轮中文只做离线 mock 样例，真实模型浏览器实测为英文。
各 BA 用例组仍按实际保持 PARTIAL/NOT_STARTED。以下较早的日期记录属于历史。

按 Danny 要求默认由 Danyang Wang 延续 Stage 2，不代表共享认领。
从 [BA-START-01](../tasks/BA-START-01.md) 和[开工入口](../../../START_HERE.zh-CN.md)开始，先只完成声明范围。

Stage 1：Danyang Wang；BA-M-01 / BA-UC-01 / BA-F-01..03。
代码 `beauty_company/modules/beauty_advisor.py`；供应方契约在
`beauty_company/contracts.py`、`beauty_company/adapters/mock.py`。
新测试 `tests/test_ba.py`，既有 `test_ba_t_*`。原文第 4–6、8.2、13.3.1 节，缺口见追踪表。

已有：明确需求/预算/无香约束；mock 提名商品；独立检查 ID、事实、库存、约束；保存咨询证据。
不改订单、库存、价格、付款或公开内容。CO 只获许可的建议上下文，模型输入无订单身份/凭据。

10 月 29 日切片后剩余：已完成记录的完整修改/取消、BA 审批、完整模型/证据失败矩阵、
通用语言理解和可选已核实替代品；有限追问/恢复及旧结果抑制已有上述覆盖。医疗关键词拦截只是有限样例，不是完整临床范围检测；
模型自列的声明不足以验证任意生成文字。

## 共享 KAN-15 边界更新 · 2026-10-21

本次未认领 BA-START-01。共享集成新增可选独立 BA 传输、模式／错误映射及 Company.consult
保存前证据复核；没有实现首批澄清／恢复／修改／取消生命周期。tests/test_llm.py 覆盖窄范围
传输和 HTTP 切片；一条实际 BA 模型路径现已通过，见 ../WINDOWS_LLM_RUNTIME.md。
完整 BA 生命周期／理解验收和独立 starter 仍未完成。
