"""Test cases for the display formatters module."""

from datetime import datetime

from quill.formatters.display import format_file_list
from quill.drive.models import DriveFile


def test_format_file_list_empty():
    """Test formatting an empty list of files."""
    result = format_file_list([])
    assert result == "No files found."


def test_format_file_list_single_file():
    """Test formatting a single file."""
    file = DriveFile(
        id="1",
        name="test.txt",
        mime_type="text/plain",
        size=100,
    )
    result = format_file_list([file])

    lines = result.split("\n")
    assert len(lines) == 3  # header, separator, file
    assert "Name" in lines[0]
    assert "Type" in lines[0]
    assert "Size" in lines[0]
    assert "test.txt" in lines[2]
    assert "text/plain" in lines[2]
    assert "100" in lines[2]


def test_format_file_list_multiple_files():
    """Test formatting multiple files."""
    files = [
        DriveFile(
            id="1",
            name="file1.txt",
            mime_type="text/plain",
            size=100,
        ),
        DriveFile(
            id="2",
            name="file2.pdf",
            mime_type="application/pdf",
            size=200,
        ),
    ]
    result = format_file_list(files)

    lines = result.split("\n")
    assert len(lines) == 4  # header, separator, file1, file2
    assert "file1.txt" in result
    assert "file2.pdf" in result
    assert "text/plain" in result
    assert "application/pdf" in result


def test_format_file_list_with_requested_fields_default():
    """Test formatting with None requested fields (default behavior)."""
    file = DriveFile(
        id="1",
        name="test.txt",
        mime_type="text/plain",
        size=100,
    )
    result = format_file_list([file], requested_fields=None)

    # Should use default 3-column layout
    lines = result.split("\n")
    assert "Name" in lines[0]
    assert "Type" in lines[0]
    assert "Size" in lines[0]


def test_format_file_list_with_custom_fields():
    """Test formatting with custom requested fields."""
    file = DriveFile(
        id="test123",
        name="test.txt",
        mime_type="text/plain",
        size=100,
    )
    result = format_file_list([file], requested_fields=["id", "name"])

    lines = result.split("\n")
    # Should show ID and Name columns
    assert "ID" in lines[0]
    assert "Name" in lines[0]
    assert "test123" in result
    assert "test.txt" in result
    # Should not show Type or Size columns in header
    assert "Type" not in lines[0]
    assert "Size" not in lines[0]


def test_format_file_list_with_complete_google_drive_id():
    """Test formatting with realistic Google Drive ID length (should not be truncated)."""
    # Realistic Google Drive ID (44 characters) - fake but same length as actual Google Drive IDs
    full_drive_id = "1ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqr"
    file = DriveFile(
        id=full_drive_id,
        name="test.txt",
        mime_type="text/plain",
        size=100,
    )
    result = format_file_list([file], requested_fields=["id", "name"])

    lines = result.split("\n")
    # Should show complete ID without truncation
    assert "ID" in lines[0]
    assert "Name" in lines[0]
    assert full_drive_id in result
    # Should NOT contain truncation indicator
    assert "..." not in result
    assert "test.txt" in result


def test_format_file_list_with_timestamps():
    """Test formatting with timestamp fields."""
    file = DriveFile(
        id="1",
        name="test.txt",
        mime_type="text/plain",
        created_time=datetime(2023, 1, 1, 12, 0, 0),
        modified_time=datetime(2023, 1, 2, 13, 0, 0),
    )
    result = format_file_list(
        [file], requested_fields=["name", "createdTime", "modifiedTime"]
    )

    lines = result.split("\n")
    assert "Created" in lines[0]
    assert "Modified" in lines[0]
    assert "2023-01-01" in result
    assert "2023-01-02" in result


def test_format_file_list_with_empty_fields():
    """Test formatting with empty requested fields list."""
    file = DriveFile(name="test.txt", mime_type="text/plain", size=100)
    result = format_file_list([file], requested_fields=[])

    # Should fall back to default display
    lines = result.split("\n")
    assert "Name" in lines[0]
    assert "Type" in lines[0]
    assert "Size" in lines[0]


def test_format_file_list_with_unsupported_fields():
    """Test formatting with unsupported field names."""
    file = DriveFile(name="test.txt", mime_type="text/plain", size=100)
    result = format_file_list([file], requested_fields=["unsupported_field"])

    # Should fall back to default display when no valid fields
    lines = result.split("\n")
    assert "Name" in lines[0]
    assert "Type" in lines[0]
    assert "Size" in lines[0]


def test_format_file_list_with_owners():
    """Test formatting with owners field."""
    file = DriveFile(
        name="test.txt",
        mime_type="text/plain",
        owners=[{"displayName": "John Doe", "emailAddress": "john@example.com"}],
    )
    result = format_file_list([file], requested_fields=["name", "owners"])

    assert "Owners" in result
    assert "John Doe" in result


def test_format_file_list_with_missing_data():
    """Test formatting when some fields are missing."""
    file = DriveFile(name="test.txt")  # Only name provided
    result = format_file_list([file], requested_fields=["id", "name", "size"])

    lines = result.split("\n")
    assert "ID" in lines[0]
    assert "Name" in lines[0]
    assert "Size" in lines[0]
    assert "N/A" in result  # Should show N/A for missing fields
