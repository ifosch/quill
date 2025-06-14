"""Formatting functions for CLI output."""

from typing import List
from ..drive.models import DriveFile


def format_file_list(files: List[DriveFile]) -> str:
    """Format a list of files for display."""
    if not files:
        return "No files found."

    # Calculate column widths
    name_width = max(len(f.name) for f in files)
    type_width = max(len(f.mime_type) for f in files)

    # Create header
    header = f"{'Name':<{name_width}}  {'Type':<{type_width}}  {'Size':>10}"
    separator = "-" * (name_width + type_width + 15)

    # Format each file
    rows = [header, separator]
    for file in files:
        size = f"{file.size:,}" if file.size else "N/A"
        rows.append(
            f"{file.name:<{name_width}}  {file.mime_type:<{type_width}}  {size:>10}"
        )

    return "\n".join(rows)
