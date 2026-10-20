# BA handoff

English is the maintained primary version. [中文阅读副本](../zh-CN/modules/BA.md).

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

Remaining: real LLM need extraction with clarification/resumption, full schema and
factual validation, asynchronous revise/cancel/stale-output suppression, BA review,
all provider failures and optional verified alternatives. Medical keyword blocking
is a limited fixture, not a complete clinical-scope detector. A model-provided list
of claims is insufficient to validate arbitrary generated prose.

## Shared KAN-15 boundary update · 21 October 2026

BA-START-01 remains separate/unclaimed by this work. The shared integrator added
opt-in standalone BA transport, mode/error mapping and Company.consult with
evidence recheck before save. No clarification/resumption/revision/cancellation
starter lifecycle was implemented. tests/test_llm.py covers the bounded transport
and HTTP slice. One actual BA model path now passes; see ../WINDOWS_LLM_RUNTIME.md.
Full BA lifecycle/perception acceptance and the separate starter remain open.
