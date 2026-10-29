# 文件归属与集成规则

中文阅读副本，依据 2026-10-18 英文主版同步。以[英文主版](../SHARED_FILES.md)为维护依据；若有歧义，按英文主版及其来源优先级处理。编号、状态、路径和命令保持原值。正文中的代码路径均相对仓库根目录。

按 Danny 要求沿用五条 Stage 1 链。这是任务范围，不是仓库权限、成员正式接受或贡献证据。
初始骨架由 AI 辅助准备，不能因为包含某人模块就将其记为该成员完成。

| 文件范围（相对仓库根目录） | 默认负责 |
|---|---|
| `beauty_company/modules/beauty_advisor.py`、`tests/test_ba.py`、`docs/modules/BA.md` | BA / Danyang Wang |
| `beauty_company/modules/customer_service.py`、`beauty_company/adapters/after_sales.py`、`tests/test_cs.py`、`docs/modules/CS.md` | CS / Siyuan Lei |
| `beauty_company/modules/marketing.py`、`tests/test_mc.py`、`docs/modules/MC.md` | MC / Zhengdu Wei |
| `beauty_company/modules/approval.py`、`tests/test_ap.py`、`docs/modules/AP.md` | AP / Jiaxuan Ren |
| `beauty_company/modules/coordination.py`、`tests/test_co.py`、`docs/modules/CO.md` | CO / Guiyu Liu |
| `docs/tasks/*.md` | 对应任务负责人，保留来源，区分提案/证据 |
| `docs/traceability.csv` | 各人只更新本前缀；GR 行须共同集成证据 |
| `docs/tasks.json` | 只按实际证据更新对应任务，保留并发变更 |

可添加归属明确的模块内 helper/测试。不为本地便利擅自搬共享商品函数；先列影响的导入/契约，另做集成。

## CS 意图／真实换货共享例外 · 2026-10-29

Danny／M1明确授权KAN-15 CS／CO共享集成、AI辅助：新adapters/cs_intent.py、modules/cs_flow.py，
共享llm／mock增量、BA目录快照helper、CS建议保存helper／旧真实入口保护、CO分阶段方法、
Company能力／HTTP／会话／UI及test_cs_live.py。test_llm／test_mc仅更正旧CS能力／禁用预期，
不改MC业务。合约／CS＋CO＋GR追溯及双语同更。未改AP／效果／结构／依赖／配置／任务登记。
保留Siyuan Lei CS、Guiyu Liu CO和原贡献，不领取／重分配KAN-11／KAN-14／starter。
相关负责人评审待办，不由测试推断；Danny授权自己PR在全部必需检查后正常保护合入，不自我Approve，
不改保护规则。

## CO 失败边界共享例外 · 2026-10-29

Danny／M1 明确授权 KAN-15 有界增量，AI 辅助：modules/coordination.py、新 tests/test_co.py，
及 web/app.js 既有 CS needs 显示的两处空值保护。共享合约、相关 CO-T 行和双语文档记录新增证据。
未改 CS 业务／AP／BA／MC 服务、HTTP 签名、结构、提供方、依赖、任务登记或归属。
Guiyu Liu／M5 保留 CO 原归属，不是 KAN-14／CO-START-01 认领。
CO／CS／共享负责人评审待办，不能由测试推断；本轮未读写 Jira、推送／PR／合并。

## MC 生成恢复检查点 · 2026-10-29

Danny / M1 授权 KAN-15 下 MC 生成保存恢复有界例外：新增 modules/mc_generation.py、复用抽出的
Marketing 校验、Company facade／快照／故障演练扩展、统一campaign HTTP和恢复／重试／取消网页。
新增测试在tests/test_mc.py，相关契约／追溯及双语说明同步。未改AP实现／schema／BA／CS／CO／
模型传输／依赖，保留原MC归属／任务登记，受影响MC／共享维护者评审待办。
仅本地，不外部Jira／PR／合并。


## MC 模板 MP4 检查点 · 2026-10-29

