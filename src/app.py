from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QLabel,
    QMenu,
    QMessageBox,
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt

import json
from pathlib import Path

from src.widgets.home_screen import HomeScreen
from src.widgets.grid_view import GridView
from src.widgets.camera_dialog import AddCameraDialog, CameraManagerDialog
from src.services.database import Database
from src.services.resource_monitor import ResourceMonitor
from src.services.logger import get_logger

logger = get_logger("app")

SETTINGS_PATH = Path("config/settings.json")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC CamTouch")
        self.setMinimumSize(1024, 768)

        logger.info("Initializing MainWindow")

        self.db = Database()
        self.grid_view = None
        self.resource_monitor = ResourceMonitor(interval_ms=2000)

        self._setup_ui()
        self._setup_toolbar()
        self._setup_menu()
        self._setup_statusbar()
        self._setup_resource_monitor()

        logger.info("MainWindow initialized successfully")

    def _setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_screen = HomeScreen()
        self.home_screen.start_clicked.connect(self._on_start)
        self.home_screen.how_to_use_clicked.connect(self._on_how_to_use)
        self.home_screen.data_export_clicked.connect(self._on_data_export)
        self.stacked_widget.addWidget(self.home_screen)

        self.viewer_widget = QWidget()
        viewer_layout = QVBoxLayout(self.viewer_widget)
        viewer_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_view = GridView()
        viewer_layout.addWidget(self.grid_view)
        self.stacked_widget.addWidget(self.viewer_widget)

        self.stacked_widget.setCurrentWidget(self.home_screen)

    def _setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.home_action = QAction("Home", self)
        self.home_action.setShortcut(QKeySequence("Ctrl+H"))
        self.home_action.setToolTip("Go to Home screen (Ctrl+H)")
        self.home_action.triggered.connect(self._go_home)
        toolbar.addAction(self.home_action)

        self.export_action = QAction("Export", self)
        self.export_action.setShortcut(QKeySequence("Ctrl+E"))
        self.export_action.setToolTip("Export data (Ctrl+E)")
        self.export_action.triggered.connect(self._on_data_export)
        toolbar.addAction(self.export_action)

        self.camera_action = QAction("Camera", self)
        self.camera_action.setShortcut(QKeySequence("Ctrl+N"))
        self.camera_action.setToolTip("Add camera (Ctrl+N)")
        self.camera_action.triggered.connect(self._add_camera)
        toolbar.addAction(self.camera_action)

        # View button with dropdown menu
        self.view_action = QAction("View", self)
        self.view_action.setToolTip("Change grid layout")
        view_menu = QMenu(self)
        view_menu.addAction("1x1", lambda: self._set_grid(1, 1))
        view_menu.addAction("2x2", lambda: self._set_grid(2, 2))
        view_menu.addAction("3x3", lambda: self._set_grid(3, 3))
        view_menu.addAction("4x4", lambda: self._set_grid(4, 4))
        self.view_action.setMenu(view_menu)
        toolbar.addAction(self.view_action)

        toolbar.addSeparator()

    def _setup_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        file_menu.addAction(self.home_action)

        open_action = QAction("&Open File...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        file_menu.addAction(self.export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        grid_1x1 = QAction("Grid 1x1", self)
        grid_1x1.triggered.connect(lambda: self._set_grid(1, 1))
        view_menu.addAction(grid_1x1)

        grid_2x2 = QAction("Grid 2x2", self)
        grid_2x2.triggered.connect(lambda: self._set_grid(2, 2))
        view_menu.addAction(grid_2x2)

        grid_3x3 = QAction("Grid 3x3", self)
        grid_3x3.triggered.connect(lambda: self._set_grid(3, 3))
        view_menu.addAction(grid_3x3)

        grid_4x4 = QAction("Grid 4x4", self)
        grid_4x4.triggered.connect(lambda: self._set_grid(4, 4))
        view_menu.addAction(grid_4x4)

        # Camera menu
        camera_menu = menubar.addMenu("&Camera")

        add_camera = QAction("&Add Camera...", self)
        add_camera.setShortcut("Ctrl+N")
        add_camera.triggered.connect(self._add_camera)
        camera_menu.addAction(add_camera)

        manage_cameras = QAction("&Manage Cameras...", self)
        manage_cameras.setShortcut("Ctrl+M")
        manage_cameras.triggered.connect(self._manage_cameras)
        camera_menu.addAction(manage_cameras)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.ram_label = QLabel("RAM: ---%")
        self.cpu_label = QLabel("CPU: ---%")

        self.statusbar.addPermanentWidget(self.ram_label)
        self.statusbar.addPermanentWidget(self.cpu_label)

        self.statusbar.showMessage("Ready")

    def _setup_resource_monitor(self):
        self.resource_monitor.updated.connect(self._on_resource_update)
        self.resource_monitor.start()

    def _on_resource_update(self, stats: dict):
        ram_percent = stats.get("ram_percent", 0)
        cpu_percent = stats.get("cpu_percent", 0)

        self.ram_label.setText(f"RAM: {ram_percent:.1f}%")
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")

    def _go_home(self):
        logger.debug("Navigating to home screen")
        self.stacked_widget.setCurrentWidget(self.home_screen)
        self.statusbar.showMessage("Home")

    def _on_start(self):
        logger.info("Start button clicked - switching to viewer")
        self.stacked_widget.setCurrentWidget(self.viewer_widget)
        self.statusbar.showMessage("Viewer ready")

    def _on_how_to_use(self):
        logger.info("How to use button clicked")
        from PyQt6.QtWidgets import QMessageBox

        author_name = "Unknown"
        author_email = ""
        if SETTINGS_PATH.exists():
            with open(SETTINGS_PATH) as f:
                settings = json.load(f)
                author_info = settings.get("author", {})
                author_name = author_info.get("name", "Unknown")
                author_email = author_info.get("email", "")

        QMessageBox.information(
            self,
            "How to Use",
            "PC CamTouch - Multi-Camera Viewer\n\n"
            "1. Click 'Start' to enter the viewer\n"
            "2. Use Camera > Add Camera to add RTSP/HTTP streams\n"
            "3. Use File > Open File to play local videos\n"
            "4. Use View menu to change grid layout (2x2, 3x3, 4x4)\n\n"
            f"Author: {author_name}\n"
            f"Email: {author_email}",
        )

    def _on_data_export(self):
        logger.info("Data export button clicked")
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(
            self,
            "Data Export",
            "Data export feature coming soon.\n\n"
            "This will allow exporting camera configurations and recordings.",
        )

    def _set_grid(self, rows: int, cols: int):
        logger.debug(f"Setting grid to {rows}x{cols}")
        if self.grid_view:
            lost_count = self.grid_view.will_lose_sources(rows, cols)
            if lost_count > 0:
                reply = QMessageBox.question(
                    self,
                    "Xác nhận thay đổi",
                    f"Thay đổi sang {rows}x{cols} sẽ mất {lost_count} video đang phát.\n"
                    "Bạn có muốn tiếp tục không?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

            self.grid_view.set_grid(rows, cols)
            self.statusbar.showMessage(f"Grid: {rows}x{cols}")
        self.stacked_widget.setCurrentWidget(self.viewer_widget)

    def _open_file(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)",
        )
        if file_path:
            logger.info(f"Opening file: {file_path}")
            self.stacked_widget.setCurrentWidget(self.viewer_widget)
            self.grid_view.play_in_next_slot(file_path)
            self.statusbar.showMessage(f"Opened: {file_path}")

    def _add_camera(self):
        dialog = AddCameraDialog(self)
        if dialog.exec():
            camera = dialog.get_camera()
            self.db.add_camera(camera)
            logger.info(f"Adding camera: {camera.name}")
            self.stacked_widget.setCurrentWidget(self.viewer_widget)
            self.grid_view.play_in_next_slot(camera.url)
            self.statusbar.showMessage(f"Added: {camera.name}")

    def _manage_cameras(self):
        dialog = CameraManagerDialog(self.db, self)
        dialog.exec()

    def _show_about(self):
        from PyQt6.QtWidgets import QMessageBox

        logger.debug("Showing about dialog")
        QMessageBox.about(
            self,
            "About PC CamTouch",
            "PC CamTouch - Multi-Camera Viewer\n\n"
            "A PyQt6 application for streaming video,\n"
            "multi-camera viewing, and video analysis.",
        )

    def closeEvent(self, event):
        logger.info("Application closing")
        self.resource_monitor.stop()
        if self.grid_view:
            self.grid_view.stop_all()
        event.accept()
