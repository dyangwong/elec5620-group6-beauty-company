# Local verification record

English is the maintained primary version. [中文阅读副本](zh-CN/VERIFICATION.md).

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
