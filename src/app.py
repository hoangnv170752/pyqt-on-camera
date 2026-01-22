from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QStatusBar,
    QToolBar,
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt

from src.widgets.home_screen import HomeScreen
from src.widgets.grid_view import GridView
from src.services.database import Database
from src.services.logger import get_logger

logger = get_logger("app")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC CamTouch")
        self.setMinimumSize(1024, 768)

        logger.info("Initializing MainWindow")

        self.db = Database()
        self.grid_view = None

        self._setup_ui()
        self._setup_toolbar()
        self._setup_menu()
        self._setup_statusbar()

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

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

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

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")

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

        QMessageBox.information(
            self,
            "How to Use",
            "PC CamTouch - Multi-Camera Viewer\n\n"
            "1. Click 'Start' to enter the viewer\n"
            "2. Use Camera > Add Camera to add RTSP/HTTP streams\n"
            "3. Use File > Open File to play local videos\n"
            "4. Use View menu to change grid layout (2x2, 3x3, 4x4)",
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
            self.grid_view.set_grid(rows, cols)
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
        from PyQt6.QtWidgets import QInputDialog

        url, ok = QInputDialog.getText(
            self, "Add Camera", "Enter stream URL (RTSP/HTTP):"
        )
        if ok and url:
            logger.info(f"Adding camera stream: {url}")
            self.stacked_widget.setCurrentWidget(self.viewer_widget)
            self.grid_view.play_in_next_slot(url)
            self.statusbar.showMessage(f"Added stream: {url}")

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
        if self.grid_view:
            self.grid_view.stop_all()
        event.accept()
