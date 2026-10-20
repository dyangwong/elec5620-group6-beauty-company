# Windows deployment and KAN-15 handoff

Current update: the local model and one actual BA HTTP path now pass after runtime
ACL repair. See [current runtime evidence and recovery commands](WINDOWS_LLM_RUNTIME.md).
The installation-blocked sections below retain the earlier attempt as history.

English primary. [中文阅读副本](zh-CN/WINDOWS_LLM.md).

Client work date: 21 October 2026 (Australia/Sydney). Danyang Wang / Danny / M1,
KAN-15 / GR-INT-02, branch `KAN-15-shared-llm-windows`, baseline `e51dfc4`.
At the initial deployment checkpoint, no commit, push, PR, merge or Jira write
had been performed; later checkpoints are recorded in VERIFICATION.md.
BA-START-01 was not claimed. AI assisted implementation, testing and documentation.

## Observed machine and baseline

| Item | Actual observation |
|---|---|
| OS | Windows 11 Pro, 25H2, build 26200.9711, x64; Python identifies Windows 11. The registry's legacy ProductName says Windows 10 Pro. |
| CPU | Intel Core Ultra 9 275HX, 24 physical cores / 24 logical processors confirmed through Windows GetLogicalProcessorInformationEx; AVX2 available. CIM is unavailable in this execution environment. |
| RAM | 33,737,986,048 usable physical bytes = 31.42 GiB; initially 16.64 GiB available, later about 14.9–15.1 GiB. This is a 32 GB class machine. |
| GPU / driver | NVIDIA GeForce RTX 5070 Ti Laptop GPU; nvidia-smi reports 12,227 MiB total VRAM, driver 617.42. Do not use Win32_VideoController.AdapterRAM's capped value. |
| Disk | Initially C: 415.13 GiB free, D: 298.50 GiB free; readings change during use. Disk interface/SSD model could not be verified through CIM. Model performance on this disk is unmeasured. |
| Tools | Git 2.51.0.windows.1, Python 3.14.5, Node 22.19.0; the `py` launcher lists no registered interpreter, so scripts use `python` or the project's virtual environment. |
| Repo | Fresh clone, clean main at e51dfc4; fetched remote state. Open PR #7 / KAN-11-cs-start-01 is teammate CS work, inspected but not merged or reimplemented. |
| Jira | No connected Jira tool; unauthenticated KAN-15 API read returned 404. This does not establish ticket deletion or workflow state. Live assignee/claim/status remain unverified. |

First baseline run: 38 tests attempted, 70 error reports from denied system temporary
directories (some tests also failed cleanup). Using workspace TEMP/TMP: all 38 passed.
The first provenance check failed on two CRLF-converted excerpts. Restoring their
exact Git blob bytes made it pass; source hashes/PDFs/manifests were not changed.
`.gitattributes` now preserves LF for reference text. The baseline web app started
on Windows, and a real browser signed into the Customer workspace.

## Initial model selection and blocked installation (historical)

