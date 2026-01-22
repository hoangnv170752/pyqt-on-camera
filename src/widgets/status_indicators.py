from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen


class StatusIndicator(QWidget):
    """A single circular status indicator."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self._color = QColor("#888888")
        self._status = "inactive"

    def set_status(self, status: str):
        """Set status: 'normal' (green), 'warning' (yellow), 'critical' (red), 'inactive' (gray)."""
        self._status = status
        colors = {
            "normal": "#4CAF50",
            "warning": "#FFC107",
            "critical": "#F44336",
            "inactive": "#888888",
        }
        self._color = QColor(colors.get(status, "#888888"))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#333333"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(self._color)

        painter.drawEllipse(2, 2, 12, 12)


class StatusIndicators(QWidget):
    """Three status indicator circles (CPU, RAM, Network)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(4)

        self.cpu_indicator = StatusIndicator()
        self.cpu_indicator.setToolTip("CPU Status")
        layout.addWidget(self.cpu_indicator)

        self.ram_indicator = StatusIndicator()
        self.ram_indicator.setToolTip("RAM Status")
        layout.addWidget(self.ram_indicator)

        self.network_indicator = StatusIndicator()
        self.network_indicator.setToolTip("Network Status")
        layout.addWidget(self.network_indicator)

    def update_from_stats(self, stats: dict):
        cpu = stats.get("cpu_percent", 0)
        ram = stats.get("ram_percent", 0)

        self.cpu_indicator.set_status(self._get_level(cpu))
        self.ram_indicator.set_status(self._get_level(ram))
        self.network_indicator.set_status("normal")

    def _get_level(self, percent: float) -> str:
        if percent > 90:
            return "critical"
        elif percent > 70:
            return "warning"
        return "normal"
