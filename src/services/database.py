import sqlite3
from pathlib import Path
from typing import Optional
from src.models.camera import Camera


class Database:
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cameras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                type TEXT DEFAULT 'rtsp',
                enabled INTEGER DEFAULT 1,
                position INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        self.conn.commit()

    def add_camera(self, camera: Camera) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO cameras (name, url, type, enabled, position)
            VALUES (?, ?, ?, ?, ?)
        """,
            (camera.name, camera.url, camera.type, camera.enabled, camera.position),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_camera(self, camera_id: int) -> Optional[Camera]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cameras WHERE id = ?", (camera_id,))
        row = cursor.fetchone()
        if row:
            return Camera.from_row(dict(row))
        return None

    def get_all_cameras(self) -> list[Camera]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cameras ORDER BY position")
        return [Camera.from_row(dict(row)) for row in cursor.fetchall()]

    def update_camera(self, camera: Camera) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE cameras
            SET name = ?, url = ?, type = ?, enabled = ?, position = ?
            WHERE id = ?
        """,
            (
                camera.name,
                camera.url,
                camera.type,
                camera.enabled,
                camera.position,
                camera.id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_camera(self, camera_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM cameras WHERE id = ?", (camera_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default

    def set_setting(self, key: str, value: str):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        """,
            (key, value),
        )
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
