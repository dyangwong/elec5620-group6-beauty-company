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
