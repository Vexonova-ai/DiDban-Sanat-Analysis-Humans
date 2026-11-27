"""Shared passive data contracts; producers enforce the documented conventions."""

from dataclasses import dataclass

import numpy as np


@dataclass
class FrameData:
    """Original BGR uint8 frame with zero-based ID and timestamp in seconds."""

    frame_id: int
    timestamp: float
    image: np.ndarray


@dataclass
class Detection:
    """Person crop, confidence, and original-frame exclusive xyxy bounds."""

    bbox: tuple[int, int, int, int]
    confidence: float
    crop: np.ndarray


@dataclass
class DetectionPacket:
    """Frame and its ordered detections, including frames with no detections."""

    frame: FrameData
    detections: list[Detection]


@dataclass
class TrackedPerson:
    """Observation with tracker ID and anonymous video-session person ID."""

    frame_id: int
    timestamp: float
    track_id: int
    person_id: int
    bbox: tuple[int, int, int, int]
    crop: np.ndarray


@dataclass
class ConfirmedPerson:
    """Selected source crop and frame after sufficient valid observations."""

    person_id: int
    frame_id: int
    timestamp: float
    confirmed_frames: int
    bbox: tuple[int, int, int, int]
    image: np.ndarray


@dataclass
class FashionResult:
    """Crop-sized Boolean masks and attributes for the selected source frame."""

    person_id: int
    frame_id: int
    masks: dict[str, np.ndarray]
    attributes: dict
