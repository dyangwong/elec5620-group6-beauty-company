# Windows 部署与 KAN-15 交接

当前更新：本地模型及一条真实 BA HTTP 路径已在 runtime ACL 修复后通过，
见 [当前运行证据与恢复命令](WINDOWS_LLM_RUNTIME.md)。下方安装受阻内容保留为此前尝试记录。

中文阅读副本；维护依据为[英文主版](../WINDOWS_LLM.md)。工作日期按客户端：2026-10-21，
Australia/Sydney。Danyang Wang / Danny / M1，KAN-15 / GR-INT-02；分支
`KAN-15-shared-llm-windows`，起点 `e51dfc4`。初次部署检查时没有 commit、push、PR、合并或
Jira 写入；后续节点见 VERIFICATION.md；未认领 BA-START-01。代码、测试、文档有 AI 协助。

## 实测电脑和基线

| 项目 | 检测结果 |
|---|---|
| 系统 | Windows 11 Pro 25H2，26200.9711，x64。Python 确认 Windows 11；注册表旧 ProductName 仍写 Windows 10 Pro。 |
| CPU | Intel Core Ultra 9 275HX，Windows 原生拓扑接口确认 24 物理核心 / 24 逻辑处理器，支持 AVX2；CIM 不可用。 |
| 内存 | 可用物理总量 33,737,986,048 字节，即 31.42 GiB，属于 32 GB 规格；初始空闲 16.64 GiB，后约 14.9–15.1 GiB。 |
| GPU | RTX 5070 Ti Laptop GPU；nvidia-smi 实报显存 12,227 MiB，驱动 617.42。 |
| 磁盘 | 初始 C 空闲约 415.13 GiB，D 约 298.50 GiB，使用中会变化；无法通过 CIM 确认 SSD 型号/接口，未测模型磁盘速度。 |
| 工具 | Git 2.51.0.windows.1、Python 3.14.5、Node 22.19.0；py 启动器未列出注册解释器，使用 python 或项目虚拟环境。 |
| 仓库 | 新克隆，干净 main / e51dfc4，已 fetch；唯一打开 PR #7 为队友 KAN-11 CS 工作，已检查，不合并、不重做。 |
| Jira | 无可用 Jira 连接；未认证读取 KAN-15 API 返回 404，不据此认定删除或任务状态。当前负责人/认领/流程状态未核实。 |

首次 38 项测试受系统临时目录权限影响，共报告 70 个错误（部分包括清理失败）；改用工作区
TEMP/TMP 后 38 项全部通过。首次来源检查因两份文本被 Git 转为 CRLF 失败，恢复 Git 原始字节
后通过；没有改来源哈希、PDF 或 manifest。新增 `.gitattributes` 固定来源文本 LF。
基线网页在 Windows 启动，实际浏览器登录客户工作区成功。

## 选择的模型与安装限制

