# Current implementation status

English is the maintained primary version. [中文阅读副本](zh-CN/STATUS.md).

Created 16 October 2026. Initial local foundation, not a final submission.
This file describes implementation at its repository revision, not live task
progress. Use Jira for current claims/status; the dated setup sections below are
historical. Update affected behaviour/gaps here in the implementation PR.

## Working slices

- Loopback web app with Customer and Founder workspaces; same-origin JSON API.
- Fictional accounts; server-created opaque sessions, role/ownership checks and CSRF.
- BA default mock advice plus opt-in standalone local Strata consultation;
  explicit constraints and independent catalogue/fact checks remain in force.
  One real BA HTTP path is verified in WINDOWS_LLM_RUNTIME.md; full natural-language
  clarification and unrestricted generated-text grounding remain incomplete.
- CS **exchange-only** intake with explicit synthetic policy; Founder-initiated CO
  handoff to BA; current Customer confirmation and exact-scope AP review.
- CS service-level assess intake retains missing/conflicting/unavailable policy outcomes;
  confirmation and the effect adapter recheck current evidence. Legacy HTTP intake
  still raises on failed policy; retained failed intake views need shared integration.
- AP approve/reject/request-revision, atomic decision/request/audit commit, separate
  delivery and same-decision redelivery. Delivery never executes business work.
- AP durable decision intent, RECORDING_FAILED on a failed decision commit and
  storage-only same-decision recovery. A pending intent grants no authority.
- AP Founder HTTP/UI recovery with the displayed revision, saved intent and exact
  scope checks; recording-failure fixture, accurate failed card and separate delivery.
- CS persistent actionRef, simulated service effect, once-only stock decrement,
  post-write-timeout lookup and outcome-recording recovery without repeat effects.
- MC deterministic script and three storyboard cards, labelled mock media;
  exact-revision review and revision history. No generated video file.
- Local event trail, source snapshots, initial tests and CI configuration.

## Prepared teammate handoff

- English primary documentation with corresponding Chinese reading copies;
  shared task/identity data and unchanged original evidence.
- START_HERE with explicit member identification and a first-message example.
- Report-grounded five-member map, one scoped READY/UNCLAIMED starter per member,
  per-task acceptance/source/model references and shared-file boundaries.
- Read-only task packet helper; optional ignored local profile, no shared claim.
- Complete privacy-redacted Stage 1 PDF, including models missing from excerpts;
  unredacted original unchanged locally/ignored, with distinct source/reference hashes.
- Remaining core/optional features and shared integration work kept in BACKLOG.

No starter implementation was executed as part of onboarding/publication. All five
were UNCLAIMED in the onboarding snapshot; no member endorsement, real-model setup, Jira claim or human
contribution percentage is inferred. A shared initial commit and public GitHub
repository have now been published; see the collaboration status below.

## Not implemented or not yet established

- Full natural-language perception/planning and live CS/MC tools beyond the verified
  standalone BA slice; schema/claim validation for unrestricted live output.
- Full BA revision/cancellation/review lifecycle and all medical/unsafe-language cases.
- Returns/refunds, routine policy alternatives, full CS cancellation and evidence
  failure modes beyond the KAN-11 service subset; default HTTP/UI retained failed
  intake integration. Initial fixture routes every exchange through human review.
- General CO dispatch/role unavailability/cancellation, unknown external outcomes,
  independent distributed services and automatic retry.
- AP expiry, cancellation and complete risk/unknown-risk classification. The
  decision-recording failure state machine and durable same-decision-intent recovery
  and its bounded HTTP/UI recovery control are implemented and tested. Queue/
  notification failure and the remaining lifecycle/risk cases remain open.
- Real/generated mock video files, media failure/quality workflows, persistent MC
  failed-generation states, full generated-claim validation and review-save recovery.
- All five optional features (OFF/not implemented); no enabled-mode claims.
- Production security, retention rules, rate limiting, TLS or public deployment.
- Full 41-case acceptance, full UML implementation audit and clean-machine/Canvas
  rehearsal. See the traceability file rather than inferring full case completion.
