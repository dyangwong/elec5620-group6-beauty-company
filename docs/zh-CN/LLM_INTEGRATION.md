# 共享 LLM 分工与模块接口

中文阅读副本，依据 2026-10-21 [英文主版](../LLM_INTEGRATION.md) 同步。

## BA 需求检查点 · 2026-10-29

Danny 授权 KAN-15 有限独立 BA 理解/追问切片，不代表领取 BA-START-01，未连接真实 CS/MC。
新增可选能力 extract_needs(messages: list[str]) -> dict，复用 StrataLlm._complete
及原有 loopback 配置、严格 JSON/响应包校验、超时和禁止跳转传输；没有新客户端、依赖、
地址或密钥。只实现旧 v1 propose/script 的注入对象仍可用于原调用；缺失提取方法时，
自然语言入口保存 INCOMPLETE / LLM_CAPABILITY_UNAVAILABLE，不替换为 MockLlm。
健康响应增加 capabilities.baNeeds=LIVE|MOCK|NOT_CONNECTED；配置不等于模型就绪。
MC 仍为 MOCK、csIntent 为 NOT_CONNECTED，真实 CS 交接限制保留。

提取 v1.1 精确字段：concern（HYDRATION/CLEANSING/null），budget（正澳元、最多两位小数、
上限 10,000 或 null），fragranceFree（布尔/null），sources（精确对应三个字段的原文引用/null）。
每个非空值须有保存在原消息中的短引用（最多 600 字符）；预算还须有预算/货币提示及
一致的字面数字，拒绝其他货币/换算。提取不接收身份、凭据、订单、政策、商品或数据库句柄。
空值触发固定的针对性追问。中英文 mock 是有限语法样例，无法明确解析/有歧义时继续追问
或安全停止。引用和结构检查不能证明任意语义正确或医疗安全，因此必须客户确认；
推荐再独立验证商品 ID、字面事实、价格、条件及当前库存。

推荐只接收客户核定的三个字段及第一条原消息，完整对话另存；本轮没有通用多轮模型记忆、
任意生成文字事实验证、真实 CS 意图识别或 MC/媒体。Windows 实测及失败证据见 VERIFICATION.md；
10 月 28 日源码 ZIP 早于本功能，只是历史证据。

