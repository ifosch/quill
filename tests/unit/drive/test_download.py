"""Tests for drive download functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

from quill.drive.client import DriveClient
from quill.drive.models import DriveFile


class TestDriveClientDownload:
    """Tests for DriveClient download functionality."""

    def test_export_google_doc_to_html(self):
        """Test exporting a Google Doc to HTML format (ZIP file)."""
        # Test data
        file_id = "1test_google_doc_id"
        mock_export_content = b"fake_html_zip_content"
        
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_document.zip"
            
            # Mock the Google Drive API service
            mock_service = MagicMock()
            mock_export_request = MagicMock()
            mock_export_request.execute.return_value = mock_export_content
            mock_service.files().export.return_value = mock_export_request
            
            # Setup client with mocked service
            client = DriveClient()
            client.service = mock_service
            
            # This should fail initially - method doesn't exist yet
            client.export_google_doc_html(file_id, str(output_path))
            
            # Verify the API was called correctly
            mock_service.files().export.assert_called_once_with(
                fileId=file_id,
                mimeType="application/zip"  # HTML export format for Google Docs
            )
            
            # Verify the file was saved
            assert output_path.exists()
            assert output_path.read_bytes() == mock_export_content

    def test_export_google_doc_html_to_current_directory(self):
        """Test exporting Google Doc to HTML in current directory with auto-naming."""
        file_id = "1test_doc_id"
        mock_export_content = b"fake_zip_content"
        
        # Mock the file metadata to get the name
        mock_file_data = {
            "id": file_id,
            "name": "My Document",
            "mimeType": "application/vnd.google-apps.document"
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory to simulate current directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Mock the Google Drive API service
                mock_service = MagicMock()
                
                # Mock get file metadata
                mock_get_request = MagicMock()
                mock_get_request.execute.return_value = mock_file_data
                mock_service.files().get.return_value = mock_get_request
                
                # Mock export request
                mock_export_request = MagicMock()
                mock_export_request.execute.return_value = mock_export_content
                mock_service.files().export.return_value = mock_export_request
                
                # Setup client
                client = DriveClient()
                client.service = mock_service
                
                # This should fail - method doesn't exist yet
                result_path = client.export_google_doc_html(file_id)
                
                # Verify file was created with expected name
                expected_path = Path("My Document.zip")
                assert expected_path.exists()
                assert expected_path.read_bytes() == mock_export_content
                assert result_path == str(expected_path)
                
                # Verify API calls
                mock_service.files().get.assert_called_once_with(
                    fileId=file_id,
                    fields="name"
                )
                mock_service.files().export.assert_called_once_with(
                    fileId=file_id,
                    mimeType="application/zip"
                )
                
            finally:
                os.chdir(original_cwd)

    def test_export_google_doc_html_file_not_found(self):
        """Test error handling when file doesn't exist."""
        from googleapiclient.errors import HttpError
        
        file_id = "nonexistent_file_id"
        
        # Mock HTTP 404 error
        mock_error_response = Mock()
        mock_error_response.status = 404
        mock_http_error = HttpError(mock_error_response, b"File not found")
        
        # Mock service to raise error
        mock_service = MagicMock()
        mock_service.files().get.side_effect = mock_http_error
        
        client = DriveClient()
        client.service = mock_service
        
        # Should raise FileNotFoundError
        with pytest.raises(FileNotFoundError, match="File with ID nonexistent_file_id not found"):
            client.export_google_doc_html(file_id)

    def test_export_google_doc_html_permission_error(self):
        """Test error handling for permission denied."""
        from googleapiclient.errors import HttpError
        
        file_id = "restricted_file_id"
        
        # Mock HTTP 403 error
        mock_error_response = Mock()
        mock_error_response.status = 403
        mock_http_error = HttpError(mock_error_response, b"Permission denied")
        
        # Mock service to raise error on export
        mock_service = MagicMock()
        mock_get_request = MagicMock()
        mock_get_request.execute.return_value = {"name": "Test Doc"}
        mock_service.files().get.return_value = mock_get_request
        mock_service.files().export.side_effect = mock_http_error
        
        client = DriveClient()
        client.service = mock_service
        
        # Should raise PermissionError
        with pytest.raises(PermissionError, match="Insufficient permissions"):
            client.export_google_doc_html(file_id) 