# Local verification record

English is the maintained primary version. [中文阅读副本](zh-CN/VERIFICATION.md).

## MC bounded live-text checkpoint · 29 October 2026

This is new **local MC text** evidence, separate from prior BA and ZIP checkpoints.
Branch KAN-15-mc-live-text, starting clean at 4f43f38a89637248874f4ed308441a5502e464ff;
fetched origin/main unchanged at 515bfa537e31a01b9e9a24400a7112f8103babb3. Danny / M1
authorised the shared-file exception, with AI assistance; task assignments unchanged.

| New check | Actual result |
|---|---|
| Windows repository Verify | **181 tests, all passed in 49.886 s**; prior 169 + 12 new MC tests. Source verification 114 files / 41 tracked groups, source hashes and handoff checks passed. JS syntax passed, including after review-label correction. MC-only suite 28 passed. |
| Offline live-MC failure/boundary tests | Explicit opt-in/default preservation; strict/minimal shared transport; invalid plan/no fallback; actual script/caption/direction/duration mutation; immutable evidence; owner/role/CSRF/exact fields; pending/decision/revision; concurrent generation vs revision; changed catalogue; final-save transaction rollback; unavailable/timeout/invalid-output retention. These use test doubles, not live inference. |
| Default mock, actual Founder browser, new DB / 5710 | MC-b3315edc057a revision 1 APPROVED; simulated/textSimulated/mediaSimulated true. Existing mock review/decision delivery passed. |
| Actual shared model, new DB / 5711 | MC-931edb7409b9 revision 1: CALM, featured Fragrance-free, all three literal catalogue facts; brief asked only Fragrance-free but model retained other authorised facts. This creative instruction mismatch is visible for Founder review, not passed as semantic compliance. Founder REQUEST_REVISION delivered. |
| Actual model new revision and approval | Same MC ID revision 2: ENERGETIC, factRefs=[50 ml], featured caption 50 ml; actual script changed to “Meet Daily Hydration Cream. 50 ml. Explore the product details.” New AP-31e86c3715fa APPROVED/DELIVERED; prior AP-d0e8fc30ccdd SUPERSEDED with its recorded revision request retained. |
| Independent persisted output checks | Reconstructed actual script/claims/three frames against untouched current P-101:v1 catalogue; mode false for text, true for media. Exact draft ID/revision/live-text/mock-media review actions checked; two distinct decisions, zero effects, stocks 12/8/0 unchanged. |
| Exact owned model stopped; new browser create | App healthy/configured LIVE_TEXT_WITH_MOCK_MEDIA; port 8080 closed. MC-de418646a5b9 GENERATION_FAILED / LLM_UNAVAILABLE / textSimulated=false, no script/claims/media/approval; no mock fallback. |
| Environment and cleanup | Windows 11 Pro 25H2 build 26200.9711; app Python 3.14.5; Strata 0.2.1, Terminal 0.1.46.1, engine 0.1.46 CUDA 13 / Python 3.12.15; model qwen3.8-flash-next-gyro-gyro-s. Existing 8192 context, single request, no vision/MTP, 1536 MiB reserve, route-tail-skip 7, 120 s / 512 output tokens reused. No install/download/dependency/config changes. Only owned 5710/5711 apps and guarded model instance stopped. Original config/database hashes and 56 model-file size/mtime inventory matched. No captured browser warnings/errors. |

Engine logs recorded the two MC generations: prompts 326/332 tokens, outputs 53/41
tokens, reported prompt/decode 6135+2062 ms and 1803+1260 ms (engine measurements,
not full browser latency). Adapter checks exact configured model ID and completed
JSON; actual persisted content and model-off failure independently distinguish this
from fixtures or health-only checks. Initial implementation tests exposed a missing
text_value import; corrected before the passing suite. Form create/revise fields
and live review title were also corrected before final browser acceptance.

Raw logs, DBs, exact-instance receipts, before/after hashes, engine log and
evidence-summary.json remain ignored in var/mc-live-20261029; screenshots are local
outputs. No sessions/keys/model files are tracked. Reproduce using WINDOWS_LLM.md.
No new ZIP/checksum is claimed: old f7bb141 archive predates BA/MC increments.

**Not verified/completed:** free-form creative prose, unrestricted/multilingual brief
semantics, medical safety, real video/media quality, MC cancellation or durable
generation-save recovery/full lifecycle, whole MC/Stage 2 acceptance, fresh-ZIP or
another-machine/venue acceptance of this increment. Final-save rollback can leave
DRAFTING with no output/review; existing AP recovery must not be described as an
MC generation-recovery button. No real CS intent/handoff added. Jira unverified /
update pending (no access/write requested); no push, PR, merge or Canvas upload.


## BA lifecycle checkpoint · 29 October 2026

First-round completion was rechecked before edits: clean local 478d522694ca381b2ba3c3c5e3711a77fb04133a,
147 passing tests and explicit normal app/model stop receipts (model exit 0).
No project crash was observed; these records do not establish Codex desktop-window
stability. Then fetched main 515bfa537e31a01b9e9a24400a7112f8103babb3 and branched
`KAN-15-ba-lifecycle-recovery` from 478d522, preserving all earlier local work.

| New round-2 check | Actual result |
|---|---|
| Repository Windows Verify, Python 3.14.5 | **169 tests passed in 46.561 s**: 147 previous + 22 new; source verification 113 files / 41 groups and JS passed |
| New offline lifecycle/failure cases | Same-ID complete replacement/history, completed cancel refusal, cancellation during extraction and recommendation, revision races, owner/session/CSRF/input guards, repeat/concurrent recovery, mode preservation, failed staging/final/failure/cancel writes, no-draft explicit retry and invalid/unsupported saved evidence |
| Real SQLite trigger aborts final advice audit in an isolated unit database | Result UPDATE rolled back with audit; durable draft retained, no COMPLETED/current result; removing the test trigger then recovering committed exactly once, without inference |
| Actual mock browser, fresh database / port 5700 | P-101 at revision 2 -> replacement `Gentle cleansing.` at revision 3 withheld old advice/asked missing fields -> answer revision 4 -> new Customer confirmation revision 5 / P-102; history retained P-101 |
| Actual mock cancellation and recovery | Another consultation CANCELLED/revision 2, no continuation controls; declared Founder BA-save fixture -> INCOMPLETE + hidden draft -> same-database app restart -> browser recovery COMPLETED at the same revision |
| Actual model in-flight cancellation, fresh database / port 5701 | Refresh exposed ACTIVE revision 1 with cancel enabled; cancellation saved revision 2; late original intake returned HTTP 409; events contain only creation/cancel, no interpretation/advice result |
| Actual model final-save simulation and persistence recovery | New consultation used real extraction and proposal; fixture retained live draft, no current result. Exact owned model instance stopped, app restarted with same test DB, model port 8080 closed. Browser recovered COMPLETED / simulated=false / P-101 at unchanged revision 2 |
| Independent SQLite/HTTP verification | Catalogue ID/version/price/constraints/reasons checked; live result price 4800 cents under budget 6000. Three further recoveries per mode retained one advice event; zero approvals/effects; stocks P-101=12, P-102=8, P-103=0 |
| Separate new live request after model shutdown | App health ok, mode still configured LIVE; saved INCOMPLETE / LLM_UNAVAILABLE / simulated=false with no recommendation; no mock fallback |
| Browser console / cleanup | No captured warnings/errors; original config/database hashes and 56-file model size/mtime inventory preserved; only owned 5700/5701 apps and this run's exact model instance stopped |

