"""Authentication handling for Google Drive API."""

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .config import Config


class Auth:
    """Handle Google Drive API authentication."""

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    def __init__(self):
        self.config = Config()
        self.credentials = None

    def get_credentials(self):
        """Get valid credentials for Google Drive API."""
        if self.credentials and self.credentials.valid:
            return self.credentials

        if (
            self.credentials
            and self.credentials.expired
            and self.credentials.refresh_token
        ):
            self.credentials.refresh(Request())
            return self.credentials

        self.config.ensure_config_dir()
        flow = InstalledAppFlow.from_client_secrets_file(
            self.config.get_credentials_path(), self.SCOPES
        )
        self.credentials = flow.run_local_server(port=0)
        return self.credentials
