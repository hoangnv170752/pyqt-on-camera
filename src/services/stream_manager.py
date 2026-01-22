from typing import Optional
from src.models.camera import Camera


class StreamManager:
    def __init__(self):
        self.active_streams: dict[int, dict] = {}

    def add_stream(self, camera: Camera) -> bool:
        if camera.id in self.active_streams:
            return False

        self.active_streams[camera.id] = {
            "camera": camera,
            "status": "connecting",
        }
        return True

    def remove_stream(self, camera_id: int) -> bool:
        if camera_id in self.active_streams:
            del self.active_streams[camera_id]
            return True
        return False

    def get_stream_status(self, camera_id: int) -> Optional[str]:
        if camera_id in self.active_streams:
            return self.active_streams[camera_id]["status"]
        return None

    def set_stream_status(self, camera_id: int, status: str):
        if camera_id in self.active_streams:
            self.active_streams[camera_id]["status"] = status

    def get_active_count(self) -> int:
        return len(self.active_streams)

    def get_all_active(self) -> list[Camera]:
        return [s["camera"] for s in self.active_streams.values()]
