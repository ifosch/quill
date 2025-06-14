# Quill - Google Drive CLI Tool

A command-line interface tool for interacting with Google Drive, providing a simple and efficient way to manage your files and folders.

## Project Structure

```
quill/
├── src/                    # Source code
│   └── quill/             # Main package
│       ├── __init__.py
│       ├── cli.py         # CLI entry point and command definitions
│       ├── config.py      # Configuration management
│       ├── auth.py        # Authentication handling
│       ├── drive/         # Google Drive integration
│       │   ├── __init__.py
│       │   ├── client.py  # Drive API client
│       │   └── models.py  # Data models for Drive entities
│       └── formatters/    # Output formatting
│           ├── __init__.py
│           └── display.py # Formatting for CLI output
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Test configuration
│   ├── unit/            # Unit tests
│   │   └── __init__.py
│   └── integration/     # Integration tests
│       └── __init__.py
├── docs/                 # Documentation
│   ├── commands/        # Command reference and examples
│   ├── setup/          # Installation and configuration guides
│   └── examples/       # Common use cases and examples
├── .pre-commit-config.yaml  # Pre-commit hooks
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

### Directory Structure Explanation

- `src/quill/`: Main package containing all source code
  - `cli.py`: Command-line interface implementation and command definitions
  - `config.py`: Configuration management and settings
  - `auth.py`: Google OAuth2 authentication handling
  - `drive/`: Google Drive integration module
    - `client.py`: Drive API client implementation
    - `models.py`: Data models for Drive entities (files, folders, etc.)
  - `formatters/`: CLI output formatting
    - `display.py`: Functions for formatting and displaying data in the terminal

- `tests/`: Test suite
  - `unit/`: Unit tests for individual components
  - `integration/`: Integration tests for end-to-end functionality

- `docs/`: Project documentation
  - `commands/`: Detailed documentation for each CLI command
  - `setup/`: Installation and configuration guides
  - `examples/`: Common use cases and examples

## Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Usage

[Usage instructions will be added as features are implemented]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

[License information to be added] 