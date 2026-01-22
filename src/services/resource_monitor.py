import psutil
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from src.services.logger import get_logger

logger = get_logger("resource_monitor")


class ResourceMonitor(QObject):
    updated = pyqtSignal(dict)

    def __init__(self, interval_ms: int = 2000, parent=None):
        super().__init__(parent)
        self.interval_ms = interval_ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        logger.info(f"ResourceMonitor initialized with {interval_ms}ms interval")

    def start(self):
        logger.debug("Starting resource monitoring")
        self._update_stats()
        self.timer.start(self.interval_ms)

    def stop(self):
        logger.debug("Stopping resource monitoring")
        self.timer.stop()

    def _update_stats(self):
        stats = self.get_stats()
        self.updated.emit(stats)

    def get_stats(self) -> dict:
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()

        stats = {
            "cpu_percent": cpu_percent,
            "ram_percent": memory.percent,
            "ram_used_gb": memory.used / (1024**3),
            "ram_total_gb": memory.total / (1024**3),
        }
        return stats

    def get_status_level(self) -> str:
        """Returns 'normal', 'warning', or 'critical' based on resource usage."""
        stats = self.get_stats()
        cpu = stats["cpu_percent"]
        ram = stats["ram_percent"]

        if cpu > 90 or ram > 90:
            return "critical"
        elif cpu > 70 or ram > 70:
            return "warning"
        return "normal"
