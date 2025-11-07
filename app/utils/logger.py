from typing import Optional
from app.core.logging import get_logger


class Logger:
    _instance = get_logger()

    @staticmethod
    def write_info(message: str) -> None:
        Logger._instance.log_info(message)

    @staticmethod
    def write_error(message: str, metadata: Optional[dict] = None) -> None:
        Logger._instance.log_error(message, metadata)

    @staticmethod
    def write_warning(message: str) -> None:
        Logger._instance.log_warning(message)

    @staticmethod
    def write_debug(message: str) -> None:
        Logger._instance.log_debug(message)
