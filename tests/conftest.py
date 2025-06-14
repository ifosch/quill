"""Test configuration and fixtures."""

import pytest
from quill.config import Config
from quill.drive.client import DriveClient


@pytest.fixture
def config():
    """Provide a test configuration."""
    return Config()


@pytest.fixture
def drive_client():
    """Provide a Drive client instance."""
    return DriveClient()
