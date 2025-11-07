from fastapi import APIRouter, Depends, status
from app.domain.models.dto import GenerateRequest, ApiResponse
from app.application.services.generation_service import generation_service
from app.api.dependencies import verify_api_key
from app.core.exceptions import raise_internal_error
from app.utils.logger import Logger

router = APIRouter()


@router.post("/generate", response_model=ApiResponse)
async def generate_answer(
    request: GenerateRequest,
    x_api_key: str = Depends(verify_api_key)
):
    try:
        result = await generation_service.generate_answer(
            query=request.query,
            output_language=request.output_language
        )

        return ApiResponse(
            status_code=status.HTTP_200_OK,
            success=True,
            message="Answer generated successfully",
            data=result
        )

    except Exception as e:
        Logger.write_error(f"Error in generate endpoint: {str(e)}")
        raise_internal_error(f"Failed to generate answer: {str(e)}")
