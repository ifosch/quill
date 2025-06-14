"""Data models for Google Drive entities."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DriveFile:
    """Represents a Google Drive file."""

    id: str
    name: str
    mime_type: str
    size: Optional[int] = None
    created_time: Optional[str] = None
    modified_time: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> 'DriveFile':
        """Create a DriveFile instance from API response data."""
        return cls(
            id=data['id'],
            name=data['name'],
            mime_type=data['mimeType'],
            size=data.get('size'),
            created_time=data.get('createdTime'),
            modified_time=data.get('modifiedTime')
        ) 