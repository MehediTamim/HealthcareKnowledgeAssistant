from typing import Optional
from app.domain.models.dto import RetrieveResponse, GenerateResponse, Document
from app.infrastructure.vector_store.faiss_repository import FAISSRepository
from app.infrastructure.embedding.embedding_service import EmbeddingService
from app.infrastructure.language.detector import LanguageDetector
from app.infrastructure.language.translator import TranslatorService
from app.infrastructure.llm.mock_generator import MockLLMGenerator
from app.core.exceptions import raise_internal_error
from app.utils.logger import Logger


class GenerationService:
    def __init__(
        self,
        faiss_repo: Optional[FAISSRepository] = None,
        embedding_svc: Optional[EmbeddingService] = None,
        language_detector: Optional[LanguageDetector] = None,
        translator: Optional[TranslatorService] = None,
        mock_llm: Optional[MockLLMGenerator] = None
    ):
        from app.infrastructure.vector_store.faiss_repository import FAISSRepository
        from app.infrastructure.embedding.embedding_service import embedding_service
        from app.infrastructure.language.detector import language_detector as lang_detect
        from app.infrastructure.language.translator import translator_service
        from app.infrastructure.llm.mock_generator import mock_llm_generator

        self.faiss_repo = faiss_repo or FAISSRepository()
        self.embedding_svc = embedding_svc or embedding_service
        self.language_detector = language_detector or lang_detect
        self.translator = translator or translator_service
        self.mock_llm = mock_llm or mock_llm_generator

    async def retrieve_documents(self, query: str, top_k: int = 3) -> RetrieveResponse:
        try:
            Logger.write_info(f"Retrieving documents for query: {query[:50]}...")

            query_language = self.language_detector.detect(query)
            Logger.write_debug(f"Query language: {query_language}")

            query_embedding = self.embedding_svc.encode([query], convert_to_numpy=True)[0]

            results = self.faiss_repo.search(query_embedding, top_k=top_k)

            documents = []
            for result in results:
                documents.append(Document(
                    content=result['content'],
                    document_id=result['document_id'],
                    chunk_id=result['chunk_id'],
                    language=result['language'],
                    score=result['score']
                ))

            Logger.write_info(f"Retrieved {len(documents)} documents")

            return RetrieveResponse(
                query=query,
                query_language=query_language,
                results=documents,
                total_results=len(documents)
            )

        except Exception as e:
            Logger.write_error(f"Error retrieving documents: {str(e)}")
            raise_internal_error(f"Error retrieving documents: {str(e)}")

    async def generate_answer(
        self,
        query: str,
        output_language: Optional[str] = None
    ) -> GenerateResponse:
        try:
            Logger.write_info(f"Generating answer for query: {query[:50]}...")

            query_language = self.language_detector.detect(query)
            Logger.write_debug(f"Query language: {query_language}")

            query_embedding = self.embedding_svc.encode([query], convert_to_numpy=True)[0]
            results = self.faiss_repo.search(query_embedding, top_k=3)

            if not results:
                answer = self.mock_llm.generate_no_results_response(query_language)
                return GenerateResponse(
                    query=query,
                    query_language=query_language,
                    answer=answer,
                    answer_language=query_language,
                    sources=[],
                    translated=False
                )

            answer = self.mock_llm.generate(
                query=query,
                context_docs=results,
                language=query_language
            )
            answer_language = query_language
            translated = False

            if output_language and output_language != query_language:
                Logger.write_info(f"Translating answer from {query_language} to {output_language}")
                answer = self.translator.translate(answer, query_language, output_language)
                answer_language = output_language
                translated = True

            sources = [
                {
                    'document_id': r['document_id'],
                    'chunk_id': r['chunk_id'],
                    'score': r['score'],
                    'language': r['language']
                }
                for r in results
            ]

            Logger.write_info("Successfully generated answer")

            return GenerateResponse(
                query=query,
                query_language=query_language,
                answer=answer,
                answer_language=answer_language,
                sources=sources,
                translated=translated
            )

        except Exception as e:
            Logger.write_error(f"Error generating answer: {str(e)}")
            raise_internal_error(f"Error generating answer: {str(e)}")


generation_service = GenerationService()
