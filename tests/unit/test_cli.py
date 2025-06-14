"""Tests for the CLI module."""

from click.testing import CliRunner
from quill.cli import cli


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


def test_list_files_command():
    """Test the list-files command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list-files"])
    assert result.exit_code == 0
    assert "Listing files..." in result.output
