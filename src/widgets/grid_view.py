from PyQt6.QtWidgets import QWidget, QGridLayout
from src.widgets.video_widget import VideoWidget
from src.services.logger import get_logger

logger = get_logger("grid_view")


class GridView(QWidget):
    def __init__(self, rows: int = 1, cols: int = 1, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.widgets: list[VideoWidget] = []
        self._sources: list[str] = []

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

    def get_active_sources(self) -> list[str]:
        """Get list of currently playing sources."""
        sources = []
        for i, widget in enumerate(self.widgets):
            if i < len(self._sources) and self._sources[i]:
                sources.append(self._sources[i])
            elif widget.is_playing():
                sources.append("")
        return [s for s in self._sources if s]

    def get_sources_count(self) -> int:
        """Get number of active sources."""
        return len([s for s in self._sources if s])

    def set_grid(self, rows: int, cols: int, preserve_sources: bool = True):
        """Change grid layout, optionally preserving sources."""
        old_sources = self._sources.copy() if preserve_sources else []

        self.rows = rows
        self.cols = cols
        self._create_grid()

        if preserve_sources and old_sources:
            self._sources = []
            new_capacity = rows * cols
            for i, source in enumerate(old_sources):
                if i < new_capacity and source:
                    self.widgets[i].play(source)
                    self._sources.append(source)
                elif i >= new_capacity:
                    break
            while len(self._sources) < new_capacity:
                self._sources.append("")

            logger.debug(f"Grid changed to {rows}x{cols}, restored {len([s for s in self._sources if s])} sources")
        else:
            self._sources = [""] * (rows * cols)

    def will_lose_sources(self, new_rows: int, new_cols: int) -> int:
        """Check how many sources will be lost when reducing grid size."""
        new_capacity = new_rows * new_cols
        current_sources = [s for s in self._sources if s]

        if len(current_sources) <= new_capacity:
            return 0

        lost_count = 0
        for i, source in enumerate(self._sources):
            if source and i >= new_capacity:
                lost_count += 1

        return lost_count

    def play_in_slot(self, index: int, source: str):
        if 0 <= index < len(self.widgets):
            self.widgets[index].play(source)
            while len(self._sources) <= index:
                self._sources.append("")
            self._sources[index] = source

    def play_in_next_slot(self, source: str):
        for i, widget in enumerate(self.widgets):
            if not widget.is_playing():
                widget.play(source)
                while len(self._sources) <= i:
                    self._sources.append("")
                self._sources[i] = source
                return
        if self.widgets:
            self.widgets[0].play(source)
            if self._sources:
                self._sources[0] = source

    def stop_slot(self, index: int):
        if 0 <= index < len(self.widgets):
            self.widgets[index].stop()
            if index < len(self._sources):
                self._sources[index] = ""

    def stop_all(self):
        for widget in self.widgets:
            widget.stop()
        self._sources = [""] * len(self.widgets)
