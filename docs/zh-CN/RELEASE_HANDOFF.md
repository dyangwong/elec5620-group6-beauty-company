# 通过 GitHub 续接游戏本交付验收

中文阅读副本，依据 2026-10-30 [英文主版](../RELEASE_HANDOFF.md)同步。

Danny / Danyang Wang / M1 已授权这次 AI 辅助的仓库维护，关联 KAN-9／内部
GR-INT-03（不是新 Jira key）。PR #18／1ad1101最初只增加交接文档；随后Danny授权
当前STATUS／VERIFICATION记录的有界广告模板打磨：原创随包素材、渲染器、两项保护测试、
配套双语指南与MC追溯，不改模型／provider或归属。
下轮Windows验收应使用已合入该增量的main；若仍只在本地／未合并，应明确缺少发布，不能把旧main当新版本验收。

## 基线与已有证据

较早应用基线为已合并 PR #16：`7c862341fe914b33b7dadcd56784288b50fb0436`。
**本轮不合并 PR #17**，它是另行评估的队友 PR。

Mac 的原 RC1 源码 ZIP 固定在该提交，共 124 文件，SHA-256 为
`7f954baab3ab90872f9b648deca0587cf2716bc032491d7d4ef0dac0d1c78369`。
全新解压／新 venv 通过 281 项测试（33.485 秒）、来源和 JS 检查。
实际 mock 网页演练完成换货、AP 保存失败、应用重启、同意图恢复及最终客户确认；
确认前 0 次效果，确认后 1 次，P-101 库存 12→11。该 Mac 轮未调用真实模型或渲染视频。
STATUS／VERIFICATION 的旧 Windows 结果各自对应当时版本；当前候选的统一 Windows 验收仍待做。

保留原 RC1 与本地收据；它们在被忽略的输出目录，不会随 GitHub 自动同步。
**这条路线无需复制那个交接包。** 通过 GitHub 取指南，在 Windows 生成新源码候选包，
记录其完整提交、文件数与 ZIP 哈希。文档和广告模板增量改变源码字节，因此新包不要仍叫 RC1、
期待旧哈希，或把旧包测试结果直接填成新包 PASS。

## 保留旧工作区，在新目录取源码

先检查旧仓库分支／未提交内容、应用进程、模型及工具。保留现状，不 reset、clean、
盲目 stash，不为同步而合并／rebase 已经 squash 合并过的旧 KAN-15 分支。

将公开仓库克隆到**不存在的相邻新目录**，旧目录继续拥有已安装模型与工具。
逐条检查命令是否成功；以下路径只是例子，已存在就换一个新名字：

```powershell
git clone https://github.com/dyangwong/elec5620-group6-beauty-company.git D:\elec5620_project\elec5620-release-next
Set-Location D:\elec5620_project\elec5620-release-next
git fetch origin main
git switch -c KAN-9-windows-release-rehearsal origin/main
git rev-parse HEAD
git status --short --branch
git diff --name-only 7c862341fe914b33b7dadcd56784288b50fb0436 HEAD
```

相对7c86234，预期包括PR #18的六个文档路径及当前广告模板增量：template_video.py、
assets/advert、test_mc.py、双语接口／模块／状态／验证／共享范围／交接指南及指定MC追溯。
核对真实diff和已合并PR收据，不静默带入其他PR或覆盖旧工作。
本增量不含BA／CS／AP／CO业务、HTTP／UI、provider、依赖或schema变更。
固定记录新 checkout 的**完整 HEAD**，不能只写会移动的 main。
读 AGENTS、本指南、STATUS／VERIFICATION 最新检查点及 Windows 指南；旧记录不是新验收证据。

## 先打包，再从解压目录运行

在干净、已提交的新 checkout 中，用已安装 Python 3.9+：

```powershell
python scripts/package_source.py --output output/elec5620-source-rc2.zip
Get-FileHash output/elec5620-source-rc2.zip -Algorithm SHA256
```

