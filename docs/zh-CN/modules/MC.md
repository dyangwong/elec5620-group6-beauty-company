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
