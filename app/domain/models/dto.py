from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    status_code: int
    success: bool
    message: str
    data: Optional[Any] = None


class IngestRequest(BaseModel):
    document_id: Optional[str] = None


class IngestResponse(BaseModel):
    status: str
    document_id: str
    language: str
    chunks_created: int
    message: str


class Document(BaseModel):
    content: str
    document_id: str
    chunk_id: int
    language: str
    score: float


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class RetrieveResponse(BaseModel):
    query: str
    query_language: str
    results: List[Document]
    total_results: int


class GenerateRequest(BaseModel):
    query: str = Field(..., min_length=1)
    output_language: Optional[str] = None


class GenerateResponse(BaseModel):
    query: str
    query_language: str
    answer: str
    answer_language: str
    sources: List[Dict]
    translated: bool
