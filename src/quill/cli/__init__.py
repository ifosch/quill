"""Command-line interface for Quill."""

import click
from .commands import list_files


@click.group()
@click.version_option()
def cli():
    """Quill - Google Drive CLI Tool."""
    pass


# Register commands
cli.add_command(list_files)

# Export the main CLI for external use
__all__ = ["cli"]
