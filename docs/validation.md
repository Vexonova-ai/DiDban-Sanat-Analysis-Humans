# Phase 0 validation record

Initial validation performed on 2026-11-28. This measures infrastructure only.

- Existing public repository reused; original MIT LICENSE and history preserved.
- Authenticated repository permission: ADMIN. No existing PRs, issues, rulesets or
  branch protection were present at preflight. Only main existed.
- Created develop from main, then chore/bootstrap from develop. No feature branches created.
- Python 3.12.16, uv 0.13.9, Windows x86-64, Intel Core i7-13620H.
- Supplied torch 2.9.0+cu128 and torchvision 0.24.0+cu128 wheels passed ZIP integrity
  and cp312/win_amd64 metadata checks and were installed locally with uv.
- CUDA build 12.8; NVIDIA RTX 4050 Laptop GPU, driver 621.14. CUDA availability and
  actual CUDA random-tensor execution succeeded. No pretrained inference was performed.
- uv.lock resolves 72 packages using portable public sources. `uv lock --check` passes.
- A separate ignored .venv-ci environment synchronized with `uv sync --locked`.
- Infrastructure tests: 21 passed. Shared core: 58 statements, 100% coverage.
- Ruff lint and formatting passed.
- Role issues 1-5 are open and unassigned, all To Do. Bootstrap work is tracked in PR 6.
- Dedicated project 2 uses a board layout with To Do, In Progress, In Review and Done. GitHub
  rejected public project visibility with `Viewer not authorized to change project
  visibility (updateProjectV2)`. The project remains private; the repository is public.

- GitHub Actions run 46068057166 completed successfully for bootstrap commit 701eedc.
  The actual required job is named infrastructure. Downloading the full log archive
  timed out locally; the run and check APIs confirmed success independently.
- Before the requested permissions correction, main and develop required PRs, one approval,
  dismissal of stale reviews, resolved
  conversations and an up-to-date infrastructure check. Protection includes admins;
  force pushes and deletion were disabled. This review policy is superseded by
  [the corrected leader-specific policy](repository_permissions.md).
- Synthetic torchvision native NMS operations succeeded on CPU and CUDA. These check
  binary compatibility only; they do not load a detector or test detection accuracy.

- Full inference synchronization completed with the documented exclusions and
  --inexact. A second guarded sync succeeded offline, checking 52 packages.
- uv pip check verified all 54 installed packages are compatible. The installed
  versions below match the lock, with the documented local CUDA build overrides.
- Local wheel provenance fingerprints were unchanged after synchronization:
  torch 2.9.0+cu128 and torchvision 0.24.0+cu128 were not replaced.
- Final environment diagnostics passed: CUDA tensor execution, CPU/CUDA torchvision
  native operations, and OpenCV binary import. No pretrained models were used.
- The final full environment also passed all 21 tests with 100% shared-core coverage,
  Ruff lint and Ruff formatting. The separate lightweight environment passed earlier.

No feature implementation, model accuracy or application performance is asserted.

## Locked dependency versions

| Package | Lock version |
| --- | --- |
| numpy | 2.5.5 |
| pyyaml | 6.0.4 |
| torch | 2.9.0 (local supplied build: 2.9.0+cu128) |
| torchvision | 0.24.0 (local supplied build: 0.24.0+cu128) |
| opencv-python | 4.14.0.94 |
| ultralytics | 8.4.220 |
| transformers | 4.57.6 |
| pillow | 12.3.0 |
| pytest | 9.2.0 |
| pytest-cov | 7.1.0 |
| ruff | 0.17.6 |

The lock also records transitive versions and hashes. Model-level compatibility remains
unverified; successful dependency resolution and native operations are not model tests.
