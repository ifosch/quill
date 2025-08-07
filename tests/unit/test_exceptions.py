"""Tests for the custom exception hierarchy."""

import pytest
from quill.exceptions import (
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


class TestQuillError:
    """Test the base QuillError exception."""

    def test_quill_error_creation(self):
        """Test QuillError can be created with message."""
        error = QuillError("Test error message")
        assert str(error) == "Test error message"

    def test_quill_error_without_message(self):
        """Test QuillError can be created without message."""
        error = QuillError("")
        assert str(error) == ""


class TestAuthenticationError:
    """Test AuthenticationError exception."""

    def test_authentication_error_creation(self):
        """Test AuthenticationError creation."""
        error = AuthenticationError("Invalid credentials")
        assert str(error) == "Invalid credentials"
        assert isinstance(error, QuillError)


class TestFileNotFoundError:
    """Test FileNotFoundError exception."""

    def test_file_not_found_error_creation(self):
        """Test FileNotFoundError creation."""
        error = FileNotFoundError("File with ID 123 not found")
        assert str(error) == "File with ID 123 not found"
        assert isinstance(error, QuillError)


class TestPermissionError:
    """Test PermissionError exception."""

    def test_permission_error_creation(self):
        """Test PermissionError creation."""
        error = PermissionError("Insufficient permissions")
        assert str(error) == "Insufficient permissions"
        assert isinstance(error, QuillError)


class TestExportError:
    """Test ExportError exception."""

    def test_export_error_creation(self):
        """Test ExportError creation."""
        error = ExportError("Failed to export file")
        assert str(error) == "Failed to export file"
        assert isinstance(error, QuillError)


class TestValidationError:
    """Test ValidationError exception."""

    def test_validation_error_creation(self):
        """Test ValidationError creation."""
        error = ValidationError("Invalid file format")
        assert str(error) == "Invalid file format"
        assert isinstance(error, QuillError)


class TestConfigurationError:
    """Test ConfigurationError exception."""

    def test_configuration_error_creation(self):
        """Test ConfigurationError creation."""
        error = ConfigurationError("Missing configuration file")
        assert str(error) == "Missing configuration file"
        assert isinstance(error, QuillError)


class TestRateLimitError:
    """Test RateLimitError exception."""

    def test_rate_limit_error_creation(self):
        """Test RateLimitError creation."""
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert isinstance(error, QuillError)


class TestNetworkError:
    """Test NetworkError exception."""

    def test_network_error_creation(self):
        """Test NetworkError creation."""
        error = NetworkError("Connection timeout")
        assert str(error) == "Connection timeout"
        assert isinstance(error, QuillError)


class TestMultipleFilesFoundError:
    """Test MultipleFilesFoundError exception."""

    def test_multiple_files_found_error_creation(self):
        """Test MultipleFilesFoundError creation."""
        error = MultipleFilesFoundError(
            "Multiple files found", files=["file1", "file2"]
        )
        assert str(error) == "Multiple files found"
        assert error.files == ["file1", "file2"]
        assert isinstance(error, QuillError)

    def test_multiple_files_found_error_without_files(self):
        """Test MultipleFilesFoundError without files parameter."""
        error = MultipleFilesFoundError("Multiple files found")
        assert str(error) == "Multiple files found"
        assert error.files == []
        assert isinstance(error, QuillError)

    def test_multiple_files_found_error_with_empty_files(self):
        """Test MultipleFilesFoundError with empty files list."""
        error = MultipleFilesFoundError("Multiple files found", files=[])
        assert str(error) == "Multiple files found"
        assert error.files == []


class TestNoFilesFoundError:
    """Test NoFilesFoundError exception."""

    def test_no_files_found_error_creation(self):
        """Test NoFilesFoundError creation."""
        error = NoFilesFoundError("No files found matching query")
        assert str(error) == "No files found matching query"
        assert isinstance(error, QuillError)


class TestExceptionInheritance:
    """Test exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_quill_error(self):
        """Test that all custom exceptions inherit from QuillError."""
        exceptions = [
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
        ]

        for exception_class in exceptions:
            error = exception_class("Test message")
            assert isinstance(error, QuillError)
            assert isinstance(error, Exception)

    def test_exception_raising_and_catching(self):
        """Test that exceptions can be raised and caught properly."""
        with pytest.raises(FileNotFoundError) as exc_info:
            raise FileNotFoundError("File not found")

        assert str(exc_info.value) == "File not found"
        assert isinstance(exc_info.value, QuillError)

    def test_multiple_files_found_error_with_files(self):
        """Test MultipleFilesFoundError with files parameter."""
        with pytest.raises(MultipleFilesFoundError) as exc_info:
            raise MultipleFilesFoundError(
                "Multiple files found", files=["file1", "file2", "file3"]
            )

        assert str(exc_info.value) == "Multiple files found"
        assert exc_info.value.files == ["file1", "file2", "file3"]
