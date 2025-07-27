"""Tests for the config module."""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from quill.config import Config


class TestConfig:
    """Test suite for Config class."""

    def test_config_initialization_default_paths(self):
        """Test that Config initializes with correct default paths."""
        config = Config()
        
        expected_config_dir = Path.home() / ".config" / "quill"
        expected_credentials_file = expected_config_dir / "credentials.json"
        expected_token_file = expected_config_dir / "token.json"
        
        assert config.config_dir == expected_config_dir
        assert config.credentials_file == expected_credentials_file
        assert config.token_file == expected_token_file

    def test_config_initialization_with_env_variable(self):
        """Test that Config respects GOOGLE_DRIVE_CREDENTIALS environment variable."""
        custom_creds_path = "/custom/path/to/credentials.json"
        
        with patch.dict(os.environ, {"GOOGLE_DRIVE_CREDENTIALS": custom_creds_path}):
            config = Config()
            
            assert str(config.credentials_file) == custom_creds_path
            # Token file should still use default location
            expected_token_file = Path.home() / ".config" / "quill" / "token.json"
            assert config.token_file == expected_token_file

    def test_ensure_config_dir_creates_directory(self):
        """Test that ensure_config_dir creates the config directory."""
        config = Config()
        
        # Mock Path.mkdir at the class level
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            config.ensure_config_dir()
            
            # Should call mkdir with parents=True and exist_ok=True
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_get_credentials_path_returns_string(self):
        """Test that get_credentials_path returns the credentials file path as string."""
        config = Config()
        
        result = config.get_credentials_path()
        
        assert isinstance(result, str)
        assert result == str(config.credentials_file)

    def test_get_credentials_path_with_env_variable(self):
        """Test that get_credentials_path works with environment variable."""
        custom_creds_path = "/custom/path/to/credentials.json"
        
        with patch.dict(os.environ, {"GOOGLE_DRIVE_CREDENTIALS": custom_creds_path}):
            config = Config()
            result = config.get_credentials_path()
            
            assert result == custom_creds_path

    def test_get_token_path_returns_string(self):
        """Test that get_token_path returns the token file path as string."""
        config = Config()
        
        result = config.get_token_path()
        
        assert isinstance(result, str)
        assert result == str(config.token_file)

    def test_config_paths_are_absolute(self):
        """Test that all config paths are absolute paths."""
        config = Config()
        
        assert config.config_dir.is_absolute()
        assert config.credentials_file.is_absolute()
        assert config.token_file.is_absolute()

    def test_config_consistency(self):
        """Test that config paths are consistent with each other."""
        config = Config()
        
        # Token file should be inside config directory
        assert config.token_file.parent == config.config_dir
        
        # Credentials file should be inside config directory (when using default)
        if "GOOGLE_DRIVE_CREDENTIALS" not in os.environ:
            assert config.credentials_file.parent == config.config_dir

    @patch.dict(os.environ, {}, clear=True)
    def test_config_without_env_variables(self):
        """Test config behavior when no environment variables are set."""
        config = Config()
        
        expected_config_dir = Path.home() / ".config" / "quill"
        assert config.config_dir == expected_config_dir
        assert config.credentials_file == expected_config_dir / "credentials.json"
        assert config.token_file == expected_config_dir / "token.json" 