文件名已占用就换名，不能覆盖旧候选。核对 ZIP 路径集合等于 `git ls-files`，每项字节等于
干净 checkout 的对应文件，并且不含运行／私有文件。私有收据记录每文件大小／SHA-256、
完整源码提交及 ZIP SHA-256。Windows 换行差异会进入实际字节；之后始终保留同一个 ZIP。
若仅含所述增量，跟踪文件为133个；以实际检查为准，不能硬填通过。
模型、工具、字体、配置、会话、数据库、生成媒体都不能打入源码包。

解压到另一个**不存在的新目录**，建议路径带空格；逐文件核对解压内容与 ZIP。
不复制旧 venv、整个 var、数据库或应用代码。检查 PYTHONPATH／PYTHONHOME 无导入重定向，
如需临时清除，保留原值。进入新解压目录：

```powershell
.\scripts\windows.ps1 -Action Setup
.\.venv\Scripts\python.exe -c "import sys, beauty_company; print(sys.executable); print(sys.prefix); print(beauty_company.__file__)"
.\scripts\windows.ps1 -Action Verify
node --check beauty_company/web/app.js
```

解释器、venv、模块路径都应在新解压目录。预期283项（281基线＋两项渲染保护），仍排除#17。
Verify 包括来源检查，但 Node 缺失会跳过 JS，因此单独记录 JS 实际结果；使用已安装 Node，
不能把跳过写成通过。

## 复用模型与媒体工具

检查旧模型实际归属路径；之前是 `D:\elec5620_project\elec5620-group6-beauty-company`。
复用 ready 的 Strata 服务、已保存模型／profile、FFmpeg／ffprobe／字体。
如模型停止，从其原工作区使用已有的受保护 StartModel，不能在新解压目录 InstallModel。
不下载、升级、搬迁权重；缺少前置条件就报告阻塞。旧 profile 详见 WINDOWS_LLM_RUNTIME.md。

在新解压目录被忽略的 var 中**排他新建**私有配置，参照实际检查的旧值，不覆盖、不公开密钥。
从运行中的本机 `/v1/models` 核实精确模型 ID，复用已准备参数。
LLM 字段是 `base_url`、`model`、`timeout_seconds`、`max_tokens`、`api_key_env`；
之前为 `http://127.0.0.1:8080/v1`、120 秒、512 输出 token，密钥只在指定环境变量。
媒体字段为绝对路径 `ffmpeg`、`ffprobe`、`font`，相对配置文件目录的 `output_dir`，及 `timeout_seconds`。
Setup 会生成示例 `var/llm.strata.json`，真实配置另取新文件名。
配置示例见 WINDOWS_LLM.md，路径须核实，不能猜测。

选择空闲端口、新 DB／配置名。实际创建 `var/rc2-llm.json` 与 `var/rc2-media.json` 后，
在解压目录例如运行：

```powershell
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5780 -Database var/rc2-mock.sqlite3
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5781 -Database var/rc2-live.sqlite3 -LlmConfig var/rc2-llm.json -VideoConfig var/rc2-media.json
```

真实验收须在**同一份启用 BA／CS／MC 文本及模板视频的配置**下完成。
MC 是独立营销路径，不硬塞进换货链。看实际推理／渲染，不能只看 health。
跨端口／角色重新登录，或分开浏览器 profile，本机端口共用 cookie 名。
只在本轮全新虚构 DB 中执行必要审批／模拟确认，不动原 DB。

## 新候选待验清单

每项记录实际日期、源码／ZIP 哈希、环境／模型／工具版本、模式、记录／版本 ID，
保存独立读库／文件证据。初始都未验证，如实填 PASS／FAIL／NOT RUN；281 测试不代表 41 组全验收。

