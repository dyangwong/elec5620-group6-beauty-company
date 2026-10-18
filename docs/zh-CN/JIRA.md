# Jira 工作与 GitHub 关联

中文阅读副本，依据 2026-10-18 英文主版同步。以[英文主版](../JIRA.md)为维护依据。

用户已建立 elec5620_team6 并连接 GitHub for Jira。2026-10-17 由 AI 辅助完成以下真实映射，
此表是设置快照，当前分配/认领/状态仍以 Jira 为准。

[看板](https://uni-team6-elec5620.atlassian.net/jira/software/projects/KAN/boards/2) ·
[Backlog](https://uni-team6-elec5620.atlassian.net/jira/software/projects/KAN/boards/2/backlog)。
共用一个 team-managed software 空间，编号 KAN；未改站点访问、计费或账号权限，保留 KAN-1/2。

| 模块 | Epic | 首批任务 | 计划负责人／设置时分配 |
|---|---|---|---|
| BA | KAN-4 | [KAN-10 / BA-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-10) | Danyang Wang／已分配 |
| CS | KAN-5 | [KAN-11 / CS-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-11) | Siyuan Lei／已分配 |
| MC | KAN-6 | [KAN-12 / MC-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-12) | Zhengdu Wei（显示 ZHENGDU WEI）／已分配 |
| AP | KAN-7 | [KAN-13 / AP-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-13) | Jiaxuan Ren／未匹配账号，未分配 |
| CO | KAN-8 | [KAN-14 / CO-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-14) | Guiyu Liu／未匹配账号，未分配 |
| 共同 | [KAN-9](https://uni-team6-elec5620.atlassian.net/browse/KAN-9) | 集成与验证，后续分别拆任务 | 每项单独分配 |

五份首批均 To Do、Medium、starter 标签、对应 Epic，描述含来源/验收、文件范围、条件、中英文链接、完成边界。
分配是计划责任，不证明本人认领、实现、审阅或贡献；未发猜测邀请。真实/本地模型暂缓。
六个 Epic 不代表六个业务 Agent，仍只有 BA/CS/MC 三个。

## 开工顺序

1. 声明身份，读 START_HERE、模块/任务、报告模型。
2. 查实际 Jira 分配/认领、阻塞、当前仓库。本地 helper 只打印映射；无连接时由人核对共享状态，
   不能假称集成自动授予 Agent Jira 权限。
3. 分支、commit、PR 标题含真实编号，例如 CS：

   ```text
   Branch: KAN-11-cs-start-01
   Commit: KAN-11 Handle policy evidence failures
   PR:     KAN-11 [CS-START-01] Preserve truthful eligibility outcomes
   ```

   任务表会给每人带实际 Jira 编号的建议分支。
4. 实际开工后从 To Do 进入 In Progress；自检、测试、PR 和相关人工审阅放 Verification。
   队友 PR 检查通过后还须至少一位非作者 Approve，等待审阅保持 Verification，不能 Done。
   仅 dyangwong 有自己 PR 例外，见 GIT_WORKFLOW。
5. 本任务条件有证据、PR 合并、模块/追踪表记清子集和待集成，才 Done。
   服务子任务不代表整模块/验收组完成；失败/未合并 PR、回执都不是完成，不按合并自动 Done。

Backlog 已启用。Sprint 时间、目标和承诺需团队实际规划，未启动 Sprint，不造截止日期、提醒、工时。
Bug 可记录缺陷；保留已有 Story/Subtask。阻塞记标识/理由，不虚构成功。

## 单一工作追踪

### 必须同步的进度节点

实际做这项工作的人负责更新；有当前用户授权和 Jira 连接的 Agent 可以代为执行，
否则由本人手动记录。每个节点查实际任务，不能只信本地快照。

| 节点 | Jira 更新 | 仓库／PR 证据 |
|---|---|---|
| 开工前 | 核对身份、分配、已有认领、范围和阻塞；明确认领，实际开工时改 In Progress。 | 从当前 main 建带任务号的分支。仅在本人任务行据实记认领；本地改 JSON 不等于共享预订。 |
| 准备验证 | 限定范围的实现可验证时改 Verification，关联 PR 并说明剩余工作。 | 更新受影响模块说明、验收追踪行和 STATUS 中变化的实现缺口；PR 填实际测试、限制、观察到的 Jira 状态。 |
| 合并及验收后 | 关联已合并 PR 和验收证据，满足本任务全部条件才改 Done；否则留 Verification 或说明原因退回 In Progress。 | 合并内容应含准确实现和证据；合并不等于整模块、验收组或父 Epic 完成。 |
| 阻塞、暂停或重开 | 写明原因、依赖和下一步；阻塞加标识。恢复实现用 In Progress，解释重开原因。 | 保留旧证据，记剩余缺口、后续任务／PR，不删失败记录，不悄悄扩大范围。 |

每次进度更新写真实任务号、日期、执行人、已完成工作、测试／PR 证据、阻塞与下一步。
在这些节点及重大阻塞／范围变化时更新，无需固定定时更新。范围或负责人变化时，在同一轮工作中
对齐 Jira 和版本化任务书／任务表，保留 Stage 1 来源并记录偏离。

### 文件分工及过期状态处理

- Jira：当前分配、认领、工作流、阻塞、规划和证据链接。
- docs/tasks.json：稳定的任务／成员／来源／文件映射；claim_state、claimed_by、pr_url
  只是版本化记录，有真实证据才改相关行。READY 是任务书就绪，不是工作流；
  jira_status_at_setup、设置时分配与日期保留为历史，不随每次状态移动重写。
- docs/jira.json：配置快照，不随任务状态更新，不把 verified_date 当作每份任务的最近核对时间。
- 模块说明、docs/traceability.csv、docs/STATUS.md：某个仓库版本的已实现行为、已测条件、技术缺口。
  在实现 PR 中更新受影响内容，不复制整块实时看板。
- PR 模板与 Jira 进度记录：连接任务、具体改动和证据。记实际观察到的 Jira 状态／日期，区分
  已执行更新与待办指令。后续节点记 Jira 或 PR，不为每次移动状态额外建提交。

无法访问 Jira 时明确写“Jira update pending”，给本人准确任务号、请求转换、进度文字和 PR／证据链接，
不能把请求更新写成已执行。共享集成前须由有权限的人核实实际认领及状态；离线状态或旧快照
不能覆盖 Jira 新记录。若 Jira 为 Done 但证据不足，要指出不一致并协调修正，不能编测试或改 Stage 1 来凑完成。

这是按节点由人／Agent 更新，不是自动双向同步。GitHub CI 检查仓库行为和结构，不验证实时 Jira 状态；
公开仓库不得保存 Jira 凭据。

Jira 管当前状态；docs/tasks.json 管版本化的成员/需求/文件/Jira 编号映射，不是第二块实时看板。
保留他人记录，明确本人认领后才据实改 claim_state/claimed_by；计划分配本身仍保持 UNCLAIMED。
快照过期如实说明，不冒充实时同步。普通任务不另建冲突 GitHub issue。
GitHub for Jira 需要实际编号才能关联开发信息，不实现/验证业务功能。

本次用 KAN-9 仓库维护 PR 验证关联，实际结果记 VERIFICATION；集成 Epic 不会因该 PR 合并就全部完成。

首批五项已从 Backlog 移入 Board，状态仍为 To Do。配置时 Board 共 7 项
（含原 KAN-1/2），Backlog 为 0；后续待规划工作可放 Backlog。
KAN-9 的 Development 已显示维护 [PR #2](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/2)、
仓库、来源分支与 main 目标。维护更新中提及的编号也可能产生开发链接，不能据此认定功能已开工或通过。

## 已保留的共享 LLM 任务 · 2026-10-18

[KAN-15／GR-INT-02](https://uni-team6-elec5620.atlassian.net/browse/KAN-15) 已建于 KAN-9 下，
按明确要求分配 Danyang Wang。分工／接口准备不等于开始实现，实现前保持 To Do；其他成员不重复
做共享供应商／部署，见 [LLM_INTEGRATION.md](LLM_INTEGRATION.md)。不认领默认 BA 首批，也不完成父 Epic。
