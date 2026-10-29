# BA handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/BA.md).

## BA conditional review checkpoint · 30 October 2026

Use a new synthetic database and a free loopback port; preserve existing demo data.
Start default mock with `scripts/windows.ps1 -Action Start -Mode mock -Port 5770 -Database var/ba-review-demo-new.sqlite3`.
Customer → Product advice: `A moisturiser for dry skin. Budget AUD 10. Fragrance-free required.`
Confirm needs, observe INCOMPLETE/no match, expand **Ask Founder to review an unresolved
product question**, enter a product-only question and tick explicit sharing consent.
**Send consented review request** must show a saved AP ID/REVIEW_PENDING, not success.
Sign out/in as Founder, open Review queue, inspect **Unresolved BA product question**
and exact consultation/revision/evidence. Choose Request revision/Reject/Approve with
a reason. Approval only permits Customer reconfirmation/fresh assessment; unchanged
AUD10 still cannot match. Correcting to AUD60 is explicit new scope, never an implied
budget increase. Routine supported advice still completes without AP.

For live evidence, reuse the installed model/config as WINDOWS_LLM.md; use another
free port/new database with `-Mode strata -LlmConfig var/llm.strata.json`. Start no
second provider/install/download. A service-off assessment can be reviewed, but
approval cannot make inference succeed while the service remains off. Restore only
your owned runtime, then Customer reconfirms for fresh evidence/model validation.
Stop only app/model instances you started. Tests/review decisions here are synthetic;
no order, stock, payment, settlement or publication effect is authorised.

Implementation: new modules/ba_review.py, existing natural ba_intake.py, additive
Company/HTTP/UI and minimal AP BA dispatch. 17 boundary tests in tests/test_ba.py;
281 full tests and actual Windows mock/live browser evidence in VERIFICATION.md.
BA-T-05/07 remain PARTIAL; broad semantics, structured-route parity and final
release acceptance remain. BA-START-01 is not newly claimed.

## BA lifecycle checkpoint · 29 October 2026

Current branch `KAN-15-ba-lifecycle-recovery`, starting at
478d522694ca381b2ba3c3c5e3711a77fb04133a; fetched main remains
515bfa537e31a01b9e9a24400a7112f8103babb3. Danny authorised this KAN-15 continuation;
no BA-START-01/Jira claim or teammate attribution was changed. Additive shared
HTTP/UI/facade changes and draft-snapshot filtering require later shared review.

Use the Windows launch instructions and a fresh database, then Product advice:

1. Complete a natural-needs consultation. Open **Replace the full request**, enter
   `Gentle cleansing.`, save, and observe missing budget/fragrance questions.
   The same ID advances revision; old advice is historical, no longer current.
   Answer with `Budget AUD 40. Fragrance-free required.`, review and confirm.
2. **Cancel consultation** is available before completion. While inference is
   pending, **Refresh** retrieves its saved revision and leaves cancel enabled.
   A successful cancel ends this session; start a new consultation to continue.
3. For an intentional test, Founder can select **BA final advice save failure
   (draft retained)** in Activity trail's Simulation controls, then Customer
   confirms needs. The card remains incomplete, with **Recover saved result**.
   Restarting the application with the same test database preserves that draft.
   Recovery checks evidence and writes once; it does not require a running model.
4. **Retry this attempt** is distinct: it is available for interrupted/incomplete
   work without a draft, creates a new revision and may call the model again.
   It is user-initiated, never automatic; it requires fresh Customer confirmation.

Actual Windows checks cover these controls, a real in-flight cancellation with
late HTTP 409, and recovery of real BA advice after model shutdown/app restart.
169 offline tests pass (147 prior + 22 new); one prior failed-save assertion now
checks the durable-draft/INCOMPLETE contract instead of the earlier ACTIVE-only gap.
Read VERIFICATION.md for the SQLite fault/audit checks and independent catalogue checks.

