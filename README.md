# Beauty Company · ELEC5620 Stage 2

English is the maintained primary version. [中文阅读副本](README.zh-CN.md).

Initial local prototype for **AI-Powered One-Person Beauty Commerce and Content
Company**, Group 6. Three business capabilities (BA/CS/MC), with human approval
(AP) and coordination/recovery (CO). The original prototype is reference only;
no legacy code, database, credential or media was imported.

**Joining with your own coding agent? Start at [START_HERE.md](START_HERE.md).**
It maps the five report members to their modules and prepared first tasks. Tell
your agent your full name/member ID/module; it can read the task packet and begin
authorised local work. Real/local model setup is deferred and is not a prerequisite.

**Current status: initial working simulation, not the completed Stage 2 submission.**
Default model responses are deterministic mocks. KAN-15 adds opt-in standalone
BA transport; one actual model-backed BA path now passes. See [runtime repair and evidence](docs/WINDOWS_LLM_RUNTIME.md) and [Windows setup](docs/WINDOWS_LLM.md). Media is a storyboard placeholder,
not a video file. No production settlement, shipment or public posting exists.
The implementation baseline remains PROPOSED until the team records acceptance.

## Run locally

Python **3.9+**, standard library only. No package installation, API key, Node,
Docker, cloud account or internet connection is needed for this initial version.

```sh
python3 -m beauty_company
```

Run that command **from this repository directory**. Open
<http://127.0.0.1:5620>. Stop with Ctrl+C. Use `--port 5621` if the default is busy.
On Windows, use `python` or `py -3` if `python3` is not available; keep the same
remaining arguments. Native Windows app execution is now verified on Python
3.14.5; use [repeatable Windows commands](docs/WINDOWS_LLM.md).
Data persists in ignored `var/company.sqlite3` across restarts. To create a fresh
isolated demo without deleting existing data:

```sh
python3 -m beauty_company --port 5621 --db var/fresh-demo.sqlite3
```

Do not expose the loopback development server to the internet. The shared local
demo accounts and simple HTTP adapter are not production identity/hosting.

| Workspace | Username | Demo password | Fixture order |
|---|---|---|---|
| Founder / Operator | `founder` | `founder-demo` | Can review all demo workflows |
| Alex / Customer | `customer` | `customer-demo` | `ORD-1001` |
| Sam / Customer | `customer-2` | `customer-demo` | `ORD-2001` |

The sign-in screen fills the appropriate shared demo password. Credentials are
fictional, intentionally documented for the local demonstration. Server-created
opaque sessions, ownership checks and CSRF checks still enforce the role boundary.

## Try the integrated slice

1. Sign in as Alex. Open **After-sales care** and submit the default request.
2. Sign out, sign in as Founder, open **Customer requests** and choose **Start
   advice handoff**. This is the explicit Founder initiation in GR-S-01.
3. Return as Alex. Inspect the proposed product/evidence; choose **Confirm proposal
   & request review**. This creates a pending AP request and executes nothing.
4. As Founder, open **Review queue**, enter a reason and approve the exact scope.
   Approval commits before delivery and executes no business action.
5. As Alex, confirm the simulated exchange. The service records one effect,
   decrements simulated stock once and CS/CO save the confirmed outcome.
6. Read **Activity trail**. No real payment/shipment has occurred.

Use separate browser profiles/private windows for simultaneous Founder/Customer
sessions; ordinary tabs share cookies. Refresh after another session changes data.

For a separate MC slice, Founder opens **Content studio**, creates a mock draft,
reviews its exact revision, then revises it to demonstrate fresh review. No video
or public post is generated. A mock draft approval is scoped only to that draft.

Founder **Activity trail → Simulation controls** can inject one post-execution
timeout, outcome-recording failure or committed-decision delivery failure. CS
then queries the same actionRef, or AP redelivers the same committed decision.

## Validate

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 scripts/start_work.py --list
```

Tests use temporary databases, never the running demo data. They cover selected
conditions from Stage 1, not all 41 case groups. Read `docs/traceability.csv` for
partial coverage and remaining conditions. The public
[GitHub repository](https://github.com/dyangwong/elec5620-group6-beauty-company)
is live. The [initial GitHub CI run](https://github.com/dyangwong/elec5620-group6-beauty-company/actions/runs/38865450983)
passed on Python 3.9 and 3.13, including all 37 tests, provenance checks and JS
syntax. Main requires PRs and passing checks. Teammate PRs require at least one
non-author Approve; only dyangwong retains the own-PR exception. On 18 October,
GitHub showed slei0644 and ZhengduWei as write collaborators; remaining invitations
need verified usernames. The [Jira KAN space](docs/JIRA.md)
now has six epics and five scoped starter tasks; assignment is not a personal claim.

## Start here when contributing

- `AGENTS.md`: progressive reading and invariant rules for coding agents.
- `START_HERE.md`: member/agent onboarding with a copyable first instruction.
- `docs/team.json` / `docs/tasks.json`: report-grounded member map and five prepared tasks.
- `docs/SHARED_FILES.md`: ownership and bounded shared-change/integration rules.
- `docs/BACKLOG.md`: remaining core/optional features and deferred shared work.
- `docs/STATUS.md`: implemented scope and material limitations.
- `docs/VERIFICATION.md`: checks actually executed and their practical limits.
- `docs/REQUIREMENTS.md`: five chains and fifteen feature IDs.
- `docs/CONTRACTS.md`: API, scope, state and transaction boundaries.
- `docs/modules/`: module responsibilities and handoff notes.
- `docs/COLLABORATION.md`: proposed Jira/branch/PR workflow and done criteria.
- `docs/DECISIONS.md`: provisional implementation choices and open decisions.
- `docs/reference/`: privacy-redacted report PDF (all 63 pages/models), text/rubric excerpts and provenance. The unredacted original stays local and is ignored.
- [Git workflow](docs/GIT_WORKFLOW.md): PRs, passing checks and non-author approval for teammates; documented own-PR exception for dyangwong.

This is the intended Git repository root. Keep the course folder and old prototype
outside it. The tracked archive must contain everything needed to run the app;
the original report is evidence, not an application runtime dependency.
