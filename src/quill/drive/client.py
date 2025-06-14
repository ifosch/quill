"""Google Drive API client implementation."""

from googleapiclient.discovery import build

from ..auth import Auth


class DriveClient:
    """Google Drive API client."""

    def __init__(self):
        self.auth = Auth()
        self.service = None

    def get_service(self):
        """Get or create the Drive API service."""
        if not self.service:
            credentials = self.auth.get_credentials()
            self.service = build('drive', 'v3', credentials=credentials)
        return self.service

    def list_files(self, page_size=10):
        """List files in Google Drive."""
        service = self.get_service()
        results = service.files().list(
            pageSize=page_size,
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        return results.get('files', []) 