已阅读官方[安装说明](https://github.com/Niko1221/Strata/blob/9ae93f7b1fe989d04a8e404d32cddaeeff10505f/docs/INSTALL.md)、
[模型说明](https://github.com/Niko1221/Strata/blob/9ae93f7b1fe989d04a8e404d32cddaeeff10505f/docs/MODELS.md)
和 [v0.2.1](https://github.com/Niko1221/Strata/releases/tag/v0.2.1)。GPU、驱动和 AVX2 符合平台条件，
实际内存余量是限制。完整 IQ2/IQ3 加系统/应用内存较紧；Coder 删去一半专家且偏代码任务，
不适合作为本业务首选。先选通用 **Gyro-S**，其压缩质量较低，需要业务实测；不把台式机速度
当成本游戏本速度。不要求本次升级硬件，更多内存可供后续更高质量规格评估。

| 项目 | 固定选择 |
|---|---|
| 发布 | v0.2.1，commit 9ae93f7b1fe989d04a8e404d32cddaeeff10505f |
| Terminal | 0.1.46.1，Windows x86_64 下载 72,126,142 字节，自带 Python 3.12.15，已下载并核对哈希 |
| Terminal SHA-256 | c2d422081eb72c44cf1b23e7f20c506a2fed371e0e614ead48be7045b7798848 |
| 引擎 | 0.1.46 Windows CUDA 13，下载 579,792,118 字节；签名 feed 选中，尚未装好 |
| 模型 | agentionai/Qwen3.8-Flash-Next-Gyro-GGUF，revision 1ada08422e404aca51ab9df665f089f34c419c6b |
| 权重 | Qwen3.8-Flash-Next-Gyro-S-TQ1_0.gguf，58,487,015,808 字节，约 58.49 GB / 54.47 GiB |
| 权重 SHA-256 | c6ea1b08ca312f99095b27588ba35976b53f948268e7f91e7761926aa01d9c87；来自上游固定版本，尚未下载核验 |
| 配置 | 8192 token、int8 KV、单并发、127.0.0.1:8080；图像/MTP 关闭，跳过调优 |
| 下载/磁盘 | 模型、引擎和 Terminal 合计约 59.14 GB；若上游准备阶段仍获取辅助文件，另留 6 GB。预留 110 GiB 给解包、准备、缓存和余量；实际安装占用未测。 |

官方给 Gyro-S 的权重 RAM+VRAM 合计需求约 27.6 GB，不等于当前空闲内存一定足够。
还要考虑 GPU 缓存、KV/临时区、Windows、浏览器和其他程序；先关闭重负载程序，再检查余量。
未验证图像、MTP、长上下文、多用户吞吐或本机速度；遵守模型 Qwen Community License，不提交或分发权重。

Terminal 版本和签名 feed 检查成功（sequence 103，内置信任 key 5d1bc23abbeffd0d）。
随后引擎安装因 WinError 5 失败：Strata 的 Windows 私有目录 owner/DACL 与本会话受限进程冲突。
申请沙箱外执行又被本会话审批策略拒绝。没有删除上游权限或签名检查。
应在用户普通 PowerShell 中重试；这不证明普通 Windows 安装一定失败。
**模型未下载、服务未启动、成功真实 BA 调用尚未验证。**

## 安装、启动、停止和诊断

在仓库根目录、普通 PowerShell 执行。无需管理员、不升级全局 Python、不装驱动、
不改执行策略。若系统策略阻止脚本，先审阅并使用获准方式，不关闭系统保护。

```powershell
.\scripts\windows.ps1 -Action Setup
.\scripts\windows.ps1 -Action Verify
.\scripts\windows.ps1 -Action Start
# 打开 http://127.0.0.1:5620
.\scripts\windows.ps1 -Action SmokeTest -Mode mock
.\scripts\windows.ps1 -Action Stop
.\scripts\windows.ps1 -Action Diagnose
```

Setup 仅在不存在时建立 `.venv` 和复制 `var/llm.strata.json` 示例，不覆盖现有配置。
应用仅用标准库，无额外包。脚本不 pull/reset/stash 代码、不清数据库。Start 保留指定路径数据，
重复启动保留原进程和配置。Stop 同时核对 PID、创建时间和可执行路径，只停本脚本启动的进程，
不批量结束 Python。日志用唯一文件名保存，停止不删数据。
独立验证可加 `-Port 5621 -Database var/my-check.sqlite3`；Stop/SmokeTest 用同一端口。
Codex 受限命令结束后可能清理后台子进程，在此环境保留前台会话：
`.\.venv\Scripts\python.exe -m beauty_company --port 5621 --db var/my-check.sqlite3`，Ctrl+C 停止。

模型单独安装，会下载上表大文件：

```powershell
.\scripts\windows.ps1 -Action InstallModel
# 安装后自动启动模型并打印 /v1/models。
# 手动将精确 ID 填入 var/llm.strata.json 的 model，保留其他本地设置。
.\scripts\windows.ps1 -Action Start -Mode strata -Database var/live-demo.sqlite3
.\scripts\windows.ps1 -Action SmokeTest -Mode strata
.\scripts\windows.ps1 -Action Stop
.\scripts\windows.ps1 -Action StopModel
# 下次：
.\scripts\windows.ps1 -Action StartModel
```

权重、运行状态、私有配置、profile 和日志都在忽略的 `var/`。脚本固定 Terminal 哈希、签名
引擎 feed。重复 InstallModel 保留已有运行配置；完成配置建立前，中断下载由上游断点续传。
已有配置但缺文件时，先看 doctor 和上游修复方法，保留本地设置。
可选 key 从指定进程环境变量读取，不放命令参数、公开示例、诊断导出或截图。不设置 LAN/防火墙。

## adapter 与实际验收

保留 `Company(path, llm=None)` 及 v1 `propose(context, evidence)` /
`generate_script(brief, evidence)`。本次仅接 BA propose；MC 明确继续 mock，CS intent 没有新接口。
live 模式的 HTTP CS coordinate/revise 返回 `LIVE_HANDOFF_NOT_CONNECTED`，等 CS/CO 负责人协调；
现有换货演示用 mock 模式。内部直接调用 BA/CS 不是已验证的真实服务 API。
AP/CO 权限规则保留，媒体和交易仍模拟。

独立咨询经 `Company.consult` 校验结构化需求，在写事务外调用模型，保存时重新比对商品/库存。
stock、facts、price、version 等改变就拒绝结果，不扩展修改/取消生命周期。
adapter 只发送允许的需求和商品证据；不用代理/重定向；限制 socket 超时、输出 token 和响应字节；
严格单对象 JSON，拒绝重复键、非有限值、多余字段、未知商品/事实、不同模型 ID 和截断输出。
BA 再独立验证候选和事实。失败记录 INCOMPLETE，错误码为 `LLM_TIMEOUT`、`LLM_UNAVAILABLE`、
`LLM_HTTP`、`LLM_INVALID_OUTPUT`，证据变化用 `LLM_STALE_EVIDENCE`；不调用 mock 回退。
不向客户暴露供应商原始响应、key 或 cookie；这些预算是项目选择，不是课程规定。

health/UI 分别标配置的 BA、MC、CS intent、媒体和交易状态；health ok 仅证明应用可用，
不是模型就绪。只有实际成功且 simulated:false 的 BA 记录才支持真实成功声明。
切到 live 配置后，旧 mock 记录仍按自身模式显示。

已执行：原有 38 项测试修复 Windows 环境后通过；扩展 45 项离线测试在 Python 3.14.5 和 3.12.15 均通过，
其中传输服务是脚本化本地 HTTP 样例，不是真实模型。仓库来源与 JS 语法检查通过。
Setup/Start/mock HTTP SmokeTest/重复 Start/Stop 已测，不创建重复启动指定的另一数据库，保留配置。
无模型时，实际 live 配置应用的 HTTP 咨询约 2.1 秒后保存 INCOMPLETE / LLM_TIMEOUT，
探针退出 1，没有 mock 建议或真实成功；更早一次探针也如实记录应用子进程已清理导致不可用。
真实模型成功、live MC/CS、多电脑网络、完整 Stage 1/UML 验收仍未验证。

探针证据写入 `var/verification/`，任何应用/供应商/结构/业务失败均非零退出。
仅使用虚构账号和需求，公开文档只保留脱敏摘要。
执行主机原始时间为 10 月 20 日 UTC，而客户端工作日期为 10 月 21 日；保留原始时间，
不把它当 Jira 日期。其他解释器检查见 VERIFICATION。

## 跨电脑交接与待审阅

本分支尚未提交，另一台电脑暂时无法 fetch 这些修改。Danny 审阅 diff 并在获准后 commit/push
同一任务分支，再到另一台电脑 clone/fetch；不要两机并行编辑同分支。重跑 Setup/Verify，按新机
实测内存选配置。权重、虚拟环境、密钥、数据库和 profile 不经 Git 同步。

共享影响：adapter/config、CLI、facade、BA HTTP 入口和窄范围 CS live 防护、BA 模式/错误映射、
网页模式标签、Windows 工具和文档。未改队友 CS/MC/AP/CO 实现或首批任务认领。
CS/CO 需审阅 HTTP 防护和错误映射，后续 MC/CS 真实接入需负责人协调；尚无队友审阅记录。

**Jira update pending — KAN-15**：先核实当前负责人/认领/状态，再按实际情况转 In Progress，
记录 Danny 已在该分支实现共享 BA adapter 和 Windows 工具，离线检查通过、真实 HTTP 模型不可用
路径安全 INCOMPLETE；受限环境阻止 Strata 安装，真实成功仍待验证；MC mock、CS intent 未接、
BA starter 未改。下一步普通 PowerShell 安装和真实 SmokeTest，再审阅共享修改。
没有真实 PR 前不填链接，不因测试通过就标 Verification/Done 或完成父 epic。

## 从其他目录调用 Windows Setup

脚本现将相对 -LlmConfig 按仓库根解析，即使用脚本绝对路径从其他目录调用也一致；
已有本地配置不覆盖。最新 47 项测试审查记录见 VERIFICATION.md，上文 38／45 项为此前观察。

## Windows 合入 CS/AP 后回归 · 2026-10-25

本机使用已有 Strata 和独立库验证了 966dae4 集成分支，两个 Windows 解释器各通过 84 项测试，
真实 BA 网页及安全模型失败通过。准确证据、本地安全停止修复及 AP 网页恢复／文案限制见
[最新运行记录](WINDOWS_LLM_RUNTIME.md) 和 [完整验证](VERIFICATION.md)。
上方安装受阻、第一阶段未提交和任务状态段落是历史，不表示现在需要重新安装模型或倒退 Jira 状态。
回归验证本身没有远程写入。
