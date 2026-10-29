# Work after the five starter tasks

English is the maintained primary version. [中文阅读副本](zh-CN/BACKLOG.md).

These are planning records, not sprint commitments or completed features. Actual
Jira mappings are identified explicitly; unmapped labels are not Jira issues. START task IDs and GR-INT IDs are internal handoff labels, never invented
Jira keys. `tasks.json` currently contains only the five executable starter briefs.
Finishing a starter does not automatically authorise every later item below.

## Current CO slice closed locally · 29 October 2026

The first CO priority in the older audit/order below has now been implemented and
verified for existing synchronous read-only CS-to-BA only: 237 full tests and
independent mock browser failure/restart/correction evidence. See STATUS.md and
VERIFICATION.md. Do not restart that slice or generalise it into a queue framework.
Generic CO lifecycle/retry remains open. Next separate choices remain conditional
BA review or a bounded CS gap, then current-source review/release and remaining
case/NFR/media/Agile evidence; no new module scope is automatically authorised by
this checkpoint. Historical planning/order below is retained for provenance.

## Current audit and bounded priorities · 29 October 2026

[STAGE2_READINESS.md](STAGE2_READINESS.md) supersedes the broad initial planning
snapshot below for current implementation/evidence. Real bounded BA/MC, optional
template MP4 and durable generation recovery are implemented; MC decision
redelivery after origin-save failure exists and was newly diagnosed successfully.
Do not implement those again merely because an older row says pending.

Proposed order: (1) retain CO invalid/unavailable/malformed handoff outcomes;
(2) bounded core BA review and CS intent/live handoff/resolution gaps, in separate
scopes; (3) close satisfied cases/NFR/model and media-review evidence;
(4) reviewed release-source ZIP/fresh-directory/venue plus actual Agile/contribution
materials. Exact stop conditions are in the audit. Optional ON remains tracked,
not a prerequisite for the next CO fix. These are proposals, not assignments,
Jira tickets or task claims. No external updates or code implemented this round.

The following starter-era rows retain historical planning context, not a current
list of wholly unimplemented capabilities.


## Full Stage 1 feature coverage remains the target

| Chain | Core still to complete after its starter | Optional feature retained |
|---|---|---|
| BA-F-01/02 | Full need clarification/resumption; actual LLM perception; independent generated-output validation; catalogue/inventory failures and evidence refresh; conditional BA review; remaining lifecycle/recording checks | BA-F-03: verified available alternatives, explicit differences, no silently relaxed constraint; ON/OFF cases |
| CS-F-01/02 | Routine return/exchange/refund-request workflows with declared policy, current confirmation, proper escalation; complete cancellation/read/write/storage paths and LLM intent interpretation | CS-F-03: permission-aware status notification, failure/OFF independent of core result |
| MC-F-01/02 | Real brief interpretation; actual permitted draft-media/video or approved labelled fallback; full quality/claim validation; decision-save recovery/cancellation/stale callbacks and review lifecycle | MC-F-03: approved-concept variant generation, each new draft freshly reviewed |
| AP-F-01/02 | Complete risk/unknown-risk routing, BA/CS/MC/CO local adapter mappings, notification, cancellation/expiry via declared policy; the recording-failure state machine and storage-only same-decision recovery are implemented (KAN-13), so the remaining lifecycle work is queue/notification failure, expiry and the remaining risk/lifecycle cases (bounded HTTP/UI recording recovery is now implemented under GR-INT-01) | AP-F-03: assisted linked corrected resubmission; REQUEST_REVISION itself remains core |
| CO-F-01/02 | General authorised role adapters, explicit context/revision correlation, unavailable/unknown outcomes, reconciliation/escalation/intervention, complete result-save/cancellation lifecycle | CO-F-03: bounded eligible automatic retry, OFF/exhaustion safe escalation; no blind uncertain-effect retry |

All fifteen features remain tracked, not silently removed because optional features
are currently OFF. Select later tasks using remaining conditions in the original
41 case groups, all twenty NFRs and the current traceability gaps. Split broad items
into bounded tasks before a member starts them. Do not reinterpret safe incomplete
outcomes as permission to leave all normal success behaviour unimplemented.

## Shared integration work to scope and assign

| Internal label | Scope | Dependency / present state |
|---|---|---|
| GR-INT-01 | Wire reviewed service changes into shared HTTP/UI, visible error/recovery states, complete client/server contracts and browser tests | Split by ready backend changes; shared frontend is not assigned to five agents simultaneously. AP recording recovery is implemented locally on 26 October: original-Founder/current-scope endpoint, recovery button, accurate failed-state message and demo fault option, with 12 HTTP tests and browser acceptance (VERIFICATION.md). Publication/affected-owner review remain pending. CS retained failed-intake/reassessment views are now implemented in a separate 27 October increment; later MC failure-view contracts are handled by repaired PR #11. Each increment retains its own review/merge receipt. |
| GR-INT-02 | Provider-neutral real model adapter/config, actual tool/schema/claim validation, model failure handling and evidence; preserve deterministic test mode | **RESERVED TO DANYANG WANG**, [KAN-15](https://uni-team6-elec5620.atlassian.net/browse/KAN-15). Local model and one BA path verified after runtime ACL repair; live MC/CS and broader acceptance pending (WINDOWS_LLM_RUNTIME.md). Others preserve seams/fakes and do not duplicate provider work. See [LLM_INTEGRATION.md](LLM_INTEGRATION.md). |
| GR-INT-03 | Full GR-S-01 and separate MC demonstration, GR-T-01..04 audit, full model/feature/NFR consistency, clean source delivery and Canvas/on-site rehearsal | Planned, owner(s) to confirm. Existing local tests/mock demo are baseline evidence only. |
| GR-INT-04 | Publish a common initial Git baseline, invite verified accounts, create real Jira tasks/claims and record actual iteration/review/contribution evidence | Partially executed at Danny's later request: public repository, initial baseline, CI and main protection are live. GitHub invitations await usernames. Jira KAN epics/starters are now created and mapped in JIRA.md; two assignees, actual personal claims/iterations and human adoption remain pending. |

Later media-provider work is separate from the real text-model adapter. A generated
script, a three-card storyboard and an actual video asset are different results.
The Stage 2 rubric's technology criterion requires an effective use case and
evidence; the existence of a framework/model name is not a guaranteed mark.

## Open decisions stay explicit

Use DECISIONS.md for actual adopted choices and reasons. Unknown return windows,
risk/expiry/freshness/quality thresholds, media costs, production retention and
hosting constraints do not become facts because an agent needs a convenient value.
Declared test fixtures are allowed and must stay visibly synthetic. No new deadline,
reminder, sprint schedule, contribution percentage or external action is created here.
