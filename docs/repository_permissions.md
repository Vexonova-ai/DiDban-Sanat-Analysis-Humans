# Repository review and merge permissions

This policy applies only to this repository's main and develop branches. Repository
visibility remains public. No organization policy, membership, collaborator role or
unrelated repository was changed.

## Before correction

Both branches used classic protection: one review approval including administrators,
no code-owner requirement, strict infrastructure CI, resolved conversations, and no
force pushes or deletion. There was no leader review exception. No applicable inherited
rulesets were returned. More than one account has administrator access, so a broad
administrator bypass would not isolate the leader.

## Corrected configuration

| Ruleset | Enforcement | Bypass |
| --- | --- | --- |
| Required CI - no bypass (28262951) | Up-to-date infrastructure check from GitHub Actions | None |
| Pull requests and branch safety - no bypass (28262952) | PR required, resolved conversations, no force push/deletion | None |
| Leader approval - leader PR-only bypass (28262953) | One approval, code-owner approval, dismiss stale reviews | Only the project leader's individual account, for PRs only |

The leader can create and merge their own PRs without another developer's approval,
review developer PRs and manage repository settings. Required CI still applies.
Developers work on feature branches and target develop. They require leader approval,
cannot bypass reviews, and cannot push directly, force-push or delete protected branches.
Existing administrator accounts retain settings access; no new administrative role
was granted. Administrators can edit settings, so policy administration remains a
trusted privilege; their current merge policy grants no blanket bypass.

Classic protections still enforce administrators, resolved conversations and the
existing force-push/deletion restrictions. Their duplicate review and CI requirements
were migrated to the rulesets above, eliminating the overlapping review requirement.
The universal PR rule requires zero approvals, no code-owner review and no extra
approval for unattributed changes; it cannot reintroduce another-reviewer requirements.

## CODEOWNERS activation dependency

The .github/CODEOWNERS file assigns every path, including itself, to the project
leader. GitHub evaluates CODEOWNERS from the PR's base branch. At configuration time,
neither main nor develop contained that file. The project leader explicitly authorized
merging bootstrap PR 6 into develop and promoting the infrastructure through a PR to
main after local validation. Ownership becomes active separately on each base when
the file reaches that branch.

During activation, the temporary update guard (28263045) prevents everyone except the leader from
merging to the protected branches. This deliberately prevents another developer's
approval from substituting for leader approval while CODEOWNERS is absent. After the
ownership file reaches each base branch and its validity is verified, remove that
branch from the temporary guard. Delete the guard only when both bases are activated.
Then developers can merge their approved PRs after all checks pass. Do not remove the
guard early or treat a CODEOWNERS file on a feature branch as active enforcement.

The ordinary PR review summary may still say REVIEW_REQUIRED because it reports the
rule's default requirement; the individual bypass is scoped to the review ruleset.
Only the explicitly authorized bootstrap and promotion merges may be used to verify
the review exception. CI and branch-safety rules must still pass for those merges.

## Organization visibility limitation

The repository endpoint with includes_parents=true and the effective-rules endpoints
reported no inherited rulesets. Listing all organization rulesets returned HTTP 404
and explicitly required the unavailable admin:org token scope. Organization-wide
inventory therefore remains unavailable; no organization policy was changed or weakened.
