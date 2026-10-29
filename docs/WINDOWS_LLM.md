# Windows deployment and KAN-15 handoff

Current update: the local model and one actual BA HTTP path now pass after runtime
ACL repair. See [current runtime evidence and recovery commands](WINDOWS_LLM_RUNTIME.md).
The installation-blocked sections below retain the earlier attempt as history.

English primary. [中文阅读副本](zh-CN/WINDOWS_LLM.md).

## BA conditional review checkpoint · 30 October 2026

Use a new synthetic database and a free loopback port; preserve existing demo data.
Start default mock with `scripts/windows.ps1 -Action Start -Mode mock -Port 5770 -Database var/ba-review-demo-new.sqlite3`.
Customer → Product advice: `A moisturiser for dry skin. Budget AUD 10. Fragrance-free required.`
Confirm needs, observe INCOMPLETE/no match, expand **Ask Founder to review an unresolved
product question**, enter a product-only question and tick explicit sharing consent.
**Send consented review request** must show a saved AP ID/REVIEW_PENDING, not success.
Sign out/in as Founder, open Review queue, inspect **Unresolved BA product question**
and exact consultation/revision/evidence. Choose Request revision/Reject/Approve with
a reason. Approval only permits Customer reconfirmation/fresh assessment; unchanged
AUD10 still cannot match. Correcting to AUD60 is explicit new scope, never an implied
budget increase. Routine supported advice still completes without AP.

For live evidence, reuse the installed model/config as WINDOWS_LLM.md; use another
free port/new database with `-Mode strata -LlmConfig var/llm.strata.json`. Start no
second provider/install/download. A service-off assessment can be reviewed, but
approval cannot make inference succeed while the service remains off. Restore only
your owned runtime, then Customer reconfirms for fresh evidence/model validation.
Stop only app/model instances you started. Tests/review decisions here are synthetic;
no order, stock, payment, settlement or publication effect is authorised.

This round used isolated 5770/5771 databases; actual stopped-model review then
restored-model BA passed, with stock/orders unchanged and no effects. See the
30 October VERIFICATION checkpoint. Existing model/config/database fingerprints
were preserved; all run-owned instances stopped.

## Current real CS exchange steps · 29 October 2026

Use current source from this CS checkpoint, not old frozen ZIP/standalone-only
instructions below. No reinstall/download is required on this prepared laptop.
Keep existing var/llm.strata.json and saved profile. Start only an already installed
model with `scripts/windows.ps1 -Action StartModel`; reuse it if already ready.
Then `scripts/windows.ps1 -Action Start -Mode strata -Port 5761 -Database
var/<new-unique-run>/live.sqlite3`. No LiveMc needed: this run keeps MC MOCK.
Application health/configured LIVE is distinct from model readiness/inference.

Customer After-sales care → Describe your service request: choose owned order,
explicit exchange intent + hydration/cleansing + AUD budget + fragrance requirement.
Inspect interpreted constraints. Missing/unsupported input clarifies/escalates;
correct using the saved natural request form (new revision, no automatic retry).
Founder Customer requests → Start advice handoff. Inspect independently verified
live product/facts, then original Customer confirmation→Founder exact approval→
Customer final simulated confirmation. No model grants authority. Existing structured
mock entry remains; old structured live records can be converted by natural correction.

Actual isolated5761 browser once-only path and stopped-model failures passed;
5760 mock browser still worked without model.264 tests/source/JS passed. Full evidence
and same-environment prerequisites: VERIFICATION.md. Stop only the owned app with
`scripts/windows.ps1 -Action Stop -Port 5761`. Leave pre-existing/shared models
running; this run stopped only its recorded new instance with --if-instance-id.
No new ZIP/Canvas/Mac/venue/remote-access or broader semantic acceptance is claimed.

## CO failure checkpoint — no model setup required · 29 October 2026

Current KAN-15-co-handoff-failures source adds bounded mock CS-to-BA failure handling.
Run the existing Windows Verify; it passes 237 offline tests, source and JS checks.
Start a new ignored DB on a free loopback port with the normal mock instructions
below. Customer correction creates a new revision; Founder must explicitly start
the new handoff. Failed advice cannot offer confirmation/review. No automatic retry.
The 5750 browser failure double/null injection used in this run is scratch-only,
not a production setting; automated tests reproduce those failure boundaries.
No new software/config/model install is needed. Real CS intent/handoff remains
unconnected/blocked; this run did not start or test the model. Existing live BA/MC
evidence is historical. Only this run's test process was stopped, original data
preserved. See VERIFICATION.md for exact evidence/limits. Frozen eb8f0de ZIP predates
this increment; perform a current-source release rehearsal after review.

