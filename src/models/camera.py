from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Camera:
    name: str
    url: str
    type: str = "rtsp"
    enabled: bool = True
    position: int = 0
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict) -> "Camera":
        return cls(
            id=row.get("id"),
            name=row.get("name"),
            url=row.get("url"),
            type=row.get("type", "rtsp"),
            enabled=bool(row.get("enabled", 1)),
            position=row.get("position", 0),
            created_at=row.get("created_at"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "type": self.type,
            "enabled": self.enabled,
            "position": self.position,
            "created_at": self.created_at,
        }
