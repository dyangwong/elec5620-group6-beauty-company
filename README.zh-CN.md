# Beauty Company · ELEC5620 Stage 2

中文阅读副本，依据 2026-10-16 英文主版同步。以[英文主版](README.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

Group 6 的 **AI-Powered One-Person Beauty Commerce and Content Company** 初始本地原型。
包含 BA/CS/MC 三个业务能力，以及 AP 人工审批和 CO 协调/恢复。旧原型仅供参考，
没有导入旧代码、数据库、凭据或媒体。

**队友与编程 Agent 从 [START_HERE.zh-CN.md](START_HERE.zh-CN.md) 开始。**
说明自己的完整姓名、成员编号或模块后，Agent 可按任务包推进已授权的本地工作。
真实/本地模型部署暂缓，不影响首批任务开工。

**当前是能运行的初始模拟版本，尚非完整 Stage 2 提交。** 模型回复为确定性 mock；
媒体只是分镜占位，没有视频文件、真实结算、发货或公开发布。设计仍为 PROPOSED，
须由团队记录是否采纳，不能把实现当成正式批准。

## 本地启动

需要 Python **3.9+**，仅用标准库。此初始版本无需安装包、API key、Node、Docker、
云账号或联网。在仓库根目录运行：

```sh
python3 -m beauty_company
```

打开 <http://127.0.0.1:5620>，按 Ctrl+C 停止。端口占用时加 `--port 5621`。
Windows 若没有 `python3`，换成 `python` 或 `py -3`；此处未验证原生 Windows 运行。
数据保存在被 Git 忽略的 `var/company.sqlite3`，重启保留。要独立演示而保留原数据：

```sh
python3 -m beauty_company --port 5621 --db var/fresh-demo.sqlite3
```

开发服务器只绑定本机，不应公开暴露。共享演示密码与简单 HTTP 入口不是生产身份/托管方案。

| 工作区 | 用户名 | 演示密码 | 虚构订单 |
|---|---|---|---|
| Founder / Operator | `founder` | `founder-demo` | 可审阅所有演示流程 |
| Alex / Customer | `customer` | `customer-demo` | `ORD-1001` |
| Sam / Customer | `customer-2` | `customer-demo` | `ORD-2001` |

登录页会填写对应共享密码。这些是有意公开的虚构演示凭据；服务端不透明会话、归属检查、
CSRF 检查仍负责角色边界。

## 体验集成流程

1. 以 Alex 登录，在 **After-sales care** 提交默认请求。
2. 换 Founder，在 **Customer requests** 点击 **Start advice handoff**，对应 GR-S-01 的 Founder 主动发起。
3. 换回 Alex，检查推荐与证据，点击 **Confirm proposal & request review**。此时仅创建待审 AP 请求。
4. Founder 在 **Review queue** 填理由、批准当前精确范围。决定先提交后投递，本身不执行业务。
5. Alex 再确认模拟换货。系统只记录一次效果、扣减一次模拟库存，并由 CS/CO 保存结果。
6. 查看 **Activity trail**。没有发生真实付款或发货。

同时演示不同角色可用不同浏览器配置或无痕窗口；普通标签页共用 cookie。
其他会话修改后需要刷新。MC 的独立流程是 Founder 在 **Content studio** 创建 mock 草稿、
审阅精确版本，再修改以展示重新审批；不会生成视频或发布，批准只针对该草稿。

Founder 的 **Activity trail → Simulation controls** 可注入一次写后超时、结果保存失败、
已提交决定投递失败。CS 查询同一 actionRef；AP 重新投递同一已提交决定。

## 检查

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 scripts/start_work.py --list
```

测试使用临时数据库，不触碰运行中的演示数据。只覆盖部分 Stage 1 条件，未完成全部 41 组。
以 `docs/traceability.csv` 了解覆盖缺口。[公开仓库](https://github.com/dyangwong/elec5620-group6-beauty-company)已建立，
[首次 CI](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/38865450983)在 Python 3.9/3.13 均通过 37 项测试、来源检查和 JS 语法检查。
main 必须 PR/检查，作者可自行合并，不强制外部批准。队友邀请待核实用户名，Jira 未建立。

## 阅读目录

- [AGENTS 中文副本](AGENTS.zh-CN.md)：Agent 入口、来源优先级和必须保持的规则。
- [开工入口](START_HERE.zh-CN.md)：身份、五人分工、可复制的指令。
- `docs/team.json` / `docs/tasks.json`：唯一共享成员映射与五份任务数据，不另建中文数据表。
- [共享文件](docs/zh-CN/SHARED_FILES.md)、[后续任务](docs/zh-CN/BACKLOG.md)。
- [当前状态](docs/zh-CN/STATUS.md)、[实际验证](docs/zh-CN/VERIFICATION.md)。
- [需求](docs/zh-CN/REQUIREMENTS.md)、[接口与状态约定](docs/zh-CN/CONTRACTS.md)。
- [协作流程](docs/zh-CN/COLLABORATION.md)、[决策](docs/zh-CN/DECISIONS.md)。
- `docs/zh-CN/modules/`、`docs/zh-CN/tasks/`：五个模块说明与任务书中文副本。
- `docs/reference/`：63 页脱敏报告（含模型）、对应摘录、评分标准与来源；未脱敏正式原件留本地并被忽略。
- [Git 工作流](docs/zh-CN/GIT_WORKFLOW.md)：必须 PR 和检查通过，作者可自行合并，无强制他人批准。

本目录是预定仓库根目录，课程总目录和旧原型留在外面。源码包须能独立运行；
原始报告是依据，不是应用运行时依赖。英文原路径是主要维护入口，中文副本方便阅读。