Reviewed the upstream [installation guide](https://github.com/Niko1221/Strata/blob/9ae93f7b1fe989d04a8e404d32cddaeeff10505f/docs/INSTALL.md),
[model guide](https://github.com/Niko1221/Strata/blob/9ae93f7b1fe989d04a8e404d32cddaeeff10505f/docs/MODELS.md)
and [v0.2.1 release](https://github.com/Niko1221/Strata/releases/tag/v0.2.1).

The GPU/driver/AVX2 meet the published platform requirements. RAM headroom is the
constraint: full IQ2/IQ3 plus Windows/application memory is tight. Coder removes
half the experts and is explicitly weaker outside coding, so it was not selected
for business advice. The first candidate is the smaller general Gyro-S; its lower
quantization quality still needs application-specific evaluation. No speed estimate
from a desktop GPU is treated as a laptop measurement. More RAM would permit
higher quality full-model quantizations, but no hardware upgrade is required here.

| Component | Selected version / size |
|---|---|
| Strata release | v0.2.1, commit 9ae93f7b1fe989d04a8e404d32cddaeeff10505f |
| Terminal | build 0.1.46.1, 72,126,142-byte Windows x86_64 archive, bundled Python 3.12.15 |
| Terminal SHA-256 | c2d422081eb72c44cf1b23e7f20c506a2fed371e0e614ead48be7045b7798848; downloaded archive matched |
| Engine | 0.1.46 Windows CUDA 13, 579,792,118-byte archive; chosen by the signed feed, not installed |
| Model | agentionai/Qwen3.8-Flash-Next-Gyro-GGUF, revision 1ada08422e404aca51ab9df665f089f34c419c6b |
| Weight file | Qwen3.8-Flash-Next-Gyro-S-TQ1_0.gguf, 58,487,015,808 bytes (~58.49 GB / 54.47 GiB) |
| Weight SHA-256 | c6ea1b08ca312f99095b27588ba35976b53f948268e7f91e7761926aa01d9c87; pinned by upstream setup, not yet downloaded/locally verified |
| Initial configuration | 8,192 tokens, int8 KV, one concurrent request, loopback 8080, pictures OFF, MTP OFF, tuning skipped |
| Download / disk budget | About 59.14 GB including model, engine archive and Terminal; keep up to 6 GB extra if upstream preparation fetches helpers. Reserve 110 GiB free for extraction/preparation/cache/headroom; actual installed model footprint remains unmeasured. |

Upstream lists Gyro-S weight memory at 27.6 GB of RAM+VRAM combined. This does not
guarantee it fits the current **available** memory: GPU cache, KV/scratch, Windows,
browser and other apps also consume memory. Start with other heavy apps closed,
check available memory and nvidia-smi, then measure. No image reader, speculative
drafting, long-context or multi-user performance has been validated on this laptop.
Respect the model's Qwen Community License; do not commit or redistribute weights.

The Terminal executable/version and signed feed check succeeded (sequence 103,
built-in signing key 5d1bc23abbeffd0d). Installing the engine then failed with
WinError 5 after Strata created private state directories. Its Windows code sets
owner/DACL rules incompatible with this session's restricted process. A request
to execute outside that sandbox was rejected by the session's approval policy.
No upstream permission check/signature protection was removed. The official
installer must be retried in the user's ordinary PowerShell session. This is not
evidence that an ordinary Windows installation will fail.

## Reproducible commands

Run these from the repository root in a normal PowerShell window. No administrator
rights, execution-policy change, driver installation or system-wide Python update
is part of this setup. If Windows blocks a script, inspect it and use an approved
local policy; do not disable system security protections.

```powershell
.\scripts\windows.ps1 -Action Setup
.\scripts\windows.ps1 -Action Verify
.\scripts\windows.ps1 -Action Start
# Open http://127.0.0.1:5620
.\scripts\windows.ps1 -Action SmokeTest -Mode mock
.\scripts\windows.ps1 -Action Stop
.\scripts\windows.ps1 -Action Diagnose
```

Setup creates `.venv` only if absent; there are no app dependencies to install.
It copies `config/llm.strata.example.json` to `var/llm.strata.json` only if absent.
It never pulls/resets/stashes code or resets a database. Start creates a new database
only at the selected path; existing data is retained. Repeat starts preserve the
existing process/configuration. Stop verifies both PID creation time and executable
before terminating only that script's process; it never kills every Python process.
Logs have unique names under `var/` and stop does not delete data.

For a separate test workspace, use `-Port 5621 -Database var/my-check.sqlite3`.
Use the same `-Port` for Stop/SmokeTest. Within Codex's restricted shell, detached
children may be cleaned up after the command returns; keep a foreground session
instead: `.\.venv\Scripts\python.exe -m beauty_company --port 5621 --db var/my-check.sqlite3`.
Ctrl+C stops this foreground process.

Model setup is separate and downloads the large file specified above:

```powershell
.\scripts\windows.ps1 -Action InstallModel
# Installer starts the local model and prints /v1/models IDs.
# Edit only var/llm.strata.json: replace model with the EXACT returned ID.
.\scripts\windows.ps1 -Action Start -Mode strata -Database var/live-demo.sqlite3
.\scripts\windows.ps1 -Action SmokeTest -Mode strata
.\scripts\windows.ps1 -Action Stop
.\scripts\windows.ps1 -Action StopModel
# Later:
.\scripts\windows.ps1 -Action StartModel
```

Weights, runtime/configuration, process receipts, profiles and logs stay under
ignored `var/`. The script pins the Terminal archive hash and a signed versioned
engine feed. Re-running InstallModel keeps an existing run configuration; it does
not silently regenerate it. Interrupted downloads are resumed by upstream setup
before the final run configuration exists. If an existing config has missing files,
inspect `doctor` and the upstream repair instructions, preserving local settings.
Never copy settings/secrets into tracked examples. Optional authentication uses
the named process environment variable; do not put keys in command arguments,
diagnostic exports or screenshots. No network/LAN/firewall setup is included.

## Current adapter and acceptance

The v1 calls `propose(context, evidence)` / `generate_script(brief, evidence)` and
`Company(path, llm=None)` remain compatible. Only `propose` is connected to Strata;
MC intentionally remains mock and reports it. CS intent has no new port. Live-mode
HTTP CS coordinate/revise operations explicitly reject with
`LIVE_HANDOFF_NOT_CONNECTED` pending CS/CO owner coordination; use mock mode for
the existing integrated exchange demo. Direct internal BA/CS calls are not a
validated live service API. AP/CO authority and all commerce/media stay simulated.

`POST /api/consultations` uses `Company.consult`: validate structured needs, call
the model outside a write transaction, then compare the selected current catalogue
record before saving. Changes to stock, facts, price or version withhold the result.
This is a new standalone consultation, not a revision/cancellation implementation.

The shared adapter sends only permitted needs and candidate facts/prices/versions,
disables proxies/redirects, uses a configurable socket timeout, output token and
response-byte budgets, and requires one complete JSON answer. It rejects duplicate
keys, non-finite values, extra fields, unknown products, unsupported facts, wrong
model IDs and truncated generation. The BA module independently checks candidate
and literal facts again. Provider failures persist safe INCOMPLETE results with
`LLM_TIMEOUT`, `LLM_UNAVAILABLE`, `LLM_HTTP` or `LLM_INVALID_OUTPUT`; stale catalogue
evidence uses `LLM_STALE_EVIDENCE`. No failure calls MockLlm. No raw provider bodies,
keys or cookies enter user errors. These are integration choices, not course limits.

Health/UI describe configured BA/MC/CS-intent/media/commerce capabilities; health
`status: ok` means app availability, not model readiness. Only a successful actual
BA record with `simulated: false` supports a live BA success claim. Historical
mock recommendations keep their own label even in a live-configured workspace.

Executed here:

- Original 38 tests passed after Windows environment repairs.
- Expanded 45-test offline suite passed on Python 3.14.5 and 3.12.15; transport fixtures are
  local scripted HTTP tests, **not real model inference**. See final verification
  record for additional interpreter checks.
- Repository/provenance checks and JavaScript syntax passed.
- Windows Setup, Start, SmokeTest mock, repeated Start and Stop executed. The
  repeated start did not create the alternate database; existing config was kept.
- Actual HTTP probe through a live-configured app without a model returned
  INCOMPLETE / LLM_TIMEOUT after about 2.1 s; the probe exited 1. No mock result,
  commerce effect or live success was recorded. An earlier probe also correctly
  failed when its app process had already been cleaned up by the restricted shell.
- **Successful real model BA inference remains unverified**, as do all live MC,
  CS intent, multi-computer network and full Stage 1/UML acceptance conditions.

`scripts/smoke_llm.py` writes timestamped evidence under ignored `var/verification/`
and exits nonzero on app/provider/schema/business failure. It uses fictional local
credentials and fixture needs. Only sanitised summaries belong in public docs.
Raw machine timestamps were 20 October UTC while the client work date was 21 October;
they are retained as observed and are not Jira workflow dates.

## Next-computer and review handoff

This branch currently has **uncommitted** changes, so another machine cannot fetch
them yet. Danny should review the listed diff, commit and push this task branch
when authorised, then clone/fetch that exact branch on the other PC. Do not edit
the same branch concurrently. Run Setup/Verify and choose that PC's own memory
configuration. Models, `.venv`, keys, databases and profiles are not Git transfers.

Affected shared surfaces: adapter/config, CLI, facade, HTTP BA route and narrow
CS live-mode guard, BA mode/error mapping, web mode labels, Windows tooling/docs.
No CS/MC/AP/CO implementation file or starter claim was changed. Review the HTTP
guard/error mapping with CS/CO, and future MC/CS live seams with their owners before
expanding the live scope. No affected-owner approval has been observed.

Jira update pending — KAN-15: first verify current assignee/claim/status; if still
appropriate, record In Progress with: “Danny implemented the local shared BA
adapter and Windows tooling on KAN-15-shared-llm-windows from e51dfc4. Offline checks
pass; actual local HTTP model-unavailable path safely records INCOMPLETE. Strata
engine/model installation is blocked in the restricted execution session; successful
real BA inference remains pending. MC stays mock, CS intent unconnected, BA starter
unchanged. Next: install in ordinary PowerShell, run actual BA smoke, then review
shared changes.” Do not mark Verification/Done or a parent epic complete merely
because local tests pass. Add a PR link only after one actually exists.

## Calling Windows Setup from another directory

The script now resolves a relative -LlmConfig against the repository root, even
when invoked by an absolute script path from another folder. Existing local
configuration remains untouched. See the latest 47-test review checkpoint in
VERIFICATION.md; the 38/45-test sections above are earlier observations.
