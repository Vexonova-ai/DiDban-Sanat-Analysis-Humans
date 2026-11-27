# DiDban-Sanat-Analysis-Humans

A modular, local computer vision project for person detection, anonymous within-video
tracking, clothing segmentation, storage and evaluation.

**Phase 0 provides project infrastructure and shared engineering contracts. Feature implementation is assigned to the engineering team.**

The objective is independently testable object-oriented components with SOLID boundaries,
stable contracts and a reviewed integration workflow. There is no runnable vision application.

## Future architecture

```mermaid
flowchart LR
  Video --> Detection[VideoReader / YOLOv8 / Crops]
  Detection --> Packet[DetectionPacket]
  Packet --> Q1[Bounded Queue 1]
  Q1 --> Tracking[ByteTrack / OSNet / Identity / Buffer]
  Tracking --> Person[ConfirmedPerson: 15 valid frames]
  Person --> Q2[Bounded Queue 2]
  Q2 --> Fashion[SegFormer / Masks / Attributes]
  Fashion --> Result[FashionResult]
  Result --> Storage[Storage and Evaluation]
```

Three future workers own detection, tracking, and fashion/storage respectively.
See [architecture and unresolved policies](docs/architecture.md).

## Technology and initial models

Python 3.12, uv, PyTorch 2.9.0, torchvision 0.24.0, NumPy, OpenCV, Ultralytics,
Transformers, Pillow, YAML, pytest/pytest-cov, Ruff, Git and GitHub Actions.
The optional inference extra keeps CI lightweight.

Candidates: YOLOv8 yolov8n.pt (person, size 640), ByteTrack, OSNet osnet_x1_0,
and [mattmdjaga/segformer_b2_clothes](https://huggingface.co/mattmdjaga/segformer_b2_clothes).
See the [model registry](docs/model_registry.md) for pending compatibility, provenance,
category and license checks. No model weights are included or downloaded by setup.

## Repository structure

```text
.github/           CI, issue templates and pull request template
src/core/          Shared schemas, abstract interfaces and exceptions
src/detection/     Role 01 package placeholder
src/tracking/      Role 02 package placeholder
src/buffer/        Role 02 package placeholder
src/fashion/       Role 03 package placeholder
src/pipeline/      Role 04 package placeholder
src/storage/       Role 05 package placeholder
tests/            Synthetic fixtures, fakes, unit and contract integration tests
configs/          Provisional pipeline.yaml
scripts/          Environment diagnostics (no model inference)
docs/             Architecture, contracts, setup, ownership and workflow
data/ weights/ outputs/  Ignored local artifacts, with tracked placeholders
```

## Setup and validation

Install uv with `winget install --id astral-sh.uv --exact` on Windows, or follow the
[uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).
From a checkout of the approved bootstrap changes:

```powershell
uv python install 3.12
uv venv --python 3.12
uv sync --locked
uv run --no-sync python scripts/check_environment.py
uv run --no-sync pytest -v
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
```

This installs only infrastructure dependencies. For inference, install your verified
local torch 2.9.0 and torchvision 0.24.0 wheels, then synchronize using:

```powershell
uv sync --locked --extra inference --inexact --no-install-package torch --no-install-package torchvision
uv run --no-sync python scripts/check_environment.py --inference
```

Follow the complete [portable wheel setup](docs/development_guide.md) first. Never
commit local paths or wheel files. Bare uv sync/run can remove or replace supplied
builds: always use the guarded sync and `--no-sync` in the inference environment.

## Team responsibilities and contribution

Roles 01-05 own detection, tracking/ReID/buffer, fashion, integration, and storage/evaluation.
See [ownership, target files, inputs and acceptance criteria](docs/module_responsibilities.md).
Feature branches target develop through Conventional Commits, passing CI and reviewed
PRs. main is stable. See the [beginner Git workflow](docs/git_workflow.md) and AGENTS.md.
Breaking shared contracts require a dedicated PR and project leader approval.

## Status and limitations

Only infrastructure, passive contracts, ABCs and test doubles exist. Contract conventions
are documented, not runtime-enforced. No feature accuracy, production performance,
model compatibility or GPU memory suitability is claimed. Buffer thresholds/expiration,
attribute schema, tracker integration and lifecycle policies remain unresolved. Full
video annotation needs original frame and tracking data beyond the confirmation contract.
See [data contracts](docs/data_contract.md) and the validation record for measured checks.

## License and privacy

The existing MIT LICENSE is preserved. Third-party software, checkpoints and datasets
have separate terms requiring review. Use anonymous identities scoped to each video.
Human parsing and face segmentation are not facial recognition. No facial recognition
or persistent cross-video identity database is planned. Keep inference local, restrict
sensitive video access, minimize retention, and never commit recordings, personal images,
weights, embeddings or generated results. Phase 0 introduces no telemetry or cloud upload.