Reused Windows 11 Pro 25H2 build 26200.9711, Strata 0.2.1 / Terminal 0.1.46.1 /
engine 0.1.46 CUDA 13 / bundled Python 3.12.15, exact model
qwen3.8-flash-next-gyro-gyro-s, saved 8192 context, single request, no vision/MTP,
1536 MiB reserve, route-tail-skip 7. No upgrade, download, weight/config copy or
new dependency. Recorded engine generation and strict configured-model validation
support real inference; model-off recovery is persistence of that prior live output,
not a new live inference or proof of model availability.

Intermediate observations: one old failed-save test initially expected the previous
raw exception/ACTIVE gap; it was updated to require the new safe 503, durable draft,
INCOMPLETE and successful storage-only recovery. A first timed live cancellation
occurred after extraction completed, so was not counted as in-flight; a second
same-call browser submit/refresh/cancel sequence produced the verified late 409.
The browser save-failure fixture is explicitly a simulation; genuine SQLite write
and audit failures are separately verified in isolated tests, not by damaging disk.

Raw logs, process receipts, before/after hashes, engine log, record snapshots and
evidence-summary.json remain ignored under `var/ba-lifecycle-20261029/` (browser
screenshots in local outputs). Only sanitised evidence is tracked. Relevant shared
changes: BA service, HTTP routes, facade draft projection/fixture and UI concurrent
refresh/cancel; no schema/provider/teammate module change. Review pending.

Not established: complete legacy structured-route lifecycle, BA review, full
catalogue/inventory faults, unrestricted language/medical safety, physical GPU
abort, automatic recovery/retry, guarantees during total disk loss, cross-machine
or new-feature ZIP/Canvas acceptance. CS/AP/MC existing offline suites passed;
their browser chains were not rerun. All BA groups remain partial as appropriate;
BA-START-01/task ownership unchanged; Jira unverified/update pending, no access or
external publication. This does not prove Stage 2 complete.

## Earlier round 1 · BA needs checkpoint · 29 October 2026

New local KAN-15 slice, not BA-START-01 acceptance or Stage 2 completion. Branch
`KAN-15-ba-needs-clarification`; starting source a577c98c010142882abc22b552c73de92e3d51d0
over fetched main 515bfa537e31a01b9e9a24400a7112f8103babb3. The local code commit
containing this checkpoint identifies the delivered implementation; older ZIP
receipts below do not include it. No Jira access/update or external publication.

| New check | Actual result |
|---|---|
| Windows 11 Pro 25H2 build 26200.9711; application Python 3.14.5 | Full unittest discovery: 147 passed in 27.301 s; 24 new BA tests, old 123 retained |
| `scripts/check_repository.py`; `node --check beauty_company/web/app.js` | 113 source files, 41 tracked groups, source fingerprints/handoff passed; JS passed, including final confirmation-label adjustment |
| Real browser mock, port 5690, fresh ignored database | Dry-skin text -> two missing questions -> same ID revision 2 after answer -> no product until Customer confirmation -> revision 3 COMPLETED / P-101 / simulated=true |
| Real browser Strata, port 5691, separate fresh ignored database | Same flow; two actual extraction requests, then one recommendation; literal sources saved, explicit needsConfirmed, revision 3 COMPLETED / simulated=false |
| Independent read-only SQLite checks after both paths | Budget 6000 cents, P-101 price 4800, catalogue:P-101:v1, stock AVAILABLE=12; reasons literal subset of product facts; zero approvals/effects, stock unchanged |
| Existing model stopped with this run's exact instance ID; app retained | App health status ok with LIVE configuration; browser saved INCOMPLETE / LLM_UNAVAILABLE / simulated=false, no result or mock fallback |
| Exercised browser console | No captured warnings/errors |
| Local originals / cleanup | Original preexisting config/database hashes and 56-file weight size/mtime inventory preserved; only this run's two apps/model stopped |

Reused Strata 0.2.1, Terminal 0.1.46.1, engine 0.1.46 CUDA 13, bundled model Python
3.12.15, qwen3.8-flash-next-gyro-gyro-s, saved 8192 context / one request / vision
and MTP off / 1536 MiB reserve / route-tail-skip 7. No install/upgrade/download or
model-folder copy. Actual engine log recorded generation during the browser flow;
strict adapter envelope verifies the exact configured model ID. This is bounded
English evidence, not a broad model-quality or Chinese-live evaluation.

New offline tests cover focused missing fields, sufficient-but-unconfirmed input,
English/Chinese mock fixtures, ambiguous budget, sentence punctuation, Customer
field correction, same-ID restart resumption, owner/session/CSRF restrictions,
extra/invalid inputs and limits, two concurrent stale-result cases, current
catalogue changes, invalid/hallucinated source output, unavailable capability/model,
no fallback, and failed final save without false completion. Transport fakes use
strict model envelopes; they are separate from the actual-model browser evidence.

Failures found and resolved: an ambiguity-regex change initially rejected the
sentence-ending period after an amount (146-test intermediate run: five failures,
five errors); fixed with an explicit punctuation/partial-decimal regression. The
verification helper initially used a nonexistent provenance filename and assumed
top-level health capabilities; rerun using check_repository.py and the actual
capabilities envelope passed. No application error was disguised as successful.

Raw logs, test databases, before/after manifests, model log and browser record
snapshots remain ignored under `var/ba-needs-20261029/`; browser screenshots are
local outputs. Only this sanitised summary and necessary source/docs are tracked.

Not newly verified/completed: full cancellation/completed-record revision, BA
review lifecycle, arbitrary natural language or medical-scope detection, full
provider/catalogue/inventory fault matrix, optional alternatives, automatic BA
storage recovery (final save rollback can leave ACTIVE), macOS/second-machine
acceptance, new-feature ZIP/Canvas rehearsal. CS/AP/MC existing cases passed in
the full offline suite, but their browser flows were not repeated this round.
MC remains mock; CS intent and real CS handoff remain unconnected/restricted.
Affected-owner review and publication remain pending. Jira unverified/update pending.

