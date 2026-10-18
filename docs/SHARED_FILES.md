# File ownership and integration rules

English is the maintained primary version. [中文阅读副本](zh-CN/SHARED_FILES.md).

Defaults follow the five Stage 1 chains at Danny's request. They express task scope,
not repository access control, formal member acceptance or evidence of contribution.
The initial scaffold was prepared with AI assistance; no member is credited with
completing it merely because it contains their module.

| Area | Default scope |
|---|---|
| `beauty_company/modules/beauty_advisor.py`, `tests/test_ba.py`, `docs/modules/BA.md` | BA / Danyang Wang |
| `beauty_company/modules/customer_service.py`, `beauty_company/adapters/after_sales.py`, `tests/test_cs.py`, `docs/modules/CS.md` | CS / Siyuan Lei |
| `beauty_company/modules/marketing.py`, `tests/test_mc.py`, `docs/modules/MC.md` | MC / Zhengdu Wei |
| `beauty_company/modules/approval.py`, `tests/test_ap.py`, `docs/modules/AP.md` | AP / Jiaxuan Ren |
| `beauty_company/modules/coordination.py`, `tests/test_co.py`, `docs/modules/CO.md` | CO / Guiyu Liu |
| `docs/tasks/*.md` | Corresponding task owner; preserve the source baseline and distinguish proposal/evidence |
| `docs/traceability.csv` | Each member updates only their prefix rows; GR rows require group integration evidence |
| `docs/tasks.json` | Update only the relevant task record with actual evidence; preserve others' concurrent changes |

New module-local helpers/tests may be added when their ownership is explicit.
Do not move shared catalogue functions merely to make a local task easier: record
the affected imports/contracts and integrate that change separately.

## Shared surfaces

`contracts.py`, `store.py`, `application.py`, `http.py`, `adapters/mock.py`,
`web/app.js`, `web/styles.css`, `web/index.html`, `tests/test_workflows.py`,
CI/scripts, root guidance and source metadata affect multiple chains.

The first BA/CS/MC/CO tasks leave these surfaces unchanged. AP-START-01 has the
specific shared exceptions listed in tasks.json: additive AP intent persistence,
the AP decision/recovery facade and the existing AP audit regression only.
This scope is prepared now; it does not require another permission request to
perform those ordinary local edits once the member is authorised to do that task.

For any additional shared change:

1. State the exact surface, before/after contract, affected callers and reason in
   the task/PR. Preserve every other chain's behaviour.
2. Coordinate a bounded shared task instead of having five agents rewrite the
   same web file or schema. Danyang's previous Stage 1 integration work is context;
   it does not prove acceptance of every future Stage 2 integration assignment.
3. Apply backward-compatible additions where feasible. Include caller, persistence,
   adapter, model-deviation and regression changes together when semantics change.
4. Seek the relevant teammate review for shared changes; it is a collaboration
   recommendation, not a mandatory GitHub approval gate. Do not interrupt routine local
   changes for repeated approval when their scope is already authorised.

A service task can finish its declared slice with an explicit pending HTTP/UI
integration note. It cannot claim a browser feature is complete without that
integration. Do not expose a changed service result through an old renderer that
assumes success. New failed-state views need the shared integration task.

## Branches, claims and conflicts

- Start from current shared main, then use the real Jira-key branch suggested in
  tasks.json (for example, `KAN-11-cs-start-01`). Follow START_HERE.md for member
  intake, visible scope and reporting; each changed area must belong to the task.
- Fetch/read current task claims before duplicate work; the local starter helper
  performs no network check and cannot guarantee a task is still unclaimed.
- Do not claim other members' chains or expand the task because unrelated gaps
  exist. Record those in BACKLOG rather than silently implementing everything.
- Preserve dirty files from other work. On a shared working directory, separate
  Git worktrees/checkouts may be used when needed; ordinary separate laptops
  already have independent checkouts. No worktree setup is performed by onboarding.
- On a conflict, compare current changes and merge purposefully. Never overwrite
  another task record, remove its test or regenerate the entire shared file blindly.
- Human review, real Jira state and actual commits/PRs are evidence. Local identity,
  generated prose, planned tasks and commit counts alone are not.

The unredacted original PDF remains immutable local evidence. The public reference
and excerpt redact student IDs only (PDF metadata is also stripped), with a
declared transformation and distinct hashes. Never replace a source hash with a
derivative hash or publish the ignored original. A new official/local
report revision requires an explicit source update and impact review, not editing
the old report, its extracted text or stored hashes to make checks pass.

## LLM reservation

Danyang Wang owns shared GR-INT-02 (deployment, common adapter/configuration,
provider prompts, future CS intent interface and mode reporting); see
[LLM_INTEGRATION.md](LLM_INTEGRATION.md). Other members keep existing injected
seams and provide local fakes/examples, preserving their original file scopes.
Changes inside another member's module still require bounded coordination; this
reservation does not transfer their business logic ownership to the integrator.
