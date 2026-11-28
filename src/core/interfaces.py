"""Abstract integration boundaries shared by independently developed modules."""

from abc import ABC, abstractmethod

from .schemas import (
    ConfirmedPerson,
    Detection,
    DetectionPacket,
    FashionResult,
    FrameData,
    TrackedPerson,
)


class IPersonDetector(ABC):
    """Detect people in a prepared frame."""

    @abstractmethod
    def detect(self, frame: FrameData) -> list[Detection]:
        """Return detections in original-frame coordinates."""
        ...


class IPersonTracker(ABC):
    """Associate observations within the current video session."""

    @abstractmethod
    def update(self, packet: DetectionPacket) -> list[TrackedPerson]:
        """Consume an ordered packet and return tracked observations."""
        ...


class IPersonBuffer(ABC):
    """Define the observation-to-confirmation boundary."""

    @abstractmethod
    def update(self, person: TrackedPerson) -> ConfirmedPerson | None:
        """Return a selected confirmation when ready, otherwise None."""
        ...


class IFashionModel(ABC):
    """Define crop-based human parsing."""

    @abstractmethod
    def predict(self, person: ConfirmedPerson) -> FashionResult:
        """Return masks aligned to the selected image and source frame."""
        ...
