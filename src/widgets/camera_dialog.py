from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QGroupBox,
    QFormLayout,
)
from PyQt6.QtCore import Qt

from src.models.camera import Camera
from src.services.logger import get_logger

logger = get_logger("camera_dialog")


class AddCameraDialog(QDialog):
    """Dialog to add a new camera source (RTSP or local file)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Camera Source")
        self.setMinimumWidth(500)
        self.camera = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Source type selection
        type_group = QGroupBox("Source Type")
        type_layout = QVBoxLayout(type_group)

        self.btn_group = QButtonGroup(self)
        self.radio_rtsp = QRadioButton("RTSP/HTTP Stream")
        self.radio_file = QRadioButton("Local Video File")
        self.radio_rtsp.setChecked(True)

        self.btn_group.addButton(self.radio_rtsp, 1)
        self.btn_group.addButton(self.radio_file, 2)

        type_layout.addWidget(self.radio_rtsp)
        type_layout.addWidget(self.radio_file)
        layout.addWidget(type_group)

        # Camera details
        details_group = QGroupBox("Camera Details")
        details_layout = QFormLayout(details_group)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Front Door Camera")
        details_layout.addRow("Name:", self.name_input)

        # URL input with browse button
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("rtsp://username:password@ip:port/stream")
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setEnabled(False)
        self.browse_btn.clicked.connect(self._browse_file)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.browse_btn)
        details_layout.addRow("URL/Path:", url_layout)

        layout.addWidget(details_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        add_btn = QPushButton("Add Camera")
        add_btn.clicked.connect(self._on_add)
        btn_layout.addWidget(add_btn)

        layout.addLayout(btn_layout)

        # Connect signals
        self.radio_rtsp.toggled.connect(self._on_type_changed)
        self.radio_file.toggled.connect(self._on_type_changed)

    def _on_type_changed(self):
        is_file = self.radio_file.isChecked()
        self.browse_btn.setEnabled(is_file)
        if is_file:
            self.url_input.setPlaceholderText("Click Browse to select a video file")
        else:
            self.url_input.setPlaceholderText("rtsp://username:password@ip:port/stream")

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv);;All Files (*)",
        )
        if file_path:
            self.url_input.setText(file_path)
            if not self.name_input.text():
                # Auto-fill name from filename
                from pathlib import Path
                self.name_input.setText(Path(file_path).stem)

    def _on_add(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a camera name.")
            return

        if not url:
            QMessageBox.warning(self, "Validation Error", "Please enter a URL or select a file.")
            return

        camera_type = "file" if self.radio_file.isChecked() else "rtsp"
        self.camera = Camera(name=name, url=url, type=camera_type)
        logger.info(f"Camera created: {name} ({camera_type})")
        self.accept()

    def get_camera(self) -> Camera:
        return self.camera


class EditCameraDialog(QDialog):
    """Dialog to edit an existing camera source."""

    def __init__(self, camera: Camera, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Camera Source")
        self.setMinimumWidth(500)
        self.camera = camera
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Source type selection
        type_group = QGroupBox("Source Type")
        type_layout = QVBoxLayout(type_group)

        self.btn_group = QButtonGroup(self)
        self.radio_rtsp = QRadioButton("RTSP/HTTP Stream")
        self.radio_file = QRadioButton("Local Video File")

        if self.camera.type == "file":
            self.radio_file.setChecked(True)
        else:
            self.radio_rtsp.setChecked(True)

        self.btn_group.addButton(self.radio_rtsp, 1)
        self.btn_group.addButton(self.radio_file, 2)

        type_layout.addWidget(self.radio_rtsp)
        type_layout.addWidget(self.radio_file)
        layout.addWidget(type_group)

        # Camera details
        details_group = QGroupBox("Camera Details")
        details_layout = QFormLayout(details_group)

        self.name_input = QLineEdit(self.camera.name)
        details_layout.addRow("Name:", self.name_input)

        # URL input with browse button
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit(self.camera.url)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setEnabled(self.camera.type == "file")
        self.browse_btn.clicked.connect(self._browse_file)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.browse_btn)
        details_layout.addRow("URL/Path:", url_layout)

        layout.addWidget(details_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

        # Connect signals
        self.radio_rtsp.toggled.connect(self._on_type_changed)
        self.radio_file.toggled.connect(self._on_type_changed)

    def _on_type_changed(self):
        is_file = self.radio_file.isChecked()
        self.browse_btn.setEnabled(is_file)

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv);;All Files (*)",
        )
        if file_path:
            self.url_input.setText(file_path)

    def _on_save(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a camera name.")
            return

        if not url:
            QMessageBox.warning(self, "Validation Error", "Please enter a URL or select a file.")
            return

        self.camera.name = name
        self.camera.url = url
        self.camera.type = "file" if self.radio_file.isChecked() else "rtsp"
        logger.info(f"Camera updated: {name}")
        self.accept()

    def get_camera(self) -> Camera:
        return self.camera


class CameraManagerDialog(QDialog):
    """Dialog to manage (view/edit/delete) camera sources."""

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Cameras")
        self.setMinimumSize(600, 400)
        self.db = db
        self._setup_ui()
        self._load_cameras()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Camera list
        self.camera_list = QListWidget()
        self.camera_list.itemDoubleClicked.connect(self._on_edit)
        layout.addWidget(self.camera_list)

        # Buttons
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Add New")
        add_btn.clicked.connect(self._on_add)
        btn_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self._on_edit)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._on_delete)
        btn_layout.addWidget(delete_btn)

        btn_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def _load_cameras(self):
        self.camera_list.clear()
        cameras = self.db.get_all_cameras()
        for camera in cameras:
            item = QListWidgetItem(f"{camera.name} ({camera.type}) - {camera.url}")
            item.setData(Qt.ItemDataRole.UserRole, camera)
            self.camera_list.addItem(item)

    def _on_add(self):
        dialog = AddCameraDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            camera = dialog.get_camera()
            self.db.add_camera(camera)
            self._load_cameras()

    def _on_edit(self):
        item = self.camera_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select a camera to edit.")
            return

        camera = item.data(Qt.ItemDataRole.UserRole)
        dialog = EditCameraDialog(camera, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_camera = dialog.get_camera()
            self.db.update_camera(updated_camera)
            self._load_cameras()

    def _on_delete(self):
        item = self.camera_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select a camera to delete.")
            return

        camera = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{camera.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_camera(camera.id)
            logger.info(f"Camera deleted: {camera.name}")
            self._load_cameras()