Remaining: legacy structured-route lifecycle parity, BA review/escalation/failures,
the complete catalogue/inventory failure matrix, general language/medical safety,
optional alternatives and cross-machine/ZIP/Canvas acceptance of these changes.
Full disk loss cannot promise a durable draft or cancellation; storage failures
are disclosed. Existing BA-T-07 remains PARTIAL; this is not all BA/Stage 2 complete.

## Earlier round 1 · BA needs checkpoint · 29 October 2026

Current Danny-authorised KAN-15 work adds `modules/ba_intake.py`, bounded extraction
in `adapters/needs.py`, the shared adapter capability, three HTTP routes and a
standalone Customer UI. This explicitly authorised shared slice overlaps BA-T-01
and selected BA-T-02/03/04/05/07 conditions; it is not an automatic BA-START-01
claim or completion. Starter task records/other owners were not changed.

Try it on Windows using the existing WINDOWS_LLM.md prerequisites and scripts:
start with a new database via `scripts/windows.ps1 -Action Start -Mode mock -Port 5690 -Database var/ba-demo-new.sqlite3`.
Sign in as the fictional Customer, open Product advice, enter
`A moisturiser for dry skin.`. Answer the budget/fragrance questions with
`My budget is AUD 60 and fragrance-free is required.`. Check the same consultation
ID and new revision; review/correct the fields, then press **Confirm needs & find
a match**. Only then should P-101 appear. Mock is explicitly labelled. The former
structured form remains under **Use explicit structured fields (existing mode)**.

For live use, first check/reuse the installed model as in WINDOWS_LLM.md; use
`-Mode strata -LlmConfig var/llm.strata.json` with another free port/new database.
Do not download a model or copy the private configuration into source. Stop only
your own app with the matching script/port; manage a model only if you started it.
This round actually tested isolated 5690/5691 databases, then stopped both apps
and its own model instance. Normal demo databases/config/model weights were preserved.

Remaining: full completed-record revision/cancellation, BA review/escalation and
review failures, complete provider/catalogue/inventory failure matrix, general
language/medical interpretation and optional verified alternatives. Saving a result
can fail safely into persisted ACTIVE; no automatic BA storage recovery is claimed.
Chinese mock fixture coverage is offline; actual model browser evidence this round
uses English. All BA case groups remain PARTIAL/NOT_STARTED as appropriate.
Older dated boundary statements below are historical.

Default Stage 2 continuation: Danyang Wang, at Danny's request; no shared claim is
inferred. Begin with [BA-START-01](../tasks/BA-START-01.md) and the explicit member
entry in [START_HERE](../../START_HERE.md). Complete only its declared slice first.

Stage 1 owner: Danyang Wang. BA-M-01 / BA-UC-01 / BA-F-01..03.
Code: `beauty_company/modules/beauty_advisor.py`; provider contract in
`beauty_company/contracts.py` and `beauty_company/adapters/mock.py`.
New task tests belong in `tests/test_ba.py`; existing tests use `test_ba_t_*`.
Original specs: source sections 4–6,
8.2 and 13.3.1. See traceability for incomplete conditions.

Initial slice: explicit need/budget/fragrance constraint; mock proposes a catalogue
candidate; independent ID/fact/stock/constraint checks; consultation evidence saved.
BA changes no order, stock, price, payment or public content. CO receives only the
permitted advice context; no order identity or credentials enter the model input.

Remaining after both 29 October slices: legacy structured-route lifecycle parity,
BA review, the complete provider/evidence failure matrix, general language understanding
and optional verified alternatives. Bounded clarification/resumption and stale-output
suppression are now covered as described above. Medical keyword blocking
is a limited fixture, not a complete clinical-scope detector. A model-provided list
of claims is insufficient to validate arbitrary generated prose.

## Shared KAN-15 boundary update · 21 October 2026

BA-START-01 remains separate/unclaimed by this work. The shared integrator added
opt-in standalone BA transport, mode/error mapping and Company.consult with
evidence recheck before save. No clarification/resumption/revision/cancellation
starter lifecycle was implemented. tests/test_llm.py covers the bounded transport
and HTTP slice. One actual BA model path now passes; see ../WINDOWS_LLM_RUNTIME.md.
Full BA lifecycle/perception acceptance and the separate starter remain open.
