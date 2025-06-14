"""Configuration management for Quill."""

import os
from pathlib import Path


class Config:
    """Configuration management for Quill."""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "quill"
        self.credentials_file = self.config_dir / "credentials.json"
        self.token_file = self.config_dir / "token.json"

    def ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_credentials_path(self):
        """Get the path to the credentials file."""
        return str(self.credentials_file)

    def get_token_path(self):
        """Get the path to the token file."""
        return str(self.token_file) 