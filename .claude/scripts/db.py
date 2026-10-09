#!/usr/bin/env python3
"""SQLite database abstraction with sqlite-vec for vectors and FTS5 for keywords."""

import sqlite3
import struct
from pathlib import Path

import sqlite_vec


def _get_db_path() -> Path:
    """Get the database path. Tries project dir, falls back to home dir if filesystem doesn't support SQLite."""
    import os

    # Allow override via env var
    env_db = os.environ.get("SECOND_BRAIN_DB")
    if env_db:
        p = Path(env_db)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    # Try project-local path first
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    db_path = project_root / ".claude" / "data" / "memory.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Test if the filesystem supports SQLite
    try:
        import sqlite3 as _sqlite3
        test_conn = _sqlite3.connect(str(db_path))
        test_conn.execute("CREATE TABLE IF NOT EXISTS _test (id INTEGER)")
        test_conn.close()
        return db_path
    except Exception:
        pass

    # Fallback to home directory
    fallback = Path.home() / ".second-brain" / "memory.db"
    fallback.parent.mkdir(parents=True, exist_ok=True)
    return fallback

DB_PATH = _get_db_path()
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
