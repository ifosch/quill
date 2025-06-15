# Quill

A command-line interface tool for interacting with Google Drive, providing a simple and efficient way to manage your files and folders.

## Features

- List files and folders in Google Drive
- View file details
- Filter and search files
- Pagination support
- Beautiful terminal output

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

### List Files

List files in your Google Drive:
```bash
quill list-files
```

Options:
- `--page-size`: Number of files to list per page (default: 10)
- `--page-token`: Token for the next page of results
- `--query`: Search query to filter files
- `--fields`: Comma-separated list of fields to include in the response (default: id,name,mimeType,size,createdTime,modifiedTime,description,owners,webViewLink)

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

#### Examples

List files with default fields:
```bash
quill list-files
```

List files with custom fields (only ID and name):
```bash
quill list-files --fields "id,name"
```

List files with pagination and search:
```bash
quill list-files --page-size 20 --query "name contains 'report'"
```

List files with specific fields and search:
```bash
quill list-files --fields "id,name,size,modifiedTime" --query "mimeType='application/pdf'"
```

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

## Development

### Setup

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
f
2. Install pre-commit hooks:ff
   ```bashf
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

### Code Quality

- Format code:
  ```bash
  ruff format .
  ```

- Check code:
  ```bash
  ruff check .
  ```

- Type checking:
  ```bash
  ty check .
  ```

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