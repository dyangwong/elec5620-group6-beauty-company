## Behaviour

Describe the concrete trigger, resulting behaviour and reason for the change.

## Traceability

- Actual Jira task key and link:
- Internal handoff task / declared member / module:
- Stage 1 requirement / feature / use case:
- Relevant model / state / contract:
- Acceptance case and conditions covered:
- Why each changed area belongs to this task; any authorised scope deviation and affected owners:

## Verification

Commands/scenarios actually executed and observed results. Identify mock/live.
Describe remaining untested conditions; do not mark an entire case passed for one subset.

## Integration and limits

Shared contract/schema impact, affected owners, deviations and remaining risks.
List any shared-file exception and pending HTTP/UI/model integration explicitly.
Use docs/SHARED_FILES.md; do not overwrite other members' registry/traceability rows.
Record AI assistance and human review accurately; do not invent approval.

## Jira progress handoff

Follow docs/JIRA.md (Chinese copy: docs/zh-CN/JIRA.md). Keep the actual key in the
branch, commit and PR title. For maintenance on an epic, identify this bounded
change; merging it does not complete the epic.

- Jira status / claim actually observed, checked date and actor (or access unavailable):
- Jira update actually applied and PR/evidence link recorded (or `Jira update pending`):
- Affected module / traceability / STATUS updates, or why none are needed:
- Remaining conditions, blockers and next action:
- Person responsible for checking acceptance and updating Jira after merge:

Move to Verification when ready for verification. After merge, mark Done only
with evidence for every condition of this task; otherwise record the remaining
work and appropriate state. Never equate a green CI or merged PR with full acceptance.

If model-related: confirm alignment with docs/LLM_INTEGRATION.md, identify any
shared interface change coordinated with Danyang Wang, and distinguish preserved
mock behaviour from actual live evidence. No duplicate provider client/deployment.

## Required review

- Requested reviewer (default @dyangwong):
- Actual non-author Approve after latest reviewable changes, or pending:
- Review comments resolved / remaining changes:

Teammate PRs must wait for an actual eligible non-author approval and required CI.
New reviewable commits dismiss old approval. Only dyangwong's own PR may use the
review-layer exception after checks; record it as an owner exception, not review.
Do not use that exception for teammate PRs. See docs/GIT_WORKFLOW.md.
