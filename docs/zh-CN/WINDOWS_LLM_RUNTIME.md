# Strata 运行目录修复与真实 BA 验证

中文阅读副本；维护依据为[英文主版](../WINDOWS_LLM_RUNTIME.md)。2026-10-21，Danny / M1，
KAN-15 / GR-INT-02，本地分支 `KAN-15-shared-llm-windows`。
此记录取代此前 Windows 交接中“安装受阻／真实 BA 成功未验证”的当前状态，不等于完成
GR-INT-02、首批任务、整个模块或完整 Stage 1 验收。

## 原因与修复

C 盘迁移至 D 盘后，`var/strata-runtime` 继承了 D 盘的 Authenticated Users 修改权限和
Users 读取／执行权限。Strata 的 Windows `is_unshared` 检查拒绝该已有目录，报
“runtime directory must be owner-only (mode 0700)”。这是迁移权限处理遗漏，并非模型缺失，
不应取消安全检查。此时模型准备和引擎下载已经完成。

原 ACL 已备份到忽略的 `var/verification/`。使用已安装官方
`private_files.restrict_to_current_user` 仅收紧 runtime 目录，并通过官方
`runtime_dir`／`is_unshared` 检查。没有删除下载、数据库或安全检查。
修复和启动通过获准的普通用户执行路径进行；Codex 受限进程本身不能读取仅当前用户可见的目录。

新增 `scripts/strata_runtime.py`，模型操作前自动做窄范围权限检查／修复：拒绝链接或重定向目录，
修改前备份 ACL。此前失败的 launch 已创建 profile，却没有保存 launch preset；
StartModel／StopModel 改为使用实际 profile `launch-elec5620-ba`，InstallModel 也按该 profile
恢复，而不再错误判断 `strata-gyro-s.json`。不会重下载或覆盖原模型选择。

原来生成在 LOCALAPPDATA 的启动配置保留原件，并转入忽略的
`var/strata-launch/elec5620-ba.json`，profile 指向新位置，日志也留在 D 盘。
原配置／profile 已私密备份。重复修复不改已有项目本地配置；运行中的 profile 等停止后才迁移来源。

## 实际配置与硬件观察

- Terminal 0.1.46.1／发布 v0.2.1；engine 0.1.46 CUDA 13，build commit
  `a7bdbfdabc9a`，支持架构 75/86/89/120；正常组件启动会验证包及文件完整性。
- 实际 API 模型 ID：`qwen3.8-flash-next-gyro-gyro-s`。
- Gyro-S 权重 58,487,015,808 字节；含 pack 和辅助文件的模型目录总文件大小
  92,758,073,216 字节，即 86.39 GiB；引擎组件约 0.83 GiB。
  即便 MTP 推理关闭，上游仍下载了 MTP 辅助文件。以上是文件大小之和，不是实际分配磁盘块测量；
  最初约 59 GB 的传输估计未覆盖所有辅助文件。
- 上下文 8192、单并发、仅本机、无图像、`mtp:false`；上游 suffix drafting 仍启用，
  关闭 MTP 不等于关闭所有推测解码。
- 首次启动日志只剩 224 MiB 显存。备份配置后增加 `--vram-reserve-mib 1536`；
  重启完成加载时日志空闲 1150 MiB，BA 请求图捕获阶段约 1064 MiB；另一次 nvidia-smi
  采样空闲 1895 MiB。这些是不同阶段的观察，不保证游戏／并发应用时仍有相同余量。
- 上游默认 `STRATA_ROUTE_TAIL_SKIP=7` 生效，日志明确说明可能稍微改变答案；
  不声称量化／运行时与完整模型完全等价，也不据此保证通用业务推理质量。

## 实际验证

- 官方 runtime 报告配置／启动身份核实和生成探针通过；`/v1/models` 返回上述精确 ID。
- 应用本地配置只将 model 占位值改成实际 ID；其他字段保留，原配置已私密备份。
- 独立数据库 `var/real-model-acceptance.sqlite3`、应用端口 5623：实际登录 →
  `POST /api/consultations` → 共享 HTTP adapter → 本地模型 → 独立商品／事实验证 → 保存记录通过。
- 首次真实 BA 完整探针 6.804 秒（含登录、HTTP、保存），状态 COMPLETED，`simulated:false`，
  商品 P-101，事实为 “Moisturises dry skin” 和 “Fragrance-free”，证据 catalogue:P-101:v1。
  引擎日志：287 输入 token 用 5685 ms，25 生成 token 用 1000 ms；这是单条短请求，
  不代表通常吞吐基准。第二次真实 BA 探针也通过。
