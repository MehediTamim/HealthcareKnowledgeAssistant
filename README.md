# Healthcare Knowledge Assistant

A production-ready, bilingual (English/Japanese) RAG-powered backend system for retrieving medical guidelines and research summaries.

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system using Domain-Driven Design principles. It provides semantic search capabilities across medical documents with bilingual support, enabling healthcare professionals to quickly find relevant information from large document repositories.

## Features

- **Bilingual Support**: Native English and Japanese document ingestion and query processing
- **Semantic Search**: Vector-based similarity search with 768-dimensional embeddings
- **Domain-Driven Design**: Clean 5-layer architecture with clear separation of concerns
- **Production Ready**: Health checks, structured logging, connection validation on startup
- **Secure**: API key authentication on all protected endpoints
- **Containerized**: Docker and docker-compose support for easy deployment
- **CI/CD Pipeline**: Automated testing and linting with GitHub Actions

## Design Decisions

### Why intfloat/multilingual-e5-base?

**Model Specifications**:
- Context Window: 512 tokens
- Embedding Dimension: 768
- Model Size: ~470MB
- Language Support: 100+ languages including English and Japanese

**Rationale**:
1. **Optimal Context Window**: 512 tokens perfectly matches our chunk size strategy, maximizing relevance without truncation
2. **Multilingual Support**: Native support for both English and Japanese without separate models
3. **Efficient Size**: Smaller than alternatives (BGE-M3: 2.3GB) while maintaining quality
4. **Production-Ready**: Well-maintained by HuggingFace with extensive usage in production systems
5. **Performance**: Fast inference on CPU, no GPU required

### Why Mock LLM?

**Decision**: Use mock LLM for response generation instead of real LLM API (OpenAI, Anthropic, Ollama).

**Rationale**:
1. **Predictable**: No external API dependencies, consistent responses for testing
2. **Cost-Effective**: Zero API costs during development and testing
3. **Fast**: Instant response generation without API latency
4. **Swappable**: Clean separation allows easy replacement with real LLM when needed
5. **Development Focus**: Validates RAG pipeline architecture without LLM complexity

**When to Replace**:
- Production deployment requiring intelligent synthesis
- User-facing applications needing natural language generation
- Cases where context-aware summarization is critical

**How to Replace**:
1. Create new LLM service in `app/infrastructure/llm/` (e.g., `openai_generator.py`)
2. Update `GenerationService` to use new LLM service
3. No changes needed to API endpoints or domain logic

### Why NOT LangChain for RAG?

**Decision**: Use LangChain ONLY for text splitting, NOT for RAG orchestration.

**Rationale**:
1. **Simplicity**: Mock LLM = simple string formatting, no need for complex chains
2. **Transparency**: Custom service layer makes control flow explicit and debuggable
3. **Maintainability**: Easier to understand and modify without framework abstractions
4. **Testability**: Direct service calls are easier to unit test than chain compositions
5. **Swappable**: Easier to replace mock with real LLM without rewriting chain logic

**LangChain Usage**:
- ✅ `RecursiveCharacterTextSplitter` - Excellent text chunking utility
- ❌ `RetrievalQA` chains - Over-engineered for our use case

### Why Domain-Driven Design?

**Benefits**:
1. **Layer Independence**: Each layer can be tested and modified in isolation
2. **Clear Dependencies**: Dependencies flow inward toward domain, never outward
3. **Swappable Components**: Easy to replace FAISS with Weaviate, mock LLM with real LLM
4. **Scalability**: Architecture supports horizontal scaling and microservices extraction
5. **Maintainability**: Clear separation makes codebase easier to navigate and extend