## MC generation recovery checkpoint · 29 October 2026

Current source adds MC generation recovery; the frozen eb8f0de ZIP below does not
contain it. Reuse the installed model/tools; no new setup/download/dependency is
needed. Use a new ignored DB and free loopback port. Actual tests used 5740 mock
and 5741 opt-in real MC/template video, with var/mc-recovery-20261029 local data.

In Activity trail select **MC final generation save failure (draft retained)** and
Apply fixture, then Content studio -> Create draft. Expect RECORDING_FAILED,
recoverable metadata and no review-ready script/media/review ID. Stop/start only
that owned app using the same DB/config; choose **Recover saved generation**.
Expect validated content and REVIEW_PENDING with one exact review, never approval.
Repeated recovery must retain that ID. A real SQLite audit-abort/browser restart
was also verified; that trigger existed only in an isolated test DB and was removed.

For real MC: start the existing owner profile only if stopped, then use
`-Mode strata -LiveMc -LlmConfig <existing local JSON> -VideoConfig <local JSON>`.
Record the runtime instance ID/ownership. After the complete generated outcome has
been staged, stop only that owned model instance with the guard below and restart
only the app. Recovery must reuse the same text and artifact/file hash without
inference/rendering. Preserve the original media output directory and supply its
template configuration on restart; without it the draft stays recoverable with
MC_MEDIA_RECOVERY_UNAVAILABLE. Model readiness and app health do not prove recovery.

If staging failed or work was interrupted before a durable outcome, no Recover
button is offered. Refresh first: GENERATING alone cannot prove the worker stopped.
**Retry generation as new revision** explicitly supersedes old work and may call
the generators again; model-off retry must remain GENERATION_FAILED / LLM_UNAVAILABLE
with live flags and no mock fallback. Correct invalid content via explicit revision.

**Cancel this campaign** saves a new cancelled revision and suppresses late
replies/old review authority; a physical model/render process may still finish and
leave ignored artifacts. A failed cancel is not confirmation of cancellation.
Cancelled campaigns require a new campaign. Approved/rejected terminal drafts use
explicit revision instead of retroactive cancellation. No publication occurs.

Test-only raw logs/readbacks remain under var/mc-recovery-20261029. Only owned
app receipts and exact model instance were stopped; original environment retained.
Full committed-MC-decision recovery and partial-render resume are outside this slice.
See CONTRACTS.md/VERIFICATION.md for exact routes/evidence; Jira unchanged/unverified.


## Frozen-source ZIP rehearsal · 29 October 2026

**Current tested package:** eb8f0de8d412344e828daf9032898c2dbb6155ee,
`elec5620-source-eb8f0de.zip`, 5,658,127 bytes / 116 files,
SHA-256 `bf7d8b0324c9797e2adb03d0727a89aa31325ebb5a22223fd7a528760d25bba4`.
Fresh extraction actually used:
`D:\elec5620_project\rehearsals\20261029-eb8f0de\fresh source`.
191 tests passed there; mock end-to-end, real BA, real MC text/template MP4/review
and model-off retained failure passed. Exact records/limits: VERIFICATION.md.
Earlier dated sections below are history. No application script repair was needed.
Keep this frozen ZIP unchanged: its docs are from eb8f0de; this later receipt must
travel separately. The old f7bb141 ZIP does not include the current BA/MC increments.

**Prepare before the venue:** Python 3.14.5 with venv, PowerShell, browser, and Node
v22.19.0 for JS checks; existing model supervisor/runtime/weights and optional
FFmpeg/ffprobe 9.0.2 + local Windows Arial. No Python package download was required.
The ZIP is source-only, not a bundled model or clean-machine installer. Keep the
old model workspace and portable media-tool paths available. Do not InstallModel,
upgrade, duplicate weights, or run media_tools Setup during this rehearsed route.
No network access/LAN exposure was added. macOS/other-machine/venue acceptance
and offline first-time preparation remain unverified.

