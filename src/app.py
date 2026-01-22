from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMenuBar,
    QStatusBar,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from src.widgets.video_widget import VideoWidget
from src.widgets.grid_view import GridView
from src.services.database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC CamTouch - Multi-Camera Viewer")
        self.setMinimumSize(1024, 768)

        self.db = Database()

        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.grid_view = GridView()
        layout.addWidget(self.grid_view)

    def _setup_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open File...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        grid_2x2 = QAction("Grid 2x2", self)
        grid_2x2.triggered.connect(lambda: self.grid_view.set_grid(2, 2))
        view_menu.addAction(grid_2x2)

        grid_3x3 = QAction("Grid 3x3", self)
        grid_3x3.triggered.connect(lambda: self.grid_view.set_grid(3, 3))
        view_menu.addAction(grid_3x3)

        grid_4x4 = QAction("Grid 4x4", self)
        grid_4x4.triggered.connect(lambda: self.grid_view.set_grid(4, 4))
        view_menu.addAction(grid_4x4)

        # Camera menu
        camera_menu = menubar.addMenu("&Camera")

        add_camera = QAction("&Add Camera...", self)
        add_camera.setShortcut("Ctrl+N")
        add_camera.triggered.connect(self._add_camera)
        camera_menu.addAction(add_camera)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")

    def _open_file(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)",
        )
        if file_path:
            self.grid_view.play_in_next_slot(file_path)
            self.statusbar.showMessage(f"Opened: {file_path}")

    def _add_camera(self):
        from PyQt6.QtWidgets import QInputDialog

        url, ok = QInputDialog.getText(
            self, "Add Camera", "Enter stream URL (RTSP/HTTP):"
        )
        if ok and url:
            self.grid_view.play_in_next_slot(url)
            self.statusbar.showMessage(f"Added stream: {url}")

    def _show_about(self):
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.about(
            self,
            "About PC CamTouch",
            "PC CamTouch - Multi-Camera Viewer\n\n"
            "A PyQt6 application for streaming video,\n"
            "multi-camera viewing, and video analysis.",
        )

    def closeEvent(self, event):
        self.grid_view.stop_all()
        event.accept()
