import logging
import sys
from abc import ABC, abstractmethod
from logging.handlers import TimedRotatingFileHandler
from typing import Optional
from app.core.config import settings


class BaseLogger(ABC):
    @abstractmethod
    def log_info(self, message: str) -> None:
        pass

    @abstractmethod
    def log_error(self, message: str, metadata: Optional[dict] = None) -> None:
        pass

    @abstractmethod
    def log_warning(self, message: str) -> None:
        pass

    @abstractmethod
    def log_debug(self, message: str) -> None:
        pass


class FileLogger(BaseLogger):
    def __init__(self):
        self._logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("healthcare_assistant")

        if not logger.hasHandlers():
            log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
            logger.setLevel(log_level)

            file_handler = TimedRotatingFileHandler(
                settings.LOG_FILE,
                when='D',
                backupCount=7
            )
            file_handler.setLevel(log_level)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    def log_info(self, message: str) -> None:
        self._logger.info(message)

    def log_error(self, message: str, metadata: Optional[dict] = None) -> None:
        if metadata:
            message = f"{message} | Metadata: {metadata}"
        self._logger.error(message)

    def log_warning(self, message: str) -> None:
        self._logger.warning(message)

    def log_debug(self, message: str) -> None:
        self._logger.debug(message)


_logger_instance = FileLogger()


def get_logger() -> BaseLogger:
    return _logger_instance