**At the venue:** verify the ZIP hash, choose a nonexistent extraction directory,
expand without overwrite, and use the Setup/Verify/import-origin commands in
“Execute from a new extraction directory” below. Confirm both printed paths point
inside the extraction. Choose free ports and new DB names; stop if occupied.
Existing Setup/Start preserve local files; they do not reset an old demonstration.
Our ports were 5730/5731; DBs var/mock-demo.sqlite3 and var/live-demo.sqlite3.

From the new extraction, create ignored local configs exclusively (existing files
must be inspected/reused or a new filename chosen, never overwritten):

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
# Inspect existing model runtime first; reuse if ready. If stopped, start from its owner:
& "$modelHome\scripts\windows.ps1" -Action StartModel
(Invoke-RestMethod 'http://127.0.0.1:8080/v1/models' -TimeoutSec 10).data.id
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5731 -Database var/live-demo.sqlite3 -LlmConfig var/llm.live.json -VideoConfig var/media.local.json
```

All application code/DB/config/output lives in the extraction; only the separate
model service and explicitly named tools/font remain external. Relative media
output_dir resolves beside its config, so output goes to fresh var/media-output.
No original app config is needed after these independent configs are created.
This local service needed no key; any future key stays in the named environment
variable. Do not package configs/sessions/DBs/model/tools/fonts/media/logs.

On 5730 exercise Customer ORD-1001 -> Founder advice handoff -> Customer proposal
confirmation -> Founder exact review -> Customer final simulated confirmation.
Before final confirmation expect zero effects; afterwards one, including replays.
On 5731 use Product advice natural hydration/fragrance-free/AUD60 requirements,
confirm explicitly, then inspect saved real BA facts. As Founder use Content studio
with an energetic teaser limited to catalogue fact “50 ml”; check real-text/template
labels, play/download/hash the MP4, and review the exact revision. Re-authenticate
when changing ports/roles: different DBs on the same hostname share a cookie name.
This is a silent text-card template, not AI-generated scenes or speech.

Check application health, model readiness and actual saved inference separately.
Only if this run started the model and the exact instance is still owned, stop it
with the guarded official command described under “Stop and diagnose” below;
leave a pre-existing/shared model running. New BA must save INCOMPLETE /
LLM_UNAVAILABLE without result or mock fallback; previous MP4 remains accessible.
CS intent remains NOT_CONNECTED and live CS handoff remains blocked.

```powershell
# From the extraction, stop only apps started using these owned receipts:
.\scripts\windows.ps1 -Action Stop -Port 5730
.\scripts\windows.ps1 -Action Stop -Port 5731
```

Retain new var for diagnosis; inspect fresh app logs, DB mode/status and separate
model engine logs. AP recovery has historical evidence but was not re-exercised in
this ZIP run; full MC recovery and full Stage 2 acceptance remain open. No Jira
access/update (unverified / update pending), push, PR, merge or Canvas upload.


## MC template MP4 checkpoint · 29 October 2026

Optional media setup is a separate action, never part of normal Setup/Start/Verify.
It requires Windows PowerShell, network only for the first portable-tool download,
and the installed Windows Arial font (not redistributed in source).

```powershell
.\scripts\media_tools.ps1 -Action Setup
.\scripts\media_tools.ps1 -Action Diagnose
# Offline text fixture + actual template MP4, no model required:
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5720 -Database var/video-demo.sqlite3 -VideoConfig var/media.template.json
# Or reuse the installed model, then real text + actual template MP4:
.\scripts\windows.ps1 -Action StartModel
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5721 -Database var/video-live-demo.sqlite3 -LlmConfig var/llm.strata.json -VideoConfig var/media.template.json
.\scripts\windows.ps1 -Action Stop -Port 5720
.\scripts\windows.ps1 -Action Stop -Port 5721
```

Choose unused ports/new DB names; existing data is preserved. Repeated tool Setup
returns immediately when config exists, without downloading or overwriting it.
No PATH/system/model changes. Missing/partial existing tool installs are preserved
for diagnosis. The pinned archive is ffmpeg-9.0.2-essentials_build.zip, 114768076 bytes,
from https://github.com/GyanD/codexffmpeg/releases/download/9.0.2/ffmpeg-9.0.2-essentials_build.zip ;
SHA-256 60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba,
verified against the publisher's GitHub release-asset digest. Portable binaries,
licenses and docs are under ignored var/media-tools; source ZIP excludes them.
Retain publisher license notices with any separately distributed binary package.

Local var/media.template.json contains explicit ffmpeg/ffprobe/font/output_dir and
timeout_seconds (120 per subprocess tested); relative paths resolve against that config file,
not the source checkout. CLI equivalent: append --mc-video-config <local JSON>.
For another unpacked checkout, pass the absolute existing media-config path, or
prepare its own tool config; do not copy the model/runtime into source. Startup
with absent tool paths is permitted so generation can record MEDIA_UNAVAILABLE.
Invalid config JSON/schema fails startup. Omitting VideoConfig preserves mock media.
Stop only owned app receipts/exact model instance as in WINDOWS_LLM_RUNTIME.md.

In Content studio sign in as Founder, create a video draft, play and download it,
compare hash and exact revision, then use existing review. A revision makes a new
file/hash/review; an old media URL returns 409. MP4 may be previewed while pending;
download is internal review, not external publication. Model-ready, renderer-present,
file-generated and browser-playable are distinct checks. Video output is silent
text cards with written camera suggestions; it does not enact those motions.
Actual Windows-only evidence is in VERIFICATION.md. New-source ZIP, other machines,
macOS, offline first-time installation and venue acceptance remain unverified.


## MC bounded live-text checkpoint · 29 October 2026

Reuse the installed model/config; do not rerun InstallModel or copy weights.
From the current source root, after Setup/Verify and checking ports/processes:

```powershell
.\scripts\windows.ps1 -Action StartModel
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5711 -Database var/mc-demo.sqlite3 -LlmConfig var/llm.strata.json
# Open http://127.0.0.1:5711; sign in as the fictional Founder; use Content studio.
.\scripts\windows.ps1 -Action Stop -Port 5711
```

Choose an unused port/new database name for an independent run; existing databases
are intentionally retained. CLI equivalent:

```powershell
.venv\Scripts\python.exe -m beauty_company --llm-mode strata --llm-config var/llm.strata.json --mc-live --port 5711 --db var/mc-demo.sqlite3
```

Omitting LiveMc/mc-live keeps MC mock;
mock + LiveMc is rejected before process changes. No configuration rewrite or new
dependencies are needed. If using fresh unpacked source, pass the existing laptop's
absolute local LlmConfig path as described below; StartModel belongs to the model-owning
workspace, not an unpacked root without its runtime. The new MC increment itself
has not yet had a fresh-directory ZIP rehearsal.

Check app health, model readiness and an actual generated result separately. For
verification use a calm brief/Fragrance-free, then request revision and use an
energetic brief/50 ml. Inspect different script/style/caption, new review, mode labels
and catalogue facts; approve only that exact revision. Text is catalogue-literal
composition; media remains MOCK_STORYBOARD. Stopped/unavailable model must retain
GENERATION_FAILED/LLM_UNAVAILABLE without text/media/review or silent mock success.
Health and configured LIVE labels alone prove neither readiness nor inference.

Stop only the app receipt/port started by the run. If the run started a model,
use the exact runtime instance guard in WINDOWS_LLM_RUNTIME.md; do not stop an
existing shared model. This rehearsal used 5710 mock and 5711 live with independent
databases under ignored var/mc-live-20261029. Both apps and the owned model ended;
original configs/databases/model inventory were preserved. Full results below are
historical where dated; current evidence is in VERIFICATION.md.


## Current ZIP deployment procedure · 28 October 2026

Frozen rehearsal ZIP: source `f7bb141f6e35c7846989adccf58841b9e128a978`,
SHA-256 `5be88639cdd33415dadc77c0e6bfdc286b34b50e4635be2568ee01f4543e6ba3`.
The final source package passed a second fresh-directory 123-test, mock/failure/
recovery and real-BA HTTP repeat. Its source stays frozen; later documentation
receipt commits do not change this archive. See the final dated receipt in
VERIFICATION.md; the earlier 515bfa5 browser package is recorded separately.


Danny / M1 authorised a local GR-INT-03 source-delivery rehearsal, separate from
BA-START-01 and the broader GR-INT-02 model task. **GR-INT-03 is an internal backlog
label, not a Jira key.** The repository has no mapped deployment-ticket key;
Jira is unverified / update pending. At Danny's request, no live Jira lookup or
write, Canvas upload, push or merge is part of this run.

### Prepare before the demonstration

- Windows PowerShell and a working Python >=3.9 with venv/ensurepip. This laptop
  used Windows 11 Pro 25H2, build 26200.9711, Python 3.14.5 and PowerShell 5.1.
  Setup creates a new local virtual environment; there are no third-party app
  packages, pip downloads, frontend builds or network assets to install.
- A browser. Node is needed for the JavaScript verification step (22.19.0 tested),
  not for serving the app. Git is needed on the packaging machine, not to run the
  unpacked source or its repository check. Verify skips JavaScript syntax if Node
  is absent: run the explicit syntax command below; do not claim it passed then.
- For real BA on this laptop only: retain the separately installed Strata 0.2.1 /
  Terminal 0.1.46.1 / bundled Python 3.12.15 / engine 0.1.46 CUDA 13 and existing
  Gyro-S weights, saved launch profile and owner-private runtime. Driver 617.42,
  RTX 5070 Ti Laptop 12227 MiB and 31.42 GiB usable RAM were observed. Existing
  model files total 86.39 GiB (56 files); they are deliberately outside the ZIP.
  Keep 8192 context, one request, vision/MTP off and the saved 1536 MiB VRAM reserve.
  Do not install/download/update or relocate the model during the demonstration.
- Confirm with the teaching team whether prepared Python/Node, cached model and
  private runtime on the demonstration laptop are permitted. This is not yet a
  clean-machine, offline-network or actual Canvas-download acceptance.

### Package an identified clean source version

From a clean committed task branch, first run Windows Verify. Record the exact
commit and ZIP hash separately; a ZIP cannot contain its own final SHA-256.
The existing packager reads source files, not an immutable Git archive: review
untracked files and require a clean worktree before claiming an exact revision.

```powershell
git status --short
git rev-parse HEAD
# Stop here if there are uncommitted/untracked source changes.
$sourceId = git rev-parse HEAD
$archive = Join-Path $PWD "output/prototype-source-$sourceId.zip"
python scripts/package_source.py --output $archive
if ($LASTEXITCODE -ne 0) { throw 'Source packaging failed' }
Get-FileHash -LiteralPath $archive -Algorithm SHA256
```

The packager refuses an existing output path. Preserve previous archives and use
a new name for a new candidate. Inspect the ZIP before delivery: no .git, .venv,
var, databases, credentials, model weights, old outputs or private source report.
The rehearsed 515bfa5 archive contained exactly the 110 tracked source files;
each archive member matched the source bytes. It includes the public redacted
reference PDF and source excerpts needed by provenance checks.

### Execute from a new extraction directory

Use an unused destination and fresh database names. Do not expand with -Force
over a prior deployment. Paths with spaces were actually exercised.

```powershell
# Set these to the chosen ZIP and an unused destination.
$archive = 'D:\submission\prototype-source.zip'
$fresh = 'D:\submission\fresh source'
if (Test-Path -LiteralPath $fresh) { throw 'Preserve existing directory; choose a new destination' }
Expand-Archive -LiteralPath $archive -DestinationPath $fresh
Set-Location -LiteralPath $fresh
Remove-Item Env:PYTHONPATH,Env:PYTHONHOME,Env:BEAUTY_DB,Env:BEAUTY_PORT -ErrorAction SilentlyContinue
.\scripts\windows.ps1 -Action Setup
.\scripts\windows.ps1 -Action Setup  # existing environment/config must survive
.\scripts\windows.ps1 -Action Verify
node --check beauty_company/web/app.js
.\.venv\Scripts\python.exe -c "import sys,beauty_company; print(sys.executable); print(beauty_company.__file__)"
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5670 -Database var/mock-demo.sqlite3
```

Both printed Python/module paths must belong to this new directory. The app
serves its own packaged HTML/JS/CSS and writes only its fresh var/database. Do
not set PYTHONPATH to the old checkout. No old working-tree code is needed.
Open http://127.0.0.1:5670, sign in as Customer with the fictional demo account,
submit ORD-1001, sign out, sign in as Founder and start the advice handoff. Return
as Customer to confirm the proposal; return as Founder to review its exact scope.
For the rehearsed failure, Activity trail -> Decision recording failure (no
approval) -> Apply fixture, then approve with a reason. It must show recording
failed, no applicable committed decision and Recover saved decision. Stop/start
only this fresh app with the same DB, log in if needed and recover. Recovery may
commit/deliver one decision but must not execute. Only the subsequent Customer
confirmation executes one simulated effect. Repeating recovery/confirmation must
not duplicate a decision, effect or stock decrement. See VERIFICATION.md for the
actual database readback, not just the visible success message.

### Connect the fresh app to the existing model service

The fresh app does not own the separately installed model environment. On the
model owner's existing workspace, inspect existing runtime/processes first. If
that saved profile is stopped, use its StartModel; if already ready, reuse it.
For this laptop the model workspace remains
`D:\elec5620_project\elec5620-group6-beauty-company`.

```powershell
$modelWorkspace = 'D:\elec5620_project\elec5620-group6-beauty-company'
# Only after confirming this is the intended installed profile:
& "$modelWorkspace\scripts\windows.ps1" -Action StartModel
$modelIds = (Invoke-RestMethod 'http://127.0.0.1:8080/v1/models' -TimeoutSec 10).data.id
$modelIds
```

Do not run InstallModel/StartModel from the new extraction: those actions look
for model state under that extraction's var. This is an explicit model-supervisor
dependency, not a hidden application import. No model folder or original private
configuration is copied. In the fresh app directory, create a separate ignored
configuration with the observed exact model ID; exclusive creation prevents an
existing local file from being replaced:

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

The local Strata service required no key. Any future key stays in the named local
environment variable, never in source/ZIP/log summaries. Keep loopback binding;
this procedure grants no LAN/SSH access. Reusing an existing config is also
supported by absolute -LlmConfig, but the completed browser probe used a newly
created config inside the fresh directory, so it needs no old app-config path.

Application /api/health showing BA LIVE is configuration evidence only. Official
runtime ready plus /v1/models establishes model readiness; only a saved completed
consultation with simulated:false and independently checked catalogue facts
establishes actual inference. In the fresh live webpage sign in as Customer,
open Product advice and submit the explicit hydration/$60/fragrance-free fixture.
Expect Live BA recommendation, P-101 and supported facts. MC remains mock and CS
intent is NOT_CONNECTED; live CS coordinate/revise remains blocked. A missing or
unready model must save INCOMPLETE, never a fabricated mock success.

### Stop and diagnose

```powershell
# Run using the scripts from this fresh directory, with the same ports.
.\scripts\windows.ps1 -Action Stop -Port 5670
.\scripts\windows.ps1 -Action Stop -Port 5671
# Verify only these owned listeners have ended. Retain var and all databases.
```

Do not stop a model that predated the rehearsal. When this rehearsal started its
own model, cleanup checked the same official runtime instance ID and used
`runtime stop --profile launch-elec5620-ba --if-instance-id <observed-id>`; a
changed identity must be left for reconciliation. No process-name-wide kills.
Inspect fresh var/app-PORT-*.err.log, its process receipt, /api/health and the
model owner's runtime/engine logs separately. Logs/databases/cookies/config stay
ignored. Port conflicts are refused without changing the existing process.
Setup preserves existing config and .venv; it refuses an incomplete environment.
Start reuses its owned app, so Stop before deliberately changing DB/mode/config.
Never repair a repeated run by deleting data or overwriting local configuration.

### This run, historical evidence and remaining work

Newly verified: ZIP 515bfa537e31a01b9e9a24400a7112f8103babb3 -> new directory,
123 Windows tests, source/JS checks, repeated Setup, browser mock main flow and
AP failure/restart/web recovery, once-only execution, and one browser real BA
call against the existing installed service. No repository code/script fix was
needed. See the 28 October entry in VERIFICATION.md for exact timings/hash.
Older 21/25 October model installation/84-test records below remain history.
The merged AP recovery button and CS retained-assessment UI are present in this
current source; earlier statements that they were absent no longer describe it.
Formal Canvas download/re-extraction, final-source-package freeze, venue/software/
cached-model permission, real CS/MC, wider acceptance, long runs and another
computer remain separate. A successful local source rehearsal is not full Stage 2.


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

## Windows post-CS/AP regression · 25 October 2026

The 966dae4 integrated branch was validated on this laptop using existing Strata
and fresh databases. Both Windows interpreters passed 84 tests; actual browser BA
and safe model failures passed. See [latest runtime checkpoint](WINDOWS_LLM_RUNTIME.md)
and [full verification](VERIFICATION.md) for precise evidence, the local safe-stop
fix and AP web recovery/display limitations. Earlier install-blocked, uncommitted
first-phase and task-status paragraphs above are historical, not current commands
to reinstall the model or move Jira backwards. The regression run itself made no remote writes.
