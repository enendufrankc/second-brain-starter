# Phase 3: Memory Search (Hybrid RAG) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local hybrid search pipeline (vector + keyword) so the agent can find relevant past context across all vault files — meeting notes, project decisions, research, team info.

**Architecture:** Markdown files are chunked (~400 tokens), embedded with FastEmbed (all-MiniLM-L6-v2, 384-dim ONNX), and stored in SQLite with sqlite-vec for vector search and FTS5 for keyword search. Hybrid scoring: 0.7 vector + 0.3 keyword. Incremental indexing via checksum comparison.

**Tech Stack:** Python 3, FastEmbed, SQLite + sqlite-vec + FTS5, argparse

---

## File Structure

| File | Responsibility |
|------|---------------|
| `.claude/scripts/embeddings.py` | FastEmbed wrapper — load model, embed text chunks |
| `.claude/scripts/db.py` | SQLite database abstraction — create tables, insert/query vectors and FTS |
| `.claude/scripts/memory_index.py` | Incremental indexer — walk vault, chunk markdown, embed, store |
| `.claude/scripts/memory_search.py` | Hybrid search CLI — `memory_search.py "query" [--path-prefix X] [--top-k N]` |
| `requirements.txt` | Python dependencies for the project |

---

### Task 1: Install dependencies and create requirements.txt

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: Create requirements.txt**

Create `requirements.txt`:

```
fastembed>=0.3.0
sqlite-vec>=0.1.0
```

- [ ] **Step 2: Install dependencies**

```bash
pip3 install fastembed sqlite-vec
```

- [ ] **Step 3: Verify imports work**

```bash
python3 -c "from fastembed import TextEmbedding; print('fastembed OK')"
python3 -c "import sqlite_vec; print('sqlite-vec OK')"
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "feat: add requirements.txt with fastembed and sqlite-vec"
```

---

### Task 2: Create embeddings.py (FastEmbed wrapper)

**Files:**
- Create: `.claude/scripts/embeddings.py`

- [ ] **Step 1: Create the scripts directory**

```bash
mkdir -p .claude/scripts
```

- [ ] **Step 2: Write embeddings.py**

Create `.claude/scripts/embeddings.py`:

```python
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
```

- [ ] **Step 3: Test embeddings**

```bash
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, str(Path('.claude/scripts')))
from embeddings import embed_texts, embed_query, EMBEDDING_DIM
vecs = embed_texts(['hello world', 'test chunk'])
print(f'Embedded 2 chunks, dim={len(vecs[0])}')
assert len(vecs) == 2
assert len(vecs[0]) == EMBEDDING_DIM
q = embed_query('search query')
assert len(q) == EMBEDDING_DIM
print('All embedding tests passed')
"
```

- [ ] **Step 4: Commit**

```bash
git add .claude/scripts/embeddings.py
git commit -m "feat: add FastEmbed wrapper for text embeddings (384-dim MiniLM)"
```

---

### Task 3: Create db.py (SQLite database abstraction)

**Files:**
- Create: `.claude/scripts/db.py`

- [ ] **Step 1: Write db.py**

Create `.claude/scripts/db.py`:

