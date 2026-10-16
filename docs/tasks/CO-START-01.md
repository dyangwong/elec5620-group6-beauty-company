# CO-START-01 · Validate and record failed handoffs

English is the maintained primary version. [中文阅读副本](../zh-CN/tasks/CO-START-01.md).

Owner: M5 / Guiyu Liu. Prepared and unclaimed. CO-M-01 / CO-UC-01;
CO-F-01/02. CO is a coordination control, not another AI business agent.

## Source and reading

CO-FR-01/02/03; CO-AC-01/02/03/04; CO-NFR-01/02/03.
Acceptance subsets CO-T-01/02/03/04/08. Read reference PDF pages 9–10, 18–19,
27–30, 35, 41, 47–48, 53–54 and 58–59. Inspect CO-CL/ACT/SEQ/STM and
the GR-S-01 Founder-initiation and minimal-context requirements.

Read the current coordination module, the CS coordinate caller and existing
CO/GR tests. The CS caller is context, not permission to rewrite CS ownership.

## Current gap

The current advice handoff assumes all required keys exist and BA is available;
it synchronously calls BA without the complete invalid-context/unavailable-role/
failed-tool record path. Exceptions can prevent a useful safe status from being saved.

## Implement this slice

Validate allowed target and required authorised context before recording a
successful handoff. Missing/invalid decision-relevant fields need clarification or
safe incomplete handling, without silently guessing. Preserve the minimal allowlist;
unrelated identities, credentials and order details do not enter BA context.

Use module-local role/tool fixtures to distinguish invalid context, role
unavailability, malformed/failed result and known successful advice. Retain the
work, handoff, actual failure and recovery/escalation reason when storage works.
A receipt cannot complete either the handoff work or the CS business request.
Expose storage failure without claiming a saved trace. Keep the current successful
CS→BA contract compatible; broader generic dispatch is a later task.

## Scope

Own `beauty_company/modules/coordination.py`, new `tests/test_co.py` and
`docs/modules/CO.md`. Prefer existing records/payloads for the initial failure
records. No shared schema, CS/BA implementation, approval policy, HTTP or frontend
edits are part of this task. Record any necessary integration contract explicitly.

## Observable completion conditions

- Valid handoff records only permitted context and a distinct advice result;
  CO does not mark the whole workflow COMPLETED before required CS work is saved.
- Missing/invalid context causes an explicit safe state and no target dispatch.
- Unavailable target causes recorded failure/escalation/cancellation as applicable,
  not acknowledgement or completion. No automatic retry is introduced.
- Failed/malformed tool results remain failure; no invented successful result.
- Persistence failure cannot claim a fully recorded handoff. Unknown business
  effects remain distinct from known no-effect read failures.
- Existing Founder-started exchange, AP boundaries and CS actionRef reconciliation
  regressions continue to pass.

Run full and CO-specific tests, map exact conditions and pending UI integration.
Optional CO-F-03 remains OFF. Retry exhaustion, generic role adapters and the
complete stillUnknown/intervention lifecycle stay in the backlog.
