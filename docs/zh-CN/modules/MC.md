# MC 模块交接

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](../../modules/MC.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

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
