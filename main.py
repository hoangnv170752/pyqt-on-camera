import sys
from PyQt6.QtWidgets import QApplication

from src.services.logger import get_logger

logger = get_logger("main")


def main():
    logger.info("Starting PC CamTouch application")

    app = QApplication(sys.argv)
    app.setApplicationName("PC CamTouch")
    app.setOrganizationName("CamTouch")

    from src.app import MainWindow

    window = MainWindow()
    window.show()

    logger.info("Application window displayed")

    exit_code = app.exec()
    logger.info(f"Application exiting with code {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
