# Git and GitHub workflow

A **repository** stores files and their history. **Clone** creates a local copy. A
**branch** names a line of development. The **working tree** contains editable files.
**Staging** selects changes for the next **commit**, a named snapshot. **Push** uploads
commits. **Fetch** updates remote references without changing files. **Pull** fetches
and integrates; use `--ff-only` to avoid unexpected merges. **Merge** combines histories.
A **pull request** proposes integration and supplies CI and **code review**, where
teammates inspect correctness and maintainability. A **merge conflict** needs manual
reconciliation of incompatible edits.

main holds stable releases; develop integrates reviewed work. chore/bootstrap contains
Phase 0. Feature PRs target develop. Use Conventional Commits (`feat:`, `fix:`, `test:`,
`docs:`, `chore:`) and English descriptions. Never commit features directly to protected
branches. Developers cannot bypass required approvals. The leader's explicitly
configured review-only exception never bypasses CI or other branch safety rules.

```powershell
git clone https://github.com/Vexonova-ai/DiDban-Sanat-Analysis-Humans.git
cd DiDban-Sanat-Analysis-Humans
git switch develop
git pull --ff-only origin develop
```

After bootstrap approval and merge, follow [uv setup](development_guide.md). Create
only your assigned branch. The reserved branches are feature/detection,
feature/tracking-reid, feature/fashion, feature/pipeline and feature/storage-evaluation.

Run exactly one branch command after the common clone, develop update and uv setup:

| Role | Command | Issue |
| --- | --- | --- |
| 01 - Detection | `git switch -c feature/detection` | #1 |
| 02 - Tracking, ReID and Buffer | `git switch -c feature/tracking-reid` | #2 |
| 03 - Fashion | `git switch -c feature/fashion` | #3 |
| 04 - Integration | `git switch -c feature/pipeline` | #4 |
| 05 - Storage and Evaluation | `git switch -c feature/storage-evaluation` | #5 |

```powershell
git switch -c feature/detection
git status
git diff
uv run --no-sync pytest -v
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
git add src/detection/
# Also stage the specific relevant test and documentation files you changed.
git diff --cached
git commit -m "feat: implement person detection"
git push -u origin feature/detection
gh pr create --base develop
```

Before synchronization, inspect status. Commit coherent work to your feature branch
or deliberately preserve it separately. Never discard or stash another person's work.
With a clean tree:

```powershell
git fetch origin
git merge origin/develop
```

For conflicts, inspect status, reconcile both intentions, remove conflict markers,
test, stage resolved files and commit the merge. Ask the owner if semantics are unclear.
`git merge --abort` abandons an in-progress merge; begin from a clean tree to preserve
earlier work. Do not use destructive resets or force pushes as shortcuts.

Link the issue, explain validation, request review, resolve conversations and await
the actual infrastructure check. Developer PRs require project leader code-owner
approval. The leader can merge their own PRs without approval from another developer
using the individual pull-request-only review bypass. Breaking contracts need a
dedicated PR and project leader approval. Release PRs target main.
The bootstrap PR must not be merged without project leader approval.

Both main and develop require PRs, resolved conversations and an up-to-date passing
infrastructure check for everyone. A separate review ruleset requires one approval,
code-owner review and dismissal of stale reviews, with a bypass for the leader alone
in pull-request mode. Other administrators have no bypass. Force pushes and deletion
remain disabled. See [the actual configuration and activation status](repository_permissions.md).
