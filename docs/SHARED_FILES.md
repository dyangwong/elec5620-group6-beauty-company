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

## MC advert-template exception · 30 October 2026

Danny / M1 authorised KAN-9 / GR-INT-03 visual polish from main1ad1101:
adapters/template_video.py, original assets/advert, tests/test_mc.py and paired
contract/module/status/verification/release-handoff guidance plus selected MC
traceability evidence. No Marketing/AP/CO/CS/BA business rule, HTTP/UI, schema,
provider signature, dependency, task registry or model installation change.
Zhengdu Wei's original MC ownership/work remains; no KAN-12 starter claim.
Affected-owner endorsement/publication is not inferred from self-checks.


## BA conditional review checkpoint · 30 October 2026

Danny / M1 explicitly authorised the bounded KAN-15 natural BA review integration:
new modules/ba_review.py; natural ba_intake scope/history and connection boundary;
minimal BA origin/receiver hooks in modules/approval.py; Company wiring, HTTP review
route/session callback and existing web views. Tests stay in tests/test_ba.py;
English/Chinese contracts/guides and selected BA/AP/GR traceability update together.
No schema, provider signature/client, dependency/config/model install, CS/MC/CO
business rule or effect adapter change. Preserve Jiaxuan Ren / M4 AP and all original
team contributions; no starter claims/reassignment. Relevant AP/shared-owner review
pending; authorised owner exception/CI is not an independent Approve.

## CS intent/live exchange shared exception · 29 October 2026

Danny / M1 explicitly authorised KAN-15 CS/CO/shared integration with AI assistance:
new adapters/cs_intent.py and modules/cs_flow.py; additive shared llm/mock methods,
BA catalogue-snapshot helper, CS advice-save helper/live legacy guard, staged CO
methods, Company capability/facade, HTTP/session/UI and tests/test_cs_live.py.
Only obsolete CS availability/guard expectations changed in test_llm.py/test_mc.py;
no MC business logic change. Contracts/CS+CO+GR traceability and English/Chinese
guidance updated together. No AP/effect/schema/dependency/config/task-registry change.
Siyuan Lei CS, Guiyu Liu CO and all original member contributions remain; no KAN-11,
KAN-14 or starter claim/reassignment. Affected-owner review remains pending, not
inferred from tests. Danny explicitly authorises his own PR exception after all
required checks, with normal protected merge; no self-Approve/protection change.

## CO failure boundary exception · 29 October 2026

Danny / M1 explicitly authorised this bounded KAN-15 shared increment, AI-assisted:
modules/coordination.py and new tests/test_co.py, plus exactly two existing
web/app.js null guards for missing saved CS needs. Shared contracts, relevant
CO-T rows and bilingual guides record the additive handoff/failure evidence.
No CS business/AP/BA/MC service, HTTP signature, schema, provider, dependency,
task registry or ownership change. Guiyu Liu / M5 remains the original CO owner;
this is not a KAN-14/CO-START-01 claim. Affected CO/CS/shared-owner review pending,
not inferred from tests. No Jira read/write, push/PR/merge this round.

## MC generation recovery checkpoint · 29 October 2026

Danny / M1 authorised this bounded MC generation-save recovery exception under
KAN-15: new modules/mc_generation.py, extracted reusable Marketing checks,
Company facade/snapshot/fault additions, unified campaign HTTP routes and recovery/
retry/cancel UI. New tests stay in tests/test_mc.py; affected contract/traceability
and bilingual guides updated together. No AP implementation/schema/BA/CS/CO/model
transport/dependency change. Original MC attribution/task ownership remain;
affected MC/shared-owner review pending. Local only: no external Jira/PR/merge.


## MC template MP4 checkpoint · 29 October 2026

Danny / M1 authorised the MC-F-02 template MP4 exception under KAN-15. New optional
template_video adapter and media_tools.ps1; additive Company media injection/access,
HTTP current-revision authenticated range/download route, CLI/Windows config switch,
MC artifact validation/review hash fields and UI playback/download labels. Tests stay
in test_mc.py. AP implementation, schema, BA/CS/CO services, task claims and model
transport/config are unchanged. New dependency rationale/setup is documented;
default mock remains independent. MC/shared-owner review pending; no endorsement
or live Jira claim inferred. No push/PR/merge authorised in this local increment.


## MC bounded live-text checkpoint · 29 October 2026

Danny / M1 explicitly authorised bounded real MC text via KAN-15. Changes touch
shared llm adapter + new pure mc_text contract, Company.campaign/mode, opt-in HTTP
dispatch, CLI/Windows switch, MC service/current review action, UI labels/form
fields and tests/test_mc.py. Existing AP implementation, schema, BA/CS/CO services,
task registry, ownership and model config/installation are unchanged. Default mock
and BA-only Strata are preserved. Original Zhengdu Wei MC code remains attributed.
Affected MC/shared-file review is pending; no teammate endorsement, Jira update,
remote PR or acceptance is inferred. This is not authority to add real CS intent,
video, MC cancellation/recovery or unrestricted prose in the same increment.


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
