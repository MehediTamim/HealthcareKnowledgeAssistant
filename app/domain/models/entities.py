from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentMetadata:
    content: str
    document_id: str
    chunk_id: int
    language: str
    score: Optional[float] = None