The dated sections below are historical records; later publication updates supersede
earlier no-remote/byte-identical-packaging statements.

16 October 2026. Evidence from the initial implementation session, not tutor or
team acceptance and not full Stage 2 completion.

## Executed checks

| Check | Observed result |
|---|---|
| Python 3.9.6: `python3 -m unittest discover -s tests` | 29 tests passed |
| Python 3.12.14: same suite | 29 tests passed |
| JavaScript syntax: `node --check beauty_company/web/app.js` | Passed |
| `python3 scripts/check_repository.py` | Source hashes, 41-case tracking and bounded runtime/credential exclusion check passed |
| Temporary source archive extracted into an independent directory | 29 tests passed there; fresh database and web assets loaded without the original course folder |
| Real browser, local HTTP server | Customer intake → Founder handoff → Customer confirmation → AP commit/delivery → Customer reconfirmation → saved simulated outcome |
| Real browser, MC | Labelled mock script/storyboard created with PENDING exact-revision review |
| Founder overview at 1280×900 and 390×844 | No horizontal document overflow; screenshot review completed |
| Browser warnings/errors after exercised workflows | None observed in captured browser console |
| Git source boundary | Local main branch initialised, no commit/remote/push; runtime database and previews ignored |

The 29 tests exercise selected conditions from multiple case groups. They do not
mean 29 of the 41 original groups are fully passed. Traceability deliberately
retains PARTIAL/NOT_STARTED and records missing conditions. In particular, no real
LLM, real generated video, external commerce provider or Jira workflow was tested.

The clean-source check used the existing local Python installation; it is not a
rehearsal on the teaching team's on-site machine and not a Canvas download test.
Temporary archives were used for verification, not uploaded or labelled as final.

Browser verification created one fictional exchange outcome and one pending mock
campaign in the ignored local demo database. These are actual local test actions,
not fabricated company activity, team decisions or human contribution evidence.

## Prepared, not externally executed

