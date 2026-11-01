# 最终交付交接 · 2026-11-01

## 当前收尾检查点 — 2026 年 11 月 1 日

Danny 现授权有界 PR／Jira 收尾及计时技术演练。冻结新功能；只在已有演示路径实际出错时处理最小修复。
五项 F-03 仍未实现／OFF，本次交付暂缓；此范围决定不等于课程豁免或 Stage 1 全部完成。

**本轮 Windows 新证据：**已提交应用 `12054e43697024eb7e5c0047f30711d43115d9f0`
经新 ZIP→全新解压目录→独立 venv／私有配置／虚构数据库运行。
**319 项测试通过（104.228 秒）**，来源及 JavaScript 检查通过。
真实 BA 澄清／建议／生命周期、真实 CS→CO→BA 与客户／Founder 精确门禁及一次模拟效果、
真实 MC 文本和可播放下载的 15 秒模板 MP4 均通过。
最终保存失败后，以同 DB／配置、模型关闭状态重启恢复通过；MC 文本／媒体哈希、大小及修改时间一致，
重复恢复无重复评审／效果。实际关闭模型后 BA／CS／MC 明确失败，无 mock 假成功。
本次未重新实测 BA 条件审批的真实推理路径；既有回归证据单独保留。

源码包：`ELEC5620_Group6_Source_12054e4_Windows_20261101.zip`，6,068,746 字节／136 跟踪文件。
SHA256：`5fe6dea4f0a2e91f3d61fe20d45a1b43e3aa834164ab4000ee7327c471400794`。
环境：Windows11 Pro25H2/build26200.9711、Python3.14.5、
Strata v0.2.1／Terminal0.1.46.1、`qwen3.8-flash-next-gyro-gyro-s`、FFmpeg9.0.2。
复用原模型／工具；私有验收回执、原日志、记录 ID 和截图保存在游戏本仓库外。

