# User Quick Start Guide

This guide will help you get started with Quill for common Google Drive tasks.

## Prerequisites

Before using Quill, make sure you have:

1. **Google Drive API credentials** - Follow the [Installation Guide](installation.md) to set up your credentials
2. **Quill installed** - Install Quill using `uv sync` or `pip install -e .`

## Basic Usage

### 1. List Your Files

Start by exploring your Google Drive files:

```bash
# Interactive browsing (default)
quill list-files

# Non-interactive mode for scripting
quill list-files --no-interactive
```

**Interactive Navigation:**
- Use `N` or `n` to go to the next page
- Use `P` or `p` to go to the previous page
- Use `Q` or `q` to quit

### 2. Search for Specific Files

Find files using Google Drive's search capabilities:

```bash
# Search for PDF files
quill list-files --query "mimeType='application/pdf'"

# Search for files modified recently
quill list-files --query "modifiedTime > '2024-01-01'"

# Search for files containing "report" in the name
quill list-files --query "name contains 'report'"

# Complex search combining multiple conditions
quill list-files --query "name contains 'report' and mimeType='application/pdf'"
```

### 3. Customize Output Fields

Choose exactly what information you want to see:

```bash
# Minimal output - just names and sizes
quill list-files --fields "name,size"

# Detailed output with timestamps
quill list-files --fields "name,size,modifiedTime,createdTime"

# Full metadata (default)
quill list-files --fields "id,name,mimeType,size,createdTime,modifiedTime,description,owners,webViewLink"
```

### 4. Get File Details

Get detailed information about a specific file:

```bash
quill get-file 1abc123def456ghi789jkl012mno345pqr678stu901vwx
```

### 5. Export Google Workspace Documents

Export your Google Workspace documents with smart defaults:

```bash
# Export with automatic format selection
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx

# Export with custom format
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format pdf

# Export to specific location
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --output "My Document.pdf"
```

## Common Workflows

### Workflow 1: Find and Export a Document

```bash
# 1. Search for your document
quill list-files --query "name contains 'Project Report'"

# 2. Copy the file ID from the output
# 3. Export the document
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format pdf
```

### Workflow 2: Export Multiple Spreadsheets

```bash
# 1. Find all Google Sheets
quill list-files --query "mimeType='application/vnd.google-apps.spreadsheet'"

# 2. Export each one to Excel format
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format xlsx --output "Sheet1.xlsx"
quill export 2def456ghi789jkl012mno345pqr678stu901vwx --format xlsx --output "Sheet2.xlsx"
```

### Workflow 3: Backup Presentations

```bash
# 1. Find all Google Slides presentations
quill list-files --query "mimeType='application/vnd.google-apps.presentation'"

# 2. Export each to PDF for backup
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --format pdf --output "Presentation1.pdf"
quill export 2def456ghi789jkl012mno345pqr678stu901vwx --format pdf --output "Presentation2.pdf"
```

## Smart Format Defaults

Quill automatically selects the best export format for each file type:

| File Type | Default Format | Use Case |
|-----------|----------------|----------|
| Google Docs | HTML (ZIP) | Web viewing, sharing |
| Google Sheets | XLSX | Excel compatibility |
| Google Slides | PDF | Presentation sharing |
| Google Drawings | PNG | Image viewing |
| Google Forms | ZIP (HTML) | Web deployment |

## Tips and Tricks

### 1. Use Verbose Mode for Debugging

```bash
quill export 1abc123def456ghi789jkl012mno345pqr678stu901vwx --verbose
```

### 2. Combine Search and Export

```bash
# Find and export in one workflow
quill list-files --query "name contains 'report'" --fields "id,name" --no-interactive
# Copy the ID and export
quill export <file_id> --format pdf
```

### 3. Batch Export with Scripting

```bash
#!/bin/bash
# Export all Google Docs to HTML
quill list-files --query "mimeType='application/vnd.google-apps.document'" --fields "id,name" --no-interactive | \
while read -r id name; do
    quill export "$id" --output "${name}.zip"
done
```

### 4. Get Help When Needed

```bash
# General help
quill --help

# Command-specific help
quill list-files --help
quill export --help
quill get-file --help
```

## Troubleshooting

### Common Issues

1. **"File not found" error**
   - Verify the file ID is correct
   - Ensure you have access to the file
   - Check if the file still exists in Google Drive

2. **"Permission denied" error**
   - Verify your Google Drive API credentials
   - Check if you have permission to access the file
   - Ensure the Google Drive API is enabled in your project

3. **"Invalid format" error**
   - Use only supported formats: `html`, `pdf`, `xlsx`, `csv`
   - Check the format compatibility with your file type

4. **Export fails**
   - Try with `--verbose` for more details
   - Check your internet connection
   - Verify the file is a Google Workspace document

## Next Steps

- Read the [Commands Reference](commands.md) for detailed command documentation
- Check the [Installation Guide](installation.md) for setup instructions
- Review the [Contributing Guidelines](contributing.md) if you want to contribute 