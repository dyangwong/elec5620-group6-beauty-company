# 队友与编程 Agent 开工入口

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](START_HERE.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

这份交接沿用本地正式 Stage 1 报告的五条成员责任链。Danny 已要求据此准备
Stage 2 默认分工；这不代表其他成员已经认领、完成工作或批准了全部设计。
本仓库中的业务模型回复和媒体仍是 mock。编程 Agent 可以先完成独立的业务逻辑、
状态和测试；真实 LLM、本地模型部署及视频服务选型暂缓，不是首批任务的前置条件。

## 1. 告诉 Agent 你是谁

使用报告中的完整姓名、成员编号或模块代号之一。不要让 Agent 猜姓名，
也不要把网页里的 Founder / Customer 演示账号当作开发成员身份。

| 成员 | 报告姓名 | 默认模块 | 首批任务 |
|---|---|---|---|
| M1 | Danyang Wang | BA · Beauty Advisor | [BA-START-01](docs/zh-CN/tasks/BA-START-01.md) |
| M2 | Siyuan Lei | CS · Customer Service and Order | [CS-START-01](docs/zh-CN/tasks/CS-START-01.md) |
| M3 | Zhengdu Wei | MC · Marketing Content | [MC-START-01](docs/zh-CN/tasks/MC-START-01.md) |
| M4 | Jiaxuan Ren | AP · Approval and Governance | [AP-START-01](docs/zh-CN/tasks/AP-START-01.md) |
| M5 | Guiyu Liu | CO · Coordination and Recovery | [CO-START-01](docs/zh-CN/tasks/CO-START-01.md) |

BA、CS、MC 是三个业务 Agent；AP、CO 是共享控制能力。GitHub 用户名尚未填入，
不会根据登录名、Git 作者、系统用户名或当前登录的网页角色推断成员身份。
机器可读映射在 [team.json](docs/team.json)，任务状态在 [tasks.json](docs/tasks.json)。

## 2. 给自己的 Agent 一条明确指令

例如，CS 成员可以粘贴：

> 我是 Siyuan Lei，按 Stage 1 负责 CS。请从 AGENTS.md 和 START_HERE.md 开始，
> 识别我的默认任务 CS-START-01，读取对应模块说明、任务书和正式报告相关模型。
> 先简短说明识别出的身份、任务范围和当前缺口，然后继续在该范围内完成本地实现、
> 测试和交接记录，不要停在计划阶段。保留队友工作；普通可逆修改不必反复确认。
> 不要安装或接入真实模型，不要创建或修改外部仓库、Jira、发布服务，不要改正式报告。

其他成员替换完整姓名、模块和任务编号即可。未知或冲突身份先澄清；已经明确匹配时，
直接按任务书推进。只读评估、仓库维护和集成交接任务不自动触发某位成员的功能任务。

所有编程工具都可由人明确要求读取这个入口。是否自动读取 AGENTS.md 取决于工具；
本交接不假定任何特定工具已安装、已连接或会在后台自动运行。

## 3. 取得一份当前任务包

从仓库根目录运行以下任一命令；也可以直接让 Agent 读取同样的文件：

```sh
python3 scripts/start_work.py --list
python3 scripts/start_work.py --member "Siyuan Lei"
python3 scripts/start_work.py --member CS --task CS-START-01 --json
```

需要 Python 3.9 或更新版本。Windows 若没有 `python3` 命令，可换成 `python` 或
`py -3`，其余参数相同。此工具无需第三方包、模型服务或联网。

输出包含正式报告指纹、指定阅读顺序、首批任务、独占/共享修改范围、任务分支建议、
验收编号和完成边界。`--save` 可额外保存到被 Git 忽略的 `var/work-session.json`，
只对本机有效；它不修改共享任务表，也不代表已在 Jira 认领、已验证真实身份或已开工。

## 4. 阅读与动手顺序

1. 总入口与当前状态：AGENTS、STATUS、REQUIREMENTS、CONTRACTS、COLLABORATION。
2. 本人的模块说明、首批任务书及其列出的报告物理 PDF 页码。
3. 相关现有实现和测试，先运行已有基线检查，保留失败证据，不掩盖既有问题。
4. 在本人的任务分支实现、验证并更新本模块记录。首批任务以服务逻辑和测试为主，
   共享页面、HTTP 路由和全局接口接入按 [共享文件规则](docs/zh-CN/SHARED_FILES.md) 协调。
5. 提交前核对任务验收条件、影响模块和剩余缺口。任务完成不等于整条需求或全组完成。

完整报告的脱敏阅读副本是 [stage1-report-public.pdf](docs/reference/stage1-report-public.pdf)。
仅移除学号和 PDF 元数据，保留 63 页和模型图；原件留本地且保持权威，来源清单分别记原件/副本哈希。
文字摘录不能替代模型图；任务书中的页码是 PDF 阅读器页码，从 1 开始，
不是报告页脚编号。对设计的变更必须写明来源和影响，不能为了实现方便偷偷改需求。
若工具暂时无法读取模型图，要明确记为未核对，先完成不依赖该图的独立工作，
不要以读过文字摘录代替已核对完整模型的声明。

## 5. GitHub 建立后怎样协作

队友从已发布的共同仓库基线 clone，再建各自任务分支，不独立创建根提交。
Jira 设置/认领仍分开处理并如实记录。流程见 [Git 工作流](docs/zh-CN/GIT_WORKFLOW.md)。

检查实际 Jira 认领与仓库分支状态后，按自己的任务实施。没有 Jira 工具时，成员可以
手动认领；暂未建立 Jira 时可先在独立分支做本地工作，但必须如实标为尚无共享认领记录。
不能因为本机脚本显示 READY 就声称已经同步 Jira，或覆盖别人已经认领的任务。

PR 使用仓库模板，填写真实任务号、需求/验收编号、实际测试结果、模型与界面影响。
强制检查通过后，作者可自行检查并合并自己的 PR，不强制他人批准。共享接口/结构/权限改动请相关队友审阅；
不能只因“自己的 Agent 说完成”就直接替代主分支。
真实 LLM 的部署可以后续进行，不影响这批任务开工。后续工作见 [BACKLOG.md](docs/zh-CN/BACKLOG.md)。

## 当前 Jira 入口

读 [JIRA.md](docs/zh-CN/JIRA.md)。BA/CS/MC/AP/CO 分别对应 KAN-10/11/12/13/14。
分支/commit/PR 用真实编号，保留内部 START 编号。工具打印版本化映射和建议分支，不实时查询 Jira。
已确认三人账号并分配，AP/CO 待账号保持未分配。开工前查实际认领，Sprint 规划与模型部署另行处理。
