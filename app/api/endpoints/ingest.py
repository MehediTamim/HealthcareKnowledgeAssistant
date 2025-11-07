from fastapi import APIRouter, UploadFile, File, Depends, status
from typing import Optional
from app.domain.models.dto import ApiResponse
from app.application.services.ingestion_service import ingestion_service
from app.api.dependencies import verify_api_key
from app.core.exceptions import raise_bad_request, raise_internal_error
from app.utils.logger import Logger

router = APIRouter()


@router.post("/ingest", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(
    file: UploadFile = File(...),
    document_id: Optional[str] = None,
    x_api_key: str = Depends(verify_api_key)
):
    try:
        Logger.write_info(f"Ingesting document: {file.filename}")

        content = await file.read()
        text = content.decode('utf-8')

        doc_id = document_id or file.filename.replace('.txt', '')

        result = await ingestion_service.ingest_document(text, doc_id)

        return ApiResponse(
            status_code=status.HTTP_201_CREATED,
            success=True,
            message=f"Document '{result['document_id']}' successfully ingested with {result['chunks_created']} chunks",
            data=result
        )

    except UnicodeDecodeError:
        raise_bad_request("File must be UTF-8 encoded text")
    except Exception as e:
        Logger.write_error(f"Error in ingest endpoint: {str(e)}")
        raise_internal_error(f"Failed to ingest document: {str(e)}")
