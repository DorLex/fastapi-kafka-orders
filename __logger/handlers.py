import logging

from .formatters import formatter
from src.config import BASE_DIR

file_handler = logging.FileHandler(
    BASE_DIR / 'logs/logs.log',
    encoding='utf-8',
    mode='w'
)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
