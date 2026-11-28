"""Shared fresh fixtures for independently developed tests."""

import pytest

from tests.fixtures.sample_data import sample_contracts


@pytest.fixture
def contracts() -> tuple:
    """Provide fresh contract objects for each test."""
    return sample_contracts()
