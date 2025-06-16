# Quill

A command-line interface tool for interacting with Google Drive, providing a simple and efficient way to manage your files and folders.

## Features

- **Interactive file browsing** with intuitive pagination controls
- List files and folders in Google Drive with advanced filtering
- View detailed file information
- **Smart pagination** with next/previous page navigation
- Advanced search and query capabilities
- Beautiful, clean terminal output
- **Token-based pagination** support for large datasets
- Flexible field selection for customized output

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quill.git
   cd quill
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## Configuration

### Google Drive API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials JSON file

### Credentials File

You can provide your Google Drive API credentials in two ways:

1. **Default Location:**
   Place the downloaded credentials file at:
   ```
   ~/.config/quill/credentials.json
   ```

2. **Custom Location:**
   Set the `GOOGLE_DRIVE_CREDENTIALS` environment variable to point to your credentials file:
   ```bash
   # Linux/macOS
   export GOOGLE_DRIVE_CREDENTIALS="/path/to/your/credentials.json"
   
   # Windows (PowerShell)
   $env:GOOGLE_DRIVE_CREDENTIALS="C:\path\to\your\credentials.json"
   
   # Windows (Command Prompt)
   set GOOGLE_DRIVE_CREDENTIALS=C:\path\to\your\credentials.json
   ```

## Usage

### Interactive File Browsing

**New!** Quill now provides an interactive pagination experience by default:

```bash
quill list-files
```

This will show your files with a clean navigation interface:
```
My Document.pdf (1.2 MB) - PDF - Modified: 2024-01-15
Project Report.docx (856 KB) - Word - Modified: 2024-01-14
...
[P]rev [N]ext [Q]uit: _
```

**Navigation:**
- **N** or **n**: Go to next page
- **P** or **p**: Go to previous page  
- **Q** or **q**: Quit and return to command line

### Non-Interactive Mode

For scripting or automated use, disable interactive mode:
```bash
quill list-files --no-interactive
```

### List Files Options

All list-files options work in both interactive and non-interactive modes:

- `--page-size`: Number of files per page (default: 10)
- `--page-token`: Specific page token for direct page access
- `--query`: Search query to filter files
- `--fields`: Custom field selection for output
- `--no-interactive`: Disable interactive pagination

#### Advanced Search Examples

**Interactive search with pagination:**
```bash
# Search for PDFs interactively
quill list-files --query "mimeType='application/pdf'"

# Find files modified in the last week (interactive)
quill list-files --query "modifiedTime > '2024-01-01'"

# Complex search with multiple conditions
quill list-files --query "name contains 'report' and mimeType='application/pdf'"
```

**Non-interactive with specific pages:**
```bash
# Get exactly 20 files, no interaction
quill list-files --page-size 20 --no-interactive

# Use page token for specific page access
quill list-files --page-token "ABC123token" --no-interactive
```

#### Field Customization

**Default fields:** `id,name,mimeType,size,createdTime,modifiedTime,description,owners,webViewLink`

Choose exactly what information you want to see:

```bash
# Use default fields (comprehensive output)
quill list-files

# Minimal output - just names and sizes
quill list-files --fields "name,size"

# Detailed output with timestamps and owners
quill list-files --fields "name,size,modifiedTime,createdTime,owners"

# Full metadata output (same as default)
quill list-files --fields "id,name,mimeType,size,createdTime,modifiedTime,description,owners,webViewLink"
```

#### Available Fields
The `--fields` option accepts any combination of these Google Drive API fields:
- `id`: File ID
- `name`: File name  
- `mimeType`: MIME type of the file
- `size`: File size in bytes
- `createdTime`: Creation timestamp
- `modifiedTime`: Last modification timestamp
- `description`: File description
- `owners`: File owners information
- `webViewLink`: Link to view the file in Google Drive
- And many others supported by the Google Drive API

**Note:** The fields `name`, `mimeType`, and `size` are always included to ensure proper display formatting.

### View File Details

Get detailed information about a specific file:
```bash
quill get-file <file_id>
```

Example:
```bash
quill get-file 1abc...xyz
```

### Help

Get help on available commands:
```bash
quill --help
```

Get help on specific commands:
```bash
quill list-files --help
quill get-file --help
```

## Architecture

Quill features a clean, modular architecture:

```
src/quill/
├── cli/                    # Command-line interface
│   ├── __init__.py        # CLI registration and main entry
│   ├── commands.py        # Click command definitions  
│   ├── pagination.py      # Pagination state management
│   └── navigation.py      # Interactive navigation logic
├── drive/                 # Google Drive integration
│   ├── client.py         # Drive API client
│   └── models.py         # Data models
├── formatters/           # Output formatting
│   └── display.py       # Terminal display formatters
├── auth.py              # Authentication handling
└── config.py            # Configuration management
```

This modular design ensures:
- **Separation of concerns** for maintainability
- **Easy testing** with focused unit tests
- **Extensibility** for future features
- **Clean interfaces** between components

## Development

### Setup

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage (fails if coverage is less than 80%):
```bash
pytest --cov=quill --cov-report=term-missing --cov-fail-under=80
```

**Current test coverage: 82.72%** ✅ (exceeds 80% requirement)

### Code Quality Checks

Run the complete verification suite:

```bash
# Format code
ruff format .

# Lint and auto-fix issues  
ruff check . --fix

# Type checking
ty check .

# Run tests with coverage
pytest --cov=quill --cov-report=term-missing --cov-fail-under=80
```

**All checks must pass before committing changes.**

### Documentation Generation

Generate HTML documentation using Sphinx:

```bash
# Build documentation
cd docs && sphinx-build -b html source build/html

# View documentation locally
# Open docs/build/html/index.html in your browser
```

**Documentation features:**
- **API documentation** - Automatically generated from docstrings
- **User guides** - Installation, quickstart, and usage examples
- **Command reference** - Detailed CLI documentation
- **Google-style docstrings** - Follow project conventions
- **Markdown support** - Write docs in Markdown format

The generated documentation includes comprehensive API reference, usage examples, and development guides.

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:
- **ruff**: Code formatting and linting
- **ty**: Type checking
- **pytest**: Test execution

Hooks run automatically on commit, or manually:
```bash
pre-commit run --all-files
```

### Project Standards

- **Test Coverage**: Minimum 80% (currently 82.72%)
- **Type Safety**: Full type annotation coverage with `ty`
- **Code Quality**: Enforced via `ruff` linting
- **Commit Messages**: Follow conventional commit format
- **Interactive Features**: Default to user-friendly interactive mode
- **Backward Compatibility**: Support non-interactive mode for automation

## Troubleshooting

### Common Issues

1. **Credentials File Not Found**
   - Ensure the credentials file exists at the default location or
   - Verify the `GOOGLE_DRIVE_CREDENTIALS` environment variable is set correctly
   - Check file permissions

2. **Authentication Errors**
   - Verify the credentials file is valid
   - Ensure the Google Drive API is enabled in your project
   - Check if the OAuth consent screen is configured correctly

3. **API Rate Limits**
   - The Google Drive API has rate limits
   - Consider implementing exponential backoff for retries
   - Monitor your API usage in the Google Cloud Console

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 