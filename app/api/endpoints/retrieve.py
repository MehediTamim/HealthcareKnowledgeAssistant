from fastapi import APIRouter, Depends, status
from app.domain.models.dto import RetrieveRequest, ApiResponse
from app.application.services.generation_service import generation_service
from app.api.dependencies import verify_api_key
from app.core.exceptions import raise_internal_error
from app.utils.logger import Logger

router = APIRouter()


@router.post("/retrieve", response_model=ApiResponse)
async def retrieve_documents(
    request: RetrieveRequest,
    x_api_key: str = Depends(verify_api_key)
):
    try:
        result = await generation_service.retrieve_documents(
            query=request.query,
            top_k=request.top_k
        )

        return ApiResponse(
            status_code=status.HTTP_200_OK,
            success=True,
            message=f"Retrieved {result['total_results']} document(s)",
            data=result
        )

    except Exception as e:
        Logger.write_error(f"Error in retrieve endpoint: {str(e)}")
        raise_internal_error(f"Failed to retrieve documents: {str(e)}")
