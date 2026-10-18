# 共享 LLM 分工与模块接口

中文阅读副本，依据 2026-10-18 [英文主版](../LLM_INTEGRATION.md) 同步。

[KAN-15 / GR-INT-02](https://uni-team6-elec5620.atlassian.net/browse/KAN-15) · 负责人：Danyang Wang · 已预留，实现未开始。

## 负责人和当前范围

2026-10-18，Danyang Wang（Danny／M1）明确由自己负责共享 LLM 集成 GR-INT-02，
与自己的 BA-START-01 分开。其他成员／Agent 做本模块业务逻辑和确定性测试，不重复部署、
选供应商、安装 SDK、另建直连客户端或重做共享模型接口。需要变化时在共享任务提出，建议请
受影响负责人审阅。负责集成不等于可以覆盖队友模块。

本次只明确分工、兼容边界和游戏本交接，不选模型／服务，不安装或连接，运行仍全部 mock。
游戏本实际系统、显存、运行时和模型选择在后续实施时核实。

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
2. 明确 mock／live 切换和各能力真实模式。现有 UI／facade 写死 simulated，声称真实能力前必须更新。
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
