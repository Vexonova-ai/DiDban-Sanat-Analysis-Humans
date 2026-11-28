"""Check the published defaults without implementing a configuration loader."""

from pathlib import Path

import yaml


def test_configuration_defaults() -> None:
    path = Path(__file__).resolve().parents[2] / "configs" / "pipeline.yaml"
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert config == {
        "detection": {
            "model": "yolov8n.pt",
            "image_size": 640,
            "confidence": 0.1,
            "device": "auto",
        },
        "tracking": {"algorithm": "bytetrack", "reid_model": "osnet_x1_0"},
        "buffer": {"confirmation_frames": 15},
        "fashion": {"model": "mattmdjaga/segformer_b2_clothes", "device": "auto"},
        "pipeline": {"workers": 3, "queue_size": 8},
        "storage": {"output_dir": "outputs/", "save_masks": True, "save_json": True},
    }
