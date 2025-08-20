# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Custom export templates (planned)

## [0.2.12] - 2025-08-15

### Added
- **ODS format support for Google Sheets export**
  - Add ODS (OpenDocument Spreadsheet) format to supported export formats
  - Update CLI command to include 'ods' in format choices
  - Add ODS MIME type mapping: `application/vnd.oasis.opendocument.spreadsheet`
  - Add ODS file extension mapping: `.ods`
  - Update documentation in README.md and export-command.md
  - Add comprehensive test for ODS format export functionality
  - Update CLI help text to include ODS in supported formats list

This enables users to export Google Sheets directly to LibreOffice Sheets format, which is natively supported by the Google Drive API. The ODS format provides better compatibility with open-source office suites and maintains formatting and structure of the original spreadsheet.

## [0.2.11] - 2025-08-15

### Fixed
- **Release workflow improvements**
  - Fix JSON escaping in GitHub release update using jq
  - Fix shell interpretation of newlines and special characters
  - Ensure GitHub release notes are updated correctly after publishing

## [0.2.10] - 2025-08-15

### Added
- **EPUB format support for Google Docs export**
  - Add EPUB format to supported export formats in DriveClient
  - Update CLI command to include EPUB in format choices
  - Add comprehensive tests for EPUB export functionality
  - Update documentation in README.md and export-command.md
  - EPUB format uses MIME type 'application/epub+zip' and file extension '.epub'
  - Maintains consistency with existing export format implementation
  - Users can now export Google Docs to EPUB format for e-book creation

### Changed
- **Release workflow improvements**
  - Implement separated release and testing workflows
  - Create new Test Package Installation workflow for manual testing
  - Simplify release workflow to focus only on publishing
  - Add configurable wait times and flexible testing options
  - Handle TestPyPI/PyPI duality with independent testing
  - Add GitHub release version auto-detection for testing
  - Remove redundant clean_after parameter (GitHub Actions is ephemeral)
  - Consolidate documentation into single comprehensive guide

## [0.2.9] - 2025-08-15

### Added
- **EPUB format support for Google Docs export**
  - Add EPUB format to supported export formats in DriveClient
  - Update CLI command to include EPUB in format choices
  - Add comprehensive tests for EPUB export functionality
  - Update documentation in README.md and export-command.md
  - EPUB format uses MIME type 'application/epub+zip' and file extension '.epub'
  - Maintains consistency with existing export format implementation
  - Users can now export Google Docs to EPUB format for e-book creation

- **Dynamic versioning implementation**
  - Replace static version in pyproject.toml with dynamic versioning
  - Add uv-dynamic-versioning to build system requirements
  - Update __init__.py to use importlib.metadata for version access
  - Remove version validation from GitHub Actions workflow
  - Add fallback version for development environments

This change enables automatic version management from Git tags, eliminating the need to manually update pyproject.toml before releases.

### Fixed
- **Release script updates for dynamic versioning**
  - Update get_current_version() to extract version from Git tag instead of pyproject.toml
  - Fix build_package() to handle dynamic versioning package names
  - Add proper error handling for missing Git tags
  - Improve version detection and display in release process

### Performance
- **Script improvements**
  - Increase timeout from 30 seconds to 60 seconds between retry attempts
  - Increase maximum retry attempts from 3 to 5 attempts
  - Improves reliability for package installation testing
  - Provides better resilience against transient network problems



## [0.2.6] - 2025-08-14

### Added
- **ODT (OpenDocument Text) export format support**
  - Add ODT format to supported export formats in drive client
  - Update CLI commands to include ODT in format choices
  - Add comprehensive tests for ODT format validation and handling
  - Update documentation to include ODT format in all relevant sections
  - Update roadmap to mark ODT format as completed

The ODT format provides users with an open standard document format that is compatible with LibreOffice, OpenOffice, and other office suites. This enhances Zenodotos' export capabilities for better interoperability with open-source office applications.

## [0.2.5] - 2025-08-14

### Added
- **TXT (plain text) export format support**
  - Add TXT format to supported export formats in CLI command
  - Implement TXT export in DriveClient with text/plain MIME type
  - Add comprehensive tests for TXT export functionality
  - Update documentation to include TXT format examples
  - Mark TXT export as completed in ROADMAP.md

The TXT export format allows users to export Google Docs as plain text files, providing a simple text-only version without formatting.





## [0.2.2] - 2025-08-12

### Added
- **RTF (Rich Text Format) export support**
  - Add RTF format to supported export formats
  - Update Drive client to support RTF MIME type and file extension
  - Add RTF to CLI export command format choices
  - Update CLI help text to include RTF format
  - Add comprehensive test coverage for RTF export
  - Update documentation across all guides to include RTF

