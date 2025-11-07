import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


class APISettings(BaseAppSettings):
    API_KEY: str = "dev-secret-key-12345"
    PROJECT_NAME: str = "Healthcare Knowledge Assistant"
    VERSION: str = "1.0.0"


class EmbeddingSettings:
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-base"
    EMBEDDING_DIMENSION: int = 768
    MAX_SEQ_LENGTH: int = 512


class StorageSettings:
    STORAGE_DIR: str = "storage"
    FAISS_INDEX_DIR: str = f"{STORAGE_DIR}/faiss_index"
    METADATA_FILE: str = f"{STORAGE_DIR}/metadata.json"


class ChunkingSettings:
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50


class LoggingSettings:
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: str = f"{LOG_DIR}/app.log"


class AppSettings(
    APISettings,
    EmbeddingSettings,
    StorageSettings,
    ChunkingSettings,
    LoggingSettings
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()

    def _ensure_directories(self):
        os.makedirs(self.STORAGE_DIR, exist_ok=True)
        os.makedirs(self.FAISS_INDEX_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)


settings = AppSettings()