- Full Jira iteration/claim/review history, completed teammate invitations, team approval, human work
  attribution or contribution percentages. GitHub publication is recorded separately;
  it does not establish those outcomes.

## Honest demonstration boundary

Database persistence, authority guards, audit commit, action identity and recovery
logic execute locally. Standalone BA can explicitly use the verified local model;
MC/media remain mocks and CS intent is not connected. The default mock alone is
not evidence of live AI capability or a completed multi-agent system.
The policy eligibility flag, always-review fixture, prices, stock and eight-hour
demo session lifetime are explicit synthetic choices, not approved business policy.

The same local SQLite store holds control records and a separately committed
simulated service-effect table. This models independent effect/receipt outcomes;
it does not prove atomicity/idempotency of any real external provider.

## Published collaboration baseline · 16 October 2026

[Public repository](https://github.com/dyangwong/elec5620-group6-beauty-company),
initial commit `570ebc3adc948ff54523920cb93b5092a2013956`. The initial CI run passed
on Python 3.9/3.13 with all 37 tests, source checks and JS syntax checks. Main
protection was applied and read back: PR required, zero required outside approvals,
both CI jobs/current-main/conversation checks, administrator enforcement, no force
push or deletion, squash-only merge. `docs/repository.json` records the setup receipt.
The maintainer handoff is updated through a task branch/PR after enabling protection.
No teammate has yet been invited because their GitHub usernames are not provided.

## Jira configuration · 17 October 2026

The human-created team-managed KAN space now has six epics (KAN-4..9) and five
scoped starter tasks (KAN-10..14), all created To Do/Medium with starter labels and
correct parents. BA/CS/MC are assigned to verified displayed member accounts;
AP/CO remain unassigned after full-name searches found no existing matching user.
Backlog is enabled, the review column is Verification and Bug was added. KAN-1/2
remain intact. No sprint, deadline, reminder, model service, agent delegation or
personal claim was created. See JIRA.md for current workflow and jira.json for the
setup snapshot. This supersedes earlier no-Jira setup statements, not evidence of
any starter implementation or full module completion.

## Shared LLM reservation · 18 October 2026

Danyang Wang reserved GR-INT-02 / KAN-15. Contract/ownership and cross-machine
handoff are prepared in LLM_INTEGRATION.md; runtime remains mock-only, deployment
and CS intent port are not implemented. Member starter scopes/claims are unchanged.

## Teammate review policy · 18 October 2026

Teammate PRs now require at least one non-author Approve plus existing CI. The
active review ruleset and own-PR exception for dyangwong are documented in
GIT_WORKFLOW and repository.json. Earlier zero-review/no-invitation sections are
dated history: two write collaborators were observed today. No application or
member task/acceptance state changed as part of this policy update.

## KAN-15 local Windows integration · 21 October 2026

Supersedes the earlier implementation-not-started snapshot only for this local
branch. Added an opt-in shared Strata BA adapter, minimal evidence/strict JSON,
typed safe failures, standalone consultation outside write transactions with
catalogue recheck, capability/record mode labels and repeatable Windows commands.
Default mock behaviour and teammate implementations/claims are preserved; MC is
explicitly mock, CS intent is not connected and live HTTP CS handoffs are blocked
pending coordination. Original 38 and expanded 45 offline tests pass on Python
3.14.5, with repository/JS checks and Windows mock HTTP/start/stop validation.
Strata Terminal/signature check passed; engine/model installation is blocked by
restricted-process private-directory permissions and execution policy. Actual
live-configured HTTP failure saved INCOMPLETE/LLM_TIMEOUT with a failing probe;
successful real model BA inference, full GR-INT-02 and Stage 1 acceptance remain
pending. Jira is inaccessible/unverified, no PR or remote write occurred. Exact
machine, selected versions, download budget and handoff: [WINDOWS_LLM.md](WINDOWS_LLM.md).

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

KAN-13 / AP-START-01 added a durable AP decision intent, the RECORDING_FAILED
state machine and storage-only same-decision recovery. A failed decision commit
leaves no committed envelope, no delivered approval and no business effect; the
intended Founder, kind, reason and exact scope stay recoverable from storage, and
a restarted service can commit that same intended decision exactly once. This is a
local SQLite simulation of a storage failure, not a real provider outage, and it
does not add the HTTP/UI recovery control (GR-INT-01), expiry or risk routing.

The implementation is open as [PR #9](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/9)
from branch `KAN-13-ap-start-01` into `main`. The Python 3.9/3.13 workflow runs
succeeded on commit `c433ef0`; a non-author approval from a reviewer with write
access is still pending, and the Jira KAN-13 workflow update is still pending for
an authorised person.


## CS/AP and LLM branch integration · 25 October 2026

PR #7 merged as `6e505f0`; AP PR #9 was updated with that main, independently
verified with 75 offline tests, approved through an explicitly authorised
AI-assisted dyangwong review and normally merged as `840ac70` after fresh required
Python 3.9/3.13 checks. The dated earlier open/pending-review records are history.

PR #8 now incorporates that main without replacing either owner's work. Six
English/Chinese documentation conflicts were resolved by retaining AP recovery
and Windows LLM evidence together. The combined candidate passes 84 offline
tests, repository/source checks (107 source files, 41 tracked case groups) and
JavaScript syntax. This Mac integration does not rerun Windows deployment or
real Strata inference; the earlier Windows evidence remains scoped as recorded.

MC PR #11 is excluded pending its failure-rendering and mutable-media validation
fixes/re-review. CS retained-intake HTTP/UI, AP HTTP/UI recovery, real CS/MC model
paths and complete acceptance remain open. Jira verification is separate from
whole-module/epic completion; no task is marked Done merely because of a merge.

## Windows post-CS/AP regression · 25 October 2026

Integrated commit 966dae4 (main 840ac70) passed all 84 offline tests on Windows
Python 3.14.5 and 3.12.15, provenance and JS checks. Actual BA browser inference,
independent saved-fact validation, timeout/unavailable non-success, CS/AP exact
scope/customer confirmation/one-effect HTTP flow and durable AP-service recovery
were exercised in fresh databases. Existing model/config/data were preserved.
MC remains mock; live CS handoff limits remain accurate. A bounded local stop
script fix in this update safely handles inaccessible PID metadata.
AP web recovery is absent; its recording-failed card also uses misleading
superseded fallback text, recorded for affected-owner/shared UI follow-up.
The regression run did not touch PR #11, BA starter claims or Jira. See the dated
VERIFICATION checkpoint; broader acceptance and actual owner review remain open.

## AP HTTP/UI recovery · 26 October 2026

KAN-9 / GR-INT-01, explicitly authorised by Danny. Based on main e141427,
branch KAN-9-ap-web-recovery adds the original-Founder/current-revision recovery
endpoint, accurate RECORDING_FAILED view, saved-intent recovery button and demo
fault option. Decision/recovery failures refresh persisted state immediately.
Existing AP commit/delivery semantics and two-argument callers are retained;
no schema, teammate business module or model change. All 96 offline tests passed,
including 12 new AP HTTP tests. Actual browser failure/recovery and independent
SQLite readback showed one decision audit, zero effects and stock 12 unchanged.
No full AP/GR acceptance, remote CI, owner review or Jira update is inferred.
CS failed-intake UI and MC PR #11 remain separate. See VERIFICATION.md.

## MC failure repair · 27 October 2026

KAN-12 PR #11 now retains failed mock drafts/revisions and safely renders their failure states, including superseded review cards. Independent evidence/storyboard snapshots close mutable-adapter validation gaps. 112 integrated offline tests and actual browser failed revision/old-review rendering passed. Initial HTTP failed-draft creation, live MC, general prose grounding and full MC acceptance remain open. See the PR for remote checks/review/merge; no member claim is reassigned.
