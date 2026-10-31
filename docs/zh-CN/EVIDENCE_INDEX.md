# 证据索引与有限安全修复 — 2026-10-31

[English primary](../EVIDENCE_INDEX.md)。本页为中文阅读副本。

Danny／M1 授权从 main `d30dc019ec6830e727a66db28c0a06effc7d0663`
在 `KAN-9-mc-ap-core-boundaries` 分支做 AI 辅助集成修复。
MC 对应 MC-F-01／MC-T-02／KAN-12；AP 对应 AP-F-01／AP-T-01／KAN-9，
不重开或重新分配 Jiaxuan 已完成的 KAN-13 存储 starter。保留原成员工作和归属。

## 已有证据与可信范围

| 证据 | 来源／版本 | 实际状态 |
|---|---|---|
| 真实 BA 澄清、确认、依据产品事实建议、纠正／取消／恢复 | [PR #22 正文](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/22) | Windows AI 辅助实际执行回执；原始运行 ID／截图仍在游戏本，本机未重跑模型。 |
| 真实 CS→CO→BA、精确审批、最终确认 | 同上：最终确认前0次 effect，之后1次，库存12→11，重复3次仍1次 | 有详细回执，原始 request／actionRef／approval／decision ID 待取回；真实推理、模拟交易。 |
| 真实 MC 有限文本→15秒 FFmpeg 视频，关模型重启恢复 | 同上：视频 SHA256 `84631247c43b6bb7c680687d529abc1b044cec297d622f992512f6b3db6bd220`，hash／mtime 不变，1个 review | 实际播放／下载／恢复回执；draft／revision／approval ID、截图仍在游戏本。视频为静音模板。 |
| 正式源码部署演练 | [最终发布回执](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/22#issuecomment-6538163217)：精确 main 全新 clone／ZIP／解压／venv，Windows307项／122.615秒 | 先前 Mac 独立 ZIP 核对133路径、CRC／来源hash通过，8个二进制精确一致、125个文本仅 CRLF 差异；最终打包没有重新推理。 |
| CI | [PR检查](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/41162186627)、[main检查](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/41162349024) | 本轮重读确认旧版本 success，不是本轮新分支 CI。 |
| 实际 PR review | [PR #17 非作者 Approve](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/17#pullrequestreview-5711332295)，c41a76e | 真实 GitHub 工作流记录，明确使用 AI 辅助，不冒充独立人工认可或团队会议。早先 dismissed review 仍保留。 |
| 敏捷开发历史 | 本地 `output/agile-history-20261030/` 的 GitHub／Jira 真实时间、CSV／JSON、图表和原生累计流图截图 | 事后审计，不是补造历史 Sprint／会议，统计是历史快照；尚无确认的真实回顾。 |
| 贡献确认 | 私人 `output/elec5620-rc1-7c86234-20261030/CONTRIBUTION_TEMPLATE.md` | Danny 已明确尚未确认。任务归属／作者／commit 数不能自动决定贡献比例。 |

旧正式包 `ELEC5620_Group6_Source_d30dc019.zip`：6,050,713 bytes，
SHA256 `3d783103a3f93419f60b5efdfb79f4198cedf467de63f7cc26728cd756906392`。
原包保持不变，**不含本次修复**。上述 Windows 验收对应 d30dc019 和内容相同的候选源码，
不能自动算作新源码的真实模型验证。

本轮本地 `output/core-boundaries-20261031/` 收拢公开回执／真实 review／CI 元数据、
已有文件的 hash 索引、最终测试日志和最小待补证据表。忽略的 output／私人记录不进入公开源码。

## 修复与本机验证

- MC 在调用文本或媒体生成器前，校验有限的已知香精词汇之间及其与布尔元数据的矛盾。
  保留 INCOMPLETE／SOURCE_CONFLICT，不产生当前脚本／视频／review。修正来源后显式创建新修订、
  新 review，保留旧历史；恢复旧／已暂存结果时同样校验，不重新推理或渲染。
- AP 登记 BA REASSESS_ADVICE、CS SIMULATED_EXCHANGE、MC mock／live 草稿审阅及模板视频 hash。
  未知／畸形动作、来源／动作范围不匹配、调用方 risk 覆盖均不能取得回执；既有审计记录服务端类别和策略版本。
  所有登记类别都要求 Founder review，不推定金额阈值，不增加自动执行业务路径。
- CS 在取得回执、新建决策意图、未提交决策恢复及投递时复核订单归属、当前策略、actionRef 和证据。
  同来源／修订的重复请求必须动作／证据／ref 完全相同；保存意图的证据不能被替换。
  重投递被拦截时保留既有已提交决策，不产生 effect。
- Mac Python3.9.6 全量 **319项／37.185秒通过**，即307+12。受控 fake-live 测试不算新真实模型证据。
  首次 MC 专项测试暴露低层 revise 在 AP 后才保存新修订，现改为同一调用方事务内先保存当前修订再申请 review。
  41组验收仍为37 PARTIAL／4 NOT_STARTED。

范围仍有限：不是通用语义矛盾检测、完整高低风险分流、免审普通 CS、expiry／队列／通知、
可选 F03 或完整 Stage2 验收。

## 最小待补事项，按顺序

1. 优先取回游戏本已有证据，不重复跑模型：BA record／revision；CS request／coordination／
   actionRef／review／decision；MC draft／revision／review／视频hash 和恢复前后。注明源码、模式、截图路径，
   凭据／数据库保持私有。
2. 现在真实进行简短 review／retrospective，记录日期、实际参与者、看了什么、发现、一条改进和下步负责人。
   如实记录缺席或未达成一致，不能把 AI 聊天变成团队出席记录。
3. 按正式要求完成私人贡献表，关联实际工作与 AI 协助，由人确认，不推算比例。
4. 后续获得发布授权并通过必需 CI 后，在 Windows 复核两处新拦截及 BA／CS／MC 正常模型主线，
   再生成新版本 ZIP，保留旧包／回执。
5. Danny 自行上传 Canvas、下载同一提交包、核对hash，再彩排从源码部署及真实模型端点。
   目前不声称已提交或已现场验收。

Jira／远程交接：本轮本地任务没有写 Jira／改状态／push／创建 PR／合并。
最后观察到的10月31日快照为 KAN-12／15／18／19 Verification、KAN-21 In Progress，
不是本轮实时认领。KAN-9 待发的最小记录：
“本地 MC 来源矛盾／AP 登记动作与策略修复，319项通过；Windows 原始证据仍在游戏本，
真实回顾／贡献确认待补。发布后需新 Windows／ZIP 验收，不关闭 epic。”
共享边界应交 MC／AP 负责人审阅，尚未发生此审阅。
