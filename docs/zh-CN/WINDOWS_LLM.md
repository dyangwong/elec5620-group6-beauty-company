# Windows 部署与 KAN-15 交接

## CO 失败检查点 — 不需模型部署 · 2026-10-29

当前 KAN-15-co-handoff-failures 增加有界 mock CS→BA 失败处理。既有 Windows Verify 实测
237 离线测试、来源及 JS 通过。按下方正常 mock 步骤选新忽略数据库和空闲 loopback 端口。
客户更正产生新版本，再由 Founder 明确新交接；失败建议不能进入确认／审批，不自动重试。
本轮 5750 故障替身／null 注入仅 scratch 验收工具，非产品配置；自动测试可复现失败边界。
不需新软件／配置／模型安装，真实 CS 意图／交接仍未连接／阻止；本轮未启动或测试模型，
已有真实 BA／MC 证据属历史。仅停止本轮进程、保留原数据，详见 VERIFICATION 的实际证据及限制。
冻结 eb8f0de ZIP 早于本增量，评审后仍需当前源码发布彩排。

## MC 生成恢复检查点 · 2026-10-29

当前源码增加 MC 生成恢复；下方冻结 eb8f0de ZIP 不含本增量。复用已安装模型／工具，
无需新安装、下载或依赖。选新忽略数据库和空闲 loopback 端口；实测 5740 mock、5741
显式真实 MC／模板视频，独立数据在 var/mc-recovery-20261029。

Activity trail 选择 **MC final generation save failure (draft retained)**、Apply fixture，
然后 Content studio→生成。应为 RECORDING_FAILED、有可恢复元数据、无待审文字／媒体／审批 ID。
仅停止／启动本轮应用，使用同一数据库／配置，点击 **Recover saved generation**。
应核验并保存内容及唯一精确待审 REVIEW_PENDING，不是批准；重复恢复 ID 不变。
还实际验证了 SQLite 审计写入失败后的网页／重启恢复，触发器仅在独立测试库存在且已移除。

真实 MC：仅在既有模型所属 profile 停止时启动，并使用
`-Mode strata -LiveMc -LlmConfig <既有本地 JSON> -VideoConfig <本地 JSON>`。
记录实例 ID／归属；完整生成结果已持久保存后，仅以保护条件停止本轮模型并重启本轮应用。
恢复必须复用同一文字、artifact／文件哈希，不推理／渲染。保留原媒体输出目录，重启时提供其模板配置；
否则返回 MC_MEDIA_RECOVERY_UNAVAILABLE、保留待恢复草稿。模型就绪及应用健康不能代替恢复证据。

阶段保存失败或持久结果前中断，不提供 Recover。先刷新，GENERATING 本身不能证明 worker 已停止。
**Retry generation as new revision** 显式使旧工作失效并可重新调用生成器；模型关闭后重试仍应
GENERATION_FAILED／LLM_UNAVAILABLE，真实标签不变、无 mock 回退。无效内容需显式修订。

**Cancel this campaign** 保存新取消修订，使迟到结果／旧审批无效；物理模型／渲染进程仍可能结束并
留下忽略文件。取消保存失败不能视为已取消；取消后需新建 campaign。已批准／拒绝终态通过显式修订，
不追溯取消。本功能不发布内容。

原始测试日志／读回在 var/mc-recovery-20261029，仅停止本轮应用回执／精确模型实例，保留原环境。
完整 MC 已提交决策恢复、部分渲染断点续作不在本范围。精确接口／证据见 CONTRACTS.md／VERIFICATION.md；
Jira 未核实且未改动。


## 冻结源码 ZIP 彩排 · 2026-10-29