```python
#!/usr/bin/env python3
"""SQLite database abstraction with sqlite-vec for vectors and FTS5 for keywords."""

import json
import sqlite3
import struct
from pathlib import Path

import sqlite_vec


DB_PATH = Path(".claude/data/memory.db")
EMBEDDING_DIM = 384


def _serialize_vector(vec: list[float]) -> bytes:
    """Serialize a float vector to bytes for sqlite-vec."""
    return struct.pack(f"{len(vec)}f", *vec)


def get_connection() -> sqlite3.Connection:
    """Get a database connection with sqlite-vec loaded."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def init_db(conn: sqlite3.Connection):
    """Create tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            checksum TEXT NOT NULL,
            UNIQUE(file_path, chunk_index)
        );

        CREATE TABLE IF NOT EXISTS file_checksums (
            file_path TEXT PRIMARY KEY,
            checksum TEXT NOT NULL
        );
    """)

    # Create FTS5 virtual table for keyword search
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
        USING fts5(content, file_path, content_rowid='id');
    """)

    # Create sqlite-vec virtual table for vector search
    conn.execute(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_vec
        USING vec0(embedding float[{EMBEDDING_DIM}]);
    """)

    conn.commit()


def insert_chunk(
    conn: sqlite3.Connection,
    file_path: str,
    chunk_index: int,
    content: str,
    checksum: str,
    embedding: list[float],
):
    """Insert a chunk with its embedding and FTS entry."""
    cursor = conn.execute(
        "INSERT OR REPLACE INTO chunks (file_path, chunk_index, content, checksum) VALUES (?, ?, ?, ?)",
        (file_path, chunk_index, content, checksum),
    )
    row_id = cursor.lastrowid

    # Insert into FTS
    conn.execute(
        "INSERT OR REPLACE INTO chunks_fts (rowid, content, file_path) VALUES (?, ?, ?)",
        (row_id, content, file_path),
    )

    # Insert into vector table
    conn.execute(
        "INSERT OR REPLACE INTO chunks_vec (rowid, embedding) VALUES (?, ?)",
        (row_id, _serialize_vector(embedding)),
    )


def delete_file_chunks(conn: sqlite3.Connection, file_path: str):
    """Delete all chunks for a file (before re-indexing)."""
    rows = conn.execute(
        "SELECT id FROM chunks WHERE file_path = ?", (file_path,)
    ).fetchall()
    for (row_id,) in rows:
        conn.execute("DELETE FROM chunks_fts WHERE rowid = ?", (row_id,))
        conn.execute("DELETE FROM chunks_vec WHERE rowid = ?", (row_id,))
    conn.execute("DELETE FROM chunks WHERE file_path = ?", (file_path,))


def get_file_checksum(conn: sqlite3.Connection, file_path: str) -> str | None:
    """Get stored checksum for a file."""
    row = conn.execute(
        "SELECT checksum FROM file_checksums WHERE file_path = ?", (file_path,)
    ).fetchone()
    return row[0] if row else None


def set_file_checksum(conn: sqlite3.Connection, file_path: str, checksum: str):
    """Store the checksum for a file."""
    conn.execute(
        "INSERT OR REPLACE INTO file_checksums (file_path, checksum) VALUES (?, ?)",
        (file_path, checksum),
    )


def vector_search(
    conn: sqlite3.Connection, query_vec: list[float], top_k: int = 10, path_prefix: str = ""
) -> list[dict]:
    """Search by vector similarity. Returns list of {id, distance, content, file_path}."""
    if path_prefix:
        rows = conn.execute(
            """
            SELECT v.rowid, v.distance, c.content, c.file_path
            FROM chunks_vec v
            JOIN chunks c ON c.id = v.rowid
            WHERE v.embedding MATCH ? AND k = ?
              AND c.file_path LIKE ?
            ORDER BY v.distance
            """,
            (_serialize_vector(query_vec), top_k * 3, f"{path_prefix}%"),
        ).fetchall()[:top_k]
    else:
        rows = conn.execute(
            """
            SELECT v.rowid, v.distance, c.content, c.file_path
            FROM chunks_vec v
            JOIN chunks c ON c.id = v.rowid
            WHERE v.embedding MATCH ? AND k = ?
            ORDER BY v.distance
            """,
            (_serialize_vector(query_vec), top_k),
        ).fetchall()

    return [
        {"id": r[0], "distance": r[1], "content": r[2], "file_path": r[3]}
        for r in rows
    ]


def keyword_search(
    conn: sqlite3.Connection, query: str, top_k: int = 10, path_prefix: str = ""
) -> list[dict]:
    """Search by FTS5 keyword match. Returns list of {id, rank, content, file_path}."""
    if path_prefix:
        rows = conn.execute(
            """
            SELECT f.rowid, rank, c.content, c.file_path
            FROM chunks_fts f
            JOIN chunks c ON c.id = f.rowid
            WHERE chunks_fts MATCH ?
              AND c.file_path LIKE ?
            ORDER BY rank
            LIMIT ?
            """,
            (query, f"{path_prefix}%", top_k),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT f.rowid, rank, c.content, c.file_path
            FROM chunks_fts f
            JOIN chunks c ON c.id = f.rowid
            WHERE chunks_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (query, top_k),
        ).fetchall()

    return [
        {"id": r[0], "rank": r[1], "content": r[2], "file_path": r[3]}
        for r in rows
    ]
```

- [ ] **Step 2: Test db module**

