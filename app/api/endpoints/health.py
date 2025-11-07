from fastapi import APIRouter, status
from app.infrastructure.vector_store.faiss_repository import FAISSRepository
from app.core.config import settings
from app.domain.models.dto import ApiResponse

router = APIRouter()


@router.get("/", response_model=ApiResponse)
async def root():
    faiss_repo = FAISSRepository()
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        success=True,
        message=f"{settings.PROJECT_NAME}",
        data={
            "version": settings.VERSION,
            "endpoints": ["/ingest", "/retrieve", "/generate"],
            "total_documents": faiss_repo.get_total_documents()
        }
    )


@router.get("/health", response_model=ApiResponse)
async def health():
    faiss_repo = FAISSRepository()
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        success=True,
        message="Service is healthy",
        data={
            "status": "healthy",
            "total_documents": faiss_repo.get_total_documents(),
            "embedding_model": settings.EMBEDDING_MODEL,
            "embedding_dimension": settings.EMBEDDING_DIMENSION
        }
    )
