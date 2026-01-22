import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt

try:
    import vlc
except Exception as e:
    vlc = None
    _VLC_IMPORT_ERROR = e


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.media = None
        self.instance = None
        self.player = None

        self._setup_ui()

        if vlc is None:
            self.label.setText(
                "VLC not available. Install VLC (libvlc) to enable playback."
            )
            return

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

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
        if vlc is None or self.instance is None or self.player is None:
            self.label.show()
            self.label.setText(
                f"VLC not available: {_VLC_IMPORT_ERROR}"
            )
            return

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
        if self.player is None:
            return
        self.player.stop()
        self.label.show()
        self.label.setText("No Stream")

    def pause(self):
        if self.player is None:
            return
        self.player.pause()

    def is_playing(self) -> bool:
        if self.player is None:
            return False
        return self.player.is_playing()

    def get_media_info(self) -> dict:
        if not self.media:
            return {}

        if self.player is None:
            return {}

        self.media.parse()
        return {
            "duration": self.player.get_length(),
            "fps": self.player.get_fps(),
            "width": self.player.video_get_width(),
            "height": self.player.video_get_height(),
        }
