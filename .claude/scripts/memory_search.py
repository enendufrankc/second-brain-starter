#!/usr/bin/env python3
"""
Hybrid Memory Search — Combines vector similarity and keyword search
across the indexed vault.

Usage:
    python3 .claude/scripts/memory_search.py "query text"
    python3 .claude/scripts/memory_search.py "query" --top-k 5
    python3 .claude/scripts/memory_search.py "query" --path-prefix drafts/sent
    python3 .claude/scripts/memory_search.py "query" --mode vector
    python3 .claude/scripts/memory_search.py "query" --mode keyword
    python3 .claude/scripts/memory_search.py "query" --mode hybrid   (default)
"""

import argparse
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import get_connection, init_db, vector_search, keyword_search
from embeddings import embed_query

# Hybrid scoring weights
VECTOR_WEIGHT = 0.7
KEYWORD_WEIGHT = 0.3


def normalize_scores(results: list[dict], score_key: str, invert: bool = False) -> list[dict]:
    """Normalize scores to 0-1 range."""
    if not results:
        return results

    scores = [r[score_key] for r in results]
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score

    for r in results:
        if score_range == 0:
            r["normalized_score"] = 1.0
        else:
            normalized = (r[score_key] - min_score) / score_range
            r["normalized_score"] = (1.0 - normalized) if invert else normalized

    return results


def hybrid_search(query: str, top_k: int = 10, path_prefix: str = "") -> list[dict]:
    """
    Perform hybrid search: vector similarity + keyword matching.
    Returns ranked results with combined scores.
    """
    conn = get_connection()
    init_db(conn)

    # Get vector results
    query_vec = embed_query(query)
    vec_results = vector_search(conn, query_vec, top_k=top_k * 2, path_prefix=path_prefix)
    vec_results = normalize_scores(vec_results, "distance", invert=True)

    # Get keyword results
    # Escape FTS5 special characters
    fts_query = " OR ".join(
        word for word in query.split()
        if len(word) > 2 and word.isalnum()
    )
    if fts_query:
        kw_results = keyword_search(conn, fts_query, top_k=top_k * 2, path_prefix=path_prefix)
        kw_results = normalize_scores(kw_results, "rank", invert=True)
    else:
        kw_results = []

    conn.close()

    # Merge results by chunk ID
    merged = {}

    for r in vec_results:
        rid = r["id"]
        merged[rid] = {
            "id": rid,
            "content": r["content"],
            "file_path": r["file_path"],
            "vec_score": r["normalized_score"],
            "kw_score": 0.0,
        }

    for r in kw_results:
        rid = r["id"]
        if rid in merged:
            merged[rid]["kw_score"] = r["normalized_score"]
        else:
            merged[rid] = {
                "id": rid,
                "content": r["content"],
                "file_path": r["file_path"],
                "vec_score": 0.0,
                "kw_score": r["normalized_score"],
            }

    # Compute combined score
    for r in merged.values():
        r["score"] = VECTOR_WEIGHT * r["vec_score"] + KEYWORD_WEIGHT * r["kw_score"]

    # Sort by combined score descending
    ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]


def vector_only_search(query: str, top_k: int = 10, path_prefix: str = "") -> list[dict]:
    """Vector-only search."""
    conn = get_connection()
    init_db(conn)
    query_vec = embed_query(query)
    results = vector_search(conn, query_vec, top_k=top_k, path_prefix=path_prefix)
    conn.close()
    return results


def keyword_only_search(query: str, top_k: int = 10, path_prefix: str = "") -> list[dict]:
    """Keyword-only search."""
    conn = get_connection()
    init_db(conn)
    fts_query = " OR ".join(
        word for word in query.split()
        if len(word) > 2 and word.isalnum()
    )
    if not fts_query:
        conn.close()
        return []
    results = keyword_search(conn, fts_query, top_k=top_k, path_prefix=path_prefix)
    conn.close()
    return results


def format_result(result: dict, index: int) -> str:
    """Format a single search result for display."""
    score = result.get("score", result.get("distance", result.get("rank", "?")))
    file_path = result.get("file_path", "unknown")
    content = result.get("content", "").strip()

    # Truncate content for display
    if len(content) > 300:
        content = content[:300] + "..."

    return f"""--- Result {index + 1} [{file_path}] (score: {score:.3f}) ---
{content}"""


def main():
    parser = argparse.ArgumentParser(description="Search vault memory")
    parser.add_argument("query", help="Search query text")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--path-prefix", default="", help="Filter by file path prefix (e.g., 'projects/', 'drafts/sent')")
    parser.add_argument("--mode", choices=["hybrid", "vector", "keyword"], default="hybrid", help="Search mode")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.mode == "hybrid":
        results = hybrid_search(args.query, top_k=args.top_k, path_prefix=args.path_prefix)
    elif args.mode == "vector":
        results = vector_only_search(args.query, top_k=args.top_k, path_prefix=args.path_prefix)
    else:
        results = keyword_only_search(args.query, top_k=args.top_k, path_prefix=args.path_prefix)

    if args.json:
        import json
        # Strip large content for JSON output
        for r in results:
            if len(r.get("content", "")) > 500:
                r["content"] = r["content"][:500] + "..."
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print(f"No results found for: {args.query}")
            return

        print(f"Search: \"{args.query}\" ({args.mode} mode, top {args.top_k})")
        if args.path_prefix:
            print(f"Filter: {args.path_prefix}*")
        print()

        for i, result in enumerate(results):
            print(format_result(result, i))
            print()


if __name__ == "__main__":
    main()
