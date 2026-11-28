# Development environment

Use Python 3.12 and uv. See the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).
On Windows:

```powershell
winget install --id astral-sh.uv --exact
uv --version
uv python install 3.12
uv venv --python 3.12
```

Run commands from the repository root. The project imports as `src` and does not yet
build a distributable package. uv.lock records lightweight dependencies and the optional
inference extra using public sources. Locking metadata does not install torch.

## Infrastructure-only environment

```powershell
uv sync --locked
uv run --no-sync python scripts/check_environment.py
uv run --no-sync pytest -v
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
```

This is the CI configuration. It requires no torch, GPU, weights, private data or
credentials. Use a separate checkout/environment for these checks if maintaining a
local inference environment.

## Supplied local wheels

PyTorch 2.9.0 and torchvision 0.24.0 are required for inference. Verify Python ABI,
operating system, CPU architecture, wheel integrity and GPU-driver compatibility.
Supply your own directory interactively; never commit its value:

```powershell
$wheelDirectory = Read-Host "Directory containing compatible local wheels"
Get-ChildItem -LiteralPath $wheelDirectory -Filter '*.whl'
$torchWheelName = Read-Host "Exact verified torch wheel filename"
$visionWheelName = Read-Host "Exact verified torchvision wheel filename"
$torchWheel = Join-Path $wheelDirectory $torchWheelName
$visionWheel = Join-Path $wheelDirectory $visionWheelName
uv pip install --python .venv/Scripts/python.exe $torchWheel $visionWheel
uv sync --locked --extra inference --inexact --no-install-package torch --no-install-package torchvision
uv run --no-sync python scripts/check_environment.py --inference
```

On Unix use `.venv/bin/python` and equivalent shell variables with compatible wheels.
If local wheels are absent or incompatible, report the blocker and obtain authorization
before downloading another PyTorch distribution. Windows wheels cannot be used on Linux.

For **every later inference-environment synchronization**, use:

```powershell
uv sync --locked --extra inference --inexact --no-install-package torch --no-install-package torchvision
```

The package exclusions prevent installing the two local distributions; `--inexact`
preserves them. Use `uv run --no-sync` thereafter. Bare sync/run or an unguarded
inference sync can remove or replace local builds. Local CUDA variants intentionally
differ from public lock artifacts; other packages follow the lock. Wheel provenance
is a separate reproducibility input, not a wholly lock-only GPU setup. Recheck versions
after synchronization. See [uv synchronization semantics](https://docs.astral.sh/uv/concepts/projects/sync/).

The checker imports torch/torchvision only with `--inference`, reports versions,
tests a synthetic native torchvision operation, and exercises CUDA when available.
It does not load pretrained models. Tests cover contracts and canned responses, not
accuracy. Core coverage does not measure future features. Fix formatting using
`uv run --no-sync ruff format .` and rerun all three validation commands before PRs.

Dependency changes require justification and lock updates. ByteTrack and OSNet package
selection belongs to Role 02. Configuration values are provisional. No production
configuration or dotenv loader exists; .env.example is a local setup template only.
