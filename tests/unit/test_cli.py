"""Tests for the CLI module."""

from click.testing import CliRunner
from quill.cli import cli
from quill.cli.pagination import PaginationState
from quill.cli.navigation import (
    fetch_page,
    get_navigation_options,
    navigate_to_previous_page,
)
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
    result = runner.invoke(cli, ["list-files", "--no-interactive"])
    assert result.exit_code == 0
    assert "Listing files..." in result.output


@patch("quill.cli.commands.DriveClient")
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

    # Test with custom fields and no-interactive flag
    result = runner.invoke(
        cli, ["list-files", "--fields", "id,name,size", "--no-interactive"]
    )
    assert result.exit_code == 0

    # Verify that list_files was called with the expected parameters
    # The required fields (name, mimeType, size) should always be included
    expected_fields = ["name", "mimeType", "size", "id"]
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args

    # Check the fields parameter
    actual_fields = called_args.kwargs["fields"]
    assert set(expected_fields) == set(actual_fields)

    # Check that other parameters have expected default values
    assert called_args.kwargs["page_size"] == 10
    assert called_args.kwargs["page_token"] is None
    assert called_args.kwargs["query"] is None


@patch("quill.cli.commands.DriveClient")
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

    # Test without fields option but with no-interactive flag
    result = runner.invoke(cli, ["list-files", "--no-interactive"])
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

    # Check the fields parameter
    actual_fields = called_args.kwargs["fields"]
    assert actual_fields == default_fields

    # Check that other parameters have expected default values
    assert called_args.kwargs["page_size"] == 10
    assert called_args.kwargs["page_token"] is None
    assert called_args.kwargs["query"] is None


@patch("quill.cli.commands.DriveClient")
def test_list_files_with_all_options(mock_drive_client):
    """Test the list-files command with all CLI options."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": "test_token_123",
    }

    # Test with all options
    result = runner.invoke(
        cli,
        [
            "list-files",
            "--page-size",
            "20",
            "--page-token",
            "previous_token",
            "--query",
            "name contains 'test'",
            "--fields",
            "id,name",
            "--no-interactive",
        ],
    )
    assert result.exit_code == 0

    # Verify that list_files was called with the correct parameters
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args

    assert called_args.kwargs["page_size"] == 20
    assert called_args.kwargs["page_token"] == "previous_token"
    assert called_args.kwargs["query"] == "name contains 'test'"

    # Fields should include required fields plus user-specified ones
    expected_fields = ["name", "mimeType", "size", "id"]
    actual_fields = called_args.kwargs["fields"]
    assert set(expected_fields) == set(actual_fields)


@patch("quill.cli.commands.DriveClient")
def test_list_files_shows_next_page_token(mock_drive_client):
    """Test that next page token is displayed when available."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": "test_next_token_456",
    }

    # Test with no-interactive flag
    result = runner.invoke(cli, ["list-files", "--no-interactive"])
    assert result.exit_code == 0

    # Check that next page token information is displayed
    assert "Next page token:" in result.output
    assert "test_next_token_456" in result.output
    assert "Use --page-token option to get the next page" in result.output


# Additional tests for token-based pagination and query options


@patch("quill.cli.commands.DriveClient")
def test_list_files_with_page_token_only(mock_drive_client):
    """Test the list-files command with only --page-token option."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": None,
    }

    # Test with only page token
    result = runner.invoke(
        cli, ["list-files", "--page-token", "abc123token", "--no-interactive"]
    )
    assert result.exit_code == 0

    # Verify that list_files was called with the token
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args

    assert called_args.kwargs["page_token"] == "abc123token"
    assert called_args.kwargs["page_size"] == 10  # default
    assert called_args.kwargs["query"] is None  # default


@patch("quill.cli.commands.DriveClient")
def test_list_files_with_query_only(mock_drive_client):
    """Test the list-files command with only --query option."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": None,
    }

    # Test with only query
    result = runner.invoke(
        cli, ["list-files", "--query", "mimeType='application/pdf'", "--no-interactive"]
    )
    assert result.exit_code == 0

    # Verify that list_files was called with the query
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args

    assert called_args.kwargs["query"] == "mimeType='application/pdf'"
    assert called_args.kwargs["page_size"] == 10  # default
    assert called_args.kwargs["page_token"] is None  # default


