# Jira work and GitHub linkage

English is the maintained primary version. [中文阅读副本](zh-CN/JIRA.md).

The human created elec5620_team6 and connected GitHub for Jira. On 17 October 2026,
AI-assisted configuration established the following real work-item mapping. This
is a setup snapshot; use Jira for current assignment, claims and workflow state.

[Board](https://uni-team6-elec5620.atlassian.net/jira/software/projects/KAN/boards/2) ·
[Backlog](https://uni-team6-elec5620.atlassian.net/jira/software/projects/KAN/boards/2/backlog).
One team-managed software space, key KAN. No site access, billing or account
permissions are changed by this setup. Existing KAN-1/2 are preserved.

| Chain | Epic | Starter task | Planned owner / verified assignment at setup |
|---|---|---|---|
| BA | KAN-4 | [KAN-10 / BA-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-10) | Danyang Wang / assigned |
| CS | KAN-5 | [KAN-11 / CS-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-11) | Siyuan Lei / assigned |
| MC | KAN-6 | [KAN-12 / MC-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-12) | Zhengdu Wei (Jira display ZHENGDU WEI) / assigned |
| AP | KAN-7 | [KAN-13 / AP-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-13) | Jiaxuan Ren / unassigned, account not matched |
| CO | KAN-8 | [KAN-14 / CO-START-01](https://uni-team6-elec5620.atlassian.net/browse/KAN-14) | Guiyu Liu / unassigned, account not matched |
| Shared | [KAN-9](https://uni-team6-elec5620.atlassian.net/browse/KAN-9) | Integration & Verification; later child tasks scoped separately | Per concrete task |

All five starters were created To Do, Medium priority, labelled starter and linked
to the correct epic. Ticket descriptions contain source/acceptance IDs, bounded
files, observable conditions, English/Chinese brief links and completion limits.
Assignment is planned responsibility, not a personal work claim, implementation,
review or contribution. No guessed invitation was sent. Real/local model setup
remains deferred. Six epics are not six business agents; BA/CS/MC remain the three.

## Work sequence

1. Identify the member and read START_HERE, the module/brief and source models.
2. Check the actual Jira task, assignment/claim, blockers and current repository.
   The helper prints a local mapping only. No connection means a human must verify
   shared state; do not pretend the integration gave the agent access to Jira.
3. Use the real key in branch, commit and PR title. For CS, for example:

   ```text
   Branch: KAN-11-cs-start-01
   Commit: KAN-11 Handle policy evidence failures
   PR:     KAN-11 [CS-START-01] Preserve truthful eligibility outcomes
   ```

   The registry supplies a Jira-prefixed suggested branch for every starter.
4. To Do → In Progress when actual work starts; Verification for self-check, tests,
   PR and any relevant teammate review. The GitHub policy allows self-merge after
   required checks and does not require an outside Approve.
5. Mark Done only when this task's declared conditions have evidence, the PR is
   merged, and module docs/traceability record the exact tested subset and remaining
   integration gaps. One service slice does not complete a module or acceptance group.
   Failed/unmerged PRs and receipts are not completion. Do not auto-Done on merge.

Backlog is enabled. Sprint dates/goals and work commitment require actual team
planning; no sprint is started and no new due date, recurring reminder or work log
is fabricated. Bug is available for discovered defects; existing Story/Subtask
work types remain. Blocked work needs a clear flag/reason, not a false success.

## Keep one work tracker

Jira owns current workflow. docs/tasks.json owns the versioned member/requirement/
file-scope/Jira-key mapping, not a competing live board. Preserve others' records.
Explicit personal claiming may update claim_state/claimed_by with evidence; planned
Jira assignment alone leaves local UNCLAIMED intact. Update stale setup snapshots
honestly rather than inventing a live sync. Do not make duplicate GitHub issues for
routine Jira tasks. GitHub for Jira links development data only when real work keys
are included; it does not implement or validate the feature.

The KAN-9 repository-maintenance PR verifies development linkage for this setup;
actual results belong in VERIFICATION. The integration epic remains broader work,
not complete merely because this configuration PR merges.
