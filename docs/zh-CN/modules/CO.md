# CO 模块交接

中文阅读副本，依据 2026-10-29 英文主版同步。以[英文主版](../../modules/CO.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

## 维护者审阅收口 · 2026-10-30

Danny已明确授权小修并审阅合并Guiyu Liu的PR #17。本次只新增三项回归测试，不新增CO实现；
保留KAN-15原实现与作者。已合入main1ad1101，恢复中文副本，非ASSESSING测试使用CS真实终态
RESOLVED，不再把所有非ASSESSING状态称为终态。没有生产代码／schema／API变化。
已授权浏览器于10月30日观察KAN-14为Verification／GuiyuLiu，完整starter验收核对前保留归属／状态。
新测试、CI、最终提交审阅和合并收据记录在PR #17；旧Approve不代表修复后版本已通过审阅。


## 当前分阶段真实只读交接 · 2026-10-29

Danny授权KAN-15例外，保留Guiyu Liu／M5归属。既有有界失败helper用于prepare_external／finish_external：
提交一次关联SENT意图，释放DB进行快照BA推理，重新核对来源／归属／版本／政策／当前目录，再原子保存
CO及CS结果。SENT不是完成或接收回执；重放不派发，客户新版本作废旧待回尝试，旧响应不应用。
原同步mock advice_handoff保留，真实CS走CsFlow，不能在旧服务写事务内推理。审计／写失败明确返回；
中断SENT需明确新版本更正，无通用CO保存恢复／队列／重试／取消框架。实际真实网页一次效果、停机失败及
264项证据见VERIFICATION；CO仍PARTIAL，更广生命周期待做，负责人评审待办、不领取任务。

按 Danny 要求默认由 Guiyu Liu 延续，不代表共享认领。
从 [CO-START-01](../tasks/CO-START-01.md) 和[开工入口](../../../START_HERE.zh-CN.md)开始，先做声明范围。

Stage 1：Guiyu Liu；CO-M-01 / CO-UC-01 / CO-F-01..03。
代码 `beauty_company/modules/coordination.py` 和 CS 结果/核对集成；新测试 `tests/test_co.py`，
既有 `test_co_t_*` / `test_gr_t_*`。CO 是控制，不是 AI 业务 Agent。

已有：Founder 明确发起 CS→BA，保存最少上下文和转交结果，等待 CS 实际结果。
AP 决定提交不等于工作完成。未知响应先查同动作，结果保存失败只恢复保存，最后必须已存结果。

当前有界失败切片（2026-10-29，Danny 授权 KAN-15、AI 辅助）：无效上下文、目标不可用／超时／失败、
畸形或独立校验失败结果均保留安全失败尝试。最小范围关联当前已存 CS 来源／修订，同版本重放不再调用。
客户更正需新修订，保留旧失败；有效只读建议不代表工作完成。SQLite 意图／结果／审计失败明确返回保存
错误并随调用方事务回滚。见 CONTRACTS／VERIFICATION：CO 新增 27 项、完整 237 项、实际 mock 网页
失败→重启→更正→待审证据，无需模型。

剩余：通用 BA／CS／MC 适配、外部独立持久调度、完整取消／升级／干预／结果保存恢复及可选有限重试。
执行不确定不盲重试，只读查询不授新权。本调用仍在既有调用方事务内同步执行，非持久队列／分阶段
恢复框架。上方分阶段路径已支持有界真实CS意图／交接。CO-T-02／03仍PARTIAL，相关宽用例仍有未验范围。
完整 UML 参与者／接收方及 Stage2 验收待做；保留 Guiyu Liu 归属／任务认领，相关负责人评审待办。

## KAN-14／CO-START-01 验证增量 · 2026-10-30

M5／Guiyu Liu从main7c86234继续AI辅助任务。原brief中的失败处理已由KAN-15实现，
本增量保留已有代码，只新增三项CO回归：非ASSESSING来源不得派发（CO-T-02）、
已存需求无效不能被有效调用参数覆盖（CO-T-02）、当前库存变UNKNOWN时拒绝旧建议（CO-T-04）。
检查持久化失败／不派发边界，以及没有审批或交易效果。
原作者记录30项CO检查通过，未修改基线281项／来源／JS通过；实际mock HTTP接收、
Founder交接、重复调用保持AWAITING_CONFIRMATION，未误报完成。

追溯仍PARTIAL：test_co_t_02／test_co_t_04覆盖新增条件，CO-T-01／03／08保留原检查。
不改共享schema、生产实现、UI、HTTP、provider、可选重试或认领；不代表完整CO／模型／Stage2验收。
原作者的Jira HTTP403及当时不合并指令是历史记录；Danny后续明确授权修复／复核／合并，
当前Jira状态见上方维护者记录。完整starter验收另核对，不自动Done；发布／CI／最终审阅／合并单独记录。
原作者最终报告Python3.12.14全284项、来源、JS及空白检查通过；维护者本轮实际结果记在PR。
