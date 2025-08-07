"""Quill - Google Drive Library and CLI Tool."""

__version__ = "0.1.0"

# Main library exports
from .client import Quill
from .drive.client import DriveClient
from .drive.models import DriveFile
from .auth import Auth
from .utils import FieldParser, validate_file_id, sanitize_filename, format_file_size
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
    # Utility functions
    "FieldParser",
    "validate_file_id",
    "sanitize_filename",
    "format_file_size",
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
