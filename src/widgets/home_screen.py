from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class HomeScreen(QWidget):
    start_clicked = pyqtSignal()
    how_to_use_clicked = pyqtSignal()
    data_export_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)

        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        title = QLabel("PCCT")
        title_font = QFont()
        title_font.setPointSize(72)
        title_font.setItalic(True)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: black;")
        layout.addWidget(title)

        layout.addSpacerItem(
            QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        button_style = """
            QPushButton {
                background-color: white;
                border: 2px solid black;
                border-radius: 8px;
                padding: 12px 40px;
                font-size: 16px;
                color: black;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """

        btn_start = QPushButton("Start")
        btn_start.setStyleSheet(button_style)
        btn_start.clicked.connect(self.start_clicked.emit)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        btn_how_to_use = QPushButton("How to use")
        btn_how_to_use.setStyleSheet(button_style)
        btn_how_to_use.clicked.connect(self.how_to_use_clicked.emit)
        layout.addWidget(btn_how_to_use, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        btn_data_export = QPushButton("Data export")
        btn_data_export.setStyleSheet(button_style)
        btn_data_export.clicked.connect(self.data_export_clicked.emit)
        layout.addWidget(btn_data_export, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
