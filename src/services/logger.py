import sys
from pathlib import Path
from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)

logger.add(
    LOG_DIR / "app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    encoding="utf-8",
)

logger.add(
    LOG_DIR / "error_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    encoding="utf-8",
)


def get_logger(name: str = None):
    if name:
        return logger.bind(name=name)
    return logger
