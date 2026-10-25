# Strata runtime repair and actual BA verification

English primary. [中文阅读副本](zh-CN/WINDOWS_LLM_RUNTIME.md).

21 October 2026, Danny / M1, KAN-15 / GR-INT-02, local branch
`KAN-15-shared-llm-windows`. This record supersedes the installation-blocked and
real-BA-success-pending statements in the earlier Windows handoff. It does not
complete GR-INT-02, a starter task, a module or full Stage 1 acceptance.

## Observed failure and repair

After the C-to-D migration, `var/strata-runtime` inherited D drive ACL entries
granting Authenticated Users modification and Users read/execute. Strata's actual
Windows `is_unshared` check rejected that existing directory with “runtime
directory must be owner-only (mode 0700)”. This was a migration permission defect,
not a missing model or a reason to relax the check. The model preparation and
engine download had already completed.

The original ACL was backed up under ignored `var/verification/`. The installed
official `private_files.restrict_to_current_user` function tightened only that
runtime directory, and Strata's own `runtime_dir`/`is_unshared` checks passed.
No downloaded file, local database or safety check was removed. This repair
requires normal user access to that directory; the Codex restricted process
cannot read an owner-only directory, so the verified repair/start used the
authorised ordinary-user execution path outside that sandbox.

`scripts/strata_runtime.py` now performs this bounded check/repair before model
actions. It rejects a linked/redirected runtime directory and backs up an ACL
before changing it. A failed launch had created a saved profile, but no launch
preset. `StartModel`/`StopModel` now use that actual saved runtime profile
(`launch-elec5620-ba`); `InstallModel` detects it instead of the incorrect
`strata-gyro-s.json` filename and resumes without downloading or rewriting settings.

The existing generated launch config in LOCALAPPDATA was preserved and adopted
under ignored `var/strata-launch/elec5620-ba.json`; its profile points there and its
log stays on D. The previous config/profile were backed up privately. Existing
project-local choices remain unchanged on repeat repair. An active profile's
source is not relocated until it has stopped.

## Actual model and machine observations

- Strata Terminal 0.1.46.1 / app release v0.2.1; engine 0.1.46 CUDA 13, build
  commit `a7bdbfdabc9a`, architectures 75/86/89/120. The normal component launch
  verifies its package/file integrity.
- Exact API model ID: `qwen3.8-flash-next-gyro-gyro-s`.
- Gyro-S GGUF present at 58,487,015,808 bytes. The prepared model directory's
  summed file sizes are 92,758,073,216 bytes (86.39 GiB), including packs and
  upstream-fetched MTP helpers despite MTP inference being disabled. Engine
  components total about 0.83 GiB. These are file-size sums, not an allocated-block
  disk measurement; the original ~59 GB transfer estimate did not cover all helpers.
- Saved context 8192, one request, loopback only, vision absent/OFF, `mtp:false`.
  Upstream suffix drafting remains active; disabling MTP does not disable that.
- The first start warned of 224 MiB free VRAM. A backed-up local config edit added
  `--vram-reserve-mib 1536`. The next start logged 1150 MiB free with everything
  loaded; the BA request logged about 1064 MiB while capturing another window.
  One nvidia-smi sample reported 1895 MiB free. These are observations at different
  stages, not a guaranteed memory margin for gaming or concurrent applications.
- Upstream's default `STRATA_ROUTE_TAIL_SKIP=7` is active, as explicitly logged;
  it can change answers slightly. No full-model equivalence or general business
  reasoning quality is claimed for this quantized/runtime configuration.

## Executed checks

- Official model runtime start reported config/launch identity verified and
  generation checked, with `/v1/models` returning the exact model ID above.
- The app config's placeholder model ID was replaced with that observed ID;
  other local fields were preserved and the original config was backed up privately.
- Actual login → `POST /api/consultations` → shared HTTP adapter → local model →
  independent catalogue/fact checks → saved record passed, in isolated
  `var/real-model-acceptance.sqlite3` on app port 5623.
- First real BA probe: 6.804 s including login/HTTP/persistence,
  COMPLETED, `simulated:false`, P-101, literal facts “Moisturises dry skin” and
  “Fragrance-free”, catalogue:P-101:v1. The engine logged 287 prompt tokens read
  in 5685 ms and 25 generated tokens in 1000 ms. This is one short request, not a
  representative throughput benchmark. The second actual BA probe also passed.
- That database contained zero commerce effects and zero approval requests.
- Repeat RepairModel preserved the byte hashes of launch config, profile and
  application config. Repeated StartModel and InstallModel preserved the same
  engine PID, without a new download, second runtime or configuration overwrite.
- Model StopModel followed by StartModel succeeded during VRAM configuration;
  no blind process-wide Python termination was used.
- All 45 offline tests passed after the repair, plus repository/source checks,
  JavaScript syntax and `git diff --check`. The offline suite still requires no
  model. Local checks are not a GitHub CI run or teammate approval.