**当前已实测包：**eb8f0de8d412344e828daf9032898c2dbb6155ee，
elec5620-source-eb8f0de.zip，5,658,127 字节／116 文件，SHA-256
`bf7d8b0324c9797e2adb03d0727a89aa31325ebb5a22223fd7a528760d25bba4`。
实际新解压目录 `D:\elec5620_project\rehearsals\20261029-eb8f0de\fresh source`，
191 项测试及 mock 全流程、真实 BA、真实 MC 文字／模板 MP4／审批和模型不可用保存失败通过。
精确记录／限制见 VERIFICATION.md，下方早期日期章节保留为历史。未需要修复应用脚本。
冻结 ZIP 不改写，包内文档截至 eb8f0de；本次后续回执需单独随包交接。
旧 f7bb141 包不含最新 BA／MC 增量。

**提前准备：**Python 3.14.5（含 venv）、PowerShell、浏览器、用于 JS 检查的 Node v22.19.0，
既有模型管理环境／运行时／权重、可选 FFmpeg／ffprobe 9.0.2 和本机 Windows Arial。
本轮不需下载 Python 包。ZIP 仅含源码，不是模型合集或全新电脑安装器。保留旧模型工作区和媒体工具路径；
本路线不运行 InstallModel、升级、重复复制权重或 media_tools Setup。未新增网络／局域网暴露。
macOS／其他电脑／现场及首次离线准备仍未验收。

**现场执行：**核对 ZIP 哈希，选不存在的解压目录，不覆盖解压；执行下方“在全新目录执行”的
Setup／Verify／导入来源命令，确认打印路径均在新目录。选空闲端口和新数据库名，占用时停止操作。
Setup／Start 保留已有文件，不会重置旧演示。本轮端口 5730／5731，数据库
var/mock-demo.sqlite3、var/live-demo.sqlite3。

从新解压目录独占创建忽略配置。遇到已存在文件，检查复用或另选名称，禁止覆盖：

```powershell
$modelHome = 'D:\elec5620_project\elec5620-group6-beauty-company'
function New-DemoConfig([string]$Path, $Value) {
    if (-not [IO.Path]::IsPathRooted($Path)) { $Path = Join-Path $PWD.Path $Path }
    $stream = [IO.File]::Open([IO.Path]::GetFullPath($Path), 'CreateNew', 'Write', 'None')
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes(($Value | ConvertTo-Json))
        $stream.Write($bytes, 0, $bytes.Length)
    } finally { $stream.Dispose() }
}
New-DemoConfig 'var/llm.live.json' @{
    base_url='http://127.0.0.1:8080/v1'; model='qwen3.8-flash-next-gyro-gyro-s'
    timeout_seconds=120; max_tokens=512; api_key_env='BEAUTY_LLM_API_KEY'
}
$toolBin = Join-Path $modelHome 'var/media-tools/ffmpeg-9.0.2-essentials_build/bin'
New-DemoConfig 'var/media.local.json' @{
    ffmpeg=(Join-Path $toolBin 'ffmpeg.exe'); ffprobe=(Join-Path $toolBin 'ffprobe.exe')
    font='C:\Windows\Fonts\arial.ttf'; output_dir='media-output'; timeout_seconds=120
}
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5730 -Database var/mock-demo.sqlite3
# 先检查既有模型运行状态，ready 则复用，stopped 时从模型所属工作区启动：
& "$modelHome\scripts\windows.ps1" -Action StartModel
(Invoke-RestMethod 'http://127.0.0.1:8080/v1/models' -TimeoutSec 10).data.id
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5731 -Database var/live-demo.sqlite3 -LlmConfig var/llm.live.json -VideoConfig var/media.local.json
```

应用代码／数据库／配置／输出全部在新目录，仅模型服务、明确指定的工具及字体是外部依赖。
相对 output_dir 从配置所在目录解析，因此写入新 var/media-output。独立配置建立后不依赖旧应用配置。
本机服务无需密钥；未来密钥仅放指定环境变量。配置、会话、数据库、模型、工具、字体、媒体和日志不打包。

