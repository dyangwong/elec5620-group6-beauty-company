# MC 模块交接

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](../../modules/MC.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

## MC 模板 MP4 检查点 · 2026-10-29

Danny 授权的 KAN-15 增量增加 MC-F-02 模板媒体，保留 Zhengdu Wei 原工作／归属。当前链路：
校验的 mock／真实文字 → 可选 CPU 模板 MP4 → 格式／完整解码／哈希检查 → 保存当前草稿 →
现有 AP 绑定文件／脚本哈希 → 内部预览，默认 MockMedia 不变。未实现第二模型、场景生成、
摄影、音频、发布、MC-F-03 变体、一般质量评估器或完整恢复／取消。镜头方向作为文字显示，不
执行相机运动；视觉抽查仅覆盖当前虚构目录。

MC-T-04/05/06 仍 PARTIAL：实际 Windows 文件／播放／下载及精确审批、工具不可用、超时／
进程／格式失败和文件篡改按记录覆盖。文件缺失安全拒绝访问，生成／最终保存恢复及更广媒体／
语义／质量验收仍待办。过期／失败文件可保留在忽略目录，但不能通过当前记录链接下载。最终
数据库保存失败可能保留无审批的 DRAFTING。审核应查看真实预览和文案，不只看哈希存在。
安装见 WINDOWS_LLM.md，新／历史证据见 VERIFICATION.md。


## MC 有界真实文字检查点 · 2026-10-29

Danny 明确授权共享模型增量，保留 Zhengdu Wei 的 KAN-12 原代码和归属。未增加视频或 AP
业务规则；共享文件影响见 SHARED_FILES.md，相关评审待办。

Founder brief + 授权商品 → 真实共享模型有界方案 → 独立核验的目录原文脚本／三镜头分镜 →
mock 媒体占位 → 保存当前修订 → 现有 AP。模型选择事实及顺序、重点字幕和 CALM/ENERGETIC/
INFORMATIVE 风格，不生成自由营销文案；创意贴合度仍由 Founder 判断。默认 mock 和 BA-only
Strata 不变，真实 MC 需显式开启。

实际 Windows 网页 calm → REQUEST_REVISION → energetic 新脚本 → 新 APPROVE 通过，旧审批
SUPERSEDED。模型停机后的新请求保存 GENERATION_FAILED/LLM_UNAVAILABLE，无输出、审批或
回退。完整 181 项（MC 28 项）通过，覆盖超时／无效结果、实际字段篡改、独立证据、当前目录、
并发修改和最终保存回滚。具体记录、环境和复现见 VERIFICATION.md。

本轮到此停止。**分镜不是视频。**媒体输出／质量、完整失败恢复／取消、更广 brief 解释和所有
Stage 1 MC 验收仍有缺口。生成最终保存失败可能保留无输出／审批的 DRAFTING，没有 MC 恢复
网页；已有 AP 决策恢复是另一能力。英语实例不证明多语言、创作、医疗安全或完整 MC 完成。

下方早期 mock-only 交接和进展是历史记录。



按 Danny 要求默认由 Zhengdu Wei 延续，不代表共享认领。
从 [MC-START-01](../tasks/MC-START-01.md) 和[开工入口](../../../START_HERE.zh-CN.md)开始，先做声明范围。

Stage 1：Zhengdu Wei；MC-M-01 / MC-UC-01 / MC-F-01..03。
代码 `beauty_company/modules/marketing.py`、`beauty_company/adapters/mock.py`；
新测试 `tests/test_mc.py`，既有 `test_mc_t_*`。

已有：Founder brief/授权商品；确定性且只含事实的 mock 脚本/分镜；有标识的占位媒体；
先保存精确版本再收审批请求回执，决定提交/投递后才有本地已审状态。修改重新审批、保留历史，不发布。

剩余：真实 brief 理解、完整声明检查、视频/标明替代媒体、失败/质量生命周期、保存失败恢复、
取消/旧回调、可选变体。三张分镜卡不是生成视频；此处批准仅限当前 mock 草稿，不授权外部发布。


## Danny 授权修复与集成 · 2026-10-27

保留 Zhengdu Wei 原 KAN-12 实现；按 Danny 明确要求，由 AI 协助将原 PR #11 同步到 main dc1b60b（含 AP #12）并修复，不重新分配 starter，不声称队友已认可。

失败修订现可在 Content studio 显示失败原因，不伪造商品、媒体或审批，并用 productId 保留更正表单选择。审批队列也处理当前失败数据，明确旧 SUPERSEDED 审阅不能批准不同的当前版本。HTTP 创建仍调用 submit，submit_draft 仍是服务入口；未新增真实模型或视频。

传给模型的证据、传给媒体适配器的输入均独立深拷贝；实际媒体帧与另一份已验证分镜快照比较，避免共享可变引用绕过验证。shot／duration 元数据和 mock 标签限定为已声明样例。适配器修改输入不能将无依据字幕带入审批，也不能替换已保存脚本／声明。这仍是确定性 mock 验证，不代表任意自然语言事实校验。

集成后的 112 项测试全部通过，含原 11 项 MC 检查和 5 项新增的适配器／证据变更、元数据、实际 HTTP 失败修订回归。实际浏览器创建后以纯空格修订，保存 INCOMPLETE／revision 2；Content studio 和旧 SUPERSEDED 审批均正常显示，保留历史。远程 CI、实际审阅／合并在 PR #11 单独记录。
