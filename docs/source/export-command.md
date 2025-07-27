# Export Command

The `export` command allows you to download and export Google Workspace documents from Google Drive with smart format defaults and customizable options.

## Overview

```bash
quill export <file_id> [OPTIONS]
```

The export command supports Google Workspace documents (Docs, Sheets, Slides, Drawings, Forms) and automatically selects the optimal export format based on the file type. You can override the default format using the `--format` option.

## Arguments

- `file_id` (required): The Google Drive file ID of the document to export

## Options

- `--output TEXT`: Output path for the exported file. If not provided, saves to current directory with document name
- `--format [html|pdf|xlsx|csv]`: Export format (auto-detected if not specified)
- `--verbose`: Show detailed progress information
- `--help`: Show help message and exit

## Smart Format Defaults

Quill automatically selects the optimal export format based on the file's MIME type:

| File Type | Default Format | Description |
|-----------|----------------|-------------|
| Google Docs | HTML (ZIP) | HTML export with embedded resources in ZIP format |
| Google Sheets | XLSX | Excel format for spreadsheets |
| Google Slides | PDF | PDF format for presentations |
| Google Drawings | PNG | PNG image format |
| Google Forms | ZIP | HTML export in ZIP format |

## Supported Formats

You can override the smart defaults with these format options:

- `html`: HTML export (ZIP file for Google Docs)
- `pdf`: PDF export
- `xlsx`: Excel format (for spreadsheets)
- `csv`: CSV format (for spreadsheets)

## Usage Examples

### Basic Export

Export a document using the smart default format:

```bash
# Export a Google Doc to HTML (default)
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx

# Export a Google Sheet to Excel (default)
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx

# Export a Google Slides presentation to PDF (default)
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx
```

### Custom Format Export

Override the default format:

```bash
# Export a Google Doc to PDF instead of HTML
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format pdf

# Export a Google Sheet to CSV instead of XLSX
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format csv

# Export a presentation to HTML instead of PDF
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format html
```

### Custom Output Path

Specify where to save the exported file:

```bash
# Export to a specific filename
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --output "My Report.pdf"

# Export to a specific directory
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --output "/path/to/exports/document.pdf"

# Export with custom name and format
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format xlsx --output "Data Analysis.xlsx"
```

### Verbose Output

Get detailed information about the export process:

```bash
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --verbose
```

This will show:
- The file ID being exported
- The detected file type
- The selected format (default or override)
- The output path
- Success confirmation

## Error Handling

The export command handles various error conditions:

### File Not Found (404)
```bash
Error: File with ID 1abc123def456ghi789jkl012mno345pqr678stu901vwx not found.
```

### Permission Denied (401/403)
```bash
Error: Insufficient permissions to export the file.
```

### Invalid Format
```bash
Error: Unsupported format: invalid_format
```

### Invalid Format Option
```bash
Error: Invalid value for '--format': 'invalid' is not one of 'html', 'pdf', 'xlsx', 'csv'.
```

## Technical Details

### Google Drive API Integration

The export command uses the Google Drive API's `files.export` endpoint for Google Workspace documents. This endpoint:

- Converts Google Workspace documents to various formats
- Maintains formatting and structure
- Handles embedded resources (images, styles, etc.)
- Provides consistent output across different document types

### File Naming

When no output path is specified, Quill automatically generates a filename based on:

1. The original document name from Google Drive
2. The appropriate file extension for the export format

For example:
- Document named "Project Report" exported as HTML → `Project Report.zip`
- Spreadsheet named "Sales Data" exported as Excel → `Sales Data.xlsx`
- Presentation named "Q4 Review" exported as PDF → `Q4 Review.pdf`

### Format Compatibility

Not all formats are compatible with all file types. The smart defaults ensure optimal compatibility:

- **Google Docs**: Best exported as HTML for web viewing or PDF for printing
- **Google Sheets**: Best exported as XLSX for Excel compatibility or CSV for data processing
- **Google Slides**: Best exported as PDF for presentation sharing
- **Google Drawings**: Best exported as PNG for image viewing
- **Google Forms**: Best exported as ZIP (HTML) for web deployment

## Related Commands

- `quill list-files` - List files to find file IDs
- `quill get-file` - Get detailed information about a specific file
- `quill --help` - Show general help information 