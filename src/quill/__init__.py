"""Quill - Google Drive Library and CLI Tool."""

__version__ = "0.1.0"

# Main library exports
from .client import Quill, FieldParser
from .drive.client import DriveClient
from .drive.models import DriveFile
from .auth import Auth
from .exceptions import (
    QuillError,
    AuthenticationError,
    FileNotFoundError,
    PermissionError,
    ExportError,
    ValidationError,
    ConfigurationError,
    RateLimitError,
    NetworkError,
    MultipleFilesFoundError,
    NoFilesFoundError,
)

__all__ = [
    # High-level library interface
    "Quill",
    "FieldParser",
    # Core components (existing)
    "DriveClient",
    "DriveFile",
    "Auth",
    # Custom exceptions
    "QuillError",
    "AuthenticationError",
    "FileNotFoundError",
    "PermissionError",
    "ExportError",
    "ValidationError",
    "ConfigurationError",
    "RateLimitError",
    "NetworkError",
    "MultipleFilesFoundError",
    "NoFilesFoundError",
    # Version
    "__version__",
]
