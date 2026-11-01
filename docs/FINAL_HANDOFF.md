# Final delivery handoff · 1 November 2026

English is maintained primary. [中文阅读副本](zh-CN/FINAL_HANDOFF.md).
Prepared for Danyang Wang (Danny / M1), continuing AI-assisted integration and
delivery under KAN-9 / KAN-21. This is the current continuation entry point;
dated STATUS, VERIFICATION and readiness entries remain historical evidence.
Official course material and the identified final Stage 1 report retain authority.

## Version and evidence boundary

| Item | Verified checkpoint | Remaining condition |
|---|---|---|
| Published application | main `12054e43697024eb7e5c0047f30711d43115d9f0`, merged [PR #23](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/23) | Inspect current remote main and any later changes before selecting the final candidate. Record its full SHA. |
| Latest repair | MC blocks bounded conflicting product facts before generation/review; AP validates registered actions, origin, scope and policy, with CS recovery checks | 319 Mac tests and required Python 3.9/3.13 CI passed. New Windows and real-model acceptance is not established by those results. |
| Existing Windows evidence | [PR #22](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/22) and [final package receipt](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/22#issuecomment-6538163217): real BA, CS→CO→BA, MC text/template MP4, failure/restart recovery; 307 tests from fresh final-package extraction | Bound to d30dc019/content-identical candidate, not automatically PR #23. Raw IDs, screenshots and runtime receipts remain on the gaming laptop. The final-package pass did not rerun inference. |
| Old frozen source | `ELEC5620_Group6_Source_d30dc019.zip`, 6,050,713 bytes; SHA256 `3d783103a3f93419f60b5efdfb79f4198cedf467de63f7cc26728cd756906392` | Preserve it; it excludes PR #23. Generate a distinct final ZIP. |
| Meeting drafts | [PR #24](https://github.com/dyangwong/elec5620-group6-beauty-company/pull/24), head `121773ec92ab9afdad5dd087ce4ff24c6c04fc4e`, open at this checkpoint | Three bilingual **unconfirmed drafts**, not evidence of completed meetings. Actual dates, participants, feedback and decisions need human confirmation. |
| Other Mac-only work | Branch `KAN-21-assessor-readme`, commit `16eb05d`; README and Chinese copy only | Not published or included in main. Private transfer kit preserves a Git bundle. Inspect separately; do not silently include its claims or merge it. |

The 319-test count describes this application baseline, not 319 official acceptance
cases or a percentage complete. Older 281/286/306/307 counts and 124/133-file counts
are version-specific. Determine actual counts for the selected final source.
This handoff is documentation; publication/merge and Windows results must be
recorded separately. No new application/model/Canvas acceptance occurred here.

## Course requirements to preserve

- Stage 2 rubric: **20 marks** — Stage 1 implementation/completeness 7; AI agent
  capabilities 4; Agile experience 4; effective advanced technology 5. Read
  [the complete rubric excerpt](reference/stage2-rubric.txt) and the original PDF
  in the private course kit, including the contribution form.
- Source due **1 November 2026, 11:59 PM** in the supplied rubric. Check the actual
  Canvas deadline/timezone and submission settings; this handoff does not verify
  submission or grant an extension.
- Teacher announcement supplied by Danny: Week 13 deployment must use source
  downloaded from Canvas and be performed on-site. Own computers, preinstalled
  environment/tools/dependencies and personal network are allowed. Check
  application/model/tool connectivity and rehearse the full process.
- Teacher Q&A supplied by Danny: mock responses or fake-data demonstrations affect
  marks. Demonstrate actual model inference; clearly label synthetic commerce
  fixtures and simulated settlement. An offline mock pass is only a diagnostic.
- Staff will inspect Jira backlog, burndown and Agile meeting logs. Keep actual
  PR/review/iteration evidence and honest meeting records. Commit history alone
  does not prove meetings, feedback or agreed contribution shares.
- Read the Lab notes in the private kit, especially Lab 2's feature expectations.
  Five F-03 features are labelled optional in Stage 1 but currently absent/OFF;
  that label is not proof they are exempt from completeness or Lab expectations.
- Use the official private contribution statement: five member percentages in
  each of the four criterion rows total 100%. Current human agreement is
  unverified; never infer percentages from commits or AI output. Names/IDs stay
  in the private submission, not the public repository. Inspect the existing
  supplied form before assuming it is blank or replacing it.

Announcement summaries above are transcribed from Danny's supplied text, not a
fresh Canvas fetch. The private kit retains that provenance and missing originals.

## Read before acting

1. AGENTS.md and this handoff; use Danny / M1 as the explicitly declared maintainer,
   not a teammate starter claim. Read docs/GIT_WORKFLOW.md and docs/JIRA.md.
2. docs/REQUIREMENTS.md, docs/CONTRACTS.md, docs/source-manifest.json and relevant
   docs/modules guides. Inspect diagrams in docs/reference/stage1-report-public.pdf
   (all 63 pages retained with student IDs redacted), or the private final report.
3. docs/WINDOWS_LLM.md and docs/WINDOWS_LLM_RUNTIME.md for actual scripts/configs;
   docs/EVIDENCE_INDEX.md for receipts; current entries in STATUS/VERIFICATION.
   Older pending/publication/count statements are historical, not new tasks.
4. The private transfer kit's README, course originals, user-supplied teaching
   clarifications and historical coverage/Agile audits. Ignored output and private
   files do not transfer through GitHub. Their old absolute Mac links are provenance,
   not Windows paths. Use their copied files and the current repository instead.

Exactly BA, CS and MC are the three AI business roles. AP and CO are deterministic
controls. The shared LLM adapter can use one local model; three model installations
are not required. Commerce is simulated. MC produces bounded LLM text and a silent
FFmpeg template advert, not generated scenes/audio. CS implements a bounded
disputed-exchange flow; CO is bounded CS→BA coordination, not a general scheduler.
Five optional features and broad acceptance/NFR coverage remain incomplete.
The 41-case ledger is 37 PARTIAL / 4 NOT_STARTED at this checkpoint; do not promote
all cases or epics to Done because tests or a PR pass. The historical 15-feature
audit predates PR #23: its MC/AP diagnostic holes were subsequently repaired.

## Windows continuation sequence

1. **Inventory without overwriting.** Inspect old repo branch/status, uncommitted
   changes, running app/model processes, existing tools/configs and raw acceptance
   receipts. Preserve all of them. No reset/clean/blind stash or replay of already
   squash-merged branches. Read the transfer kit before asking Danny to restate
   course requirements. Keep the old model-owning workspace in place.
2. **Select one committed candidate.** Fetch GitHub, inspect main/open PRs and
   record the full SHA. If this handoff is not merged yet, obtain it from remote
   branch `KAN-21-final-handoff` or the private kit. For source, clone main into a
   new, nonexistent sibling directory. Do not mix in PR #24 or the saved README
   branch automatically. Record later documentation merges in the final SHA.
3. **Create a new source ZIP and extract elsewhere.** Use
   `python scripts/package_source.py --output output/<new-name>.zip` from the
   clean committed checkout. Verify archive paths against `git ls-files`, file
   bytes against the checkout and extraction against the archive. Record source
   SHA, file count, ZIP size/SHA256; exclude runtime data, models and private kit.
   Use a new extraction, venv, config names, synthetic DB and free ports. Confirm
   imports resolve inside that extraction, not an old workspace/PYTHONPATH.
4. **Reuse existing dependencies and model.** Inspect the actual Windows paths;
   prior owner was `D:\elec5620_project\elec5620-group6-beauty-company`.
   Strata and its model/profile, FFmpeg/ffprobe/font are already prepared there.
   StartModel, if needed, belongs to that existing owner, not the new extraction.
   No InstallModel, downloads, upgrades, model moves or overwritten profiles.
   Prior endpoint `http://127.0.0.1:8080/v1`, timeout120s, max_tokens512 are
   historical inspected values; verify the current config and `/v1/models`.
   Model name/version must be observed, not replaced with a suggested new model.
5. **Verify from the extraction.** Run scripts/windows.ps1 Setup then Verify;
   explicitly record provenance and `node --check beauty_company/web/app.js`.
   Expected baseline regression is 319 tests; investigate deviations. A skipped
   JavaScript check is not PASS. Do not install another stack to make counts fit.
6. **Run actual combined live acceptance.** Create private configs referencing
   the existing model and installed media tools. Inspect exact options in the
   Windows guide; use Start with Mode strata, LiveMc, LlmConfig and VideoConfig,
   a new DB and free loopback port. Use separate browser profiles for Customer
   and Founder (ports can share the session cookie). Perform the table below.
7. **Package and submission closure.** If a blocking defect is fixed, use a task
   branch/PR and required CI, then create/retest a new committed-source archive.
   Never repair an extraction and attribute success to unchanged ZIP bytes.
   Danny uploads the final source plus required contribution material to Canvas,
   downloads the actual submitted ZIP, checks its hash and rehearses fresh
   deployment from it. Canvas writes require a separate explicit instruction.
8. **Evidence and cleanup.** Keep a short English receipt plus Chinese copy under
   ignored output: date, candidate/ZIP hashes, environment, mode, IDs, screenshots,
   PASS/FAIL/NOT RUN and remaining work. Retrieve old evidence instead of rerunning
   solely to recreate screenshots. Stop only this run's owned processes; a shared
   pre-existing model stays running. No LAN/firewall/public hosting changes.

| Acceptance | What to observe and retain |
|---|---|
| BA live | Free-text needs → missing-field clarification → explicit Customer confirmation → grounded in-stock advice; correction/cancel and conditional review stay truthful. Save record/revision IDs and inference evidence. |
| CS→CO→BA live | Owned ORD-1001 exchange → Founder handoff → grounded BA proposal → Customer proposal confirmation → exact Founder AP → final Customer confirmation. Record request/handoff/actionRef/review/decision IDs. Zero effects before final confirmation, one after; P-101 stock12→11; replay remains one. |
| MC live/media | Catalogue-grounded brief → actual live script → playable/downloadable 15s template MP4 → hash-bound current-revision review; revision needs fresh review. Record draft/revision/review IDs and MP4 SHA256. |
| PR #23 guards | Conflicting bounded fragrance facts retain SOURCE_CONFLICT/INCOMPLETE, no model/media/review; corrected new revision can proceed. Unknown/malformed AP action or caller risk override cannot obtain approval receipt or business effect. Use existing regression/service tests for deliberately invalid inputs; do not invent a web control. |
| Recovery/failure | Final-save failure → same DB/config app restart → same saved revision/artifact, no repeated inference/render or duplicate review/effect. Model/endpoint unavailability produces explicit failure with no mock fallback. Use new synthetic data and inspect effect/file evidence. |
| Deployment | Clean package extraction, correct import paths, current tests/provenance/JS, real model/FFmpeg connectivity, then actual Canvas download/hash/source-based deployment. Health checks alone do not prove inference. |

Suggested Customer input: “Please exchange my item for a fragrance-free moisturiser
for dry skin. My budget is AUD 60.” Suggested MC input: “Create an energetic teaser
highlighting the catalogue fact ‘50 ml’.” These are bounded examples, not guarantees
of arbitrary semantic understanding. Authentication and exact-scope approvals remain
server-side; no bypass to obtain a smoother demonstration.

## Minimal Agile and collaboration closure

- Retrieve actual review/iteration evidence and hold/confirm real short review and
  retrospective records. Drafts remain drafts until real facts are supplied.
- Jira KAN board2 is canonical. Keep a brief checkpoint with source/PR, actual
  result, safe evidence link and next gap; no long repeated comments or blanket
  status/owner/sprint changes. If access/authority is absent, mark update pending.
- Its Sprint start was extended to17Oct because original Jira tasks began then;
  actual Sprint start and membership were30Oct. Extending the date did not recreate
  earlier membership or remaining-work history. The HRP board3 reconstruction
  experiment is isolated: a fresh Sprint could start, but historical native
  burndown was not validated. It is not original Agile evidence and is not a
  prerequisite to submission. Do not fabricate history to smooth the chart.
- Normal GitHub task branches, PRs, current required checks and review rules apply.
  Teammate PRs need a non-author Approve. Danny's documented own-PR review-layer
  exception is not self-Approve or permission to skip CI; future publication and
  merging follow the current human instruction. No guessed contributor shares.

## Copyable Windows-agent instruction

```text
I am Danyang Wang (Danny / M1), continuing ELEC5620 Stage 2 final delivery.
Read docs/FINAL_HANDOFF.md first (or the private transfer kit copy / remote
KAN-21-final-handoff branch if not on main), then its source requirements and
Windows/evidence guides. Course originals are in my private transfer kit.
Inspect current local/remote versions and existing Windows evidence before edits.
Application checkpoint: main12054e4, PR23 MC/AP guards merged,319 Mac tests/CI;
old d30dc019 Windows307/real-flow evidence and ZIP do not establish new acceptance.
Preserve the existing workspace, model, tools, configs, databases and receipts.
Use a clean committed candidate→new ZIP→fresh extraction route; reuse the installed
model/FFmpeg and run current regression/provenance/JS, real BA/CS→CO→BA/MC,
new guards and failure/restart recovery. Record actual IDs/hashes/screenshots and
PASS/FAIL/NOT RUN. Freeze features; fix only demonstrated delivery blockers.
Do not install/upgrade models, replay old branches, invent meetings/contributions
or treat mock runs as live evidence. Inspect PR24 drafts and the saved Mac README
separately; do not merge automatically. Keep Jira brief and only when authorised.
First report observed version, evidence already available, blockers and the exact
bounded next action. Do not automatically publish/merge or submit to Canvas.
```
