# Git 协作工作流

中文阅读副本，依据 2026-10-18 英文主版同步。以[英文主版](../GIT_WORKFLOW.md)为维护依据。

Danny 要求公开课程仓库，2026-10-18 进一步要求队友 PR 必须非作者批准。采用 GitHub Flow：一个 main、各自短任务分支，无需长期 develop。
实际设置负责强制执行：`.github/main-protection.json` 是基础保护，
`.github/teammate-review-ruleset.json` 叠加批准规则，提交文件本身不自动启用。

## 日常流程

1. 从共同仓库 clone，不自己另建根提交：

   ```sh
   git clone https://github.com/dyangwong/elec5620-group6-beauty-company.git
   cd elec5620-group6-beauty-company
   ```

2. 明确身份，读 START_HERE/AGENTS、本人任务和报告模型，检查实际共享认领。
   GitHub 权限不等于成员身份，不自动认领；按 [Jira 进度节点](JIRA.md) 核对实际 KAN 任务。
3. 保留无关脏文件，从最新 main 建任务分支：

   ```sh
   git switch main
   git pull --ff-only
   git switch -c KAN-11-cs-start-01
   ```

   换成本人的真实 Jira 编号分支，commit 和 PR 标题也含编号，不用队友的分支。
4. 仅做任务范围，检查和看 diff 后提交。明确添加源码文件，不强加忽略的报告/数据/key。
   修改规范时同步中英文。
5. push 任务分支，向 main 开 PR，填真实任务/需求/验收、验证、共享影响和限制。
   填模板的 Jira 进度交接：实际观察状态／日期、已执行或待更新、阻塞、合并后核验负责人；
   可验证时进入 Verification，未发送的更新不能写成已执行。
6. CI 须基于当前 main 通过；需要时 fetch 并将当前 main 合入任务分支，保留队友改动解决冲突，重跑检查。
   合并前处理审阅讨论。
7. 队友 PR 至少一位非作者、有 write 权限的审阅者实际 **Approve**（默认 dyangwong），
   检查通过后获授权者才能 Squash and merge。待审阅保持 Verification；新可审阅提交使旧批准失效，
   修改后重新获批。仅 dyangwong 保留自己 PR 检查通过后的合并例外。
   GitHub 不允许给自己点 Approve，自己检查/合并不能写成他人审阅。编程 Agent 可准备代码/PR，
   外部发布/合并须在当前用户任务授权内，普通本地实现不自动授权这些操作。合并后更新本地 main，删已完成任务分支。依据已合并证据对齐 Jira；
   满足任务全部条件才 Done，否则记剩余工作。父 Epic 自身范围未完成时保持开放。

## main 保护

- 基础保护要求 PR；生效的 Teammate PR approval 规则集叠加**至少 1 位非作者批准**，
  新提交撤销旧批准，须处理讨论。基础 JSON 的 0 不能当成组合后的实际要求。
- 必须 `Python 3.9 checks` / `Python 3.13 checks`，且任务分支更新到当前 main。
  检查包括应用/交接测试、来源校验、JS 语法；通过不代表 Stage 1 全部验收完成。
- 处理完讨论，管理员也遵守规则。
- 禁止强推/删除 main，采用 squash 保持线性历史。
- 不强制 CODEOWNERS 批准。共享契约、数据库结构、权限检查、他人模块变更请相关队友审阅，
  CODEOWNERS 默认请求 dyangwong；任一合格非作者 write 审阅者均可满足一次批准。不得编造证据。

第一份共同初始基线由维护者在保护启用前发布；启用后全部走 PR，普通工作不绕过。
公开只允许任何人阅读/clone，不授写权限。队友须用核实的 GitHub 用户名邀请，不按姓名猜，
不为写模块授管理员权限；邀请实际发出后才能记为已邀请。

## 公开源码范围

公开报告副本移除学号/元数据，保留 63 页、模型、物理页码。未脱敏正式原件留本地且忽略，
见[来源说明](reference/README.md)。真实凭据、会话/数据库、旧原型不发布，README 演示密码为虚构。
公开不自动赋开源许可证，也不允许虚构贡献。

## 维护者验证

发布后读回实际 main 规则、核实真实 CI，用实际出现的检查名。可用设置验证 PR 观察：检查待运行时阻止合并，
通过后还须满足适用审阅要求才合并。实际结果记 VERIFICATION。Jira、真实模型、队友邀请分开处理。

## 主账号例外与审阅职责

[生效审阅规则](https://github.com/dyangwong/elec5620-group6-beauty-company/rules/25333272)
仅给 dyangwong（ID 226655466）PR 场景的审阅层例外，保留自己 PR 合并偏好；Agent 只能用于其本人
PR 并记录，不能叫自我 Approve。GitHub 按操作账号而非 PR 作者给例外，技术上 Danny 也可绕过
队友 PR，但本工作流禁止这种常规使用。队友 write 账号没有例外，没有改账号权限。
基础保护仍强制所有人 PR、当前 main 的 Python 检查、处理讨论、线性 squash、禁强推／删除，
审阅层例外不能跳过基础保护。不能用 admin merge 跳 CI 或合并未获批准的队友 PR。

审阅者检查需求／任务范围、实际 diff、共享影响、验证和未完成条件，有问题 Request changes；
CI 绿不等于审阅。记真实审阅账号，区分人工与明确授权的 Agent 审阅，不虚构本人看过。
作者默认请求 dyangwong、处理意见；审阅／验收及合并完成前 Jira 保持 Verification。
