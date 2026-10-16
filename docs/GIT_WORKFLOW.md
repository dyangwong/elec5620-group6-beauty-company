# Git collaboration workflow

English is the maintained primary version. [中文阅读副本](zh-CN/GIT_WORKFLOW.md).

Danny requested a public course repository and a lightweight review process.
Use GitHub Flow: one shared main branch and short task branches. A separate
long-lived develop branch is not required. The repository's actual settings are
the enforcement mechanism; `.github/main-protection.json` records the intended
configuration, but committing it alone does not activate protection.

## Everyday work

1. Clone the common repository, rather than creating another root commit:

   ```sh
   git clone https://github.com/dyangwong/elec5620-group6-beauty-company.git
   cd elec5620-group6-beauty-company
   ```

2. Identify yourself and read START_HERE/AGENTS, your task and its report models.
   Check the actual shared task claim. GitHub access does not establish member
   identity or automatically claim a prepared task. Jira setup remains separate.
3. Start a task branch from current main, preserving any unrelated dirty work:

   ```sh
   git switch main
   git pull --ff-only
   git switch -c work/cs-start-01
   ```

   Substitute your own prepared branch name; do not reuse a teammate's branch.
4. Implement only the task scope, run relevant checks, and inspect the diff before
   committing. Add explicit source paths; never force-add ignored report/data/key
   files. Include both English and Chinese documentation when guidance changes.
5. Push the task branch and open a PR into main. Use the template with actual task,
   requirement/case IDs, verification, shared impact and remaining limitations.
6. Required CI must pass against current main. Fetch/merge current main into the
   task branch if needed, resolve conflicts without overwriting teammates, and
   rerun checks. Resolve review discussions before merging.
7. The author may inspect the final diff and **Squash and merge their own PR**.
   No outside approval is mandatory. GitHub does not permit self-Approve reviews;
   self-checking and self-merging must not be recorded as another person's review.
   A coding agent prepares code/PRs; merging a concrete PR still needs the human's
   explicit instruction. After merging, update main and delete the finished branch.

## main protection

- Require a PR, with **0 required external approvals**.
- Require `Python 3.9 checks` and `Python 3.13 checks`, and an up-to-date branch.
  These jobs run application/onboarding tests, repository provenance checks and
  JavaScript syntax checks. Passing them is not full Stage 1 acceptance coverage.
- Require conversation resolution; enforce protection for administrators too.
- Block force pushes and deletion of main; keep a linear history via squash merge.
- No mandatory CODEOWNERS approval. Request relevant teammate review when changing
  shared contracts, schema, authority checks or another member's module. Routine
  scoped work need not wait for a second person. Do not invent review evidence.

The maintainer publishes the first common baseline before protection exists.
Once protection is active, later changes use PRs. Do not bypass it for ordinary
work. Public visibility allows reading/cloning, not writing: actual teammates need
collaborator invitations using verified GitHub usernames. No username is guessed
from a report name. Do not grant repository administration merely to implement a
module. No collaborator invitation is claimed until it was actually sent.

## Public-source boundary

This public repository includes a report reading derivative with student IDs and
PDF metadata removed. All 63 pages/models and physical page numbering remain.
The unredacted final PDF stays local and ignored; see [reference provenance](reference/README.md).
No real credentials, local sessions/databases or old prototype files belong here.
Shared demo passwords in README are intentionally fictional. Public visibility
does not assign an open-source licence or permit invented contribution claims.

## Maintainer verification

After publication, verify actual CI runs and read back the protected-main settings.
Select the observed CI contexts rather than relying on names that never ran. A
setup PR can verify that merging is blocked while checks are pending and allowed
after success without an outside approval. Record real results in VERIFICATION.
Jira, real-model setup and teammate invitations remain distinct actions.