RTF (Rich Text Format) provides a portable format for Google Docs that preserves formatting while being more compatible than HTML. This format is particularly useful for documents that need to be opened in various word processors while maintaining formatting.

## [0.2.1] - 2025-08-12

### Added
- **Markdown format support for Google Docs export**
  - Add markdown format support to export command
  - Support --format md option for Google Docs export
  - Use text/markdown MIME type for Google Drive API
  - Generate .md file extensions for markdown exports
  - Update Drive client implementation with markdown support
  - Add "md" to supported formats validation
  - Add markdown MIME type mapping (text/markdown)
  - Add markdown file extension mapping (.md)
  - Enhance CLI command interface with markdown support
  - Add comprehensive test coverage for markdown export
  - Update documentation across all guides with markdown examples

This feature enables users to export Google Docs as markdown files, making it easier to work with documentation, GitHub repositories, and other markdown-based workflows.

### Changed
- **CI/CD improvements**
  - Add GitHub Actions workflow for automated releases
  - Add manual release workflow with workflow_dispatch trigger
  - Orchestrate all three decoupled scripts (publish → verify → test)
  - Support manual version input with validation
  - Include TestPyPI validation before PyPI release
  - Add automated Git tagging and GitHub release creation
  - Add comprehensive documentation for GitHub Actions workflow

## [0.2.0] - 2025-08-10

### Added
- **Query support for file retrieval**
  - Add --query option to get-file command for searching files by criteria
  - Make file_id argument optional when using --query option
  - Add search_and_get_file method to Zenodotos library class
  - Implement proper validation for mutually exclusive file_id and query options
  - Add comprehensive error handling for multiple matches and no matches
  - Update command help text and documentation to reflect new functionality
  - Add 8 new tests for query functionality (5 CLI + 3 library)
  - Update existing test to handle new optional file_id behavior
  - Improve test coverage from ~37% to 95.76% across affected modules
  - Update documentation in README, get-file-command.md, and library.md
  - Add query examples and usage patterns in documentation
  - Maintain backward compatibility with existing file_id usage

This enhancement allows users to get file details by searching for them instead of requiring the file ID, significantly improving usability for interactive workflows where users know file names but not IDs.

## [0.1.1] - 2025-08-08

### Fixed
- **Dependency management**
  - Add PyYAML>=6.0.0 as required dependency to fix configuration loading
  - Remove automatic installation test from release script due to index propagation delays
  - Add guidance for manual testing after release to handle PyPI index delays

This resolves the issue where users encountered "PyYAML is required for YAML configuration files" error when running zenodotos commands with configuration files.

### Changed
- **Project renaming**
  - Renamed the project from quill to zenodotos, which was free in both PyPI and TestPyPI

### Added
- **CI/CD infrastructure**
  - Add centralized version management system
  - Add .github/versions.env as single source of truth for tool versions
  - Create scripts/update-versions.sh for automated version updates across all files
  - Update CI workflows to load versions from .env file using source command
  - Add comprehensive documentation in docs/setup/version-management.md
  - Support both v1.2.3 and 1.2.3 version formats
  - Include fallback values to ensure CI stability
  - Add color-coded output for better user experience
  - Support updating versions in pyproject.toml, pre-commit config, and CI workflows
  - Add sync command to align pre-commit hook versions with .env file

- **Comprehensive GitHub Actions CI/CD pipeline**
  - Add main CI workflow with multi-Python testing (3.11, 3.12, 3.13)
  - Add quality checks workflow with code analysis and performance monitoring
  - Implement comprehensive quality gates (linting, formatting, type checking, coverage)
  - Add security scanning with Bandit (replacing Safety CLI)
  - Add documentation validation and CLI integration testing
  - Configure workflows to trigger on all branches, PRs, and releases
  - Add comprehensive CI documentation and badge configuration
  - Remove redundant Safety CLI dependency
  - Update Python version alignment across all workflows
  - Fix branch references to match actual repository structure

Quality Gates:
- Minimum 80% test coverage enforcement
- Ruff linting and formatting checks
- Type checking with ty
- Security scanning with Bandit
- TODO/FIXME and debug statement detection
- Package build validation
- Secret detection and security best practices



---

## Release Notes

### Version Naming Convention
This project follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backward compatible manner
- **PATCH**: Backward compatible bug fixes

### Breaking Changes
- No breaking changes have been introduced in the 0.x series
- All changes maintain backward compatibility

### Migration Guide
- No migration required for any version in the 0.x series
- All updates are backward compatible

### Support
- Python 3.11+ required
- Google Drive API credentials required
- See README.md for detailed setup instructions

### Contributors
- **Ignasi Fosch** (@ifosch) - Primary maintainer and developer

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
