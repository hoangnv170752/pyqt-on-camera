from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QImage, QPixmap

from pathlib import Path

from src.services.logger import get_logger

logger = get_logger("video_widget")

try:
    from pyvidplayer2 import Video
except ImportError as e:
    Video = None
    _IMPORT_ERROR = str(e)

try:
    import cv2
except ImportError:
    cv2 = None


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video = None
        self._playing = False
        self._audio_only = False
        self._audio_source: str | None = None
        self._pygame_error: str | None = None
        self._audio_sound = None
        self._pygame_surface = None
        self._is_muted = False
        self._is_stream = False
        self._cv_capture = None

        self._setup_ui()
        self._setup_timer()

        if Video is None:
            self.label.setText(f"pyvidplayer2 not available.\n{_IMPORT_ERROR}")
            logger.error(f"pyvidplayer2 import failed: {_IMPORT_ERROR}")

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
        self.label.setScaledContents(True)

        frame_layout = QVBoxLayout(self.video_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.label)

        controls_container = QWidget(self.video_frame)
        controls_container.setStyleSheet("background: transparent;")
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(5, 5, 5, 5)
        controls_layout.setSpacing(5)
        
        controls_layout.addStretch()
        
        self.mute_btn = QPushButton("🔊")
        self.mute_btn.setFixedSize(32, 32)
        self.mute_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 200);
            }
        """)
        self.mute_btn.clicked.connect(self._toggle_mute)
        self.mute_btn.hide()
        controls_layout.addWidget(self.mute_btn)
        
        self.pause_btn = QPushButton("⏸")
        self.pause_btn.setFixedSize(32, 32)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 200);
            }
        """)
        self.pause_btn.clicked.connect(self._toggle_pause)
        self.pause_btn.hide()
        controls_layout.addWidget(self.pause_btn)
        
        self.controls_container = controls_container
        self.controls_container.setGeometry(0, 0, self.video_frame.width(), 42)
        self.controls_container.raise_()
        
        self.progress_bar = QProgressBar(self.video_frame)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(1000)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(0, 0, 0, 100);
                height: 4px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        self.progress_bar.hide()
        self.progress_bar.setGeometry(0, self.video_frame.height() - 4, self.video_frame.width(), 4)
        self.progress_bar.raise_()

        layout.addWidget(self.video_frame)
        
        self.video_frame.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if obj == self.video_frame and event.type() == QEvent.Type.Resize:
            self.controls_container.setGeometry(0, 0, self.video_frame.width(), 42)
            self.progress_bar.setGeometry(0, self.video_frame.height() - 4, self.video_frame.width(), 4)
        return super().eventFilter(obj, event)

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)

    def _update_frame(self):
        if not self._playing:
            return

        if self._is_stream and self._cv_capture is not None:
            try:
                ret, frame = self._cv_capture.read()
                if ret:
                    self._display_cv_frame(frame)
                else:
                    logger.warning("Failed to read frame from stream")
                    self._playing = False
            except Exception as e:
                logger.error(f"Error reading stream frame: {e}")
                self._playing = False
            return

        if self.video is None:
            return

        if self.video.active:
            try:
                import pygame
                if self._pygame_surface is None:
                    size = self.video.current_size
                    self._pygame_surface = pygame.Surface(size)
                
                if self.video.draw(self._pygame_surface, (0, 0), force_draw=False):
                    self._display_frame(self._pygame_surface)
                
                if self.video.duration > 0:
                    progress = int((self.video.get_pos() / self.video.duration) * 1000)
                    self.progress_bar.setValue(progress)
            except Exception as e:
                logger.error(f"Error updating frame: {e}")
        else:
            if self.video.active is False:
                self.video.restart()

    def _display_frame(self, surface):
        try:
            import pygame
            width = surface.get_width()
            height = surface.get_height()

            data = pygame.image.tostring(surface, "RGB")
            image = QImage(data, width, height, width * 3, QImage.Format.Format_RGB888)

            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(scaled_pixmap)
        except Exception as e:
            logger.error(f"Error displaying frame: {e}")
    
    def _display_cv_frame(self, frame):
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            
            image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(scaled_pixmap)
        except Exception as e:
            logger.error(f"Error displaying CV frame: {e}")

    def play(self, source: str):
        if Video is None:
            self.label.setText(f"pyvidplayer2 not available.\n{_IMPORT_ERROR}")
            return

        try:
            self.stop()

            logger.info(f"Playing: {source}")

            self._is_stream = source.startswith(("rtsp://", "http://", "https://", "rtp://"))
            
            if not self._is_stream:
                suffix = Path(source).suffix.lower()
                if suffix in {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg"}:
                    self._play_audio(source)
                    return

            if self._is_stream:
                if cv2 is None:
                    self.label.setText("OpenCV not available for RTSP streams")
                    logger.error("OpenCV not installed")
                    return
                
                self._cv_capture = cv2.VideoCapture(source)
                if not self._cv_capture.isOpened():
                    self.label.setText(f"Failed to open stream: {source}")
                    logger.error(f"Failed to open stream: {source}")
                    self._cv_capture = None
                    return
                
                self._playing = True
                self._is_muted = False
                self.timer.start(33)
                
                self.label.setText("")
                self.mute_btn.hide()
                self.pause_btn.show()
                self.pause_btn.setText("⏸")
                self.progress_bar.hide()
            else:
                self.video = Video(source)
                self._playing = True
                self._is_muted = False

                fps = self.video.frame_rate
                interval = int(1000 / fps) if fps > 0 else 33
                self.timer.start(interval)

                self.label.setText("")
                self.mute_btn.show()
                self.pause_btn.show()
                self.pause_btn.setText("⏸")
                self.progress_bar.show()
                self.mute_btn.setText("🔊")

        except Exception as e:
            logger.error(f"Error playing video: {e}")
            self.label.setText(f"Error: {str(e)}")
            self._playing = False

    def _play_audio(self, source: str):
        self._audio_only = True
        self._audio_source = source
        self.timer.stop()

        try:
            try:
                import pygame
            except ImportError as e:
                self._pygame_error = str(e)
                logger.error(f"pygame not installed: {e}")
                self._playing = False
                self.label.setPixmap(QPixmap())
                self.label.show()
                self.label.setText("Audio playback requires pygame. Please install: pip install pygame")
                return

            if not pygame.mixer.get_init():
                pygame.mixer.init()

            self._audio_sound = pygame.mixer.Sound(source)
            self._audio_sound.play()
            self._playing = True

            name = Path(source).name
            self.label.setPixmap(QPixmap())
            self.label.show()
            self.label.setText(f"Playing audio: {name}")
        except Exception as e:
            self._pygame_error = str(e)
            logger.error(f"Error playing audio: {e}")
            self._playing = False
            self.label.setPixmap(QPixmap())
            self.label.show()
            self.label.setText(f"Error: {str(e)}")

    def stop(self):
        self._playing = False
        self._audio_only = False
        self._audio_source = None
        self._is_stream = False
        self.timer.stop()

        if self._cv_capture is not None:
            try:
                self._cv_capture.release()
            except Exception:
                pass
            self._cv_capture = None

        if self.video is not None:
            try:
                self.video.close()
            except Exception:
                pass
            self.video = None
        
        self._pygame_surface = None

        try:
            import pygame

            if self._audio_sound is not None:
                self._audio_sound.stop()
                self._audio_sound = None
        except Exception:
            pass

        self.label.setPixmap(QPixmap())
        self.label.setText("No Stream")
        self.mute_btn.hide()
        self.pause_btn.hide()
        self.progress_bar.hide()
        self.progress_bar.setValue(0)

    def _toggle_pause(self):
        if self._is_stream:
            if self._playing:
                self._playing = False
                self.timer.stop()
                self.pause_btn.setText("▶")
            else:
                self._playing = True
                self.timer.start(33)
                self.pause_btn.setText("⏸")
            return
        
        if self._audio_only:
            try:
                import pygame

                if self._audio_sound is not None:
                    if self._playing:
                        self._audio_sound.set_volume(0.0)
                        self._playing = False
                        self.pause_btn.setText("▶")
                    else:
                        self._audio_sound.set_volume(1.0)
                        self._playing = True
                        self.pause_btn.setText("⏸")
            except Exception:
                pass
            return

        if self.video is not None:
            try:
                self.video.toggle_pause()
                if self.video.paused:
                    self.pause_btn.setText("▶")
                else:
                    self.pause_btn.setText("⏸")
            except Exception as e:
                logger.error(f"Error toggling pause: {e}")
    
    def pause(self):
        if self._audio_only:
            try:
                import pygame

                if self._audio_sound is not None:
                    self._audio_sound.set_volume(0.0)
            except Exception:
                pass
            return

        if self.video is not None:
            self.video.toggle_pause()

    def resume(self):
        if self._audio_only:
            try:
                import pygame

                if self._audio_sound is not None:
                    self._audio_sound.set_volume(1.0)
            except Exception:
                pass
            return

        if self.video is not None:
            self.video.resume()

    def is_playing(self) -> bool:
        if self._audio_only:
            try:
                import pygame

                if self._audio_sound is not None:
                    return self._playing and pygame.mixer.get_busy()
                return False
            except Exception:
                return False

        return self._playing and self.video is not None and self.video.active

    def _toggle_mute(self):
        if self.video is None:
            return
        
        try:
            self._is_muted = not self._is_muted
            if self._is_muted:
                self.video.set_volume(0.0)
                self.mute_btn.setText("🔇")
            else:
                self.video.set_volume(1.0)
                self.mute_btn.setText("🔊")
        except Exception as e:
            logger.error(f"Error toggling mute: {e}")

    def get_media_info(self) -> dict:
        if self.video is None:
            return {}

        return {
            "duration": self.video.duration,
            "fps": self.video.frame_rate,
            "width": self.video.current_size[0] if self.video.current_size else 0,
            "height": self.video.current_size[1] if self.video.current_size else 0,
        }

    def set_volume(self, volume: int):
        """Set volume (0-100)."""
        if self.video is not None:
            self.video.set_volume(volume / 100.0)

    def seek(self, position: float):
        """Seek to position in seconds."""
        if self.video is not None:
            self.video.seek(position)

    def get_position(self) -> float:
        """Get current position in seconds."""
        if self.video is not None:
            return self.video.get_pos()
        return 0.0