**Agile：**Danny 确认 10 月 17、23、30 日微信讨论均为五名成员参与；
[PR #24](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/24)
记录有来源的回忆追记。后两次具体决定／行动仍未确认，不是当时形成的原始纪要或其他成员独立背书。
Danny 已确认原贡献表完成，不重新制作。

计时技术演练及逐项任务验收另行进行，不等于五人发言彩排、Canvas 下载、现场验收或全部 41 组用例通过。
文档合并不改变已验收 ZIP；若生成新提交包，另记版本和哈希。以下较早检查点保留为历史。

中文阅读副本；以[英文主版](../FINAL_HANDOFF.md)为维护依据。
用于 Danyang Wang（Danny／M1）在 KAN-9／KAN-21 下继续 AI 辅助集成和交付。
本文件是当前续接入口；STATUS、VERIFICATION、readiness 的旧条目属于历史证据。
官方课程要求及来源清单标识的正式 Stage 1 报告仍有优先权。

## 版本与证据边界

| 项目 | 已核对检查点 | 待完成条件 |
|---|---|---|
| 已发布应用 | main `12054e43697024eb7e5c0047f30711d43115d9f0`，已合并 [PR #23](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/23) | 选最终候选前重新检查远端 main 与后续改动，记录完整 SHA。 |
| 最新修复 | MC 在生成／评审前拦截有界产品事实冲突；AP 校验登记动作、来源、范围、策略及 CS 恢复 | 319 项 Mac 测试及 Python3.9／3.13 必需 CI 通过；不代表最新版已完成 Windows／真实模型验收。 |
| Windows 旧证据 | [PR #22](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/22) 与[最终包回执](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/22#issuecomment-6538163217)：真实 BA、CS→CO→BA、MC 文案／模板 MP4、失败／重启恢复，全新最终包解压307项测试 | 对应 d30dc019／源码内容相同的候选，不自动覆盖 #23。原始 ID、截图及回执仍在游戏本；最终包那轮未重新推理。 |
| 旧冻结源码 | `ELEC5620_Group6_Source_d30dc019.zip`，6,050,713 字节，SHA256 `3d783103a3f93419f60b5efdfb79f4198cedf467de63f7cc26728cd756906392` | 保留；不含 #23，需另建最终 ZIP。 |
| 会议草稿 | [PR #24](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/24)，head `121773ec92ab9afdad5dd087ce4ff24c6c04fc4e`，检查时未合并 | 三份双语未确认草稿；真实日期、参与人、反馈、决定须由人确认，不能算已发生会议。 |
| Mac 其他工作 | 分支 `KAN-21-assessor-readme`／提交 `16eb05d`，仅 README 及中文副本 | 未发布／不在 main；私有转移包保留 Git bundle，单独审阅，不自动合入或采信其全部表述。 |

319 是该应用基线的回归测试数，不是319条官方验收或完成率。旧281／286／306／307项、
124／133文件数均对应历史版本；最终候选实际统计。本交接仅改文档，发布／合并和 Windows
结果须分别记录，本轮未进行新应用／模型／Canvas 验收。

## 必须保留的课程要求

- Stage 2 共20分：Stage 1 实现完整性7、AI agent 能力4、Agile4、先进技术有效应用5。
  阅读[完整评分摘录](../reference/stage2-rubric.txt)及私有课程包里的原 PDF／贡献表。
- 评分文件写源码截止 **2026-11-01 23:59**；Canvas 实际截止／时区／提交设置须核对，
  本文件不代表已提交或获得延期。
- Danny 提供的老师公告：Week13 必须从 Canvas 下载源码并现场部署；可用自己电脑，
  可提前准备环境／工具／依赖，可用个人网络。必须演练完整过程和应用／模型／工具连通。
- Danny 提供的老师答疑：mock 或 fake-data 演示影响分数。展示真实模型推理，同时明确
  商品／订单数据为合成 fixture，交易执行为模拟；离线 mock 通过仅作诊断。
- 老师将看 Jira backlog、burndown、Agile 会议记录。保留实际 PR／评审／迭代证据，
  提交历史不能证明会议、反馈或已同意的贡献比例。
- 阅读私有包中的 Lab notes，尤其 Lab2 的功能要求。五个 F-03 虽在 Stage1 标 optional，
  当前未实现／OFF；该标签不能证明对完整性评分或 Lab 要求免除。
- 使用正式私有贡献表：四项评分标准每行五名成员比例合计100%。当前人工确认未核实，
  不从提交量／AI 输出推定比例。先检查现有表，不默认它空白或覆盖它；姓名／学号留在私有提交。

以上公告摘要来自 Danny 在对话中提供的文字，非本轮访问 Canvas；私有包保留来源说明及原件缺口。

## 开始前阅读

1. AGENTS、本文件、GIT_WORKFLOW、JIRA。身份已明确为 Danny／M1 的交付维护，不重新领取队友 starter。
2. REQUIREMENTS、CONTRACTS、source-manifest 和相关 modules。图表读完整63页脱敏 Stage1 PDF
   或私有正式报告；摘录不能替代模型图。
3. WINDOWS_LLM、WINDOWS_LLM_RUNTIME、EVIDENCE_INDEX，以及 STATUS／VERIFICATION 当前条目。
   历史待办／发布状态／测试数不能当作新任务。
4. 私有转移包 README、课程原件、老师补充说明和历史覆盖／Agile 核对。
   忽略 output／私有文件不会随 GitHub 同步。旧 Mac 绝对链接是来源记录，不是 Windows 路径。

三个 AI 业务角色恰为 BA、CS、MC，AP／CO 是确定性控制。共享 LLM adapter 可调用一个本地模型，
不需安装三个模型。交易为模拟；MC 是真实模型文案＋静音 FFmpeg 模板广告，不是生成式画面／音频。
CS 仅有界争议换货，CO 仅有界 CS→BA 协调，不是通用调度器。五个 optional 和广泛验收／NFR 仍未完成。
41组状态为37 PARTIAL／4 NOT_STARTED，不能因测试／PR 通过把全部验收或 epic 标 Done。
历史15功能核对早于 #23，其中 MC/AP 诊断缺口已由 #23 修复。

## 游戏本续接顺序

1. **盘点并保留。** 检查旧仓库分支／未提交内容、应用／模型进程、工具、配置和原始验收记录。
   不 reset、clean、盲目 stash，不重放已 squash 合并的分支。先读资料包，再问缺失信息。
   旧模型所属工作区留在原位。
2. **选择单一已提交候选。** fetch 并检查 main／PR，记录完整 SHA。本交接未合并时从
   `KAN-21-final-handoff` 远端分支或私有包读取。在不存在的新同级目录 clone 主线；不自动
   混入 #24 或 README 分支。后续文档合并也应进入最终版本 SHA。
3. **新 ZIP／新解压目录。** 干净 checkout 运行
   `python scripts/package_source.py --output output/<new-name>.zip`。
   包路径对照 `git ls-files`，逐文件比对 checkout／ZIP／解压内容，记录 SHA、文件数、大小和包哈希。
   排除运行数据、模型、私有包。新 venv／配置名／模拟 DB／空闲端口；确认导入来自本次解压，
   不被旧工作区或 PYTHONPATH 指向其他代码。
4. **复用现有模型工具。** 实查路径；历史模型所有者为
   `D:\elec5620_project\elec5620-group6-beauty-company`。Strata、模型／profile、FFmpeg／ffprobe／字体
   已准备。需要 StartModel 时从原 owner 启动，不从新解压目录安装。不要 InstallModel、下载、升级、
   移动模型或覆盖 profile。历史 endpoint 为 `http://127.0.0.1:8080/v1`、timeout120s、max_tokens512，
   实查配置和 `/v1/models`，不擅换模型／猜版本。
5. **在解压目录验证。** scripts/windows.ps1 Setup 后 Verify，明确记录来源检查及
   `node --check beauty_company/web/app.js`。基线预期319项，有差异就查原因；跳过 JS 不能写通过。
6. **真实模型综合验收。** 新建私有配置引用原模型／媒体工具，按 Windows 指引核对 Start 参数：
   Mode strata、LiveMc、LlmConfig、VideoConfig，新 DB 和 loopback 端口。客户／Founder 用独立浏览器
   profile，跨端口也可能共享 cookie。逐项完成下表，不以健康检查替代推理。
7. **打包与提交收口。** 若修阻碍问题，走分支／PR／CI 后重新生成并验收新包，不能修改解压目录
   却把成功归给旧 ZIP。Danny 提交最终源码和所需贡献材料，再从 Canvas 下载原包、核对哈希、
   彩排全新部署；Canvas 写入另需明确指令。
8. **证据与清理。** 忽略 output 中保存简短英文回执及中文副本：日期、源码／包哈希、环境、模式、
   ID、截图、PASS／FAIL／NOT RUN、遗留项。旧截图先找原记录，不仅为重拍而重跑。
   只停止本轮拥有的进程；预先存在的共享模型保留。不改 LAN／防火墙／公开部署。

| 验收 | 观察并保存 |
|---|---|
| BA live | 自然输入→缺字段澄清→客户明确确认→有依据的有库存建议；更正／取消／条件审批真实。记录 record／revision 和推理证据。 |
| CS→CO→BA live | ORD-1001→Founder handoff→BA 建议→客户确认方案→精确 Founder AP→客户最终确认。保存 request／handoff／actionRef／review／decision；最终确认前0次效果、后1次，库存12→11，重放仍1次。 |
| MC live／媒体 | 有依据 brief→真实文案→可播放／下载15秒 MP4→绑定当前 revision 和文件哈希的评审；改版重新审阅。保存 draft／revision／review 和视频 SHA256。 |
| #23 保护 | 有界香精事实冲突保留 SOURCE_CONFLICT／INCOMPLETE，无模型／媒体／评审；修正新 revision 可继续。未知／畸形 AP 动作或调用者风险覆盖不能获得 receipt／业务效果。非法输入用既有回归／服务测试，不虚构网页入口。 |
| 失败／恢复 | 最终保存失败→同 DB／配置重启→原 revision／artifact 恢复，无第二次推理／渲染或重复评审／效果。模型／endpoint 不可用明确失败，无 mock fallback。 |
| 部署 | 新解压、正确导入、最新测试／来源／JS、模型／FFmpeg 连通，再做实际 Canvas 下载／哈希／源码部署。 |

客户示例：“Please exchange my item for a fragrance-free moisturiser for dry skin.
My budget is AUD 60.” MC 示例：“Create an energetic teaser highlighting the catalogue fact ‘50 ml’.”
这是有界例子，不是任意语义保证。身份和精确审批保持服务端校验，不绕过以获得流畅演示。

## 最小 Agile／协作收口

- 找真实评审／迭代证据，举行或确认真实简短 review／retrospective；草稿在事实确认前仍是草稿。
- KAN board2 是正式记录；只写版本／PR、实际结果、安全证据链接和下一缺口。无长篇重复评论，
  不批量改状态／owner／sprint；无权限或授权就记 pending。
- Sprint 展示开始改到17Oct（最早正式任务），但实际启动／入 Sprint 是30Oct。改日期未补出旧
  remaining-work 历史。HRP board3 是隔离重建实验：新 Sprint 启动成功，历史原生 burndown 未验证；
  不能作原始敏捷证据，也不作为提交前提，不造历史来美化曲线。
- 走正常分支／PR／当前必需检查；队友 PR 要非作者 Approve。Danny 本人 PR 的 review-layer
  例外不是 self-Approve 或跳过 CI；未来发布／合并按当次指令。贡献比例不猜。

## 可复制给游戏本 agent 的指令

使用[英文主版末尾的完整 prompt](../FINAL_HANDOFF.md#copyable-windows-agent-instruction)。
它声明 Danny／M1 身份，要求先读本交接和私有课程资料，盘点现有环境、版本和证据，再按
已提交候选→新 ZIP→新解压顺序验收；冻结功能，保留模型环境，不自动合并／发布／提交 Canvas。
