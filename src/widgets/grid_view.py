from PyQt6.QtWidgets import QWidget, QGridLayout
from src.widgets.video_widget import VideoWidget


class GridView(QWidget):
    def __init__(self, rows: int = 2, cols: int = 2, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.widgets: list[VideoWidget] = []

        self._setup_ui()

    def _setup_ui(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(4, 4, 4, 4)

        self._create_grid()

    def _create_grid(self):
        for widget in self.widgets:
            widget.stop()
            widget.deleteLater()
        self.widgets.clear()

        for i in range(self.layout.count()):
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for row in range(self.rows):
            for col in range(self.cols):
                video_widget = VideoWidget()
                self.layout.addWidget(video_widget, row, col)
                self.widgets.append(video_widget)

    def set_grid(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self._create_grid()

    def play_in_slot(self, index: int, source: str):
        if 0 <= index < len(self.widgets):
            self.widgets[index].play(source)

    def play_in_next_slot(self, source: str):
        for widget in self.widgets:
            if not widget.is_playing():
                widget.play(source)
                return
        if self.widgets:
            self.widgets[0].play(source)

    def stop_slot(self, index: int):
        if 0 <= index < len(self.widgets):
            self.widgets[index].stop()

    def stop_all(self):
        for widget in self.widgets:
            widget.stop()
