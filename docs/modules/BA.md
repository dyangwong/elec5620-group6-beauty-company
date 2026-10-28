# BA handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/BA.md).

## BA needs checkpoint · 29 October 2026

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

Remaining after the 29 October slice: full completed-record revision/cancellation,
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
