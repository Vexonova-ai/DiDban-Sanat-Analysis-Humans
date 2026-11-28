"""Guard exact interface signatures and import isolation."""

import inspect
import subprocess
import sys
from typing import get_type_hints

import pytest

from src.core.interfaces import IFashionModel, IPersonBuffer, IPersonDetector, IPersonTracker
from src.core.schemas import (
    ConfirmedPerson,
    Detection,
    DetectionPacket,
    FashionResult,
    FrameData,
    TrackedPerson,
)


@pytest.mark.parametrize(
    ("cls", "method", "argument", "input_type", "output_type"),
    [
        (IPersonDetector, "detect", "frame", FrameData, list[Detection]),
        (IPersonTracker, "update", "packet", DetectionPacket, list[TrackedPerson]),
        (IPersonBuffer, "update", "person", TrackedPerson, ConfirmedPerson | None),
        (IFashionModel, "predict", "person", ConfirmedPerson, FashionResult),
    ],
)
def test_interface_contract(cls, method, argument, input_type, output_type) -> None:
    with pytest.raises(TypeError):
        cls()
    function = getattr(cls, method)
    assert list(inspect.signature(function).parameters) == ["self", argument]
    assert get_type_hints(function) == {argument: input_type, "return": output_type}
    assert cls.__abstractmethods__ == {method}
    # ABC method bodies intentionally contain no implementation.
    assert function(None, None) is None


def test_safe_imports() -> None:
    code = """
import importlib.abc
import sys
class BlockHeavyImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch', 'torchvision', 'ultralytics', 'transformers', 'cv2'}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, BlockHeavyImports())
import src.core.schemas, src.core.interfaces, src.core.exceptions
import src.detection, src.tracking, src.buffer, src.fashion, src.pipeline, src.storage
"""
    subprocess.run([sys.executable, "-c", code], check=True)
