import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt

import vlc


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self.video_frame = QFrame()
        self.video_frame.setStyleSheet(
            "QFrame { background-color: #1a1a1a; border: 1px solid #333; }"
        )
        self.video_frame.setMinimumSize(320, 240)

        self.label = QLabel("No Stream")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { color: #666; font-size: 14px; }")

        frame_layout = QVBoxLayout(self.video_frame)
        frame_layout.addWidget(self.label)

        layout.addWidget(self.video_frame)

    def play(self, source: str):
        self.label.hide()
        self.media = self.instance.media_new(source)
        self.player.set_media(self.media)

        if sys.platform == "darwin":
            self.player.set_nsobject(int(self.video_frame.winId()))
        elif sys.platform == "win32":
            self.player.set_hwnd(int(self.video_frame.winId()))
        else:
            self.player.set_xwindow(int(self.video_frame.winId()))

        self.player.play()

    def stop(self):
        self.player.stop()
        self.label.show()
        self.label.setText("No Stream")

    def pause(self):
        self.player.pause()

    def is_playing(self) -> bool:
        return self.player.is_playing()

    def get_media_info(self) -> dict:
        if not self.media:
            return {}

        self.media.parse()
        return {
            "duration": self.player.get_length(),
            "fps": self.player.get_fps(),
            "width": self.player.video_get_width(),
            "height": self.player.video_get_height(),
        }
