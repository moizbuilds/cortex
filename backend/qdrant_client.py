import os
from qdrant_client import QdrantClient as _QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

COLLECTION = "cortex_docs"
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2

_client = None
_embedder = None

def _get_client() -> _QdrantClient:
    global _client
    if _client is None:
        QDRANT_URL = os.environ["QDRANT_URL"]
        _client = _QdrantClient(url=QDRANT_URL)
    return _client

def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

def ensure_collection():
    client = _get_client()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )

def upsert_chunks(chunks: list[dict]):
    """chunks: list of {text, section, page}"""
    client = _get_client()
    embedder = _get_embedder()
    vectors = embedder.encode([c["text"] for c in chunks]).tolist()
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={"text": c["text"], "section": c["section"], "page": c["page"]},
        )
        for c, vec in zip(chunks, vectors)
    ]
    client.upsert(collection_name=COLLECTION, points=points)

def search(query: str, top_k: int = 5) -> list[dict]:
    client = _get_client()
    embedder = _get_embedder()
    vec = embedder.encode([query])[0].tolist()
    hits = client.search(collection_name=COLLECTION, query_vector=vec, limit=top_k)
    return [
        {"text": h.payload["text"], "section": h.payload["section"], "page": h.payload["page"]}
        for h in hits
    ]
