# Agent entry point

English is the maintained primary version. [中文阅读副本](AGENTS.zh-CN.md).

This is an initial implementation of ELEC5620 Group 6 Stage 2.
Start with `START_HERE.md`. Before feature implementation, resolve the human's
explicit full name/member ID/module against `docs/team.json` and select only that
member's task in `docs/tasks.json`. Never infer identity from Git/system login,
an application demo account or an old local profile. If the identity is missing or
conflicting, ask one concise clarification before member-specific edits. If the
human has clearly named a matching member/task, proceed with authorised routine
local work without redundant approval. A read-only assessment or Danny-authorised
repository maintenance/integration task does not automatically claim a member's
starter or implement their feature.

Read `docs/STATUS.md`, `docs/REQUIREMENTS.md`, `docs/CONTRACTS.md`,
`docs/COLLABORATION.md`, `docs/JIRA.md`, `docs/SHARED_FILES.md`, the relevant module guide and
the selected task brief. `python3 scripts/start_work.py --member <declared-member>`
prints the reading/scope packet; it performs no shared claim or external action.
The optional saved profile is ignored local session data, never identity proof.
Inspect the task's model pages in the privacy-redacted `docs/reference/stage1-report-public.pdf`;
text excerpts do not preserve every diagram. Source hashes are in the manifest.

## Authority and evidence

1. Explicit current human instructions and official course requirements.
2. The final local Stage 1 report, identified by `docs/source-manifest.json`.
3. Explicitly recorded team decisions in `docs/DECISIONS.md`.
4. Derived requirements/contracts and implementation.
5. Legacy prototype and new AI suggestions (reference only).

The retained report calls its design PROPOSED. Implementing it does not invent
formal team/tutor approval. Do not restore the old rule that Google Drive is
canonical. Do not access, copy or change sibling course/report/prototype folders
unless the current human task calls for it. No legacy certificate, credential,
database, session, ZIP, Git directory or customer media belongs in this repo.

## Invariants

- Exactly three AI business roles: BA, CS and MC. AP and CO are shared controls.
- Current adapters are deterministic mocks. Never describe this as a working live
  LLM multi-agent system or a generated video. No real settlement/publication.
- Real/local model deployment is deferred, not an onboarding prerequisite. Do not
  install/download/connect providers or request keys as part of a starter task.
- Validate evidence independently of model output; UNKNOWN stock is not available.
- Authentication comes from server-side sessions, not user IDs or role fields in
  request bodies/headers. Enforce role and record ownership on the server.
- Review receipt, committed decision, delivery, business execution and recorded
  success are separate. AP never executes the business action.
- Bind decisions to origin, exact action, revision and actionRef. Revisions need
  fresh confirmation/review. Duplicate delivery cannot cause duplicate effects.
- Persist intent before effects. Query uncertain actionRef outcomes before repeat.
  Storage recovery does not execute the action. Never invent rollback.
- Optional features are currently not implemented/OFF. Core safety must work with
  all five OFF; REQUEST_REVISION remains core.
- Policy, budget/stock fixtures and session lifetime are declared demo choices,
  not real company policies or approved numerical acceptance thresholds.

## Working rules

- Use Python standard library for the current local skeleton and buildless web
  assets. New dependencies or framework migration need a recorded rationale,
  reproducible setup and relevant tests; do not silently add a second stack.
- Keep changes within the assigned requirement chain. Shared contract changes
  must update affected callers, docs, fixtures and tests together and be flagged
  for the affected owners' review. Do not claim that review has occurred.
- Use the prepared primary/shared scope in the task registry. BA/CS/MC/CO starter
  tasks avoid common HTTP/UI/schema files; AP has narrow explicit exceptions.
  Add tests in the assigned per-module test file rather than all five members
  rewriting the shared regression file. Preserve others' work and claim records.
- Check actual shared task status before duplicate work. READY/UNCLAIMED is a
  prepared local record, not a live Jira claim. No GitHub accounts are inferred.
- Never invent Jira IDs, sprint history, feedback, member work or contribution
  percentages. Record AI assistance honestly. No Jira/GitHub write is implied.
- Run `python3 -m unittest discover -s tests -v` and the checks relevant to the
  changed workflow. Map evidence in `docs/traceability.csv`; a partial case stays
  partial until every documented condition is exercised.
- Run the app with `python3 -m beauty_company`. Bind to loopback only. Keep data
  under ignored `var/`; do not expose this development server publicly.
- Complete work means runnable code, accurate docs, evidence and known limits.
  Passing the initial test suite is not completion of all 41 acceptance cases.

## Documentation language

English documents at the existing root/docs paths are the maintained primary
versions and the default coding-agent entry. Root `*.zh-CN.md` and `docs/zh-CN/`
are Chinese reading copies, not a second requirements baseline. If wording differs,
use the English document subject to the authority order above. Update the English
first and synchronise its Chinese copy in the same change; if translation is
pending, visibly mark the Chinese copy as outdated. Preserve IDs, paths, commands
and state values. Keep member/task/status data in the existing shared JSON/CSV
files; never create a separately editable translated task registry. Original report
PDFs remain unchanged locally. Public derivatives redact student IDs/metadata only,
with original and derivative hashes recorded separately in the source manifest. This policy concerns documentation,
not application UI or generated business-content language.

## Git workflow

Follow `docs/GIT_WORKFLOW.md`: use a task branch and a PR to main; required checks
must pass. The author may self-check and merge their own PR, with zero mandatory
external approvals. This is not a self-Approve review. Seek a relevant teammate's
review for shared contracts/schema/authority changes, but do not claim it happened.
Never push directly, force-push or delete main. Repository writes and PR merges
follow the current human task authorisation; a local feature task does not by
itself authorise external publication or merging. Protect the local
unredacted report; never add ignored files with git add -f.

## Jira handoff

The team-managed KAN space and real starter tasks are recorded in docs/JIRA.md,
docs/jira.json and each task's jira_key/jira_url. Prefer the actual Jira key in
branch/commit/PR names, keeping START IDs for requirement traceability. Jira is
current workflow authority; the registry is a versioned mapping/snapshot and the
local helper does not query it live. Assignment is planned responsibility, not a
personal claim or completed work. Confirm actual claim/status without overwriting
other members. Use To Do → In Progress → Verification → Done; Done requires the
declared task conditions and evidence, not only a merged PR. Do not auto-start a
sprint, set deadlines, enable agents, invite guessed accounts or auto-complete work.
GitHub for Jira exposes development links; it does not grant a coding agent Jira
read/write access. Use an authorised Jira connection/browser or give the human
precise updates to record; never claim an unsent Jira update happened.

Apply the progress checkpoints in docs/JIRA.md before implementation, at PR
handoff and after merge. Fill the PR template's Jira progress handoff with the
observed status/date, applied or pending update and next owner/action. Update
affected module/traceability/implementation gaps in the implementation PR. Preserve
setup snapshots; do not mirror every Jira move into JSON or infer live status from
STATUS.md. Without authorised Jira access, supply exact pending updates and state
the limitation; never report the workflow as synchronised until it was observed.
