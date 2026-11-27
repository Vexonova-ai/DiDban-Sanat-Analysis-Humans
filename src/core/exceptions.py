"""Shared error taxonomy; feature modules supply handling policies."""


class FashionVisionError(Exception):
    """Base exception for the shared computer vision contracts."""


class ConfigurationError(FashionVisionError):
    """Raised when project configuration is invalid."""


class PipelineError(FashionVisionError):
    """Raised when pipeline execution fails."""


class ModelLoadError(FashionVisionError):
    """Raised when a model cannot be loaded."""


class InvalidFrameError(FashionVisionError):
    """Raised when an input frame is invalid."""


class StorageError(FashionVisionError):
    """Raised when output data cannot be stored."""