| 检查 | 必须观察到 |
|---|---|
| 源码／启动 | ZIP与解压字节一致，新venv／导入路径，283项测试、来源及JS，随包PNG素材齐全。 |
| Mock BA | 缺预算／香味要求会澄清，同 ID 继续；客户明确确认后才产生有依据建议。 |
| 真实 CS／CO／BA | 归属 ORD-1001 的自然换货 → Founder 发起交接 → 有依据 BA → 客户确认方案 → Founder 精确 AP → 客户最终确认。 |
| 效果边界 | 独立核实当前证据／政策／actionRef；最终确认前 0 效果、后 1 效果，重复仍 1；P-101 库存 12→11。 |
| 真实 MC／媒体 | P-101 有活力 brief 仅用目录事实“50 ml”；真实有界文本、实际可播放／下载 15 秒 MP4、哈希绑定当前版本审批。静音 FFmpeg 模板，无 AI 场景／音频／发布。 |
| BA 条件审批 | AUD10 无匹配 → 客户明确同意 → 精确 AP；REJECT／REQUEST_REVISION 不造成功，APPROVE 后仍需客户重新确认／新推理／当前证据，无交易效果。 |
| MC 保存恢复 | 最终保存失败 → 已持久化未提交生成结果 → 同 DB／配置重启 → 同版本／文本／媒体恢复，不再次推理或渲染，只一个待审。 |
| 模型失败 | 模型／端点不可用时真实保留 live INCOMPLETE／FAILED，无 mock 假成功。 |
| Canvas／现场 | 另经授权上传、实际下载同 ZIP／哈希、全新部署，确认允许的预装软件／模型／工具与现场条件。本指南没有完成这些。 |
| 评估材料 | 讲清三个角色、技术／限制，保留真实 Jira／PR／迭代记录，贡献表由人确认，不虚构比例或认可。 |

换货例句：`Please exchange my item for a fragrance-free moisturiser for dry skin. My budget is AUD 60.`
MC 例句：`Create an energetic teaser highlighting the catalogue fact “50 ml”.`
它们只是测试例子，不代表通用语义理解保证。

只凭本轮归属收据停止本轮应用。原本运行的共享模型保留；只有本轮启动且 instance ID
仍匹配，才用官方保护命令停止。否则在独立失败配置使用已确认空闲的本机端点，
准确标为“端点不可用”，不能说实际关闭模型。不改 LAN、防火墙、SSH 或公开部署。

原始 DB／配置／cookie／日志保留私有；在忽略的 output 生成简短英文收据及中文副本，
列 PASS／FAIL／NOT RUN、剩余条件，并在结束后重新核对源码与 ZIP 哈希。
若必须修源码，保留当前候选，独立任务分支／PR 修复，再生成新包完整重验；
不能改了解压代码却声称原 ZIP 通过。本轮不扩功能、不合 #17；仅按保护规则 PR／检查
发布安全证据，自己的 PR 例外不等于人类 Approve。

已授权 Jira 可用时，只在 KAN-9 补一条简短版本／实际结果／证据链接／下一缺口；
否则明确 **Jira update pending**。不把 epic／KAN-15 标 Done，不改分工，不虚构贡献。
Canvas 上传仍是单独的人类动作／明确授权。

## 可直接交给游戏本 Agent 的指令

```text
我是 Danyang Wang（Danny / M1），继续 ELEC5620 Stage 2 交付验收，关联 KAN-9／内部 GR-INT-03。
先保留游戏本旧工作区的未提交内容、分支、模型、工具、配置、数据库和进程。
fetch GitHub main 后读取 docs/RELEASE_HANDOFF.md；可用
git show origin/main:docs/RELEASE_HANDOFF.md 在不切换旧分支的情况下阅读。
按指南从全新 clone → 新 ZIP → 新解压目录开始，不合 PR #17、不加业务功能。
记录实际完整源码 SHA 和新 ZIP 哈希，RC1 只作历史证据。
复用已有模型／媒体工具，完成清单中的统一 mock／真实模型／恢复验收，保存如实的中英文收据。
只操作本轮虚构新数据、只停止本轮归属进程。Jira 有授权访问时简短记一条，否则明确待更新。
不自动上传 Canvas。
```