5730：Customer 提交 ORD-1001→Founder 启动建议交接→Customer 确认建议→Founder 精确审批→
Customer 最终模拟确认。最终确认前零效果，后为一个，重复确认不增加。
5731：Product advice 输入自然补水／无香／AUD60 需求并明确确认，检查保存的真实 BA 事实；
Founder 在 Content studio 请求仅用目录事实“50 ml”的 energetic teaser，核对真实文字／模板标签、
播放／下载／哈希后审批具体修订。同一主机不同端口／角色切换需重新登录，数据库不共享但 cookie 名相同。
视频为静音文字卡模板，不是 AI 生成场景或语音。

分别确认应用健康、模型就绪和真实推理保存成功。仅当本轮启动且仍拥有同一实例时，按下方“停止与诊断”
的官方实例保护命令停止模型；不停止先前／共享模型。新 BA 应保存 INCOMPLETE／LLM_UNAVAILABLE，
无结果或 mock 回退，旧 MP4 仍可访问。CS 意图仍 NOT_CONNECTED，真实 CS 交接仍阻止。

```powershell
# 从新目录仅停止本轮对应回执的应用：
.\scripts\windows.ps1 -Action Stop -Port 5730
.\scripts\windows.ps1 -Action Stop -Port 5731
```

保留新 var 诊断，分别检查新应用日志、数据库模式／状态和模型引擎日志。
AP 恢复保留历史证据，本轮 ZIP 未重做；MC 完整恢复及完整 Stage 2 仍开放。
Jira 未核实／更新待办，本轮不访问／更新；不推送、PR、合并或上传 Canvas。


## MC 模板 MP4 检查点 · 2026-10-29

媒体工具为独立可选操作，普通 Setup／Start／Verify 不会安装。需要 Windows PowerShell、
首次下载网络和本机 Windows Arial 字体，字体不随源码分发。

```powershell
.\scripts\media_tools.ps1 -Action Setup
.\scripts\media_tools.ps1 -Action Diagnose
# mock 文字 + 实际模板 MP4，无需模型：
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5720 -Database var/video-demo.sqlite3 -VideoConfig var/media.template.json
# 或复用既有模型，真实文字 + 实际模板 MP4：
.\scripts\windows.ps1 -Action StartModel
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5721 -Database var/video-live-demo.sqlite3 -LlmConfig var/llm.strata.json -VideoConfig var/media.template.json
.\scripts\windows.ps1 -Action Stop -Port 5720
.\scripts\windows.ps1 -Action Stop -Port 5721
```

选择空闲端口／新库名，保留原数据。重复工具 Setup 遇到原配置直接返回，不下载或覆盖，不改
PATH／系统／模型；原有不完整工具目录留待诊断。固定包 ffmpeg-9.0.2-essentials_build.zip，
114768076 字节，来自 https://github.com/GyanD/codexffmpeg/releases/download/9.0.2/ffmpeg-9.0.2-essentials_build.zip ，
SHA-256 60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba，
对照发行方 GitHub asset digest 核验。工具／许可证／说明在忽略的 var/media-tools，源码 ZIP
不包含；另行分发二进制包需保留发行方许可声明。

忽略配置 var/media.template.json 含 ffmpeg／ffprobe／font／output_dir／timeout_seconds，
本机每个子进程 120 秒；相对路径相对配置文件，不是源码目录。CLI 加 --mc-video-config <本地 JSON>。
另一新解压源码可传既有媒体配置绝对路径或独立准备工具配置，不复制整个模型环境。工具路径缺失
允许应用启动，以便生成时保存 MEDIA_UNAVAILABLE；无效 JSON／结构拒绝启动。省略 VideoConfig
保持 mock 媒体。只停本轮应用及准确模型实例，见 WINDOWS_LLM_RUNTIME.md。

Founder 在 Content studio 创建、播放、下载、比较哈希／修订，再使用现有审批。修改生成新文件／
哈希／审批，旧媒体 URL 返回 409。待审允许内部预览，下载不代表发布。模型就绪、工具存在、
文件生成和浏览器可播放分别验。视频是静音文字卡及书面镜头建议，不实际执行相机运动。证据见
VERIFICATION.md；新增量 ZIP、其他电脑、macOS、首次离线安装和现场验收未验证。


