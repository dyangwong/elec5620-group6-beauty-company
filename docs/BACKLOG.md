# Work after the five starter tasks

English is the maintained primary version. [中文阅读副本](zh-CN/BACKLOG.md).

These are planning records, not sprint commitments or completed features. Actual
Jira mappings are identified explicitly; unmapped labels are not Jira issues. START task IDs and GR-INT IDs are internal handoff labels, never invented
Jira keys. `tasks.json` currently contains only the five executable starter briefs.
Finishing a starter does not automatically authorise every later item below.

## Full Stage 1 feature coverage remains the target

| Chain | Core still to complete after its starter | Optional feature retained |
|---|---|---|
| BA-F-01/02 | Full need clarification/resumption; actual LLM perception; independent generated-output validation; catalogue/inventory failures and evidence refresh; conditional BA review; remaining lifecycle/recording checks | BA-F-03: verified available alternatives, explicit differences, no silently relaxed constraint; ON/OFF cases |
| CS-F-01/02 | Routine return/exchange/refund-request workflows with declared policy, current confirmation, proper escalation; complete cancellation/read/write/storage paths and LLM intent interpretation | CS-F-03: permission-aware status notification, failure/OFF independent of core result |
| MC-F-01/02 | Real brief interpretation; actual permitted draft-media/video or approved labelled fallback; full quality/claim validation; decision-save recovery/cancellation/stale callbacks and review lifecycle | MC-F-03: approved-concept variant generation, each new draft freshly reviewed |
| AP-F-01/02 | Complete risk/unknown-risk routing, BA/CS/MC/CO local adapter mappings, notification, cancellation/expiry via declared policy, full current-scope and delivery/recording lifecycle | AP-F-03: assisted linked corrected resubmission; REQUEST_REVISION itself remains core |
| CO-F-01/02 | General authorised role adapters, explicit context/revision correlation, unavailable/unknown outcomes, reconciliation/escalation/intervention, complete result-save/cancellation lifecycle | CO-F-03: bounded eligible automatic retry, OFF/exhaustion safe escalation; no blind uncertain-effect retry |

All fifteen features remain tracked, not silently removed because optional features
are currently OFF. Select later tasks using remaining conditions in the original
41 case groups, all twenty NFRs and the current traceability gaps. Split broad items
into bounded tasks before a member starts them. Do not reinterpret safe incomplete
outcomes as permission to leave all normal success behaviour unimplemented.

## Shared integration work to scope and assign

| Internal label | Scope | Dependency / present state |
|---|---|---|
| GR-INT-01 | Wire reviewed service changes into shared HTTP/UI, visible error/recovery states, complete client/server contracts and browser tests | Prepared scope only; split by ready backend changes. Each owner supplies result examples and affected callers. Shared frontend is not assigned to five agents simultaneously. |
| GR-INT-02 | Provider-neutral real model adapter/config, actual tool/schema/claim validation, model failure handling and evidence; preserve deterministic test mode | **RESERVED TO DANYANG WANG**, [KAN-15](https://uni-team6-elec5620.atlassian.net/browse/KAN-15). Contract/handoff prepared; deployment and implementation not started. Others preserve seams/fakes and do not duplicate provider work. See [LLM_INTEGRATION.md](LLM_INTEGRATION.md). |
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