GitHub Actions configuration uses the official action interfaces documented at
[checkout](https://github.com/actions/checkout),
[setup-python](https://github.com/actions/setup-python) and
[setup-node](https://github.com/actions/setup-node). No GitHub CI run occurred.
Jira, external models/media, hosting and Canvas have not been connected or changed.

Preview images live under ignored `output/previews/`; they are not runtime inputs
or part of a source submission. Launch instructions and fictional credentials are
in the root README. No legacy private key, certificate or runtime data was copied.

## Teammate onboarding update · 16 October 2026

- Added seven onboarding-tool tests alongside the unchanged 29 application tests;
  the combined suite passed all 36 tests.
- Verified all five full-name CLI entry packets resolve the report member's own
  task and existing reading files. Unknown/partial identities, mismatched tasks,
  stale source fingerprints and conflicting claims are rejected.
- Verified dry preparation writes no member profile or shared claim; optional
  local saving is tested only in temporary directories and does not edit tasks.json.
- Cross-checked names/modules against the actual extracted Stage 1 roster;
  detected intentionally swapped identities and colliding primary-file scopes.
- The complete report reference is byte-identical to the original final local
  PDF. The original report, application implementation and demo data were unchanged
  by the handoff update.
- All five starter briefs remain READY/UNCLAIMED with null Jira/PR/account fields.
  Prepared responsibilities do not prove member acceptance or work performed.
- Entry/tooling text reads explicitly use UTF-8. Windows command variants are
  documented, but native Windows execution has not been tested here.

The handoff prepares local work, not an external claim or an implementation of the
starter tasks. Real/local model setup remains deferred. No initial Git commit,
GitHub repository, invitation, Jira task or source publication was performed.

## Documentation language update · 16 October 2026

- Established 21 English primary / Chinese reading-copy pairs, including the
  contributor entry, agent rules, shared guides, five module guides and five
  starter briefs. English retains the canonical paths and helper reading order.
- Checked all 94 local Markdown links in those guides and verified reciprocal
  primary/copy links. Original source evidence and shared JSON/CSV data were not
  translated or modified. This does not change the application UI language.
- Repository checks passed with 79 source files; source fingerprints and all 41
  tracked acceptance groups remain valid. All 36 existing tests passed on Python
  3.9.6. No new application behaviour or external action was introduced.

## Public-source preparation · 16 October 2026

- Replaced the publishable byte-identical report with a labelled privacy derivative:
  all 63 pages/models retained; 25 student-ID occurrences across 11 pages removed,
  PDF metadata stripped. Inspected rendered cover/roster/contribution/model pages.
- Preserved the original final PDF unchanged locally, explicitly ignored it and
  retained the unredacted excerpt only under ignored var/private-reference/.
  Public excerpt uses an explicit redaction marker. Source and derivative hashes
  are recorded separately; added tamper/source-binding regression coverage.
- The 84-file source set passed student-ID/obvious-token/runtime-file checks and
  all local Markdown links resolved. These are bounded checks, not a full audit.
- Python 3.9.6 passed 37 tests and repository provenance/41-case tracking checks.
- Prepared an explicit main protection payload and matching CI job names, PR-only
  changes with zero required outside approvals, self-merge allowed after checks.
  A committed payload alone does not prove GitHub settings have been activated.
- Live GitHub publication, CI and protection results are recorded separately
  after execution. Jira, real-model deployment and starter-task claims are unchanged.

## Executed GitHub publication · 16 October 2026

- Published public `dyangwong/elec5620-group6-beauty-company`, initial commit
  `570ebc3adc948ff54523920cb93b5092a2013956` with 84 source files. Unredacted original,
  runtime data, previews and credentials are not in that commit.
- [Initial CI run](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/38865450983)
  succeeded on Python 3.9 and 3.13: 37 tests, provenance/41-case tracking and JS syntax.
- Applied main protection and read it back through GitHub: PR required, zero outside
  approvals, both observed check names from github-actions, current-main checks,
  conversation resolution, admins included, no force push/deletion, linear history.
  Repository allows squash only and deletes merged task branches.
- Independently extracted the public source archive without the original course
  folder: source checks, all 37 tests and the CS member entry passed. Neither the
  private original nor ignored runtime/previews were present in that archive.
- The publication handoff update uses a PR after protection was activated; its
  actual check/merge outcome is recorded in GitHub rather than invented here.
- No Jira setup, starter claim, real model or teammate invitation was performed;
  invitation recipients still need verified GitHub usernames.

## Jira configuration and mapping · 17 October 2026

- Configured the existing team-managed KAN space through its authenticated UI.
  Renamed In Review to Verification, enabled Backlog and added Bug; existing
  KAN-1/2, Story/Subtask and due dates were preserved. No sprint was started.
- Created six epics KAN-4..9 and five scoped starter tasks KAN-10..14, then refreshed
  the backlog and verified To Do, Medium, correct epic names and assignments.
  BA/CS/MC match existing displayed accounts; AP/CO full-name searches produced
  no existing matching account, so tasks remain unassigned. No guessed invite sent.
- Each task retains the original brief's source/acceptance IDs, allowed files,
  observable conditions, English/Chinese links and service-slice completion limit.
  Assignment is not recorded as a personal work claim or completed feature.
- The space automation Flows list showed No flows created yet. No automatic Done,
  coding-agent delegation, deadline, reminder, estimate or sprint history was added.
- Bound the actual keys/links/parents/suggested branches into the versioned registry.
  The local helper prints them without claiming a live sync. Added a regression for
  duplicate cross-member Jira keys and mismatched task URLs. Python 3.9.6 passed
  all 38 tests; provenance/41-case checks and local Markdown links passed.
- The KAN-9 maintenance PR exercises GitHub-for-Jira linkage; its actual development
  panel/CI/merge result is recorded after observation, not inferred from app installation.

- Moved only the five selected starters to Board and observed Board 7 / Backlog 0;
  all five remained To Do. The board displays To Do / In Progress / Verification /
  Done with correct starter parents and assignments. Original KAN-1/2 stay intact.
- In KAN-9 Development, observed one commit and one OPEN pull request, then opened
  its pull-request detail row: actual repository, PR #2, KAN-9-jira-onboarding → main
  and correct GitHub URL. This is observed linkage, not a claim of feature work.
- PR #2 initial CI runs [39032162481](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/39032162481)
  and [39032164622](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/39032164622)
  passed Python 3.9 and 3.13 checks. Final checks and merge receipt remain on the PR.

## Jira progress checkpoint rules · 17 October 2026

- Added explicit start / verification / merge-and-acceptance / blocked-or-reopened
  responsibilities and evidence in JIRA, agent/onboarding/Git instructions and
  the PR template, with Chinese reading copies. Jira remains live workflow authority;
  setup fields remain historical. No automatic sync or status change is implied.
- Removed obsolete pre-Jira wording and the old branch example; clarified that
  STATUS describes implementation at a revision and claim fields are receipts.
- Adjusted the existing preparation regression to include an already-claimed
  teammate task: preparing/saving CS must preserve that claim and the registry
  bytes. This allows real future claims without assuming perpetual UNCLAIMED.
- Python 3.9.6 passed all 38 tests. Repository source/41-case tracking checks passed.
  This maintenance work does not implement or claim any member's starter.

## Member intake and collaboration visibility · 17 October 2026

- Added missing-information-only intake, concise start/progress/handoff reports
  and task-boundary checks to AGENTS/START_HERE, with Chinese copies. Existing
  explicit identity/authorisation is reused; unavailable Jira remains unverified.
- PRs now explain why changed areas belong to the task and identify authorised
  deviations/affected owners. Shared-file guidance uses the real Jira-key branch.
- All 38 existing tests and repository provenance/41-case checks pass locally on
  Python 3.9.6. No application change, new personal claim or feature completion.

## Reserved shared LLM contract · 18 October 2026

- Danny explicitly reserved shared GR-INT-02 to himself, separate from BA starter.
  Created and observed KAN-15, parent KAN-9, assignee Danyang Wang, status To Do.
  Provider/model selection, installation and implementation have not started.
- Inspected current constructors/call sites and documented actual injected BA/MC
  signatures/units. CS has no independent intent port; its future seam is explicit,
  not falsely labelled implemented. Mode labels and transaction/network gaps are
  future integration acceptance, not claims of existing live capability.
- Added English/Chinese contract and gaming-laptop handoff, entry/brief/PR guidance,
  shared-work registry reservation and helper reading order. Starter claims unchanged.
- All 38 tests and 90-source-file provenance/41-case checks passed on Python 3.9.6.
  CS helper includes the contract and still selects only CS-START-01 / KAN-11.

## Enforced teammate approval · 18 October 2026

- Read existing main protection and actual collaborators. Found only dyangwong
  admin and slei0644 / ZhengduWei write; no account permissions changed.
- Created and read back active main ruleset 25333272: one required approval,
  stale-approval dismissal, resolved threads, squash; only dyangwong user
  226655466 has pull_request-only bypass of this review layer. Policy limits
  that exception to own PRs; GitHub itself applies it to the acting account.
- Read back unchanged classic protection: required current-main Python 3.9/3.13
  checks from github-actions, admins enforced, conversation resolution, no force
  push/deletion. Review-layer bypass does not remove the base protections.
- Updated English/Chinese agent/onboarding/Jira/Git guidance, default CODEOWNERS
  reviewer and PR review fields. Earlier zero-review policy is superseded.
- This is configuration readback, not a test using a teammate's credentials or
  evidence of any teammate review. Danny chose to retain maintenance PR #6 for
  teammate Approve; it remains open, not merged using the owner exception.

## KAN-15 Windows checks · 21 October 2026 client work date

Baseline e51dfc4: initial 38-test run failed with temporary-directory permissions;
workspace TEMP/TMP rerun passed all 38. Initial provenance check failed on Git
CRLF conversion; exact Git bytes restored, hashes unchanged, check passed.
Added seven integration tests (45 total) and passed on Windows Python 3.14.5.
Repository/JS syntax checks passed. Windows Setup/Start/mock HTTP probe/repeated
Start/Stop ran successfully; configuration was preserved and the repeat-start
alternate database was not created. Actual live-configured HTTP request without
the model saved INCOMPLETE/LLM_TIMEOUT in about 2.1 s, and the probe exited 1.
Strata Terminal archive hash and signed feed check passed; engine/model installation
failed on restricted-process private directory access. Sandbox-external execution
was rejected by approval policy. No successful real inference is claimed.
The exact machine/versions, CLI commands, redacted failure evidence, remaining
conditions and pending Jira handoff are in WINDOWS_LLM.md. Raw host evidence uses
20 October UTC timestamps; client work date is 21 October, not a Jira observation.

Additional local interpreter check: all 45 tests and repository checks also passed
on Strata Terminal's bundled Python 3.12.15. These are local checks, not GitHub CI.
Browser validation showed a completed mock recommendation and an INCOMPLETE model
timeout record with separate configured mode labels. Windows native topology
also confirmed 24 physical cores / 24 logical processors.

## Runtime ACL repair and real BA · 21 October 2026

Supersedes the earlier blocked-install/real-success-pending snapshot. Migration
left runtime permissions inherited from D; the official owner-private ACL check
now passes after a backed-up repair. Windows scripts support RepairModel and
resume the installed saved profile, without duplicate download/start or config
overwrite. Strata 0.1.46 CUDA 13 / Gyro-S is running at 8192 context, one request,
MTP/vision off, VRAM reserve 1536 MiB. Exact model ID and actual evidence are in
[WINDOWS_LLM_RUNTIME.md](WINDOWS_LLM_RUNTIME.md). Actual authenticated BA HTTP
consultation passed (6.804 s, COMPLETED, simulated:false, grounded P-101 facts),
then passed again; zero effects/approvals. All 45 offline tests, repository/JS
checks and diff checks passed. Repeat repair preserved config/profile hashes;
repeat StartModel/InstallModel retained the same engine process. MC remains mock,
CS intent/live handoffs unconnected, broader acceptance/review pending. No Jira,
commit, push, PR or merge action occurred.

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

## AP recording recovery slice · 24 October 2026

- Added `tests/test_ap.py` (15 cases) and adapted the existing AP atomic-audit-failure
  regression in `tests/test_workflows.py`. The combined suite passes 53 tests on
  Python 3.13.3 locally; `python3 scripts/check_repository.py` passes with 93 source
  files and the 41 tracked case groups intact, and `node --check
  beauty_company/web/app.js` passes. The Python 3.9/3.13 CI outcome is recorded on
  the pull request rather than asserted here.
- Verified against a temporary SQLite database: an injected decision-recording
  failure leaves the approval at RECORDING_FAILED with no decision id, decision,
  reason or founder, no delivered approval, no business effect and no
  DECISION_COMMITTED audit. The intended Founder, kind, reason and exact scope
  stay readable from storage.
- Verified that a new service instance over the same database recovers the same
  intended decision exactly once: one authoritative decision, one decision audit,
  one delivery, and no duplicate business dispatch when the Customer confirms.
- Verified that a conflicting kind or reason is refused, that a stale revision or
  a superseded request is refused, that a non-Founder and a different Founder are
  refused, and that a request receipt or a pending intent is never read back as
  an approval.
- Verified that a failed delivery after a recovery preserves the committed
  decision and that redelivery reuses its decision id.
- Not verified here: a real external storage outage (the failure is an injected
  local fixture), the HTTP/UI recovery control and the demo fault dropdown option
  (GR-INT-01 shared integration), expiry, notification/queue failure and risk
  routing. AP-T-05 therefore stays PARTIAL rather than PASSED.
- Observed on the pull request [PR #9](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/9):
  the "Local prototype checks" workflow runs for the push event and the pull
  request event both completed successfully on commit `c433ef0` (Python 3.9 and
  Python 3.13 jobs). The branch protection requires one non-author Approve from a
  reviewer with write access, so the pull request stays open and unmerged; no
  approval was observed when it was opened.


## Protected merge and combined integration · 25 October 2026

At Danny's explicit request, PR #7 merged normally as `6e505f0` with its retained
non-author approval and passing required checks. AP PR #9 incorporated that main
at `a1ae058`: all 75 offline tests and repository checks passed locally; fresh
Python 3.9/3.13 CI passed before the authorised AI-assisted review and normal
squash merge `840ac70`. Neither merge used a review/admin bypass.

The PR #8 integration candidate preserves CS/AP code, tests and claim receipts.
All six document conflicts retain both relevant changes. Python 3.9.6 passed
84 tests; repository checks passed for 107 source files / 41 case groups; bundled
Node passed `--check beauty_company/web/app.js`; staged whitespace checks passed.
No current Windows/model execution, complete acceptance, MC #11 fix or unseen
teammate approval is inferred. Remote checks and the remaining PR review are
reported on PR #8 after publication, separately from this local verification.

## Windows post-CS/AP regression · 25 October 2026

Danny / M1 continued KAN-15 / GR-INT-02 only. A clean Windows checkout fast-forwarded
from bd63c08 to **966dae4fd1c8afcaeb60b8af84289ae5b6edaa60**, incorporating main
**840ac7004723c62995a427191eda4f0cd4151917**. This is the exact application code
validated below; this update also includes the bounded stop-script fix and
bilingual evidence. No BA starter claim, CS/MC live feature or PR #11 work.

- `scripts/windows.ps1 -Action Verify`: Python 3.14.5 passed all **84 tests**
  (24.250 s; final rerun after the stop fix: 24.422 s); repository/provenance
  passed (107 source files, 41 original case groups), and Node 22.19.0 JavaScript
  syntax passed. Bundled Python 3.12.15
  independently passed all 84 (22.052 s). Counts: workflows 29, onboarding 9,
  LLM 9, CS 22 and AP 15; the original 47 plus CS/AP 37 explains the increase.
- Fresh loopback apps/databases: 5635 mock, 5636 Strata, 5637 unavailable-model
  endpoint, 5638 AP web failure, and 5639 the positive stop check. All databases
  and raw evidence are isolated under ignored `var/regression-20261025-966dae4/`.
- Actual browser login and BA submission passed in default mock and Strata modes.
  Live record BA-b7e1e655e3cf persisted COMPLETED/simulated:false and the page showed
  Live BA recommendation. An independent SQLite read checked P-101, integer-cent
  price/budget, fragrance constraint, current stock/version, catalogue:P-101:v1
  and both literal reasons against the saved catalogue. No BA-related approval
  or commerce effect was created. Engine log: 297 prompt tokens read in 6201 ms,
  25 tokens generated in 1042 ms; this is one fixture, not a general benchmark.
- Browser submission with an unused model port and 0.5 s socket budget persisted
  INCOMPLETE/LLM_TIMEOUT/simulated:false, displayed The model timed out, and had no
  product or mock success. On Windows the short connect budget expired before
  refusal; an additional actual connection-refusal service probe with a 5 s budget
  persisted INCOMPLETE/LLM_UNAVAILABLE. Neither probe stopped the real model.
- Actual CS/AP HTTP exchange: pending execution and customer self-approval refused;
  stale revision refused with STALE_SCOPE. Exact-scope approval/delivery left zero
  effects; three subsequent current customer confirmations produced one effect
  for the same actionRef and one stock decrement (12 to 11), ending RESOLVED.
- AP injected decision-save failure persisted RECORDING_FAILED with no decision id,
  no delivery and no effect. A new Company instance over the same fresh database
  recovered the durable same-scope intent; repeat recovery retained one decision/
  audit and zero effects. Only later customer confirmations produced one effect.
  HTTP save failure was also exercised; `/api/approvals/{id}/recover` returned 404.
- AP browser status correctly showed recording failed/no committed decision, with
  no recovery control. **Observed UI gap:** its fallback sentence incorrectly said
  the review was superseded by changed context. This is an AP/shared UI integration
  limitation, not a successful recovery button; no AP business/UI redesign was made.
- Strata-mode HTTP CS coordinate/revise retained 503/LIVE_HANDOFF_NOT_CONNECTED.
  Health retained MC:MOCK and csIntent:NOT_CONNECTED. A campaign created in that
  live-configured app remained simulated:true/REVIEW_PENDING, with mock media.

The existing Terminal 0.1.46.1 / Strata v0.2.1 / engine 0.1.46 CUDA 13 and
qwen3.8-flash-next-gyro-gyro-s were reused: model API 127.0.0.1:8080, context 8192,
one request, vision/MTP off, VRAM reserve 1536 MiB, upstream route-tail-skip 7.
No install/update/download was run. The original local configuration/profile/
database SHA-256 values stayed unchanged; all 56 existing model-file size/mtime
entries stayed unchanged. This is not a newly recomputed full weight checksum.

During the execution-permission transition, the test listeners disappeared; no
unverified PID was killed. The stop script exposed a null StartTime on a recorded
PID that still existed but could not be identified. The bounded local fix requires
both readable start time and executable before comparing the existing receipt.
The inaccessible PID was preserved; a new identity-matched app on 5639 was then
started/stopped successfully and its database retained. All six test ports,
including model 8080, were confirmed without listeners at final cleanup.

Earlier diagnostic attempts also exposed an overly narrow probe expectation
(LLM_UNAVAILABLE vs the observed Windows connect timeout), and the existing CS
DUPLICATE_REQUEST guard when a completed order was reused for another AP probe.
The probes were corrected/isolated; no test-count padding or business-rule change.

No real external storage outage, AP web recovery, retained CS failed-intake UI,
real CS/MC inference, network deployment, general model quality or full 41-case
acceptance is claimed. GitHub CLI returned 401; the connected GitHub read retrieved
PR #8 and its exact head. PR text reports an earlier authenticated Jira Verification
update, but the regression run did not independently verify Jira or perform any
Jira/PR write. Danny subsequently authorised publication of this evidence and
stop fix to PR #8. Fresh CI and actual review must apply to the publication commit;
this self-check is not an Approve. No merge, review bypass or Jira write is included.

## Local model stability and restart · 25 October 2026

Danny / M1 continued KAN-15 / GR-INT-02 at exact commit
`dbb6662fc1f71db9d40657bfa959cb712364b7bd`, using a new database on loopback
port 5641 and the existing Strata/Gyro-S profile on 8080. No model/config/code
change, dependency install, BA starter claim or CS/MC expansion was made.

- Completed 20 serial actual authenticated HTTP BA requests (10 hydration,
  10 cleansing), a measured 180 s idle interval, three post-idle calls, model
  stop/start and three post-restart calls. All **26** succeeded as
  COMPLETED/simulated:false. SQLite readback independently checked product,
  literal facts, integer-cent price/budget, fragrance, stock and version.
- Continuous-call min/median/max: 1.292/1.385/15.203 s; post-idle:
  1.277/1.321/2.802 s; post-restart: 1.994/2.421/7.386 s. These include local
  HTTP/persistence validation and are fixture timings, not general throughput.
- Initial model readiness took 18.816 s, restart readiness 20.017 s. Repeated
  StartModel retained the same instance/listener PID; after idle the same
  instance stayed ready. Restart created a new instance from the same profile.
- With the model actually stopped, a consultation saved
  INCOMPLETE/LLM_UNAVAILABLE/simulated:false in 2.109 s, with no mock fallback.
  All 84 offline tests passed during that stopped-provider interval (23.512 s).
  The same application/database remained available across the model restart.
- Final database: 26 COMPLETED, one expected INCOMPLETE, zero approvals and
  zero commerce effects; catalogue stock remained 12/8/0. No OOM, fatal CUDA
  error, traceback or crash marker was found in captured model logs.
- Loaded/request/idle samples: free VRAM 1957–2023 MiB; available system RAM
  2.35–11.16 GiB. RAM headroom is limited. No tuning or cache-clearing was done.
- Captured original config/profile/database hashes and all 56 model-file
  size/mtime entries stayed unchanged. All processes created by both attempts
  were stopped by their owned receipts/instance identities; test ports ended.

One initial controller attempt produced zero consultations: an inherited Windows
output pipe kept the launcher waiting after the app was ready. Only its owned
app/model were stopped. File-backed controller output resolved the wait; the
completed run used a fresh database. This was not counted as a successful test.

The successful window was 319.467 s (about 5.3 minutes), single request at a time,
using short structured fixtures. It does not validate overnight operation,
Windows reboot/sleep/resume, long prompts, concurrent users, broad advice quality,
remote Mac/Windows access or real CS/MC. No memory-leak guarantee is inferred.
This was actual HTTP automation, not a new manual browser acceptance run.
Raw evidence stays ignored under
`var/stability-20261025-dbb6662-20261025T053019994156Z/`. Bilingual evidence
records were prepared locally without a remote write during the stability run. Danny then
authorised publication of these four bilingual evidence documents to PR #8.
The tested application remains the exact commit above; fresh CI must apply
to the documentation publication commit. No model/config/code, SSH/firewall
or Jira change, merge or review bypass is included.

## AP HTTP/UI recording recovery · 26 October 2026

**Scope and authority.** Danny explicitly authorised the three AP shared HTTP/UI
gaps under KAN-9 / GR-INT-01: accurate recording-failure text, a recovery endpoint
and a recovery button. Branch KAN-9-ap-web-recovery starts from main
`e141427c393df6515ad8091f035e1c2f81cba65d`. This does not claim Jiaxuan's AP starter
or change approval.py, schema, CS/MC modules, model deployment or PR #11.

**Contract.** The authenticated original Founder posts only the displayed positive
integer contextRevision to `/api/approvals/{id}/recover`. The current origin,
revision and review link are checked even for repeat calls after commit; existing
service validation checks the durable exact action/actionRef before commit.
Decision, reason, actor and action overrides are rejected. Existing two-argument
service callers are retained. Recovery commits the saved intention once, then
attempts separate delivery; a failed delivery needs explicit same-ID redelivery.
Neither recovery nor delivery executes a business action. The failed card shows
the stored kind/reason as non-authoritative and offers recovery only to its
original Founder for a current origin. Decide/recover errors refresh saved state.
The new approval_recording menu option is an injected local fixture.

**Automated verification.** Mac Python 3.9.6 passed all **96 tests in 12.810 s**,
including all existing 84 and 12 new AP HTTP/session/SQLite tests. New scenarios:
restart and repeated recovery, later Customer-only once-only execution, preserved
REJECT/REQUEST_REVISION, unauthenticated/wrong-CSRF/Customer/other-Founder denial,
missing/invalid/extra/overridden inputs, old displayed revision, superseded origin,
changed action scope, stale repeat after commit, absent intent/unknown review,
repeat recording failure, and failed delivery with explicit same-ID redelivery.
Node syntax and whitespace checks passed. No real model was started or called.

**Actual browser acceptance.** A fresh ignored database on loopback port 5661 was
seeded with a mock CS pending review through the existing service calls. Browser
login used the fictional Founder. Under Activity trail, selected Decision recording
failure (no approval), applied it and clicked Approve exact scope with a reason.
The HTTP 409 refreshed the card immediately to recording failed, saved intention
(not a committed decision), saved reason and No applicable committed decision;
Recover saved decision appeared. The incorrect superseded sentence was absent.
Clicking recovery showed APPROVED, a committed decision ID and DELIVERED; the
recovery button disappeared and a later refresh kept the same decision.
Independent SQLite readback: approval AP-d53f12341a0d, decision DEC-6349abf72f19,
one DECISION_COMMITTED audit, zero effects, P-101 stock still 12, and the CS
request still AWAITING_CONFIRMATION. Raw database/screenshots remain ignored in
var/ap-web-20261026-first.sqlite3 and output/previews/ respectively. These are
mock business effects/fixture failure, not a real storage-outage test.

**Handoff.** Full AP-T-05 and GR acceptance remain PARTIAL. Queue/notification,
expiry, full risk routing, CS failed-intake UI and MC PR #11 remain separate.
Jira KAN-9 was read on 26 October: Integration & Verification, To Do, Unassigned;
no separate GR-INT-01 child appeared in its child list (KAN-15 is listed).
GitHub had only MC PR #11 open when overlap was checked. No new Jira claim,
status/comment, remote publication, CI or teammate review is claimed for this
local change. Prepared with AI assistance at Danny's request.

**Jira update pending:** record this bounded GR-INT-01 AP web-recovery increment
under KAN-9, link its PR once authorised/published, and request Jiaxuan's review
of the shared AP boundary. Include the 96-test/browser/no-execution evidence and
remaining cases above. Do not mark the broad integration epic Done or change
KAN-13/KAN-15/teammate claims based on this local implementation.

## MC repair acceptance · 27 October 2026

The original KAN-12 implementation by Zhengdu Wei is retained. At Danny's explicit request, the original PR #11 was brought up to main dc1b60b (merged AP #12) and repaired with AI assistance. This does not reassign the starter or claim the teammate's endorsement.

Failed revisions now render as failed records in Content studio, with their permitted reason, no fabricated product/media/approval, and a corrected-draft form using productId. The review queue also handles failed current payloads and shows that a superseded review cannot approve a different current revision. Existing HTTP creation still calls submit; submit_draft remains a service entry point. No live model or video generation is added.

Model evidence and media inputs are deep copies; media frames are checked against an independent verified storyboard snapshot, rather than a mutable alias. Shot/duration metadata and the mock-media label are bounded to the declared fixture. A mutating adapter cannot introduce unsupported captions or alter the saved script/claims by changing its input. This remains deterministic mock validation, not unrestricted prose grounding.

The full integrated suite passed 112 tests, including the original 11 MC tests and five new regressions for adapter/evidence mutation, metadata and the actual failed HTTP revision contract. Actual browser creation followed by a whitespace-only revision saved INCOMPLETE/revision 2; both Content studio and the old SUPERSEDED review rendered without crashing. Initial revision history and old review are retained. Remote CI and actual review/merge are recorded on PR #11 separately.

## CS failed-intake web acceptance · 27 October 2026

Danny-authorised GR-INT-01 integration, based on merged AP main dc1b60b; MC PR #11
is a separate repaired branch. HTTP intake now commits assess outcomes, the view
renders evidence failure/reassessment and refreshes errors; no CS module/schema/
model change. All 107 offline tests passed, including 11 new CS HTTP tests.
Actual browser missing-policy receipt, corrected-evidence revision 2 and subsequent
confirmation-error refresh passed in an isolated database on 5663. The Founder
handoff in this negative probe used the existing service; policy changes were
controlled test fixtures, not a new application editing feature. Independent DB
readback: one CS record, no approval/effect and stock unchanged at 12. Full CS/GR
acceptance remains partial. Remote CI, owner review and Jira publication receipts
are recorded separately on the PR; no whole-module completion is inferred.

## Combined MC/CS integration checkpoint · 27 October 2026

PR #11 merged as 8bcc329 after an explicitly authorised AI-assisted review through
dyangwong and passing required checks. PR #13 has merged that main into its task
branch; both MC and CS implementation and bilingual evidence sections are retained.
The combined tree passed **123/123 offline tests in 15.884 s** on Mac Python 3.9.6,
repository provenance (110 source files / 41 tracked cases), JavaScript syntax
and whitespace checks. The 112/107-test entries above describe their earlier
separate baselines, not the combined tree. Existing browser probes are recorded
above; no new combined browser probe is claimed by this checkpoint.

Danny explicitly requested merging both #11 and #13. For his own #13, this
authorises the documented owner review-layer exception after fresh current-main CI;
self-checking is not a self-Approve or an independent human review. The previous
#12-only authorisation is not being reused. PR #13's remote head, fresh CI, actual
merge and Jira receipts are recorded on GitHub/Jira after they occur. Whole MC, CS
and GR acceptance and real CS/MC model integration remain open.

## GR-INT-03 source ZIP / fresh-directory Windows rehearsal · 28 October 2026

**Scope/version.** Danny / M1 authorised local deployment verification and local
commits only. Internal GR-INT-03 is not a Jira key; repository mapping has no
deployment child key. Jira unverified / update pending; external Jira was neither
read nor written by explicit request. No BA starter/teammate claim, business
feature, live CS/MC, Canvas upload, push or merge. Clean local main e141427
fast-forwarded to current origin/main **515bfa537e31a01b9e9a24400a7112f8103babb3**;
no newer main existed at fetch. Branch: GR-INT-03-zip-windows.

**New environment evidence.** Windows 11 Pro 25H2 / 26200.9711 x64; system and new
venv Python 3.14.5; Windows PowerShell 5.1; Git 2.51.0.windows.1; Node 22.19.0;
driver 617.42, RTX 5070 Ti Laptop 12227 MiB. Initial D free 210.60 GiB. No existing
project/model process or listener on the selected ports was found. Baseline
Windows Verify passed **123 tests in 36.202 s**, provenance **110 source files /
41 tracked cases**, and JavaScript syntax. The Mac 123-test timing is historical,
not substituted for this run. Counts include 12 AP HTTP, 11 CS HTTP and 16 MC
tests in addition to the earlier 84-test suite; no tests were changed.

**Archive/extraction.** Existing scripts/package_source.py produced 5,565,726 bytes,
110 files, from that clean source. SHA-256:
`6d6517d837137db65def0223db449f8e0a8dd5c3943e1ecd15be1fb1fa040fb0`.
Names exactly matched the tracked file list; every member matched source bytes.
No .git/.venv/var/database/key/model/old output/private report was included.
Reusing the output name exited 2 and preserved its hash. Extracted into previously
nonexistent `D:\elec5620_project\rehearsals\20261028-515bfa5\fresh source retry`.
Both setup runs passed; the config hash stayed unchanged. New venv executable and
beauty_company.__file__ both resolved inside that directory, with inherited Python
and BEAUTY path overrides removed. Complete new-directory Verify passed **123
tests in 40.384 s**, 110-file/41-case provenance and JS syntax, without .git.

An initial external-controller list comparison counted the trailing empty Git
entry and aborted before extraction/startup. The empty destination and original
ZIP were retained; filtering that empty entry fixed the controller, not project
code. Separately, the browser sandbox refused writing a screenshot on D; the
screenshot was saved under the authorised C output directory instead. Neither
attempt is counted as an application failure or a successful deployment probe.

**Actual mock browser workflow.** New app on 127.0.0.1:5670, new
var/mock-browser.sqlite3. Customer login -> ORD-1001 intake -> Founder CS/CO-to-BA
handoff -> grounded Mock recommendation -> current Customer confirmation -> exact
AP review. The existing approval_recording fixture caused RECORDING_FAILED.
Independent SQLite: no decision ID, no committed-decision audit/effect, stock 12.
Only this app was stopped/restarted with the same DB. Its persisted failure view
offered Recover saved decision. Browser recovery saved APPROVED/DELIVERED, one
decision audit, zero effects, stock 12; three repeated actual HTTP recoveries kept
the same decision. Later Customer browser confirmation saved RESOLVED and one
simulated actionRef effect; three repeated confirmations kept one effect and
stock **12 -> 11**. Exact action/revision/actionRef and product/fact/price/budget/
fragrance/version were independently checked in SQLite. This is the actual newly
merged AP web recovery, superseding the 25 October absent-button limitation.

**Actual fresh-app/model path.** The old model runtime was stopped; the existing
owner-private profile was verified and started using its model workspace's
StartModel in 20.535 s (includes checks). No reinstall/download/weight migration.
Official runtime ready and /v1/models reported qwen3.8-flash-next-gyro-gyro-s.
Strata 0.2.1, Terminal 0.1.46.1, bundled Python 3.12.15, engine 0.1.46 CUDA 13;
8192 context, one request, vision/MTP off, saved VRAM reserve 1536 MiB unchanged.
The fresh app used 127.0.0.1:5671 and new var/live-browser.sqlite3. An initial
health-only launch used absolute -LlmConfig against the original private config;
before any BA consultation it was restarted with a separately created fresh
var/llm.rehearsal.json (120 s / 512 tokens / loopback8080 / exact model ID). Setup
also preserved that existing file's hash. No old app config is needed thereafter.

Actual Customer browser submission saved **COMPLETED / simulated:false / P-101**,
with **Live BA recommendation**. Independent SQLite checked saved product/facts,
integer-cent price/budget, fragrance, stock and version; zero approval/effect.
The current engine log recorded **297 prompt tokens in 7496 ms and 25 generated
tokens in 1223 ms**. One sample is not a general benchmark. A loaded snapshot had
1967 MiB free VRAM and about 4.0 GiB available RAM. MC stayed MOCK, csIntent
NOT_CONNECTED, and an actual fresh-app CS coordinate request still returned
503 / LIVE_HANDOFF_NOT_CONNECTED. Real CS/MC was not connected or expanded.

**Dependencies/limits.** Mock runs from packaged code/static assets with new local
state and installed Python; Node is verification-only, Git packaging-only. Live
BA additionally depends on the pre-existing Windows Strata installation, model
files/profile/private runtime/driver and loopback service; it does not depend on
old workspace application imports or an old app config. No deployment-script or
business-code change was necessary; only existing bilingual guides/status/evidence
were updated. Original config/database hashes and the 56-file model size/mtime
inventory remained unchanged at the browser checkpoint. Raw evidence stays in
ignored var/rehearsal-20261028-515bfa5/ and the fresh directories' var folders.

The original 41 acceptance groups remain tracked at their existing statuses; this
does not promote full cases/modules to PASSED. Formal Canvas upload/download,
final package identity/re-extraction, clean machine/network, teaching-team software/
cached-model approval, overnight/sleep/reboot/long-context/concurrent use, real
CS/MC and broader Stage 2 acceptance remain separate. A later documentation-only
source package must retain its own commit, SHA-256 and fresh-directory recheck
receipt outside the ZIP rather than pretending the earlier archive hash applies.

## Frozen rehearsal package receipt · 28 October 2026

The final documentation-inclusive ZIP is frozen at source commit
`f7bb141f6e35c7846989adccf58841b9e128a978` (local branch GR-INT-03-zip-windows),
110 files / **5,579,703 bytes**, SHA-256:
`5be88639cdd33415dadc77c0e6bfdc286b34b50e4635be2568ee01f4543e6ba3`.
Its non-document files are byte-identical to the validated main 515bfa5 source.
This after-the-fact receipt is a subsequent documentation-only commit: it does
not change the ZIP or pretend its source commit equals the later receipt HEAD.

A second unused extraction at
`D:\elec5620_project\rehearsals\20261028-f7bb141\final fresh source`
passed repeated Setup/config preservation and independent import-origin checks.
Its new venv ran **123 tests in 36.100 s**, provenance (110 files / 41 cases)
and JavaScript syntax successfully, without .git or old application imports.

Actual authenticated HTTP on final extracted ports 5680/mock and 5681/live
repeated the CS -> BA -> Customer -> AP -> simulated-effect chain. AP recording
failed with no authority/effect; after app restart, saved-intent recovery plus
three repeats kept one decision and zero effects. Customer confirmation plus
three repeats kept one effect, same actionRef and stock 12 -> 11. The earlier
515bfa5 package has the actual browser acceptance; this final-package repeat is
actual HTTP automation, not another browser acceptance claim.

One actual final-package BA request saved COMPLETED/simulated:false/P-101 in
**2.780 s**, using the same existing model instance and a separate new-directory
config. Independent SQLite readback verified full saved payload, facts, stock,
price/budget, fragrance and version; zero approvals/effects. After the run-owned
model was stopped with its exact instance guard, the final app remained healthy;
another request saved **INCOMPLETE/LLM_UNAVAILABLE/simulated:false**, with no
product and no mock fallback. Both final apps and the run-owned model stopped.
Original config/database hashes and all 56 model-file size/mtime entries match
the preflight inventory. No code/script/model/dependency change was necessary.

Raw final reports/logs/DBs are ignored. Archive and machine-readable source/hash/
verification receipt were copied to the local handoff output directory. No Jira
read/write, remote push/PR/merge or Canvas upload occurred. GR-INT-03 remains an
internal rehearsal label; formal Canvas download, venue prerequisites/permission,
clean-machine/network, real CS/MC and wider Stage 2 acceptance remain unverified.
