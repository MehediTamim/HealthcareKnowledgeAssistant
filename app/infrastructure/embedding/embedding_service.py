import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.utils.logger import Logger


class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._load_model()

    def _load_model(self):
        try:
            Logger.write_info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(
                settings.EMBEDDING_MODEL,
                device='cpu'
            )
            self._model.max_seq_length = settings.MAX_SEQ_LENGTH
            Logger.write_info(f"Embedding model loaded (dim={settings.EMBEDDING_DIMENSION}, max_seq={settings.MAX_SEQ_LENGTH})")
        except Exception as e:
            Logger.write_error(f"Failed to load embedding model: {e}")
            raise

    def encode(self, texts: List[str], convert_to_numpy: bool = True) -> np.ndarray:
        try:
            embeddings = self._model.encode(
                texts,
                convert_to_numpy=convert_to_numpy,
                show_progress_bar=False,
                normalize_embeddings=True
            )
            Logger.write_debug(f"Encoded {len(texts)} texts")
            return embeddings
        except Exception as e:
            Logger.write_error(f"Error encoding texts: {e}")
            raise

    def is_loaded(self) -> bool:
        return self._model is not None

    def get_model_name(self) -> str:
        return settings.EMBEDDING_MODEL

    def get_dimension(self) -> int:
        return settings.EMBEDDING_DIMENSION


embedding_service = EmbeddingService()