Timestamped actual probe JSON and ACL/config backups are ignored local evidence
in `var/verification/`; no cookies, tokens, keys, databases or weights enter Git.
This is structured catalogue selection over explicit needs, not the full BA
natural-language clarification/revision/cancellation lifecycle. MC remains mock;
CS intent and live HTTP CS handoffs remain unconnected/blocked pending coordination.

## Commands from the D drive repository

```powershell
Set-Location 'D:\elec5620_project\elec5620-group6-beauty-company'
.\scripts\windows.ps1 -Action RepairModel  # optional diagnostic repair; no download
.\scripts\windows.ps1 -Action StartModel   # reuses an already-ready runtime
.\scripts\windows.ps1 -Action Start -Port 5623 -Mode strata -Database var/real-model-acceptance.sqlite3
.\scripts\windows.ps1 -Action SmokeTest -Port 5623 -Mode strata
# App: http://127.0.0.1:5623; model API/chat: http://127.0.0.1:8080
.\scripts\windows.ps1 -Action Stop -Port 5623
.\scripts\windows.ps1 -Action StopModel
```

Once the model is installed, use StartModel for normal starts. InstallModel also
reuses the installed saved profile. If a runtime is still starting/failed, the
script reports that state instead of starting another process or overwriting it.
Keep model/runtime paths private; do not expose ports beyond loopback.

Jira update pending — KAN-15: verify current claim/status first, then record the
runtime ACL fix, installed versions and actual BA acceptance above. MC/CS and
broader acceptance remain open. No Jira update, commit, push, PR, merge or
affected-owner approval was performed by this repair.

## Local review before the BA phase commit · 21 October 2026

Reviewed the KAN-15 diff against fetched origin/main e51dfc4; no newer main or
teammate implementation was incorporated. Two new regression tests first failed:
a truncated chunked model response escaped as HTTP 500, and HTTPError response
streams were not closed. Both are fixed: protocol exceptions save safe
INCOMPLETE/LLM_INVALID_OUTPUT, and rejected response streams are closed without
exposing provider bodies. External-directory Windows Setup also reproduced an
incorrect configuration path; it now resolves relative LlmConfig against the repo
and verifies the environment executable before reporting ready. Running that
Setup twice from work/ created only var/setup-path-review.json and preserved its
hash. All 47 tests passed on local Python 3.14.5 and 3.12.15, with repository and
JS checks. These are local checks; remote CI, affected-owner approval and Jira
claim/status remain unverified. The diff is prepared for a local phase commit
and a PR-description draft; no publication or merge is implied.

## Windows post-CS/AP regression · 25 October 2026

The exact integrated application commit 966dae4fd1c8afcaeb60b8af84289ae5b6edaa60
(main 840ac7004723c62995a427191eda4f0cd4151917) was rerun on this laptop. Existing
Strata/model/configuration were reused without installation or download. All 84
Windows tests passed on Python 3.14.5 and 3.12.15, plus provenance/JS checks.
Actual browser login and BA inference saved COMPLETED/simulated:false/P-101 with
independently checked catalogue facts and a Live BA recommendation label. The
unused-model-endpoint browser probe saved INCOMPLETE/LLM_TIMEOUT; a longer-budget
connection-refusal service probe saved LLM_UNAVAILABLE. Neither fell back to mock.

Fresh CS/AP HTTP and restarted AP-service recovery checks passed. MC remained
mock and CS intent unconnected; live CS coordinate/revise stayed blocked. AP web
recovery remains absent: the failure page's superseded fallback sentence is also
misleading, despite correct failed/no-authority state. The local Windows stop
script now safely refuses unreadable PID metadata; negative and owned-positive
stop checks passed. No test listeners remain, and original config/database hashes
and all 56 model-file size/mtime entries are unchanged. No remote publication or
Jira write occurred during the regression run. Full evidence, local patch scope and limitations are in the
25 October Windows checkpoint in [VERIFICATION.md](VERIFICATION.md).

## Local model stability and restart · 25 October 2026

At exact application commit dbb6662, a 319.467 s single-request local run passed:
20 continuous BA calls, 180 s idle plus three calls, a safely saved unavailable
result with the model stopped, and three calls after restarting the same saved
profile. All 26 positive results were COMPLETED/simulated:false and independently
validated; the stopped-provider result was INCOMPLETE/LLM_UNAVAILABLE, with no
fallback. The 84 offline tests passed while the provider was stopped. Repeat
StartModel reused its instance; restart readiness was 20.017 s. Both test attempts
were cleaned up and original data/config/model inventory preserved.

Free VRAM was 1957–2023 MiB while loaded, but system RAM reached only 2.35 GiB
available. Keep the validated single-request configuration. This is a short fixture
run, not overnight, sleep/reboot, multi-user, full-context or remote acceptance.
An initial controller pipe-wait issue was fixed outside application code and its
zero-call attempt excluded. See the same-date stability checkpoint in
[VERIFICATION.md](VERIFICATION.md). Danny subsequently authorised publication
of these bilingual evidence records to PR #8; the stability run itself made
no remote write. No Jira update, merge or review bypass is included.
