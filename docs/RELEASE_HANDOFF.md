# GitHub handoff to the gaming laptop

## Include the BA/MC repair · 31 October 2026

The next Windows candidate must include the merged KAN-10/KAN-12 repair linked
from Jira: structured BA service lifecycle/current-evidence storage recovery, MC
missing-facts guard, regression tests and paired evidence. Bounded shared changes
include application.py, BaIntake and the existing structured HTTP creation session
recheck; no UI, model, schema or dependency change. This supersedes the older
advert/CO-only candidate boundary below. Inspect current main, pin the full commit
and generate a new ZIP/hash; do not replay old branches or reuse prior archives.
Structured lifecycle remains service-only; exercise the existing natural BA UI.
Current expectation is **305 tests** (286 prior +19 new), provenance133 files/41
case groups and JS; actual current Windows results must be recorded separately.

English is the maintained primary version. [中文阅读副本](zh-CN/RELEASE_HANDOFF.md).

Danny / Danyang Wang / M1 authorised this AI-assisted repository-maintenance
increment on 30 October 2026, under KAN-9 / internal GR-INT-03 (not a new Jira key).
PR #18 at 1ad1101 originally added this documentation-only route. Danny then
authorised the bounded advert-template polish described in current STATUS and
VERIFICATION: original packaged artwork, renderer and two guard tests, with paired
guidance/MC traceability. No model/provider or ownership change. Use a merged
main containing that increment for its next Windows acceptance; if it is still
local/unmerged, report the missing publication rather than testing old main as new.
Danny subsequently authorised PR #17's repair/review/merge: it is now merged as
91281dc, with three CO regression tests and paired documentation only. Do not
replay its old branch; the next candidate includes that reviewed increment.

## Baseline and evidence

The earlier application baseline is merged PR #16, commit
`7c862341fe914b33b7dadcd56784288b50fb0436`. Historical RC1 excluded PR #17;
the current candidate also includes its repaired, reviewed merge 91281dc.

The Mac prepared a local RC1 source ZIP at that exact commit: 124 files,
SHA-256 `7f954baab3ab90872f9b648deca0587cf2716bc032491d7d4ef0dac0d1c78369`.
Its fresh extraction/new venv passed 281 tests in 33.485 s, provenance and JS.
An actual mock-browser exchange exercised AP save failure, app restart, same-intent
recovery, and final Customer confirmation: zero effects before confirmation,
one afterwards, P-101 stock 12 -> 11. No new model/video run occurred on that Mac.
Earlier Windows BA/CS/MC evidence in STATUS/VERIFICATION is version-specific;
one combined current-candidate Windows run is still pending.

RC1 and its local receipts stay unchanged. They are ignored local artifacts,
not files that GitHub automatically transfers. **You do not need that kit for
this route.** Fetch the guide through GitHub and create a new source candidate
on Windows, recording its own full commit, file count and archive hash. The
documentation and advert-template increments change source bytes; do not call the new ZIP RC1, expect
the old hash, or copy RC1's results into a new candidate's PASS column.

## Get a clean source without changing the old workspace

First inspect the old gaming-laptop repository's branch/dirty state, running apps,
model and prepared tools. Preserve them. Do not reset, clean, stash blindly,
rebase or merge the old KAN-15 branches after their squash merges.

Clone this public repository into a **nonexistent sibling directory**, leaving
the old workspace as the model/tool owner. Check every command's exit status.
The name below is an example; choose another unused path if it already exists.

```powershell
git clone https://github.com/dyangwong/elec5620-group6-beauty-company.git D:\elec5620_project\elec5620-release-next
Set-Location D:\elec5620_project\elec5620-release-next
git fetch origin main
git switch -c KAN-9-windows-release-rehearsal origin/main
git rev-parse HEAD
git status --short --branch
git diff --name-only 7c862341fe914b33b7dadcd56784288b50fb0436 HEAD
```

The intended difference from 7c86234 includes PR #18's six documentation paths
and the current bounded advert-template increment: template_video.py, assets/advert,
test_mc.py, paired contract/module/status/verification/shared-scope/handoff guides
and selected MC traceability evidence, plus PR #17's three CO tests/paired guides.
Inspect the actual diff and merged PR
receipts; do not silently include another PR or reset old work. No BA/CS/AP/CO
business, HTTP/UI, provider, dependency or schema change belongs to this increment.
Pin and record this new checkout's **full HEAD**, not a moving `main` name.
Read AGENTS, this guide, current STATUS/VERIFICATION and the current Windows guides.
Historical commands/counts in older checkpoints are not new acceptance evidence.

