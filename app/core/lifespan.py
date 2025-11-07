from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.utils.logger import Logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    Logger.write_info(f"Starting {app.title}...")

    try:
        await check_connections()
        Logger.write_info("✓ All connections healthy")
    except Exception as e:
        Logger.write_error(f"Startup failed: {str(e)}", metadata={"error": str(e)})
        raise ConnectionError(f"Startup check failed: {e}")

    yield

    Logger.write_info("Shutting down gracefully...")


async def check_connections():
    from app.infrastructure.vector_store.faiss_repository import FAISSRepository
    from app.infrastructure.embedding.embedding_service import EmbeddingService

    Logger.write_info("Checking FAISS vector store...")
    faiss_repo = FAISSRepository()
    if not faiss_repo.is_healthy():
        raise ConnectionError("FAISS initialization failed")
    Logger.write_info(f"✓ FAISS ready with {faiss_repo.get_total_documents()} documents")

    Logger.write_info("Checking embedding service...")
    embedding_service = EmbeddingService()
    if not embedding_service.is_loaded():
        raise ConnectionError("Embedding model not loaded")
    Logger.write_info(f"✓ Embedding model loaded: {embedding_service.get_model_name()}")