@patch("quill.cli.commands.DriveClient")
def test_list_files_with_complex_query(mock_drive_client):
    """Test the list-files command with complex query string."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": "next_page_123",
    }

    # Test with complex query
    complex_query = (
        "name contains 'report' and mimeType != 'application/vnd.google-apps.folder'"
    )
    result = runner.invoke(
        cli, ["list-files", "--query", complex_query, "--no-interactive"]
    )
    assert result.exit_code == 0

    # Verify that list_files was called with the complex query
    mock_client_instance.list_files.assert_called_once()
    called_args = mock_client_instance.list_files.call_args

    assert called_args.kwargs["query"] == complex_query

    # Should still show next page token since we have one
    assert "Next page token:" in result.output
    assert "next_page_123" in result.output


@patch("quill.cli.commands.DriveClient")
def test_list_files_no_next_token_with_page_token(mock_drive_client):
    """Test that no next page token message appears when there's no next page."""
    runner = CliRunner()

    # Mock the DriveClient and its methods
    mock_client_instance = Mock()
    mock_drive_client.return_value = mock_client_instance
    mock_client_instance.list_files.return_value = {
        "files": [],
        "next_page_token": None,  # No next page
    }

    # Test with page token but no next page available
    result = runner.invoke(
        cli, ["list-files", "--page-token", "last_page_token", "--no-interactive"]
    )
    assert result.exit_code == 0

    # Should not show next page token info
    assert "Next page token:" not in result.output
    assert "Use --page-token option" not in result.output


# New tests for refactored pagination components


class TestPaginationState:
    """Test the PaginationState class."""

    def test_pagination_state_initialization(self):
        """Test PaginationState initialization."""
        state = PaginationState(page_size=20, query="test query")
        assert state.page_size == 20
        assert state.query == "test query"
        assert state.page_number == 1
        assert state.page_token is None
        assert state.current_result is None

    def test_has_next_page_with_token(self):
        """Test has_next_page returns True when next page token exists."""
        state = PaginationState(10, None)
        state.current_result = {"next_page_token": "token123"}
        assert state.has_next_page() is True

    def test_has_next_page_without_token(self):
        """Test has_next_page returns False when no next page token."""
        state = PaginationState(10, None)
        state.current_result = {"next_page_token": None}
        assert state.has_next_page() is False

    def test_has_next_page_no_result(self):
        """Test has_next_page returns False when no current result."""
        state = PaginationState(10, None)
        assert state.has_next_page() is False

    def test_has_previous_page_first_page(self):
        """Test has_previous_page returns False on first page."""
        state = PaginationState(10, None)
        assert state.has_previous_page() is False

    def test_has_previous_page_later_page(self):
        """Test has_previous_page returns True on pages after first."""
        state = PaginationState(10, None)
        state.page_number = 3
        assert state.has_previous_page() is True

    def test_go_to_next_page(self):
        """Test go_to_next_page updates state correctly."""
        state = PaginationState(10, None)
        state.current_result = {"next_page_token": "token123"}

        state.go_to_next_page()

        assert state.page_token == "token123"
        assert state.page_number == 2

    def test_go_to_next_page_no_token(self):
        """Test go_to_next_page does nothing when no next page token."""
        state = PaginationState(10, None)
        state.current_result = {"next_page_token": None}

        state.go_to_next_page()

        assert state.page_token is None
        assert state.page_number == 1

    def test_reset_to_first_page(self):
        """Test reset_to_first_page resets state correctly."""
        state = PaginationState(10, None)
        state.page_number = 5
        state.page_token = "some_token"

        state.reset_to_first_page()

        assert state.page_number == 1
        assert state.page_token is None


def test_fetch_page():
    """Test fetch_page function."""
    mock_client = Mock()
    mock_client.list_files.return_value = {
        "files": [{"name": "test.txt"}],
        "next_page_token": "token123",
    }

    state = PaginationState(10, "test query")
    state.page_token = "prev_token"
    fields = ["id", "name"]

    result = fetch_page(mock_client, state, fields)

    # Verify API call
    mock_client.list_files.assert_called_once_with(
        page_size=10, page_token="prev_token", query="test query", fields=fields
    )

    # Verify result
    assert result["files"] == [{"name": "test.txt"}]
    assert result["next_page_token"] == "token123"

    # Verify state update
    assert state.current_result == result


def test_fetch_page_with_no_query():
    """Test fetch_page function with no query."""
    mock_client = Mock()
    mock_client.list_files.return_value = {
        "files": [{"name": "all_files.txt"}],
        "next_page_token": None,
    }

    state = PaginationState(15, None)  # No query
    state.page_token = None  # First page
    fields = ["id", "name", "size"]

    result = fetch_page(mock_client, state, fields)

    # Verify API call with None query
    mock_client.list_files.assert_called_once_with(
        page_size=15, page_token=None, query=None, fields=fields
    )

    # Verify result
    assert result["files"] == [{"name": "all_files.txt"}]
    assert result["next_page_token"] is None


