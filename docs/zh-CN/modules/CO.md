# CO 模块交接

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](../../modules/CO.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求默认由 Guiyu Liu 延续，不代表共享认领。
从 [CO-START-01](../tasks/CO-START-01.md) 和[开工入口](../../../START_HERE.zh-CN.md)开始，先做声明范围。

Stage 1：Guiyu Liu；CO-M-01 / CO-UC-01 / CO-F-01..03。
代码 `beauty_company/modules/coordination.py` 和 CS 结果/核对集成；新测试 `tests/test_co.py`，
既有 `test_co_t_*` / `test_gr_t_*`。CO 是控制，不是 AI 业务 Agent。

已有：Founder 明确发起 CS→BA，保存最少上下文和转交结果，等待 CS 实际结果。
AP 决定提交不等于工作完成。未知响应先查同动作，结果保存失败只恢复保存，最后必须已存结果。

剩余：通用 BA/CS/MC 适配、目标不可用、更完整上下文/版本关联、全部失败/取消/升级、可选有限重试。
执行不确定后不盲重试，只读查询不授新权限。模型类型/记录只部分落地，未完成全 UML 参与者/接收方审查。