```bash
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.claude/scripts')))
from db import get_connection, init_db, insert_chunk, vector_search, keyword_search, _serialize_vector

conn = get_connection()
init_db(conn)

# Insert a test chunk
test_vec = [0.1] * 384
insert_chunk(conn, 'test/file.md', 0, 'hello world test content', 'abc123', test_vec)
conn.commit()

# Vector search
results = vector_search(conn, test_vec, top_k=1)
print(f'Vector search returned {len(results)} results')
assert len(results) >= 1

# Keyword search
results = keyword_search(conn, 'hello world', top_k=1)
print(f'Keyword search returned {len(results)} results')
assert len(results) >= 1

# Cleanup test db
conn.close()
import os
os.remove('.claude/data/memory.db')
print('All db tests passed')
"
```

- [ ] **Step 3: Commit**

```bash
git add .claude/scripts/db.py
git commit -m "feat: add SQLite database abstraction with sqlite-vec and FTS5"
```

---

### Task 4: Create memory_index.py (Incremental indexer)

**Files:**
- Create: `.claude/scripts/memory_index.py`

- [ ] **Step 1: Write memory_index.py**

Create `.claude/scripts/memory_index.py`:

```python
#!/usr/bin/env python3
"""Incremental indexer: walks vault markdown files, chunks, embeds, stores in SQLite."""

import hashlib
import re
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import (
    get_connection,
    init_db,
    insert_chunk,
    delete_file_chunks,
    get_file_checksum,
    set_file_checksum,
)
from embeddings import embed_texts


VAULT_DIR = Path("vault")
CHUNK_TARGET = 400  # target tokens per chunk (approx 4 chars per token)
CHUNK_OVERLAP = 50  # overlap tokens


def compute_checksum(content: str) -> str:
    """Compute MD5 checksum of file content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def chunk_markdown(content: str, target_chars: int = 1600, overlap_chars: int = 200) -> list[str]:
    """Split markdown into chunks, first by headers, then by paragraph.

    Target ~400 tokens ≈ 1600 chars. Overlap ~50 tokens ≈ 200 chars.
    """
    # Split by markdown headers (## or ###)
    sections = re.split(r"(?=^#{1,3}\s)", content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    chunks = []
    for section in sections:
        if len(section) <= target_chars:
            chunks.append(section)
        else:
            # Split long sections by double newline (paragraph)
            paragraphs = section.split("\n\n")
            current = ""
            for para in paragraphs:
                if len(current) + len(para) + 2 <= target_chars:
                    current = current + "\n\n" + para if current else para
                else:
                    if current:
                        chunks.append(current)
                    current = para
            if current:
                chunks.append(current)

    # Add overlap between chunks
    if len(chunks) > 1 and overlap_chars > 0:
        overlapped = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_tail = chunks[i - 1][-overlap_chars:]
            overlapped.append(prev_tail + "\n\n" + chunks[i])
        chunks = overlapped

    return chunks if chunks else [content]


def get_vault_files(vault_dir: Path) -> list[Path]:
    """Get all markdown files in the vault, excluding .gitkeep."""
    return sorted(
        f for f in vault_dir.rglob("*.md")
        if f.name != ".gitkeep"
    )


def index_vault(vault_dir: Path = VAULT_DIR, verbose: bool = False):
    """Index all vault markdown files incrementally."""
    conn = get_connection()
    init_db(conn)

    files = get_vault_files(vault_dir)
    indexed = 0
    skipped = 0

    for file_path in files:
        rel_path = str(file_path.relative_to(vault_dir.parent))
        content = file_path.read_text(encoding="utf-8")
        checksum = compute_checksum(content)

        stored_checksum = get_file_checksum(conn, rel_path)
        if stored_checksum == checksum:
            skipped += 1
            if verbose:
                print(f"  SKIP (unchanged): {rel_path}")
            continue

        # File changed or new — re-index
        delete_file_chunks(conn, rel_path)

        chunks = chunk_markdown(content)
        if not chunks:
            continue

        embeddings = embed_texts(chunks)

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            insert_chunk(conn, rel_path, i, chunk, checksum, embedding)

        set_file_checksum(conn, rel_path, checksum)
        indexed += 1
        if verbose:
            print(f"  INDEX ({len(chunks)} chunks): {rel_path}")

    conn.commit()
    conn.close()

    print(f"Indexing complete: {indexed} files indexed, {skipped} unchanged")


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else VAULT_DIR
    index_vault(vault, verbose=verbose)
```

- [ ] **Step 2: Run the indexer on the vault**

```bash
python3 .claude/scripts/memory_index.py --verbose
```

Expected: Should index all vault markdown files (SOUL.md, USER.md, MEMORY.md, etc.)

