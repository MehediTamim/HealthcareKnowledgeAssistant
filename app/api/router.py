from fastapi import APIRouter
from app.api.endpoints import health, ingest, retrieve, generate

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health Check"])
api_router.include_router(ingest.router, tags=["Ingestion"])
api_router.include_router(retrieve.router, tags=["Retrieval"])
api_router.include_router(generate.router, tags=["Generation"])
