"""Test passive contract compatibility, not nonexistent runtime validation."""

from dataclasses import MISSING, fields
from typing import get_type_hints

import numpy as np
import pytest

from src.core import exceptions, schemas


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("FrameData", {"frame_id": int, "timestamp": float, "image": np.ndarray}),
        ("Detection", {"bbox": tuple[int, int, int, int], "confidence": float, "crop": np.ndarray}),
        ("DetectionPacket", {"frame": schemas.FrameData, "detections": list[schemas.Detection]}),
        (
            "TrackedPerson",
            {
                "frame_id": int,
                "timestamp": float,
                "track_id": int,
                "person_id": int,
                "bbox": tuple[int, int, int, int],
                "crop": np.ndarray,
            },
        ),
        (
            "ConfirmedPerson",
            {
                "person_id": int,
                "frame_id": int,
                "timestamp": float,
                "confirmed_frames": int,
                "bbox": tuple[int, int, int, int],
                "image": np.ndarray,
            },
        ),
        (
            "FashionResult",
            {"person_id": int, "frame_id": int, "masks": dict[str, np.ndarray], "attributes": dict},
        ),
    ],
)
def test_exact_required_fields(name: str, expected: dict) -> None:
    cls = getattr(schemas, name)
    assert [f.name for f in fields(cls)] == list(expected)
    assert get_type_hints(cls) == expected
    assert all(f.default is MISSING and f.default_factory is MISSING for f in fields(cls))
    with pytest.raises(TypeError):
        cls()


def test_fixture_conventions(contracts: tuple) -> None:
    frame, detection, packet, tracked, person, result = contracts
    for image in (frame.image, detection.crop, tracked.crop, person.image):
        assert image.dtype == np.uint8
        assert image.shape == (400, 200, 3)
        assert tuple(image[0, 0]) == (255, 0, 0)
    x1, y1, x2, y2 = detection.bbox
    assert detection.crop.shape == frame.image[y1:y2, x1:x2].shape
    assert 0 <= detection.confidence <= 1
    assert packet.frame is frame
    assert tracked.track_id != tracked.person_id
    assert person.frame_id == result.frame_id == tracked.frame_id
    assert person.person_id == result.person_id == tracked.person_id
    assert person.timestamp == person.frame_id / 30
    assert person.confirmed_frames == 15
    assert not np.shares_memory(person.image, frame.image)
    for mask in result.masks.values():
        assert mask.dtype == np.bool_
        assert mask.shape == person.image.shape[:2]


def test_zero_frame_and_empty_packet() -> None:
    frame = schemas.FrameData(0, 0.0, np.zeros((2, 3, 3), dtype=np.uint8))
    assert schemas.DetectionPacket(frame, []).detections == []


def test_dataclasses_are_passive() -> None:
    assert schemas.Detection((4, 4, 0, 0), 2.0, np.zeros(1)).confidence == 2.0


@pytest.mark.parametrize(
    "name",
    ["ConfigurationError", "PipelineError", "ModelLoadError", "InvalidFrameError", "StorageError"],
)
def test_exception_hierarchy(name: str) -> None:
    with pytest.raises(exceptions.FashionVisionError, match="synthetic failure"):
        raise getattr(exceptions, name)("synthetic failure")
