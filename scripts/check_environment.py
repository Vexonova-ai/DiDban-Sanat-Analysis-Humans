"""Report dependency versions and optionally exercise local CUDA tensor execution."""

import argparse
import importlib.metadata
import platform


def main() -> None:
    """Check the selected environment without loading pretrained models."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inference", action="store_true")
    args = parser.parse_args()
    print(f"Python: {platform.python_version()}")
    if platform.python_version_tuple()[:2] != ("3", "12"):
        raise SystemExit("Python 3.12 is required.")
    packages = ["numpy", "pyyaml", "pytest", "pytest-cov", "ruff"]
    if args.inference:
        packages += [
            "torch",
            "torchvision",
            "opencv-python",
            "ultralytics",
            "transformers",
            "pillow",
        ]
    for package in packages:
        print(f"{package}: {importlib.metadata.version(package)}")
    if args.inference:
        import torch
        import torchvision

        if torch.__version__.split("+")[0] != "2.9.0":
            raise SystemExit("PyTorch 2.9.0 is required.")
        if torchvision.__version__.split("+")[0] != "0.24.0":
            raise SystemExit("torchvision 0.24.0 is required.")
        print(f"CUDA build: {torch.version.cuda}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        boxes = torch.tensor([[0.0, 0.0, 2.0, 2.0]])
        assert torchvision.ops.nms(boxes, torch.tensor([0.9]), 0.5).tolist() == [0]
        print("torchvision CPU native operation: passed")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(torch.rand(2, 2, device="cuda"))
            assert torchvision.ops.nms(
                boxes.cuda(), torch.tensor([0.9], device="cuda"), 0.5
            ).tolist() == [0]
            torch.cuda.synchronize()
            print("CUDA tensor execution and torchvision native operation: passed")


if __name__ == "__main__":
    main()
