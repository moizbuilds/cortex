import pytest
from unittest.mock import patch, MagicMock
from backend.ingestion import chunk_text

def test_chunk_text_produces_overlapping_chunks():
    text = " ".join([f"word{i}" for i in range(200)])
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    assert len(chunks) > 1
    # Overlap: last 10 tokens of chunk 0 appear in chunk 1
    last_of_first = chunks[0].split()[-10:]
    first_of_second = chunks[1].split()[:10]
    assert last_of_first == first_of_second

def test_chunk_text_short_text_returns_one_chunk():
    chunks = chunk_text("Hello world", chunk_size=50, overlap=10)
    assert len(chunks) == 1
    assert chunks[0] == "Hello world"