[KAN-15 / GR-INT-02](https://uni-team6-elec5620.atlassian.net/browse/KAN-15) · 负责人：Danyang Wang · 本地模型已部署，一条真实 BA 路径已验证，更广集成仍待完成。

## 负责人和当前范围

2026-10-18，Danyang Wang（Danny／M1）明确由自己负责共享 LLM 集成 GR-INT-02，
与自己的 BA-START-01 分开。其他成员／Agent 做本模块业务逻辑和确定性测试，不重复部署、
选供应商、安装 SDK、另建直连客户端或重做共享模型接口。需要变化时在共享任务提出，建议请
受影响负责人审阅。负责集成不等于可以覆盖队友模块。

10 月 18 日只预留分工／接口；10 月 21 日 Danny 授权游戏本部署与共享集成。默认仍 mock，
现已新增可选独立 BA adapter、分能力模式显示和 Windows 脚本；Terminal 已下载，
初次受限安装失败后，模型已安装并修复迁移目录 ACL，一条实际 BA HTTP 路径已通过；
见 [运行证据](WINDOWS_LLM_RUNTIME.md)和 [安装历史](WINDOWS_LLM.md)。
MC 保持 mock，CS intent 未连接。

## 已有可调用边界（v1，保持兼容）

`Company(path, llm=None)` 默认使用 MockLlm，传入的对象供 BA、MC 共用；两者构造函数
支持注入。这是 Python 调用，不是 HTTP 端点，未来由共享 adapter 转换模型服务协议。

| 调用 | 输入 | 返回形状 |
|---|---|---|
| `llm.propose(context, evidence)` | 已验证 message、concern、整数澳分 budget、fragranceFree；候选商品列表 | dict：productId 为候选 ID 或 null，factRefs 为所给商品事实文字列表，simulated 为 bool |
| `llm.generate_script(brief, evidence)` | brief 字符串和一个授权商品记录 | dict：script 字符串、claims 事实列表、storyboard 的 shot／duration／caption／direction 对象列表、simulated bool |

商品现有 id、name、facts、澳分 price、version、fragrance_free、availability／库存观察。
只给必要且允许的证据，不传数据库句柄、会话、凭据、无关订单。字段／单位保持稳定；空／非法结果
不能当作成功建议或已保存草稿。上述只是现有 fixture 兼容形状，不证明完整运行校验或自然语言理解。

业务模块只消费结构化结果，不写供应商 URL、模型名、SDK、网络调用、供应商 prompt 或响应解析。
共享 adapter 统一负责配置、分角色 prompt、解析、时限和模式。成员可写领域 prompt 需求／样例，
不另建供应商流程；测试保留可注入 fake。

CS 当前接结构化输入，通过 CO 请求 BA，还没有独立 LLM 意图提取接口。身份／订单／政策／库存
判断独立于语言理解。先保留结构化服务边界，在 CS 交接里提供脱敏输入、期望意图／澄清和失败样例；
Danny 后续与 CS 负责人一起定义并版本化缺失接口，再声称真实 CS 理解。不要造空接口冒充接通。
AP／CO 保留确定性的权限和状态控制，模型不能批准、确认、改库存或执行交易／发布。

## 各模块需要交付什么

- BA：保留注入的 propose，独立验证候选／事实，结果应用前核对当前版本及取消状态。
- CS：保留结构化 intake 和权威证据判断，给后续意图接口样例，不直连模型。
- MC：保留注入的 generate_script，媒体边界分开；检查实际脚本／字幕，不只信模型自报 claims。
  分镜不等于视频。
- AP／CO：保留 revision／actionRef 与精确权限；说明无效、不可用、旧结果怎样进入安全状态。
- 模块 PR 展示正常 fake、非法／不支持输出、调用失败，以及适用的旧版本／取消处理。
  基线测试不依赖模型联网，映射本人任务验收子集，列未覆盖条件，不扩大首批任务去完成全部未来能力。

超时、服务不可用、格式错误、无证据内容不能变为真实成功。本指南不新建错误码，也不声称现有失败
路径齐全；按任务书记录现有状态和缺口。接真实 adapter 前，Danny 须与调用方对齐错误映射。
旧结果依据本地保存的当前范围判断，不能信模型提供的身份／版本。

## Danny 后续集成的验收

1. 单一共享 adapter／配置，保留 v1 调用方和默认离线 mock 测试；角色行为走共同边界，不让每人另建服务。
   不兼容变化同 PR 更新调用方、样例和文档，不暗改签名。
2. 明确 mock／live 切换和各能力真实模式。UI／facade 已按 BA／MC／CS intent／媒体／交易分项标配置模式；应用 health 不证明模型就绪。
   真实文本不等于真实媒体／交易，不能静默回退 mock 却显示 live。
3. 先做一条 BA 正常路径及独立证据检查、非法输出、不可用／超时和安全失败，再分批接 MC、约定的 CS
   意图接口。BA 演示不等于整个 GR-INT-02 或 Stage 1 验收完成。
4. 交付可复现运行／配置说明、实测机器限制、模型／版本、脱敏请求结果及局限。预算／时限记为明确选择，
   不冒充课程要求。网络调用移出当前数据库写事务、保存前重查版本可能需要限定共享集成修改。
5. 权重放忽略的 var/models/，本机配置放忽略的 var/ 或 .env，只提交安全样例；业务代码不写固定 IP 或
   密钥。两机授权网络设置后续另定，本次不改应用 loopback 绑定。

## 换电脑接续

切换前 push 未完成任务分支，另一台 clone／fetch 同仓库同分支，避免两机同时改同一分支。
明确声明：“我是 Danyang Wang，继续 GR-INT-02 共享 LLM 集成，不是默认 BA 首批任务。
先读 AGENTS、本指南、CONTRACTS、STATUS、BACKLOG 和实际 Jira 任务。”
开工 helper 默认仍选 BA，这份指南是独立共享任务入口，不认领 BA-START-01。

交接在 Jira／PR 和相关版本文档记录分支／提交、实际状态、改动、验证、剩余工作及安装前置。
不依赖聊天记忆／本机 profile；权重、密钥、数据库不通过公开仓库同步。

## 当前本地切片 · 2026-10-21

错误映射、独立 BA 写事务外调用／保存前复核、HTTP CS 转交防护、预算、签名、测试和待填 Jira
内容见 WINDOWS_LLM.md。共享审阅未完成，未修改队友模块或首批认领。v1 兼容不等于 live MC/CS
或 GR-INT-02 全部验收；UI/facade 现已分能力标配置模式，health 不证明模型就绪。
