"""
logs/logger.py
Centralized logging configuration used across the whole project.
"""
import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__))
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

_file_handler = logging.FileHandler(LOG_FILE)
_file_handler.setFormatter(_formatter)

_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_formatter)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.addHandler(_file_handler)
        logger.addHandler(_console_handler)
    return logger