## MC 有界真实文字检查点 · 2026-10-29

复用已安装模型／配置，不重新 InstallModel 或复制权重。当前源码根目录完成 Setup／Verify
并检查端口／进程后：

```powershell
.\scripts\windows.ps1 -Action StartModel
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5711 -Database var/mc-demo.sqlite3 -LlmConfig var/llm.strata.json
# 浏览器打开 http://127.0.0.1:5711，以虚构 Founder 登录 Content studio。
.\scripts\windows.ps1 -Action Stop -Port 5711
```

独立演练选择空闲端口和新库名，原数据库保留。CLI 同等参数为 --llm-mode strata、--llm-config
var/llm.strata.json、--mc-live、--port 5711、--db var/mc-demo.sqlite3。省略 LiveMc/mc-live
保持 MC mock；mock + LiveMc 在进程变动前拒绝。无需改写配置或新增依赖。新解压源码应按下方
步骤传入游戏本原本地配置的绝对路径；StartModel 仍从拥有模型环境的原目录执行。本次 MC 增量
尚未做新目录 ZIP 演练。

分别检查应用健康、模型就绪、实际结果。calm／Fragrance-free brief 生成后要求修订，再用
energetic／50 ml，检查脚本／风格／字幕变化、新审批、模式和目录事实，仅批准当前精确修订。
文字是目录原文组合，媒体仍 MOCK_STORYBOARD。模型停机应保存 GENERATION_FAILED /
LLM_UNAVAILABLE，无文字／媒体／审批或静默 mock 成功；LIVE 配置和健康不证明就绪或推理。

只停止本轮端口／回执对应的应用；本轮启动的模型用 WINDOWS_LLM_RUNTIME.md 的准确实例保护
停止，不关闭已有共享模型。本次用 5710 mock、5711 live 及 var/mc-live-20261029 下独立库；
两个应用和所启模型均已停止，原配置／数据库／模型保留。下方旧日期证据属历史，当前见
VERIFICATION.md。


## 当前 ZIP 部署步骤 · 2026-10-28

冻结演练包源码 `f7bb141f6e35c7846989adccf58841b9e128a978`，
SHA-256 `5be88639cdd33415dadc77c0e6bfdc286b34b50e4635be2568ee01f4543e6ba3`。
最终包已在第二个新目录通过 123 项测试、mock／失败恢复和真实 BA 的实际 HTTP 复验。
之后的文档回执提交不改变该 ZIP；最终回执见 VERIFICATION.md，515bfa5 的网页演练另列。


Danny / M1 授权本次 GR-INT-03 本地源码交付演练，不领取 BA-START-01，不补完整个
GR-INT-02。**GR-INT-03 是内部 BACKLOG 标签，不是 Jira key。**仓库没有对应部署任务的
Jira 编号映射；Jira 未核实／更新待办。按用户要求，本轮不查询或修改外部 Jira，不上传
Canvas，不推送或合并 PR。

### 现场前准备

- Windows PowerShell、可用 Python >=3.9（含 venv/ensurepip）与浏览器。本机实测 Windows
  11 Pro 25H2 / 26200.9711、Python 3.14.5、PowerShell 5.1。Setup 在新目录创建环境，
  应用只用标准库，不需要下载 pip 依赖、前端构建或联网资源。
- Node 只用于 JavaScript 核验（实测 22.19.0），运行应用不需要它。Git 只在打包机需要，
  解压运行和无 Git 的来源检查不依赖 Git。Verify 在缺少 Node 时会跳过语法步骤，所以应
  显式运行下列 node 检查；缺少时不能说该项通过。
- 真实 BA 另需本机预装 Strata 0.2.1、Terminal 0.1.46.1、其 Python 3.12.15、engine
  0.1.46 CUDA 13、Gyro-S 权重、原保存 profile 和 owner-private runtime。本机驱动
  617.42、RTX 5070 Ti Laptop 显存 12227 MiB、可用物理 RAM 总量 31.42 GiB。
  模型文件合计 86.39 GiB／56 个，故意不放 ZIP。保留已验证的 8192 上下文、单请求、
  vision/MTP off、1536 MiB VRAM reserve。现场不下载、升级或搬移模型。
