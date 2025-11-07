import faiss
import numpy as np
import json
from typing import List, Dict
from pathlib import Path
from app.core.config import settings
from app.utils.logger import Logger


class FAISSRepository:
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIMENSION
        self.index = None
        self.metadata = []
        self.index_path = Path(settings.FAISS_INDEX_DIR) / 'index.faiss'
        self.metadata_path = Path(settings.METADATA_FILE)

        self._load_or_create()

    def _load_or_create(self):
        try:
            if self.index_path.exists() and self.metadata_path.exists():
                self.index = faiss.read_index(str(self.index_path))
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                Logger.write_info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                self.index = faiss.IndexFlatL2(self.dimension)
                Logger.write_info(f"Created new FAISS index (dimension={self.dimension})")
        except Exception as e:
            Logger.write_error(f"Error loading FAISS index: {e}")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def add_documents(self, embeddings: np.ndarray, metadata: List[Dict]) -> None:
        try:
            if len(embeddings) != len(metadata):
                raise ValueError("Embeddings and metadata length mismatch")

            self.index.add(embeddings.astype('float32'))
            self.metadata.extend(metadata)
            self._save()

            Logger.write_info(f"Added {len(embeddings)} documents to FAISS index")
        except Exception as e:
            Logger.write_error(f"Error adding documents: {e}")
            raise

    def search(self, query_vector: np.ndarray, top_k: int = 3) -> List[Dict]:
        try:
            if self.index.ntotal == 0:
                Logger.write_warning("FAISS index is empty")
                return []

            query_vector = query_vector.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))

            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(self.metadata) and idx != -1:
                    result = self.metadata[idx].copy()
                    result['score'] = float(1 / (1 + dist))
                    results.append(result)

            Logger.write_debug(f"Search returned {len(results)} results")
            return results
        except Exception as e:
            Logger.write_error(f"Error searching FAISS: {e}")
            return []

    def _save(self):
        try:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            Logger.write_debug("FAISS index and metadata saved")
        except Exception as e:
            Logger.write_error(f"Error saving FAISS index: {e}")
            raise

    def is_healthy(self) -> bool:
        return self.index is not None

    def get_total_documents(self) -> int:
        return self.index.ntotal if self.index else 0

    def clear(self):
        try:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            self._save()
            Logger.write_info("FAISS index cleared")
        except Exception as e:
            Logger.write_error(f"Error clearing FAISS index: {e}")
            raise
