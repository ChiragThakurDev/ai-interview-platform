import logging 
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR=Path("logs")
LOG_DIR.mkdir(exist_ok = True)

logger =logging.getLogger("app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler=logging.StreamHandler()

console_handler.setLevel(logging.INFO)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
)

file_handler.setLevel(logging.INFO)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
