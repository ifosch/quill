"""Command-line interface for Quill."""

import click
from quill.drive.client import DriveClient
from quill.formatters.display import format_file_list


@click.group()
@click.version_option()
def cli():
    """Quill - Google Drive CLI Tool."""
    pass


@cli.command()
@click.option(
    "--fields",
    default=None,
    help="Comma-separated list of fields to retrieve for each file. "
    "Defaults to: id,name,mimeType,size,createdTime,modifiedTime,description,owners,webViewLink. "
    "Note: name, mimeType, and size are always included for proper display.",
)
def list_files(fields):
    """List files in your Google Drive."""
    client = DriveClient()

    # Define default fields (same as in DriveClient)
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

    # Required fields for display formatter
    required_fields = {"name", "mimeType", "size"}

    if fields:
        # Parse user-provided fields
        user_fields = set(f.strip() for f in fields.split(",") if f.strip())
        # Combine user fields with required fields
        all_fields = list(required_fields | user_fields)
        # Keep track of originally requested fields for display
        requested_fields = list(user_fields)
    else:
        # Use default fields if none specified
        all_fields = default_fields
        requested_fields = None

    result = client.list_files(fields=all_fields)
    click.echo(format_file_list(result["files"], requested_fields))
