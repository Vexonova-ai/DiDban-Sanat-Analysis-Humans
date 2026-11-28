"""Fresh synthetic examples of every contract, without private images."""

import numpy as np

from src.core.schemas import (
    ConfirmedPerson,
    Detection,
    DetectionPacket,
    FashionResult,
    FrameData,
    TrackedPerson,
)


def sample_contracts() -> tuple:
    """Return independent arrays and a consistent selected-frame identity."""
    image = np.zeros((400, 200, 3), dtype=np.uint8)
    image[..., 0] = 255  # Synthetic blue in OpenCV BGR ordering.
    frame = FrameData(14, 14 / 30, image)
    detection = Detection((0, 0, 200, 400), 0.9, image.copy())
    packet = DetectionPacket(frame, [detection])
    tracked = TrackedPerson(14, 14 / 30, 7, 1, detection.bbox, image.copy())
    person = ConfirmedPerson(1, 14, 14 / 30, 15, detection.bbox, image.copy())
    result = FashionResult(1, 14, {"synthetic_region": np.ones((400, 200), dtype=bool)}, {})
    return frame, detection, packet, tracked, person, result