- 须向教学团队确认预装软件和缓存模型是否允许。尚未验证真正全新电脑、断网环境或
  实际 Canvas 下载；不能把它们当成已经满足的前置条件。

### 打包准确的干净提交

先在已提交、干净的任务分支运行 Windows Verify。提交号和 ZIP SHA-256 单独记录，
ZIP 无法包含自身最终哈希。现有打包器读取工作区源文件，**不是不可变 Git archive**，
因此须检查未追踪文件，并在工作区干净时才能把包对应到准确提交。

```powershell
git status --short
git rev-parse HEAD
# 有未提交／未追踪源码时先停止，保留并核对。
$sourceId = git rev-parse HEAD
$archive = Join-Path $PWD "output/prototype-source-$sourceId.zip"
python scripts/package_source.py --output $archive
if ($LASTEXITCODE -ne 0) { throw 'Source packaging failed' }
Get-FileHash -LiteralPath $archive -Algorithm SHA256
```

同名 ZIP 会被拒绝覆盖；新候选使用新文件名。检查包中不含 .git、.venv、var、数据库、
凭证、模型、旧输出或未脱敏原报告。515bfa5 的实测包准确包含 110 个追踪源文件，
逐文件与源字节一致，保留来源检查所需的公开脱敏 PDF 和文本摘录。

### 现场从全新目录运行

选择不存在的目标和全新数据库；不要用 -Force 覆盖旧解压目录。已实际验证含空格路径。

```powershell
$archive = 'D:\submission\prototype-source.zip'
$fresh = 'D:\submission\fresh source'
if (Test-Path -LiteralPath $fresh) { throw 'Preserve existing directory; choose a new destination' }
Expand-Archive -LiteralPath $archive -DestinationPath $fresh
Set-Location -LiteralPath $fresh
Remove-Item Env:PYTHONPATH,Env:PYTHONHOME,Env:BEAUTY_DB,Env:BEAUTY_PORT -ErrorAction SilentlyContinue
.\scripts\windows.ps1 -Action Setup
.\scripts\windows.ps1 -Action Setup
.\scripts\windows.ps1 -Action Verify
node --check beauty_company/web/app.js
.\.venv\Scripts\python.exe -c "import sys,beauty_company; print(sys.executable); print(beauty_company.__file__)"
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5670 -Database var/mock-demo.sqlite3
```

Python 和模块路径都应在新目录。应用使用包内 HTML/JS/CSS，只向新 var／数据库写入；
不要设置指向旧源码的 PYTHONPATH。打开 5670，Customer 提交 ORD-1001；切到 Founder
发起 BA 交接，再由 Customer 确认提案并请求审核。Founder 查看准确范围；本轮在 Activity
trail 选择 Decision recording failure (no approval) 并 Apply fixture，再填写原因审批。
应出现 recording failed、No applicable committed decision、Recover saved decision。
只停启这个新应用并使用同一数据库；重新登录／刷新后恢复。恢复只提交／送达一次决定，
不能产生业务效果；后续 Customer 再确认才产生一次模拟执行。重复恢复和确认不能重复
决定、效果或扣库存。实际 SQLite 证据见 VERIFICATION.md，不只看成功提示。

### 新应用连接既有模型服务

模型由独立的旧模型工作区管理。先检查保存的 profile／进程；已 ready 就复用，只有确认
它已停止才使用该环境的 StartModel。此游戏本模型环境仍在：
`D:\elec5620_project\elec5620-group6-beauty-company`。

```powershell
$modelWorkspace = 'D:\elec5620_project\elec5620-group6-beauty-company'
& "$modelWorkspace\scripts\windows.ps1" -Action StartModel
$modelIds = (Invoke-RestMethod 'http://127.0.0.1:8080/v1/models' -TimeoutSec 10).data.id
$modelIds
```

