"""Canned interface responses only; no model, association, or buffer algorithms."""

from src.core.interfaces import IFashionModel, IPersonBuffer, IPersonDetector, IPersonTracker
from src.core.schemas import (
    ConfirmedPerson,
    Detection,
    DetectionPacket,
    FashionResult,
    FrameData,
    TrackedPerson,
)


class FakeDetector(IPersonDetector):
    """Return injected detections."""

    def __init__(self, result: list[Detection]) -> None:
        self.result = result

    def detect(self, frame: FrameData) -> list[Detection]:
        """Return the canned response without inspecting pixels."""
        return self.result


class FakeTracker(IPersonTracker):
    """Return injected observations."""

    def __init__(self, result: list[TrackedPerson]) -> None:
        self.result = result

    def update(self, packet: DetectionPacket) -> list[TrackedPerson]:
        """Return the canned response without association."""
        return self.result


class FakeBuffer(IPersonBuffer):
    """Return an injected confirmation or None without counting frames."""

    def __init__(self, result: ConfirmedPerson | None) -> None:
        self.result = result

    def update(self, person: TrackedPerson) -> ConfirmedPerson | None:
        """Return the canned response without storing observations."""
        return self.result


class FakeFashionModel(IFashionModel):
    """Return injected synthetic masks."""

    def __init__(self, result: FashionResult) -> None:
        self.result = result

    def predict(self, person: ConfirmedPerson) -> FashionResult:
        """Return the canned response without segmentation."""
        return self.result
