"""High-level Google Drive client library."""

from typing import List, Optional, Dict, Any

from .drive.client import DriveClient
from .drive.models import DriveFile


class Quill:
    """High-level Google Drive client for easy file operations.

    This class provides a simplified interface for common Google Drive operations
    while maintaining access to advanced features needed by the CLI and other
    applications.

    Example:
        ```python
        from quill import Quill

        # Basic usage
        quill = Quill()
        files = quill.list_files(page_size=20, query="name contains 'report'")

        # Get file details
        file_info = quill.get_file("file_id_here")

        # Export file
        exported_path = quill.export_file("file_id_here", format="pdf")
        ```
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize the Quill client.

        Args:
            credentials_path: Optional path to credentials file. If not provided,
                uses default authentication configuration.
        """
        self._client = DriveClient()
        # TODO: Add credentials_path support when DriveClient supports it

    def list_files(
        self,
        page_size: int = 10,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> List[DriveFile]:
        """List files with simplified interface.

        Args:
            page_size: Number of files to return (default: 10)
            query: Search query to filter files (e.g., "name contains 'report'")
            fields: List of fields to include in response

        Returns:
            List of DriveFile objects

        Raises:
            PermissionError: If authentication fails or insufficient permissions
            RuntimeError: For other API errors
        """
        result = self._client.list_files(
            page_size=page_size, query=query, fields=fields
        )
        return result["files"]

    def list_files_with_pagination(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """List files with pagination information (for CLI and advanced use).

        Args:
            page_size: Number of files to return per page
            page_token: Token for the next page of results
            query: Search query to filter files
            fields: List of fields to include in response

        Returns:
            Dict containing:
                - files: List of DriveFile objects
                - next_page_token: Token for the next page (if any)

        Raises:
            PermissionError: If authentication fails or insufficient permissions
            RuntimeError: For other API errors
        """
        return self._client.list_files(
            page_size=page_size, page_token=page_token, query=query, fields=fields
        )

    def get_file(self, file_id: str) -> DriveFile:
        """Get detailed information about a specific file.

        Args:
            file_id: The Google Drive file ID

        Returns:
            DriveFile object with file metadata

        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If user doesn't have permission to access the file
            RuntimeError: For other API errors
        """
        return self._client.get_file(file_id)

    def export_file(
        self,
        file_id: str,
        output_path: Optional[str] = None,
        format: Optional[str] = None,
    ) -> str:
        """Export a file from Google Drive.

        Args:
            file_id: The Google Drive file ID
            output_path: Output path for the exported file. If not provided,
                saves to current directory with document name
            format: Export format (html, pdf, xlsx, csv). If not provided,
                uses smart default based on file type

        Returns:
            Path to the exported file

        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If user doesn't have permission to access the file
            ValueError: If the format is not supported
            RuntimeError: For other API errors
        """
        return self._client.export(file_id, output_path, format)

    def search_and_export(
        self,
        query: str,
        output_path: Optional[str] = None,
        format: Optional[str] = None,
    ) -> str:
        """Search for files and export single match (for CLI export --query).

        Args:
            query: Search query to find files
            output_path: Output path for the exported file
            format: Export format (html, pdf, xlsx, csv)

        Returns:
            Path to the exported file

        Raises:
            FileNotFoundError: If no files found matching the query
            ValueError: If multiple files found matching the query
            PermissionError: If user doesn't have permission
            RuntimeError: For other API errors
        """
        files = self.list_files(query=query, page_size=100)

        if not files:
            raise FileNotFoundError("No files found matching the query")

        if len(files) > 1:
            raise ValueError(f"Multiple files found ({len(files)} matches)")

        return self.export_file(files[0].id, output_path, format)

    def get_field_parser(self) -> "FieldParser":
        """Get field parsing utilities (for CLI --fields option).

        Returns:
            FieldParser instance for handling field options
        """
        return FieldParser()


class FieldParser:
    """Helper for parsing and validating field options."""

    def __init__(self):
        self.required_fields = {"name", "mimeType", "size"}
        self.default_fields = [
            "id",
            "name",
            "mimeType",
            "size",
            "createdTime",
            "modifiedTime",
            "description",
            "owners",
            "webViewLink",
        ]

    def parse_fields(
        self, fields_str: Optional[str]
    ) -> tuple[List[str], Optional[List[str]]]:
        """Parse fields string and return (all_fields, requested_fields).

        Args:
            fields_str: Comma-separated string of field names

        Returns:
            Tuple of (all_fields, requested_fields) where:
                - all_fields: Complete list including required fields
                - requested_fields: Original user-requested fields (for display)
        """
        if not fields_str:
            return self.default_fields, None

        user_fields = [f.strip() for f in fields_str.split(",") if f.strip()]

        # Remove duplicates while preserving order
        seen = set()
        unique_fields = []
        for field in user_fields:
            if field not in seen:
                seen.add(field)
                unique_fields.append(field)

        # Combine with required fields
        all_fields = unique_fields.copy()
        for field in self.required_fields:
            if field not in all_fields:
                all_fields.append(field)

        return all_fields, unique_fields
