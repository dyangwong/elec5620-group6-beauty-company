# CS 模块交接

中文阅读副本，依据 2026-10-18 [英文主版](../../modules/CS.md)同步。
以英文及原始来源为准；编号、状态、路径和命令保持原值。

Stage 1 负责人：Siyuan Lei（M2），CS-M-01 / CS-UC-01 / CS-F-01..03。
任务：[CS-START-01](../tasks/CS-START-01.md) / KAN-11。
2026-10-18 使用 Codex 辅助准备实现；审核、合并及 Jira 验收仍分别处理。
观察到 Jira 经办人为 Siyuan Lei、To Do；本次实现没有更改 Jira 状态或应用共享认领。

代码：`beauty_company/modules/customer_service.py`、模块内部
`beauty_company/modules/cs_evidence.py`、`beauty_company/adapters/after_sales.py`。
新增测试在 `tests/test_cs.py`；`tests/test_workflows.py` 原有全部回归测试保持不变。

## 本次服务层实现

保留原成功流程：本人订单、明确虚构政策、Founder 经 CO 发起 BA 建议、Customer
确认当前版本、AP 审批、客户再次确认后只执行一次。审批不能创造资格或库存。
效果独立提交后再保存收据；不确定结果继续查询原 actionRef。所有业务结果仍为模拟，
没有真实付款、退款、发货或发布。

新增 `CustomerService.assess(db, actor, data)` 供服务层保存证据失败结果。
调用方应在返回 NEEDS_INFORMATION/UNRESOLVED 后提交事务。首次身份/订单不符或
验证不可用仍抛通用 DomainError，不创建请求，也不读取政策、调用模型或审批。
验证归属以后：

| 证据 | 请求状态 | 保护措施 |
|---|---|---|
| SUFFICIENT | ASSESSING | 保留精确政策及引用，允许 Founder 发起建议 |
| MISSING | NEEDS_INFORMATION | 保存允许记录的原因与引用，不猜退货期限 |
| CONFLICTING / UNSUPPORTED | UNRESOLVED | 保存原因与引用，不伪造资格或执行 |
| UNAVAILABLE 政策读取 | UNRESOLVED | 保存通用原因，不暴露供应方诊断 |

已目视核对报告物理页 24、37-38、43-45、50 的 CS 类图、活动图、序列图与状态图。
复用原有 NEEDS_INFORMATION/UNRESOLVED，没有增加 RequestState。

`ExchangeEvidence` 仅在 CS 和模拟售后适配器内部注入。默认按客户与订单联合查询，
然后判断政策；种子政策不变。受控样例可缺字段、声明 `missingFields: ["returnWindow"]`，
或用 `conflictingRefs` 提供冲突的授权政策引用。非法 JSON 属冲突证据；明确不符合资格或
订单状态不受支持时停止自动处理。这些样例不是实际退货期限、门槛或替代政策。
通过 reader 的 order/policy/stock 方法注入失败，不从请求 JSON 接收故障设置。
读取的 SQLite 错误、超时或连接失败映射为安全结果；存储写入失败继续抛出，不能声称已保存。

建议交接、修改和确认都复查订单归属与政策。确认区分 AVAILABLE/UNAVAILABLE/UNKNOWN。
必要读取失败、政策变更或库存不可用时保存安全结果，清除客户确认，并作废/解除旧审批关联，
避免迟到投递重新打开旧范围。确认在提交失败结果后再抛 DomainError。
修改需要新的 Founder 交接、actionRef、客户确认与精确审批。不会自动换成另一商品；
受支持的变更需客户重新选择/修改并重新审批，通用替代商品界面仍待完成。
售后适配器在业务效果事务内部再次检查归属、政策、选中范围和库存，保留唯一 actionRef
及条件扣库存；已执行动作重放只返回相同收据，不重复扣库存。

## 共享集成与兼容性

按用户明确要求，共享回归测试全部不变。旧 `submit(db, actor, data)` 和当前 HTTP
受理入口保持政策失败时 DomainError/事务回滚的行为，与 assess 共用验证和成功流程，
但不会保存首次受理的失败结果。这是明确的兼容边界，不代表浏览器已经接入新评估流程。

后续受限 HTTP/UI 集成需要把受理转到 assess，安全显示没有 `payload.policy` 或建议的
失败记录，并提供修正/重新评估。确认报错后应刷新快照，显示已保存的状态。
切换默认入口前需和共享集成负责人一起审阅调用方与测试。本次没有修改 schema、AP/CO
实现、共享模型接口、HTTP 或界面。

## 验证与剩余范围

`python -m unittest discover -s tests -v` 包括原有 38 项回归和新增 22 项 CS 测试：
归属先于披露、充分/缺失/冲突/非法政策、安全的政策/订单/库存读取失败、补充证据后的新版本、
审批后政策变更、迟到投递、三类库存、保存意图后的证据变化、重放冲突及保存失败。
原有成功、并发/重复确认、写后超时、仅存储恢复测试不变。
CS-T-01/02/04/06 仍为部分覆盖，见 docs/traceability.csv，没有声称整组通过。

剩余：默认 HTTP/UI 保存失败受理结果的集成、常规退货退款、完整政策/验证失败矩阵、
通用替代商品、取消、可选授权通知、全部保存/审计/供应方失败、真实供应方幂等性和完整模型一致性。
真实模型集成由 Danyang Wang 负责，见 [LLM_INTEGRATION](../LLM_INTEGRATION.md)。
未来意图样例：“换货”需订单编号与归属验证；政策缺失应澄清；“用另一客户的订单”只能返回通用
纠正/支持提示。意图输出不能赋予身份、审批、库存或执行权限，本次未新增独立模型客户端。

## 共享 HTTP/UI 集成 · GR-INT-01 · 2026-10-27

Danny 明确授权 HTTP 入口切换到 assess，并补安全失败展示／重评。覆盖上文对当前 HTTP 回滚契约的交接；
服务 submit 本身及成员测试均不变。验证归属后，政策缺失保存 NEEDS_INFORMATION，冲突／不支持／不可读保存 UNRESOLVED。
证据受阻卡片显示安全原因／引用，隐藏旧建议和当前确认，指引客户在权威证据刷新后重评已有请求；
保留历史，重新交接／确认／审阅。未改政策编辑、故障接口、服务签名、模型或 schema。

新增 11 项 HTTP／会话／SQLite 检查，覆盖保留结果／重启／归属、初始身份拒绝、政策读取诊断隐藏、伪造政策、
证据更新／仍受阻重评、保存后的确认错误、存储回滚。分支完整 107 项离线检查及来源／JS 检查通过。
实际客户网页受理保存 NEEDS_INFORMATION；在测试控制器更新服务端政策样例后，网页重评产生 revision 2／ASSESSING。
受控调用原 Founder 交接服务后，再次缺政策时实际网页确认 HTTP 409，立即展示已保存受阻状态。
独立读库为一条 CS、零审批／效果、库存 12。全部为 mock 政策／业务样例。
CS-T-01/02/06 保留 PARTIAL；常规退款、完整取消、真实 CS 意图与完整失败矩阵仍待完成。
远程 CI／审阅／合并及 Jira 实时进度另记在集成 PR。
