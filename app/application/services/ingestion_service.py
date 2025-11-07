from typing import Optional
from app.domain.models.dto import IngestResponse
from app.infrastructure.vector_store.faiss_repository import FAISSRepository
from app.infrastructure.embedding.embedding_service import EmbeddingService
from app.infrastructure.language.detector import LanguageDetector
from app.infrastructure.language.chunker import SemanticChunker
from app.core.exceptions import raise_bad_request, raise_internal_error
from app.utils.logger import Logger


class IngestionService:
    def __init__(
        self,
        faiss_repo: Optional[FAISSRepository] = None,
        embedding_svc: Optional[EmbeddingService] = None,
        language_detector: Optional[LanguageDetector] = None,
        chunker: Optional[SemanticChunker] = None
    ):
        from app.infrastructure.vector_store.faiss_repository import FAISSRepository
        from app.infrastructure.embedding.embedding_service import embedding_service
        from app.infrastructure.language.detector import language_detector as lang_detect
        from app.infrastructure.language.chunker import semantic_chunker

        self.faiss_repo = faiss_repo or FAISSRepository()
        self.embedding_svc = embedding_svc or embedding_service
        self.language_detector = language_detector or lang_detect
        self.chunker = chunker or semantic_chunker

    async def ingest_document(self, text: str, document_id: str) -> IngestResponse:
        try:
            Logger.write_info(f"Starting document ingestion: {document_id}")

            if not text or not text.strip():
                raise_bad_request("Document text is empty")

            language = self.language_detector.detect(text)
            Logger.write_info(f"Detected language: {language}")

            chunks = self.chunker.chunk_text(text)
            if not chunks:
                raise_bad_request("No chunks created from document")
            Logger.write_info(f"Created {len(chunks)} chunks")

            embeddings = self.embedding_svc.encode(chunks, convert_to_numpy=True)

            metadata = []
            for i, chunk in enumerate(chunks):
                metadata.append({
                    'content': chunk,
                    'document_id': document_id,
                    'chunk_id': i,
                    'language': language
                })

            self.faiss_repo.add_documents(embeddings, metadata)

            Logger.write_info(f"Successfully ingested document: {document_id}")

            return IngestResponse(
                status="success",
                document_id=document_id,
                language=language,
                chunks_created=len(chunks),
                message=f"Document '{document_id}' successfully ingested with {len(chunks)} chunks"
            )

        except ValueError as e:
            Logger.write_error(f"Validation error in ingestion: {str(e)}")
            raise_bad_request(str(e))
        except Exception as e:
            Logger.write_error(
                f"Error in document ingestion: {str(e)}",
                metadata={"document_id": document_id, "error": str(e)}
            )
            raise_internal_error(f"Error ingesting document: {str(e)}")


ingestion_service = IngestionService()
