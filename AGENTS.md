# Repository instructions

- Write all new repository content in professional English.
- Use Python 3.12 and uv; preserve PyTorch 2.9.0 and compatible torchvision 0.24.0.
- Follow docs/development_guide.md for local wheel installation. Never replace a local
  PyTorch build through an unqualified sync. Do not download another distribution
  without explicit authorization when a local wheel is required.
- Preserve exact shared fields and interface signatures. Breaking contract changes
  require a dedicated pull request and project leader approval.
- Respect docs/module_responsibilities.md ownership boundaries. Phase 0 contains
  infrastructure only; feature implementations require a subsequent assigned task.
- Use type hints, meaningful docstrings, object-oriented design, and SOLID principles.
- Add relevant tests and run pytest, Ruff lint, and Ruff format checks before completion.
- Avoid unrelated changes and unnecessary dependencies. Keep fakes under tests only.
- Never commit private data, embeddings, results, weights, credentials, or personal paths.
- Use Conventional Commits and feature pull requests targeting develop. Developers
  require project leader approval and may not bypass reviews or push directly to
  protected branches. The leader has an individual, pull-request-only review bypass
  and may merge their own PRs without another developer's approval. This exception
  never bypasses required CI or branch safety. Do not use an administrator-wide bypass.
- Follow docs/repository_permissions.md for CODEOWNERS activation and the temporary
  leader-only merge guard. Do not merge the bootstrap PR without explicit leader authorization.
- Do not implement facial recognition or persistent cross-video identity databases.
- Report incomplete functionality and failed validation honestly.
