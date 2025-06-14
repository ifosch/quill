"""Command-line interface for Quill."""

import click


@click.group()
@click.version_option()
def cli():
    """Quill - Google Drive CLI Tool."""
    pass


@cli.command()
def list_files():
    """List files in your Google Drive."""
    click.echo("Listing files...")  # Placeholder for actual implementation
