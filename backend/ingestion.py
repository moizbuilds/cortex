import re
from docx import Document
import io
from backend.qdrant_client import ensure_collection, upsert_chunks
from backend.models import IngestionStatus

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

def _extract_paragraphs(docx_bytes: bytes) -> list[dict]:
    """Returns list of {text, section, page}. DOCX has no page info so page=0."""
    doc = Document(io.BytesIO(docx_bytes))
    paragraphs = []
    current_section = "Introduction"
    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            current_section = para.text.strip() or current_section
        text = para.text.strip()
        if text:
            paragraphs.append({"text": text, "section": current_section, "page": 0})
    return paragraphs

def ingest_docx(file_bytes: bytes) -> IngestionStatus:
    ensure_collection()
    paragraphs = _extract_paragraphs(file_bytes)
    all_chunks = []
    for para in paragraphs:
        for chunk in chunk_text(para["text"]):
            all_chunks.append({"text": chunk, "section": para["section"], "page": para["page"]})
    upsert_chunks(all_chunks)
    return IngestionStatus(
        chunks_written=len(all_chunks),
        collection="cortex_docs",
        status="ok",
    )