不要从新解压目录执行 InstallModel／StartModel，它们会在新目录 var 查找模型。
这是明确保留的模型管理依赖，不是旧代码导入。权重和原私密配置均不复制。新应用目录
可以创建自己独立的忽略配置；CreateNew 确保已有文件不会被覆盖：

```powershell
$chosenModel = 'qwen3.8-flash-next-gyro-gyro-s'
if ($chosenModel -notin $modelIds) { throw 'Expected installed model ID was not reported' }
$configPath = Join-Path $PWD 'var/llm.demo.json'
$json = @{base_url='http://127.0.0.1:8080/v1'; model=$chosenModel;
  timeout_seconds=120; max_tokens=512; api_key_env='BEAUTY_LLM_API_KEY'} | ConvertTo-Json
$stream = [IO.File]::Open($configPath, 'CreateNew', 'Write', 'None')
try { $bytes=[Text.Encoding]::UTF8.GetBytes($json); $stream.Write($bytes,0,$bytes.Length) }
finally { $stream.Dispose() }
.\scripts\windows.ps1 -Action Start -Mode strata -Port 5671 -Database var/live-demo.sqlite3 -LlmConfig var/llm.demo.json
.\scripts\windows.ps1 -Action SmokeTest -Mode strata -Port 5671
```

本机 Strata 不需要密钥；未来密钥只放本地环境变量，不进源码／ZIP／证据摘要。保持
loopback，本流程不授权 LAN／SSH。绝对 -LlmConfig 也支持复用旧配置，但本轮完成的网页
真实推理使用新目录自己新建的配置，故不依赖旧应用配置路径。

应用 /api/health 的 BA LIVE 只证明配置；官方 runtime ready 和 /v1/models 证明模型就绪；
只有实际咨询保存 COMPLETED／simulated:false 并独立核对目录事实，才证明真实推理。
在 5671 登录 Customer、进入 Product advice、提交保湿／60 AUD／无香样例，应出现 Live
BA recommendation、P-101 和支持事实。MC 仍 mock，CS intent 为 NOT_CONNECTED，live
CS coordinate/revise 仍受阻。模型失败必须保存 INCOMPLETE，不能伪装 mock 成功。

### 停止与诊断

```powershell
.\scripts\windows.ps1 -Action Stop -Port 5670
.\scripts\windows.ps1 -Action Stop -Port 5671
```

仅停止当前新目录拥有的进程，保留 var／数据库。不要停止演练前已存在的模型；本轮自己
启动的模型在清理时先核对 instance ID，再用 `runtime stop --profile launch-elec5620-ba
--if-instance-id <observed-id>` 停止，身份变化应保留排查，不能按进程名批量结束。
分别检查新 var/app-PORT-*.err.log、进程凭据、/api/health，以及原模型环境的 runtime／
引擎日志。不要公开会话、配置或数据库。端口占用会拒绝启动，不终止既有进程。
Setup 保留已有配置和 .venv，不完整环境会拒绝处理。Start 会复用自己的应用；要改数据库、
模式或配置时先 Stop。重复演练不能通过删除数据库或覆盖配置来“修好”。

### 本轮、历史与剩余条件

本轮新验证：源码 515bfa537e31a01b9e9a24400a7112f8103babb3 的 ZIP 解压到全新目录、
123 项 Windows 测试、来源／JS 检查、重复 Setup、网页 mock 主线、AP 保存失败／应用重启／
网页恢复、一次性效果和 1 次网页真实 BA。无需修改应用或部署脚本。准确耗时和哈希见
VERIFICATION.md 的 28 日记录。下方 21／25 日安装与 84 项测试是历史；当前源码已有
AP 恢复按钮和 CS 失败状态 UI，旧“尚未实现”说法不代表当前版本。
正式 Canvas 下载／解压复演、最终包冻结、现场软件／模型许可、真实 CS/MC、更广验收、
长期运行和跨电脑仍需分别完成。此演练通过不等于 Stage 2 全部完成。


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
