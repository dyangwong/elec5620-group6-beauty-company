# Reference provenance and public redaction

English is the maintained primary version. [中文阅读副本](../zh-CN/reference/README.md).

The authoritative source is the final local Stage 1 report identified by
`docs/source-manifest.json`. It remains unchanged locally. The public repository
contains `stage1-report-public.pdf`, a **privacy derivative**, not a byte-identical
original. All 63 physical pages, models and requirement content are retained;
25 student-ID occurrences on 11 pages are redacted, and PDF metadata is removed.
The text excerpt replaces student IDs with `[STUDENT_ID_REDACTED]`. Names and
module ownership remain so the five members can identify their assigned chains.

The manifest records the original SHA-256, derivative SHA-256, original page count,
redaction scope/page log and excerpt hash separately. `team.json` and `tasks.json`
remain bound to the original source fingerprint. The task packet exposes both
original and reference hashes; validation checks the actual portable derivative.
Do not describe a redacted file as hash-identical to its original or alter source
hashes to make unrelated changes pass. A privacy derivative is not a new approved
design revision. Source authority and PROPOSED design status are unchanged.

The unredacted local `stage1-final-report.pdf` is explicitly ignored. Its original
text excerpt is retained only under ignored `var/private-reference/`. Neither is
included in source archives. Original course folders and the old prototype remain
outside this repository. Other reference excerpts are original-source text, not a
substitute for model-diagram inspection or evidence of completed acceptance.

If an official report revision is adopted, record its original fingerprint and
impact, then intentionally regenerate/sanitise its public reading derivative.
Do not fill absent policy values or rewrite requirements during redaction.