**Layer Structure**:
```
API (endpoints) → Application (services) → Infrastructure (FAISS, embeddings, LLM)
                         ↓
                      Domain (models, DTOs)
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | FastAPI | 0.115.0 |
| Embeddings | intfloat/multilingual-e5-base | 512 ctx, 768 dim |
| Vector Store | FAISS (CPU) | 1.9.0 |
| Text Splitting | LangChain | 0.3.0 |
| Server | Uvicorn | 0.32.0 |
| Testing | Pytest | 8.3.0 |
| Linting | Black + Flake8 | 24.10.0 + 7.1.0 |

## Project Structure

```
healthcare-knowledge-assistant/
├── app/
│   ├── core/                      # Core infrastructure
│   │   ├── config.py             # Settings (only API_KEY from env)
│   │   ├── lifespan.py           # Startup health checks
│   │   ├── exceptions.py         # Custom exceptions
│   │   └── logging.py            # File-based logging with rotation
│   ├── domain/                    # Business models
│   │   └── models/
│   │       ├── dto.py            # API request/response models
│   │       └── entities.py       # Domain entities
│   ├── application/               # Business logic orchestration
│   │   └── services/
│   │       ├── ingestion_service.py
│   │       └── generation_service.py
│   ├── infrastructure/            # External systems
│   │   ├── vector_store/
│   │   │   └── faiss_repository.py
│   │   ├── embedding/
│   │   │   └── embedding_service.py
│   │   ├── language/
│   │   │   ├── detector.py       # Regex-based EN/JA detection
│   │   │   ├── translator.py     # Mock translation
│   │   │   └── chunker.py        # LangChain text splitter
│   │   └── llm/
│   │       └── mock_generator.py # Mock LLM responses
│   ├── api/                       # HTTP endpoints
│   │   ├── dependencies.py       # Dependency injection
│   │   ├── router.py             # Route aggregation
│   │   └── endpoints/
│   │       ├── health.py         # Health checks
│   │       ├── ingest.py         # Document ingestion
│   │       ├── retrieve.py       # Vector search
│   │       └── generate.py       # RAG generation
│   └── main.py                    # FastAPI app
├── storage/                       # FAISS index + metadata
├── logs/                          # Application logs (auto-created)
├── tests/                         # Test suite
├── .env                          # API_KEY only
├── requirements.txt              # 16 exact dependencies
├── Dockerfile                    # Multi-stage build
├── docker-compose.yml            # Single-service deployment
└── .github/workflows/
    └── ci-cd.yml                 # Super-Linter + pytest
```

## Quick Start

### Local Development

```bash
# Clone and setup
git clone <repository-url>
cd healthcare-knowledge-assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure (optional - default API_KEY works for dev)
cp .env.example .env
# Edit .env if needed

# Run server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access API docs: http://localhost:8000/docs

### Docker Deployment

```bash
docker-compose up -d
docker-compose logs -f
```

## API Endpoints

All endpoints return a consistent `ApiResponse` structure:

```json
{
  "status_code": 200,
  "success": true,
  "message": "Descriptive message",
  "data": { /* endpoint-specific data */ }
}
```

### Health Check

