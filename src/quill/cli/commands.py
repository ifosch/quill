"""CLI command definitions."""

import click
from quill.drive.client import DriveClient
from quill.formatters.display import format_file_list
from .navigation import interactive_pagination


@click.command()
@click.option(
    "--page-size",
    default=10,
    type=int,
    help="Number of files to display per page (default: 10)",
)
@click.option(
    "--page-token",
    default=None,
    help="Token for a specific page of results (for advanced use)",
)
@click.option(
    "--query",
    default=None,
    help="Search query to filter files (e.g., \"name contains 'report'\")",
)
@click.option(
    "--fields",
    default=None,
    help="Comma-separated list of fields to retrieve for each file. "
    "Defaults to: id,name,mimeType,size,createdTime,modifiedTime,description,owners,webViewLink. "
    "Note: name, mimeType, and size are always included for proper display.",
)
@click.option(
    "--no-interactive",
    is_flag=True,
    help="Disable interactive pagination and show only the first page",
)
def list_files(page_size, page_token, query, fields, no_interactive):
    """List files in your Google Drive with interactive pagination."""
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
        # Parse user-provided fields while preserving order and removing duplicates
        user_fields_raw = [f.strip() for f in fields.split(",") if f.strip()]
        # Remove duplicates while preserving order of first occurrence
        seen = set()
        user_fields = []
        for field in user_fields_raw:
            if field not in seen:
                seen.add(field)
                user_fields.append(field)
        
        # Combine user fields with required fields, preserving user-specified order
        all_fields = user_fields.copy()
        for field in required_fields:
            if field not in all_fields:
                all_fields.append(field)
        # Keep track of originally requested fields for display (preserving order, no duplicates)
        requested_fields = user_fields
    else:
        # Use default fields if none specified
        all_fields = default_fields
        requested_fields = None

    # If page_token is provided or no-interactive is set, use single page mode
    if page_token is not None or no_interactive:
        result = client.list_files(
            page_size=page_size, page_token=page_token, query=query, fields=all_fields
        )
        click.echo(format_file_list(result["files"], requested_fields))

        # Show next page token if available (for advanced users)
        if result.get("next_page_token"):
            click.echo(f"\nNext page token: {result['next_page_token']}")
            click.echo("Use --page-token option to get the next page")
    else:
        # Use interactive pagination by default
        interactive_pagination(client, page_size, query, all_fields, requested_fields)


@click.command()
@click.argument("file_id", required=True)
@click.option(
    "--output",
    default=None,
    help="Output path for the exported file. If not provided, saves to current directory with document name.",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show detailed progress information",
)
def export(file_id, output, verbose):
    """Export a file from Google Drive.
    
    Currently supports Google Docs export to HTML format (ZIP file).
    
    FILE_ID is the Google Drive file ID of the document to export.
    
    The exported file will be saved as a ZIP file containing the HTML representation
    of the Google Doc, including embedded images and styling.
    """
    try:
        client = DriveClient()
        
        if verbose:
            click.echo(f"Exporting file with ID: {file_id}")
        
        result_path = client.export(file_id, output)
        
        click.echo(f"Successfully exported to: {result_path}")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.ClickException("File not found")
    except PermissionError as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.ClickException("Permission denied")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.ClickException("Export failed")