## Package, then work from the extraction

From the clean committed checkout, use installed Python 3.9+:

```powershell
python scripts/package_source.py --output output/elec5620-source-rc2.zip
Get-FileHash output/elec5620-source-rc2.zip -Algorithm SHA256
```

Use a new filename if occupied; never overwrite RC1 or another candidate. Verify
that the ZIP's path list equals `git ls-files`, all entry bytes equal the clean
checkout's files, and no runtime/private files appear. Record each file's size and
SHA-256, the full source commit and archive SHA-256 in a local receipt. Windows
checkout line endings are reflected in these bytes; keep the exact ZIP thereafter.
There are 133 tracked source files including this advert-template increment, if
no other changes entered main; determine the actual count rather than hardcoding
a pass. Models, tools, fonts, configs, sessions, DBs and generated media stay out.

Extract the ZIP to another **nonexistent directory** (a path containing spaces is
useful), compare every extracted source file with the ZIP, and run from there.
Do not copy an old venv, whole var directory, DB or application code. Ensure no
PYTHONPATH/PYTHONHOME setting redirects imports; preserve any previous values.

```powershell
.\scripts\windows.ps1 -Action Setup
.\.venv\Scripts\python.exe -c "import sys, beauty_company; print(sys.executable); print(sys.prefix); print(beauty_company.__file__)"
.\scripts\windows.ps1 -Action Verify
node --check beauty_company/web/app.js
```

The printed interpreter/venv/module paths must all belong to the new extraction.
Expected application regression is 286 tests (281 baseline + three CO regression
tests + two renderer guards). Verify also
runs provenance; it skips JS when Node is absent, so record JS separately and
use already-installed Node rather than claiming a skipped check passed.

## Reuse the installed model and media tools

Inspect the actual old model-owning path; previously it was
`D:\elec5620_project\elec5620-group6-beauty-company`. Reuse its ready Strata service,
saved model/profile and installed FFmpeg/ffprobe/font. If stopped, use the installed
owner's guarded StartModel, not InstallModel in the new extraction. No download,
upgrade or model-weight relocation is authorised here. Missing prerequisites are
blockers to report. Prior profile/model details are in WINDOWS_LLM_RUNTIME.md.

Create new private configs in the extraction's ignored `var/`, using exclusive
creation and inspected existing values (never publish secrets). Confirm the exact
model ID from the running loopback `/v1/models`; use the existing prepared settings.
LLM fields: `base_url`, `model`, `timeout_seconds`, `max_tokens`, `api_key_env`.
Prior values: `http://127.0.0.1:8080/v1`, 120 s, 512 output tokens; any key stays in
the named environment variable. Media fields: absolute `ffmpeg`, `ffprobe`, `font`,
relative `output_dir` beside the new config, and `timeout_seconds`.
Setup creates `var/llm.strata.json` as an example; use a distinct new live filename.
See WINDOWS_LLM.md for config schema/examples; verify paths rather than guessing.

Choose free ports, new DB names and new config filenames. For example, from the
extraction, after actually creating `var/rc2-llm.json` and `var/rc2-media.json`:

```powershell
.\scripts\windows.ps1 -Action Start -Mode mock -Port 5780 -Database var/rc2-mock.sqlite3
.\scripts\windows.ps1 -Action Start -Mode strata -LiveMc -Port 5781 -Database var/rc2-live.sqlite3 -LlmConfig var/rc2-llm.json -VideoConfig var/rc2-media.json
```

Live acceptance must use **one configuration enabling BA, CS, MC text and template
video together**. MC has a separate campaign workflow; do not insert it into the
exchange chain. Check actual inference/rendering, not just app/model health.
Reauthenticate between ports/roles or use separate browser profiles: loopback
ports share a cookie name. Use only these new synthetic test DBs for approvals
and simulated confirmations; original DBs remain untouched.

## Pending acceptance for the new candidate

