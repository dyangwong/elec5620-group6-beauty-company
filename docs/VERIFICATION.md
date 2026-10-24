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
