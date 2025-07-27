"""Tests for export CLI commands."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock
from click.testing import CliRunner

from quill.cli import cli


class TestExportCommand:
    """Tests for export CLI command."""

    def test_export_with_file_id_only(self):
        """Test export command with only file ID (auto-naming)."""
        runner = CliRunner()
        
        # Mock the DriveClient.export method
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.return_value = "My Document.zip"
            
            result = runner.invoke(cli, ['export', '1abc123'])
            
            # Verify command executed successfully
            assert result.exit_code == 0
            assert "Successfully exported" in result.output
            assert "My Document.zip" in result.output
            
            # Verify DriveClient was called correctly
            mock_client.export.assert_called_once_with('1abc123', output_path=None, format=None)

    def test_export_with_output_path(self):
        """Test export command with custom output path."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "custom_name.zip")
            
            with patch('quill.cli.commands.DriveClient') as mock_client_class:
                mock_client = Mock()
                mock_client_class.return_value = mock_client
                mock_client.export.return_value = output_path
                
                result = runner.invoke(cli, [
                    'export', 
                    '1abc123', 
                    '--output', output_path
                ])
                
                assert result.exit_code == 0
                assert "Successfully exported" in result.output
                assert "custom_name.zip" in result.output
                
                # Verify DriveClient was called with output path
                mock_client.export.assert_called_once_with('1abc123', output_path=output_path, format=None)

    def test_export_file_not_found(self):
        """Test export command when file doesn't exist."""
        runner = CliRunner()
        
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.side_effect = FileNotFoundError("File not found")
            
            result = runner.invoke(cli, ['export', 'nonexistent123'])
            
            assert result.exit_code == 1
            assert "Error: File not found" in result.output

    def test_export_permission_error(self):
        """Test export command when user lacks permission."""
        runner = CliRunner()
        
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.side_effect = PermissionError("Permission denied")
            
            result = runner.invoke(cli, ['export', 'restricted123'])
            
            assert result.exit_code == 1
            assert "Error: Permission denied" in result.output

    def test_export_generic_error(self):
        """Test export command when a generic error occurs."""
        runner = CliRunner()
        
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.side_effect = RuntimeError("API connection failed")
            
            result = runner.invoke(cli, ['export', '1abc123'])
            
            assert result.exit_code == 1
            assert "Error: API connection failed" in result.output

    def test_export_missing_file_id(self):
        """Test export command without required file ID argument."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['export'])
        
        # Should show usage/help for missing required argument
        assert result.exit_code == 2  # Click returns 2 for usage errors
        assert "Missing argument" in result.output or "Usage:" in result.output

    def test_export_help(self):
        """Test export command help text."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['export', '--help'])
        
        assert result.exit_code == 0
        assert "Export a file from Google Drive" in result.output
        assert "FILE_ID" in result.output
        assert "--output" in result.output

    def test_export_verbose_output(self):
        """Test export command with verbose output."""
        runner = CliRunner()
        
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.return_value = "Report.zip"
            
            result = runner.invoke(cli, [
                'export', 
                '1abc123',
                '--verbose'
            ])
            
            assert result.exit_code == 0
            assert "Exporting file with ID: 1abc123" in result.output
            assert "Successfully exported" in result.output
            assert "Report.zip" in result.output 

    def test_export_with_format_option(self):
        """Test export command with --format option."""
        runner = CliRunner()
        
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.return_value = "test.pdf"
            
            result = runner.invoke(cli, ['export', '1abc123', '--format', 'pdf'])
            
            assert result.exit_code == 0
            assert "Successfully exported to: test.pdf" in result.output
            mock_client.export.assert_called_with(
                '1abc123', output_path=None, format='pdf'
            )

    def test_export_with_invalid_format_option(self):
        """Test export command with invalid --format option."""
        runner = CliRunner()
        
        # Click will reject invalid choices before reaching our code
        result = runner.invoke(cli, ['export', '1abc123', '--format', 'invalid'])
        
        assert result.exit_code == 2  # Click's error code for invalid options
        assert "Invalid value for '--format'" in result.output

    def test_export_format_option_help(self):
        """Test that --format option shows in help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['export', '--help'])
        
        assert result.exit_code == 0
        assert "--format" in result.output
        assert "Export format" in result.output

    def test_export_smart_default_no_format_specified(self):
        """Test export command uses smart defaults when no format specified."""
        runner = CliRunner()
        
        with patch('quill.cli.commands.DriveClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_client.export.return_value = "test.html"
            
            result = runner.invoke(cli, ['export', '1abc123'])
            
            assert result.exit_code == 0
            assert "Successfully exported to: test.html" in result.output
            # Should call export with format=None (uses smart default)
            mock_client.export.assert_called_with(
                '1abc123', output_path=None, format=None
            ) 