Danny / M1 授权 KAN-15 的 MC-F-02 模板 MP4 共享例外。新增可选 template_video 适配器和
media_tools.ps1；Company 媒体注入／访问、HTTP 当前修订认证范围下载、CLI／Windows 开关、MC
文件校验／审批哈希及 UI 播放／下载标签增量修改，测试在 test_mc.py。AP 实现、结构、BA／CS／
CO 服务、任务登记、模型传输／配置不变。记录可选依赖理由和安装，默认 mock 独立。相关评审
待办，不推断认可或 Jira claim，本轮不推送／PR／合并。


## MC 有界真实文字检查点 · 2026-10-29

Danny / M1 明确授权 KAN-15 有界真实 MC 文字。本轮涉及共享 llm 适配器、新纯 mc_text
契约、Company.campaign/mode、可选 HTTP 分发、CLI／Windows 开关、MC 服务／当前审批 action、
UI 标签／表单及 tests/test_mc.py。既有 AP 实现、数据库结构、BA／CS／CO 服务、任务登记／归属、
模型配置／安装不变；保留默认 mock、BA-only Strata 及 Zhengdu Wei 原 MC 工作署名。
相关 MC／共享文件评审待办，不推断队友认可、Jira 更新、远程 PR 或验收。本授权不包含同轮增加
真实 CS 意图、视频、MC 取消／恢复或自由文案。


## 共同文件

`contracts.py`、`store.py`、`application.py`、`http.py`、`adapters/mock.py`、
`web/app.js`、`web/styles.css`、`web/index.html`、`tests/test_workflows.py`、
CI/脚本、根目录规范和来源元数据影响多链。

BA/CS/MC/CO 首批不改共同文件；AP-START-01 仅有 tasks.json 列出的 AP 意图新增保存、
决定/恢复 facade、既有 AP 审计回归例外。该范围已准备好，成员获授权后不必反复请示普通本地修改。

更多共同变更需要：

1. 在任务/PR 写明具体文件、变更前后约定、调用方与理由，保留其他链行为。
2. 设有界共同任务，避免五个 Agent 同改前端/结构。Danyang 以往集成经历不代表接受所有未来集成任务。
3. 尽量兼容增加；语义变化时一起更新调用方、保存、适配器、模型偏差、回归。
4. 共享改动请相关队友审阅，这是协作建议，不是 GitHub 强制批准门槛；已授权的普通本地修改无需重复打断。

服务任务可完成明确范围，并标 HTTP/UI 待接；没有接入不能称浏览器功能完成。
旧页面若假设成功，不可直接暴露新失败返回；失败视图由共享集成任务处理。

## 分支、认领与冲突

- 从当前共同 main 创建 tasks.json 建议的真实 Jira 编号分支，例如 `KAN-11-cs-start-01`。
  按 START_HERE.md 确认成员、公开范围并汇报；每个改动区域必须属于本任务。
- 重复工作前读取实际认领；本地 helper 不联网，不能保证仍未认领。
- 不认领他人链，不因发现其他缺口自行扩大；记入 BACKLOG。
- 保留其他脏文件。共享目录必要时可独立 worktree/checkout；不同笔记本本来就独立。
  开工工具不创建 worktree。
- 冲突时比较并有意合并，不覆盖任务记录、删他人测试或盲目重生成共享文件。
- 人工审阅、真实 Jira、实际 commit/PR 才是证据；本地身份、生成文字、计划或提交数量本身不是。

未脱敏正式 PDF 保留本地不变。公开 PDF/摘录仅去学号（PDF 另去元数据），分别记录变换与哈希，
不能用派生哈希冒充原件哈希，也不能发布被忽略的原件。新正式报告版本须明确更新来源并评估影响，不可为过检查修改旧报告、
提取文本或存储指纹。同步中文副本不改变代码归属，也不建立第二套任务状态。

## LLM 工作预留

Danyang Wang 负责共享 GR-INT-02 部署、adapter／配置、供应商 prompt、后续 CS 意图接口和模式显示，
见 [LLM_INTEGRATION.md](LLM_INTEGRATION.md)。其他成员保留已有注入边界、给本地 fake／样例，
遵守原文件范围。集成改队友模块仍需限定协调，不转移队友业务逻辑负责人。