**GET /** - Basic service information

```bash
curl -X GET "http://localhost:8000/"
```

**Response**:
```json
{
  "status_code": 200,
  "success": true,
  "message": "Healthcare Knowledge Assistant",
  "data": {
    "version": "1.0.0",
    "endpoints": ["/ingest", "/retrieve", "/generate"],
    "total_documents": 5
  }
}
```

**GET /health** - Detailed health check

```bash
curl -X GET "http://localhost:8000/health"
```

**Response**:
```json
{
  "status_code": 200,
  "success": true,
  "message": "Service is healthy",
  "data": {
    "status": "healthy",
    "total_documents": 5,
    "embedding_model": "intfloat/multilingual-e5-base",
    "embedding_dimension": 768
  }
}
```

### Document Ingestion

**POST /ingest**

Upload UTF-8 text documents for semantic search.

```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "X-API-Key: dev-secret-key-12345" \
  -F "file=@medical_document.txt" \
  -F "document_id=diabetes_guideline_2024"
```

**Request**:
- `file`: UTF-8 .txt file (required)
- `document_id`: Custom identifier (optional, auto-generated if not provided)

**Response**:
```json
{
  "status_code": 201,
  "success": true,
  "message": "Document 'diabetes_guideline_2024' successfully ingested with 12 chunks",
  "data": {
    "status": "success",
    "document_id": "diabetes_guideline_2024",
    "language": "en",
    "chunks_created": 12,
    "message": "Document 'diabetes_guideline_2024' successfully ingested with 12 chunks"
  }
}
```

### Document Retrieval

**POST /retrieve**

Semantic search for relevant document chunks.

```bash
curl -X POST "http://localhost:8000/retrieve" \
  -H "X-API-Key: dev-secret-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are treatment options for Type 2 diabetes?",
    "top_k": 3
  }'
```

**Request**:
```json
{
  "query": "string",
  "top_k": 3
}
```

**Response**:
```json
{
  "status_code": 200,
  "success": true,
  "message": "Retrieved 3 document(s)",
  "data": {
    "query": "What are treatment options for Type 2 diabetes?",
    "query_language": "en",
    "results": [
      {
        "content": "Treatment typically includes lifestyle changes...",
        "document_id": "diabetes_guideline_2024",
        "chunk_id": 0,
        "language": "en",
        "score": 0.87
      }
    ],
    "total_results": 3
  }
}
```

### Answer Generation

**POST /generate**

RAG-powered answer generation with optional translation.

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "X-API-Key: dev-secret-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What medications are recommended for Type 2 diabetes?",
    "output_language": "ja"
  }'
```

**Request**:
```json
{
  "query": "string",
  "output_language": "en" | "ja" (optional)
}
```

**Response**:
```json
{
  "status_code": 200,
  "success": true,
  "message": "Answer generated successfully",
  "data": {
    "query": "What medications are recommended for Type 2 diabetes?",
    "query_language": "en",
    "answer": "Based on the medical guidelines...",
    "answer_language": "en",
    "sources": [
      {
        "document_id": "diabetes_guideline_2024",
        "chunk_id": 2,
        "score": 0.89,
        "language": "en"
      }
    ],
    "translated": false
  }
}
```

## Configuration

**Environment Variables** (.env):

| Variable | Description | Default |
|----------|-------------|---------|
| API_KEY | API authentication key | dev-secret-key-12345 |

**Hardcoded Settings** (app/core/config.py):

| Setting | Value | Purpose |
|---------|-------|---------|
| EMBEDDING_MODEL | intfloat/multilingual-e5-base | Sentence transformer model |
| EMBEDDING_DIMENSION | 768 | Vector dimension |
| MAX_SEQ_LENGTH | 512 | Max tokens per chunk |
| CHUNK_SIZE | 512 | Characters per chunk |
| CHUNK_OVERLAP | 50 | Overlap between chunks |
| LOG_LEVEL | INFO | Logging verbosity |
| STORAGE_DIR | storage | FAISS index location |
| LOG_DIR | logs | Log file location |

**Why Hardcoded?**
- These are architectural constants that shouldn't change per deployment
- Prevents misconfiguration (e.g., dimension mismatch between model and FAISS)
- Simplifies deployment - only API_KEY needs to be secured
- Changes to these values require code review and testing

## Architecture

### RAG Pipeline Flow

```
1. User Query (EN/JA)
        ↓
2. Language Detection (regex-based)
        ↓
3. Query Embedding (multilingual-e5-base)
        ↓
4. Vector Search (FAISS L2 similarity)
        ↓
5. Context Retrieval (top-k chunks)
        ↓
6. Answer Generation (mock LLM)
        ↓
7. Translation (if output_language specified)
        ↓
8. Response (JSON with sources)
```

### Dependency Injection Pattern

Services accept optional dependencies for testability:

```python
class IngestionService:
    def __init__(
        self,
        faiss_repo: Optional[FAISSRepository] = None,
        embedding_svc: Optional[EmbeddingService] = None,
        chunker: Optional[SemanticChunker] = None,
        detector: Optional[LanguageDetector] = None
    ):
        self.faiss_repo = faiss_repo or FAISSRepository()
        self.embedding_svc = embedding_svc or EmbeddingService()
        # Allows mock injection for testing
```

### Key Design Patterns

| Pattern | Usage | Location |
|---------|-------|----------|
| Repository | Isolate FAISS data access | FAISSRepository |
| Service Layer | Business logic orchestration | IngestionService, GenerationService |
| Dependency Injection | Testability via optional params | All services |
| Singleton | One embedding model instance | EmbeddingService |
| Facade | Simplified logging interface | Logger |
| Composition | Settings inheritance | AppSettings |

## Development

### Running Tests

```bash
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Code Quality

```bash
# Format
black app/ tests/

# Lint
flake8 app/ tests/

# Type checking (optional)
mypy app/
```

### Analyzing Dependencies

```bash
# Show only top-level dependencies (excludes sub-dependencies)
pip-chill
```

## CI/CD Pipeline

**Triggers**:
- Push to `main` or `develop`: Run lint + test
- Pull request to `main`: Run lint + test

**Workflow Steps**:
- Super-Linter (Black, Flake8)
- Pytest execution
- Dependency caching

**Note**: This is an assessment/portfolio project, so CI/CD focuses on code quality (linting + testing) rather than automated Docker builds. Docker deployment is available locally via `docker-compose up` - see Docker Deployment section above.

**Industry Note**: Production projects often include automated Docker builds in CI/CD, but for assessment projects, demonstrating code quality practices is typically sufficient. Separate CD tools (ArgoCD, GitOps) are commonly used for production deployments.

## Deployment

### Production Checklist

- [ ] Change `API_KEY` in .env to secure random value
- [ ] Configure persistent volumes for `storage/` and `logs/`
- [ ] Enable HTTPS with reverse proxy (nginx/traefik)
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure FAISS index backups
- [ ] Review Docker resource limits
- [ ] Set up log aggregation (ELK, Loki)

### Scaling Considerations

**Current Architecture**:
- Stateless API (horizontal scaling ready)
- FAISS index loaded per instance (read-only)
- No shared state between instances

**Scalability Enhancements**:
1. **Distributed Vector Store**: Replace FAISS with Weaviate/Pinecone for multi-node
2. **Embedding Cache**: Add Redis to cache embeddings (60-80% load reduction)
3. **Async Ingestion**: Queue large documents in Celery/RabbitMQ
4. **API Separation**: Separate read API from write API for different scaling profiles
5. **CDN**: Cache frequently accessed documents

### Future Improvements

**LLM Integration**:
- Replace mock LLM with OpenAI/Anthropic client
- Add streaming response support
- Implement prompt templates and versioning

**Search Enhancements**:
- Hybrid search (semantic + keyword BM25)
- Reranking with cross-encoder
- Query expansion with synonyms
- Metadata filtering

**Monitoring**:
- Prometheus metrics (latency, throughput, errors)
- Grafana dashboards
- Structured logging with trace IDs
- OpenTelemetry integration

**Security**:
- Per-API-key rate limiting
- JWT authentication
- Role-based access control
- Audit logging

## Troubleshooting

### Embedding Model Not Loading

**Issue**: Model download fails or times out

**Solution**:
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-base')"
```

### FAISS Index Corruption

**Issue**: Index cannot be loaded

**Solution**:
```bash
rm -rf storage/faiss_index/*
rm storage/metadata.json
# Re-ingest documents via /ingest endpoint
```

### Memory Issues

**Issue**: Out of memory during embedding

**Solution**:
- Reduce `MAX_SEQ_LENGTH` to 256 in `app/core/config.py`
- Process documents in smaller batches
- Increase Docker memory limit in docker-compose.yml

### Port Already in Use

**Issue**: Port 8000 already occupied

**Solution**:
```bash
# Find process
lsof -i :8000

# Kill process or use different port
uvicorn app.main:app --port 8001
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Acknowledgments

- **Architecture**: Domain-Driven Design principles
- **Embeddings**: intfloat/multilingual-e5-base by HuggingFace
- **Vector Search**: Facebook FAISS
- **Framework**: FastAPI by Sebastián Ramírez
