"""Custom exceptions for the Quill library."""

from typing import Optional


class QuillError(Exception):
    """Base exception for all Quill library errors."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        """Initialize the exception.

        Args:
            message: Human-readable error message
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.original_error = original_error


class AuthenticationError(QuillError):
    """Authentication-related errors.

    Raised when:
    - Credentials are invalid or expired
    - OAuth flow fails
    - Service account authentication fails
    """

    pass


class FileNotFoundError(QuillError):
    """File not found in Google Drive.

    Raised when:
    - File ID doesn't exist
    - File has been deleted
    - File is in trash
    """

    pass


class PermissionError(QuillError):
    """Permission-related errors.

    Raised when:
    - User doesn't have access to the file
    - Insufficient permissions for the operation
    - File is shared but user lacks required permissions
    """

    pass


class ExportError(QuillError):
    """Export operation errors.

    Raised when:
    - Export format is not supported
    - File type cannot be exported
    - Export operation fails
    """

    pass


class ValidationError(QuillError):
    """Input validation errors.

    Raised when:
    - Invalid file ID format
    - Invalid query syntax
    - Invalid field names
    - Invalid format options
    """

    pass


class ConfigurationError(QuillError):
    """Configuration-related errors.

    Raised when:
    - Configuration file is invalid
    - Required configuration is missing
    - Environment variables are misconfigured
    """

    pass


class RateLimitError(QuillError):
    """API rate limiting errors.

    Raised when:
    - Google Drive API quota is exceeded
    - Too many requests in a short time
    - Rate limiting is enforced
    """

    pass


class NetworkError(QuillError):
    """Network-related errors.

    Raised when:
    - Network connection fails
    - Timeout occurs
    - DNS resolution fails
    """

    pass


class MultipleFilesFoundError(QuillError):
    """Multiple files found when expecting single match.

    Raised when:
    - Search query returns multiple files
    - Export with query finds multiple matches
    """

    def __init__(self, message: str, files: Optional[list] = None):
        """Initialize the exception.

        Args:
            message: Human-readable error message
            files: List of files that were found
        """
        super().__init__(message)
        self.files = files or []


class NoFilesFoundError(QuillError):
    """No files found when expecting at least one match.

    Raised when:
    - Search query returns no results
    - Export with query finds no matches
    """

    pass
