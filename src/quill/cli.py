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
def list_files():
    """List files in your Google Drive."""
    client = DriveClient()
    result = client.list_files()
    click.echo(format_file_list(result["files"]))