- 验证数据库商业效果为 0，审批请求为 0。
- 重复 RepairModel 后，启动配置、profile 和应用配置字节哈希不变；重复 StartModel／InstallModel
  保持同一引擎 PID，不重下载、不重复启动、不覆盖配置。
- 调整显存期间，StopModel 后 StartModel 成功；没有批量结束 Python 进程。
- 修复后 45 项离线测试、来源检查、JS 语法和 `git diff --check` 通过。
  离线测试仍不需要模型；这些是本地检查，不是 GitHub CI 或队友批准。

带时间的实际探针 JSON 和权限／配置备份都在忽略的 `var/verification/`；
cookie、token、key、数据库和权重不进入 Git。本次是明确约束下的结构化商品选择，
不等于完整自然语言澄清／修改／取消生命周期。MC 仍 mock；CS intent／live HTTP CS 转交仍待协调。

## D 盘仓库中的操作

```powershell
Set-Location 'D:\elec5620_project\elec5620-group6-beauty-company'
.\scripts\windows.ps1 -Action RepairModel  # 可选，仅修复／检查，不下载
.\scripts\windows.ps1 -Action StartModel
.\scripts\windows.ps1 -Action Start -Port 5623 -Mode strata -Database var/real-model-acceptance.sqlite3
.\scripts\windows.ps1 -Action SmokeTest -Port 5623 -Mode strata
# 项目：http://127.0.0.1:5623；模型 API／聊天：http://127.0.0.1:8080
.\scripts\windows.ps1 -Action Stop -Port 5623
.\scripts\windows.ps1 -Action StopModel
```

安装后通常使用 StartModel；InstallModel 也会复用已有 profile。
如果模型仍在启动或失败，脚本报告状态，不擅自创建第二个进程或覆盖它。
服务只监听本机，不配置外网访问。

**Jira update pending — KAN-15**：先核实当前认领／状态，再记录 runtime 权限修复、
安装版本和以上真实 BA 证据；MC／CS 和更广验收继续保留缺口。
本次没有 Jira 写入、commit、push、PR、合并或已确认的受影响负责人批准。

## BA 阶段提交前本地审查 · 2026-10-21

已对照 fetch 后 origin/main e51dfc4 审查 KAN-15 差异，没有引入更新 main 或队友实现。
两个新增回归先复现失败：chunked 模型响应截断会变成 HTTP 500，HTTPError 响应流未关闭。
现已分别修复为安全保存 INCOMPLETE/LLM_INVALID_OUTPUT 和及时关闭响应，不暴露供应商原文。
还复现仓库外调用 Windows Setup 时配置路径解析错误，已改为相对仓库根解析 LlmConfig，
并在报告就绪前检查环境解释器。由 work/ 连跑两次，只生成 var/setup-path-review.json，哈希不变。
本地 Python 3.14.5 和 3.12.15 各通过 47 项测试，来源／JS 检查通过。
这是本地验证；远程 CI、受影响负责人批准和 Jira 认领／状态仍未核实。
差异准备作本地阶段提交及 PR 描述草稿，不代表发布或合并。

## Windows 合入 CS/AP 后回归 · 2026-10-25

本机重新验证准确应用提交 966dae4fd1c8afcaeb60b8af84289ae5b6edaa60
（main 840ac7004723c62995a427191eda4f0cd4151917）。复用已有 Strata／模型／配置，
没有安装或下载。Python 3.14.5、3.12.15 各通过 84 项 Windows 测试，来源与 JS 检查通过。
实际网页登录并调用 BA，保存 COMPLETED/simulated:false/P-101，独立核对目录事实，
页面显示 Live BA recommendation。空模型端口的网页探针保存 INCOMPLETE/LLM_TIMEOUT；
较长连接预算的实际拒绝连接服务探针保存 LLM_UNAVAILABLE，都没有回退成 mock。

新库 CS/AP HTTP 和 AP 服务重启后恢复通过。MC 仍 mock、CS intent 未连接、真实 CS
coordinate/revise 仍受阻。AP 网页没有恢复功能，失败页误用 superseded 兜底文案，
但失败／无权威状态正确。Windows 停止脚本现安全拒绝无法读取的 PID 元数据，
拒绝不匹配进程与正常停止本轮进程均已验证。最终测试端口无监听，原配置／数据库哈希和
56 个模型文件大小／修改时间清单保持不变。回归验证本身没有远程发布或 Jira 写入。
完整证据、局部补丁和限制见 [VERIFICATION.md](VERIFICATION.md) 的本日 Windows 记录。
