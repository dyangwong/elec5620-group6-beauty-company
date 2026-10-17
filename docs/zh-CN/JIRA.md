# Jira 工作与 GitHub 关联

中文阅读副本，依据 2026-10-17 英文主版同步。以[英文主版](../JIRA.md)为维护依据。

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
   GitHub 检查通过后允许自己合并，不强制外部 Approve。
5. 本任务条件有证据、PR 合并、模块/追踪表记清子集和待集成，才 Done。
   服务子任务不代表整模块/验收组完成；失败/未合并 PR、回执都不是完成，不按合并自动 Done。

Backlog 已启用。Sprint 时间、目标和承诺需团队实际规划，未启动 Sprint，不造截止日期、提醒、工时。
Bug 可记录缺陷；保留已有 Story/Subtask。阻塞记标识/理由，不虚构成功。

## 单一工作追踪

Jira 管当前状态；docs/tasks.json 管版本化的成员/需求/文件/Jira 编号映射，不是第二块实时看板。
保留他人记录，明确本人认领后才据实改 claim_state/claimed_by；计划分配本身仍保持 UNCLAIMED。
快照过期如实说明，不冒充实时同步。普通任务不另建冲突 GitHub issue。
GitHub for Jira 需要实际编号才能关联开发信息，不实现/验证业务功能。

本次用 KAN-9 仓库维护 PR 验证关联，实际结果记 VERIFICATION；集成 Epic 不会因该 PR 合并就全部完成。
