"""Tests for the display formatter module."""

from quill.drive.models import DriveFile
from quill.formatters.display import format_file_list


def test_format_file_list_empty():
    """Test formatting an empty list of files."""
    result = format_file_list([])
    assert result == "No files found."


def test_format_file_list_single_file():
    """Test formatting a list with a single file."""
    files = [
        DriveFile(
            id="123",
            name="test.txt",
            mime_type="text/plain",
            size=1024,
        )
    ]
    name_width = max(len(f.name) for f in files)
    type_width = max(len(f.mime_type) for f in files)
    header = f"{'Name':<{name_width}}  {'Type':<{type_width}}  {'Size':>10}"
    separator = "-" * (name_width + type_width + 15)
    size = f"{files[0].size:,}" if files[0].size else "N/A"
    row = (
        f"{files[0].name:<{name_width}}  {files[0].mime_type:<{type_width}}  {size:>10}"
    )
    expected = f"{header}\n{separator}\n{row}"
    result = format_file_list(files)
    assert result == expected


def test_format_file_list_multiple_files():
    """Test formatting a list with multiple files."""
    files = [
        DriveFile(
            id="123",
            name="test.txt",
            mime_type="text/plain",
            size=1024,
        ),
        DriveFile(
            id="456",
            name="document.pdf",
            mime_type="application/pdf",
            size=2048576,
        ),
        DriveFile(
            id="789",
            name="image.jpg",
            mime_type="image/jpeg",
            size=None,
        ),
    ]
    name_width = max(len(f.name) for f in files)
    type_width = max(len(f.mime_type) for f in files)
    header = f"{'Name':<{name_width}}  {'Type':<{type_width}}  {'Size':>10}"
    separator = "-" * (name_width + type_width + 15)
    rows = [header, separator]
    for file in files:
        size = f"{file.size:,}" if file.size else "N/A"
        rows.append(
            f"{file.name:<{name_width}}  {file.mime_type:<{type_width}}  {size:>10}"
        )
    expected = "\n".join(rows)
    result = format_file_list(files)
    assert result == expected
