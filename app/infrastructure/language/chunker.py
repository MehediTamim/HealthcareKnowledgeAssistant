from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from app.utils.logger import Logger


class SemanticChunker:
    def __init__(self):
        try:
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
                is_separator_regex=False,
            )
            Logger.write_info(f"Chunker initialized (size={settings.CHUNK_SIZE}, overlap={settings.CHUNK_OVERLAP})")
        except Exception as e:
            Logger.write_error(f"Failed to initialize chunker: {e}")
            raise

    def chunk_text(self, text: str) -> List[str]:
        try:
            if not text or len(text.strip()) == 0:
                return []

            chunks = self.splitter.split_text(text)
            Logger.write_debug(f"Text chunked into {len(chunks)} pieces")
            return chunks

        except Exception as e:
            Logger.write_warning(f"Error in chunking, returning original text: {e}")
            return [text]


semantic_chunker = SemanticChunker()
