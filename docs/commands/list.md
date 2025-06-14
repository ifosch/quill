# List Files Command

The `list` command displays files from your Google Drive.

## Usage

```bash
quill list
```

## Options

- `--page-size`: Number of files to display (default: 10)

## Examples

List the first 10 files:
```bash
quill list
```

List 20 files:
```bash
quill list --page-size 20
```

## Output Format

The command displays files in a table format with the following columns:
- Name: The name of the file
- Type: The MIME type of the file
- Size: The size of the file in bytes (if available) 