Record actual date, source/ZIP hashes, environment/model/tool versions, mode,
record/revision IDs, and independent DB/file evidence. Start every row unverified;
report PASS / FAIL / NOT RUN honestly. Existing tests are not all 41 case groups.

| Check | Required observation |
|---|---|
| Source/startup | Archive and extraction byte checks; fresh venv/import origins; 286 tests, provenance and JS; bundled PNG assets present. |
| Mock BA | Missing budget/fragrance clarifies on the same ID; explicit Customer confirmation precedes grounded advice. |
| Live CS/CO/BA | Owned ORD-1001 natural exchange -> Founder starts handoff -> grounded BA -> Customer proposal confirmation -> exact Founder AP -> final Customer confirmation. |
| Effect boundary | Independently check current evidence/policy/actionRef: zero effects before final confirmation, one afterwards; repeat confirmation stays one; P-101 stock 12 -> 11. |
| Live MC + media | P-101 energetic brief limited to literal catalogue fact “50 ml”; live bounded text; actual playable/downloadable 15 s MP4 and hash-bound current-revision review. Silent FFmpeg template, no AI scenes/audio/public posting. |
| BA conditional review | AUD10 unresolved product assessment -> explicit consent -> exact AP. REJECT/REQUEST_REVISION cannot invent success; APPROVE requires fresh Customer confirmation/inference/current evidence, zero commerce effects. |
| MC save recovery | Final-save failure -> persisted uncommitted generation -> same DB/config app restart -> same revision/text/artifact recovery without a second model/render call; one pending review. |
| Provider failure | Truthful live INCOMPLETE/FAILED and no mock fallback when model/endpoint is unavailable. |
| Canvas/venue | Separately authorised actual upload, actual download of the same ZIP/hash, fresh deployment, permitted preinstalled software/model/tools and venue constraints. Not performed by this guide. |
| Assessment material | Clear three-role demo, technology/limits, real Jira/PR/iteration evidence and human-confirmed contribution form; no invented percentages/endorsement. |

Suggested Customer input: `Please exchange my item for a fragrance-free moisturiser
for dry skin. My budget is AUD 60.` Suggested MC input: `Create an energetic teaser
highlighting the catalogue fact “50 ml”.` Use these as examples, not semantic guarantees.

Stop only this run's apps using their exact owned receipts. Leave a pre-existing
shared model running. Stop a model only if this run started it and the official
guard still matches its instance ID. Otherwise demonstrate a verified-unused
loopback endpoint in a separate failure config and label it endpoint unavailability,
not an actual model shutdown. Do not change LAN/firewall/SSH/public hosting.

Keep raw DBs/configs/cookies/logs private; make a short English receipt plus Chinese
reading copy under ignored output, with PASS/FAIL/NOT RUN and remaining conditions.
Recheck source and archive hashes after the run. If a source fix is needed, preserve
this candidate, use a separate task branch/PR, and create/retest a new archive;
do not edit an extraction and claim the unchanged old ZIP passed. No new business
features or replay of PR #17's already merged branch in this task. Publish only safe evidence through the
normal protected PR/check workflow; owner exception is not a human Approve.

With authorised Jira access, add one brief KAN-9 checkpoint with exact revision,
actual results, evidence link and next gap. Otherwise say **Jira update pending**.
Do not complete the epic/KAN-15, reassign members or fabricate contribution shares.
Canvas upload remains a separate explicit human action/authorisation.

## Copyable continuation instruction

```text
I am Danyang Wang (Danny / M1), continuing ELEC5620 Stage 2 delivery acceptance
under KAN-9 / internal GR-INT-03. Preserve the gaming laptop's existing dirty work,
branches, model, tools, configs, databases and processes. Fetch the repository's
main and read docs/RELEASE_HANDOFF.md (or git show origin/main:docs/RELEASE_HANDOFF.md
without changing the old branch); follow its new-clone/new-ZIP/new-extraction route.
PR #17 is already merged; do not replay its old branch or add features. Record the actual full source SHA and new ZIP
hash; RC1 is historical. Reuse prepared model/media tooling and run the pending
combined mock/live/recovery acceptance, saving honest English/Chinese receipts.
Only touch synthetic new demo data; stop only owned processes. Keep Jira to one
short checkpoint if authorised, otherwise pending. No automatic Canvas upload.
```
