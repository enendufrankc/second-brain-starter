#!/usr/bin/env python3
"""FastEmbed wrapper for generating text embeddings."""

from fastembed import TextEmbedding

# Singleton model instance — loaded once, reused
_model = None

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


def get_model() -> TextEmbedding:
    """Load the embedding model (cached after first call)."""
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of text chunks. Returns list of 384-dim float vectors."""
    model = get_model()
    return [vec.tolist() for vec in model.embed(texts)]


def embed_query(query: str) -> list[float]:
    """Embed a single query string. Returns a 384-dim float vector."""
    model = get_model()
    return list(next(model.embed([query])).tolist())