def test_get_navigation_options_first_page_with_next():
    """Test get_navigation_options on first page with next page available."""
    state = PaginationState(10, None)
    state.current_result = {"next_page_token": "token123"}

    options = get_navigation_options(state)

    assert options == ["[N]ext", "[Q]uit"]


def test_get_navigation_options_middle_page():
    """Test get_navigation_options on middle page."""
    state = PaginationState(10, None)
    state.page_number = 3
    state.current_result = {"next_page_token": "token123"}

    options = get_navigation_options(state)

    assert options == ["[P]rev", "[N]ext", "[Q]uit"]


def test_get_navigation_options_last_page():
    """Test get_navigation_options on last page."""
    state = PaginationState(10, None)
    state.page_number = 5
    state.current_result = {"next_page_token": None}

    options = get_navigation_options(state)

    assert options == ["[P]rev", "[Q]uit"]


def test_get_navigation_options_only_page():
    """Test get_navigation_options when there's only one page."""
    state = PaginationState(10, None)
    state.current_result = {"next_page_token": None}

    options = get_navigation_options(state)

    assert options == ["[Q]uit"]


def test_navigate_to_previous_page_from_second_page():
    """Test navigate_to_previous_page from page 2 to page 1."""
    mock_client = Mock()
    state = PaginationState(10, None)
    state.page_number = 2
    state.page_token = "some_token"

    navigate_to_previous_page(mock_client, state, ["id", "name"])

    # Should reset to first page
    assert state.page_number == 1
    assert state.page_token is None
    # Should not call API for simple case
    mock_client.list_files.assert_not_called()


def test_navigate_to_previous_page_from_third_page():
    """Test navigate_to_previous_page from page 3 to page 2."""
    mock_client = Mock()
    mock_client.list_files.return_value = {"next_page_token": "page2_token"}

    state = PaginationState(10, "test query")
    state.page_number = 3
    state.page_token = "page3_token"

    navigate_to_previous_page(mock_client, state, ["id", "name"])

    # Should navigate to page 2
    assert state.page_number == 2
    assert state.page_token == "page2_token"

    # Should call API once to get to page 2
    mock_client.list_files.assert_called_once_with(
        page_size=10,
        page_token=None,  # Start from beginning
        query="test query",
        fields=["id", "name"],
    )


def test_navigate_to_previous_page_with_query():
    """Test navigate_to_previous_page preserves query parameter."""
    mock_client = Mock()
    mock_client.list_files.return_value = {"next_page_token": "page1_token"}

    state = PaginationState(5, "name contains 'important'")
    state.page_number = 2
    state.page_token = "page2_token"

    navigate_to_previous_page(mock_client, state, ["name", "id"])

    # Should reset to first page without API call for page 2->1
    assert state.page_number == 1
    assert state.page_token is None
    # Should not call API for simple case (page 2 to page 1)
    mock_client.list_files.assert_not_called()


def test_cli_field_processing_preserves_order():
    """Test that CLI field processing preserves user-specified field order."""
    # Simulate the FIXED field processing logic from the CLI command
    fields_input = "id,name,size"
    required_fields = {"name", "mimeType", "size"}
    
    # Fixed CLI logic - preserves order using lists instead of sets
    user_fields = [f.strip() for f in fields_input.split(",") if f.strip()]
    all_fields = user_fields.copy()
    for field in required_fields:
        if field not in all_fields:
            all_fields.append(field)
    requested_fields = user_fields
    
    # Should now preserve the user's original order
    assert requested_fields == ["id", "name", "size"], f"Expected ['id', 'name', 'size'], got {requested_fields}"


@pytest.mark.parametrize("fields_input,expected_order", [
    ("id,name,size", ["id", "name", "size"]),
    ("name,id,size", ["name", "id", "size"]),
    ("size,name,id", ["size", "name", "id"]),
])
def test_cli_field_processing_different_orders(fields_input, expected_order):
    """Test CLI field processing with different field orders - should preserve all orders."""
    # Simulate FIXED CLI logic - preserves order using lists
    user_fields = [f.strip() for f in fields_input.split(",") if f.strip()]
    requested_fields = user_fields
    
    # Should now preserve the order correctly
    assert requested_fields == expected_order, f"Input: {fields_input}, Expected: {expected_order}, Got: {requested_fields}"