- [ ] **Step 3: Verify the database was created**

```bash
python3 -c "
import sqlite3
from pathlib import Path
import sys
sys.path.insert(0, str(Path('.claude/scripts')))
import sqlite_vec

conn = sqlite3.connect('.claude/data/memory.db')
conn.enable_load_extension(True)
sqlite_vec.load(conn)
conn.enable_load_extension(False)

count = conn.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]
files = conn.execute('SELECT COUNT(*) FROM file_checksums').fetchone()[0]
print(f'Chunks: {count}, Files indexed: {files}')
conn.close()
"
```

Expected: Multiple chunks and files indexed.

- [ ] **Step 4: Commit**

```bash
git add .claude/scripts/memory_index.py
git commit -m "feat: add incremental memory indexer with markdown chunking"
```

---

### Task 5: Create memory_search.py (Hybrid search CLI)

**Files:**
- Create: `.claude/scripts/memory_search.py`

- [ ] **Step 1: Write memory_search.py**

Create `.claude/scripts/memory_search.py`:

```python
#!/usr/bin/env python3
"""Hybrid search CLI: combines vector similarity (0.7) + keyword matching (0.3)."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db import get_connection, init_db, vector_search, keyword_search
from embeddings import embed_query


def hybrid_search(
    query: str, top_k: int = 5, path_prefix: str = ""
) -> list[dict]:
    """Run hybrid search: 0.7 * vector_score + 0.3 * keyword_score."""
    conn = get_connection()
    init_db(conn)

    # Get vector results
    query_vec = embed_query(query)
    vec_results = vector_search(conn, query_vec, top_k=top_k * 2, path_prefix=path_prefix)

    # Get keyword results
    kw_results = keyword_search(conn, query, top_k=top_k * 2, path_prefix=path_prefix)

    conn.close()

    # Normalize vector distances to scores (lower distance = higher score)
    if vec_results:
        max_dist = max(r["distance"] for r in vec_results) or 1.0
        for r in vec_results:
            r["vec_score"] = 1.0 - (r["distance"] / (max_dist + 0.001))
    else:
        vec_results = []

    # Normalize keyword ranks to scores (more negative rank = better match in FTS5)
    if kw_results:
        min_rank = min(r["rank"] for r in kw_results) or -1.0
        for r in kw_results:
            r["kw_score"] = r["rank"] / (min_rank - 0.001) if min_rank < 0 else 0.0
    else:
        kw_results = []

    # Merge results by chunk ID
    merged = {}
    for r in vec_results:
        merged[r["id"]] = {
            "id": r["id"],
            "content": r["content"],
            "file_path": r["file_path"],
            "vec_score": r["vec_score"],
            "kw_score": 0.0,
        }

    for r in kw_results:
        if r["id"] in merged:
            merged[r["id"]]["kw_score"] = r["kw_score"]
        else:
            merged[r["id"]] = {
                "id": r["id"],
                "content": r["content"],
                "file_path": r["file_path"],
                "vec_score": 0.0,
                "kw_score": r["kw_score"],
            }

    # Compute hybrid score
    for item in merged.values():
        item["score"] = 0.7 * item["vec_score"] + 0.3 * item["kw_score"]

    # Sort by hybrid score descending
    ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)

    return ranked[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Search vault memory (hybrid RAG)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--path-prefix", default="", help="Filter by file path prefix (e.g., 'vault/drafts/sent')")
    args = parser.parse_args()

    results = hybrid_search(args.query, top_k=args.top_k, path_prefix=args.path_prefix)

    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} (score: {r['score']:.3f}) ---")
        print(f"File: {r['file_path']}")
        print(f"Content:\n{r['content'][:500]}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test hybrid search**

```bash
python3 .claude/scripts/memory_search.py "hackathon management platform"
```

Expected: Results showing hackathon-platform related chunks ranked by relevance.

- [ ] **Step 3: Test with path-prefix filter**

```bash
python3 .claude/scripts/memory_search.py "project status" --path-prefix vault/projects
```

Expected: Only results from `vault/projects/` directory.

- [ ] **Step 4: Make both scripts executable**

```bash
chmod +x .claude/scripts/memory_index.py .claude/scripts/memory_search.py
```

- [ ] **Step 5: Commit**

```bash
git add .claude/scripts/memory_search.py
git commit -m "feat: add hybrid search CLI (0.7 vector + 0.3 keyword)"
```

---
