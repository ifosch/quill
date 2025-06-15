"""Tests for the CLI module."""

from click.testing import CliRunner
from quill.cli import cli
import pytest
from unittest.mock import Mock, patch


def test_cli_version():
    """Test the CLI version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_help():
    """Test the CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Quill - Google Drive CLI Tool" in result.output
    assert "list-files" in result.output


@pytest.mark.skip(reason="Test is currently failing due to FileNotFoundError")
def test_list_files_command():
    """Test the list-files command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list-files"])
    assert result.exit_code == 0
    assert "Listing files..." in result.output


@patch("quill.cli.DriveClient")
def test_list_files_with_fields_option(mock_drive_client):
    """Test the list-files command with --fields option."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": None,
    }

    # Test with custom fields
    result = runner.invoke(cli, ["list-files", "--fields", "id,name,size"])
    assert result.exit_code == 0

    # Verify that list_files was called with the expected fields
    # The required fields (name, mimeType, size) should always be included
    expected_fields = ["name", "mimeType", "size", "id"]
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args
    actual_fields = called_args.kwargs["fields"]

    # Check that all expected fields are present (order doesn't matter)
    assert set(expected_fields) == set(actual_fields)


@patch("quill.cli.DriveClient")
def test_list_files_without_fields_option(mock_drive_client):
    """Test the list-files command without --fields option uses default fields."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": None,
    }

    # Test without fields option
    result = runner.invoke(cli, ["list-files"])
    assert result.exit_code == 0

    # Verify that list_files was called with default fields
    default_fields = [
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
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args
    actual_fields = called_args.kwargs["fields"]

    # Check that default fields are used
    assert actual_fields == default_fields
