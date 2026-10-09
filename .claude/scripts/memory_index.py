#!/usr/bin/env python3
"""
Incremental Memory Indexer — Walks vault markdown files, chunks them,
embeds with FastEmbed, and stores in SQLite for hybrid search.

Only re-indexes files whose content has changed (checksum comparison).

Usage:
    python3 .claude/scripts/memory_index.py              # Index all vault files
    python3 .claude/scripts/memory_index.py --force       # Force full re-index
    python3 .claude/scripts/memory_index.py --stats       # Show index statistics
"""

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import get_connection, init_db, insert_chunk, delete_file_chunks, get_file_checksum, set_file_checksum
from embeddings import embed_texts


# Priority weights for different vault directories
DIR_PRIORITY = {
    "projects": 3,
    "meetings": 3,
    "daily": 2,
    "team": 2,
    "research": 2,
    "drafts": 1,
    "goals": 1,
    "ideas": 1,
    "portfolio": 1,
}

# Target chunk size in characters (~400 tokens ≈ 1600 chars)
CHUNK_TARGET_CHARS = 1600
CHUNK_OVERLAP_CHARS = 200


def find_vault() -> Path:
    """Find the vault directory."""
    env_path = os.environ.get("SECOND_BRAIN_PATH", "")
    if env_path:
        vault = Path(env_path) / "vault"
        if vault.is_dir():
            return vault

    cwd = Path.cwd()
    for base in [cwd] + list(cwd.parents)[:5]:
        vault = base / "vault"
        if vault.is_dir() and (vault / "SOUL.md").exists():
            return vault

    fallback = Path.home() / "Documents" / "Personal" / "Second Brain Starter" / "vault"
    if fallback.is_dir():
        return fallback

    print("Error: Could not find vault directory", file=sys.stderr)
    sys.exit(1)


def compute_checksum(content: str) -> str:
    """Compute MD5 checksum of file content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def get_markdown_files(vault: Path) -> list[Path]:
    """Get all markdown files in the vault, sorted by priority."""
    files = list(vault.rglob("*.md"))
    # Exclude hidden dirs like .obsidian
    files = [f for f in files if not any(part.startswith(".") for part in f.relative_to(vault).parts)]
    return files


def chunk_markdown(content: str, file_path: str) -> list[str]:
    """
    Split markdown into chunks, respecting headers and paragraphs.

    Strategy:
    1. Split by ## headers first
    2. If a section is too long, split by paragraphs
    3. If a paragraph is too long, split by sentences with overlap
    """
    chunks = []

    # Split by level-2 headers
    sections = re.split(r'\n(?=##\s)', content)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        if len(section) <= CHUNK_TARGET_CHARS:
            chunks.append(section)
        else:
            # Split by paragraphs (double newline)
            paragraphs = re.split(r'\n\n+', section)
            current_chunk = ""

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                if len(current_chunk) + len(para) + 2 <= CHUNK_TARGET_CHARS:
                    current_chunk = f"{current_chunk}\n\n{para}" if current_chunk else para
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    if len(para) <= CHUNK_TARGET_CHARS:
                        current_chunk = para
                    else:
                        # Split long paragraph by sentences
                        sentences = re.split(r'(?<=[.!?])\s+', para)
                        current_chunk = ""
                        for sentence in sentences:
                            if len(current_chunk) + len(sentence) + 1 <= CHUNK_TARGET_CHARS:
                                current_chunk = f"{current_chunk} {sentence}" if current_chunk else sentence
                            else:
                                if current_chunk:
                                    chunks.append(current_chunk)
                                current_chunk = sentence
                        # Don't forget the last chunk from sentences

            if current_chunk:
                chunks.append(current_chunk)

    # Add file path context as prefix to each chunk
    rel_path = file_path
    return [f"[{rel_path}]\n{chunk}" for chunk in chunks if chunk.strip()]


def index_vault(vault: Path, force: bool = False):
    """Index all vault markdown files incrementally."""
    conn = get_connection()
    init_db(conn)

    files = get_markdown_files(vault)
    print(f"Found {len(files)} markdown files in vault")

    indexed = 0
    skipped = 0
    total_chunks = 0

    for file_path in files:
        rel_path = str(file_path.relative_to(vault))
        content = file_path.read_text(encoding="utf-8")
        checksum = compute_checksum(content)

        # Check if file has changed
        if not force:
            stored_checksum = get_file_checksum(conn, rel_path)
            if stored_checksum == checksum:
                skipped += 1
                continue

        # File changed or new — re-index
        print(f"  Indexing: {rel_path}")
        delete_file_chunks(conn, rel_path)

        chunks = chunk_markdown(content, rel_path)
        if not chunks:
            set_file_checksum(conn, rel_path, checksum)
            conn.commit()
            continue

        # Batch embed all chunks for this file
        embeddings = embed_texts(chunks)

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_checksum = compute_checksum(chunk)
            insert_chunk(conn, rel_path, i, chunk, chunk_checksum, embedding)

        set_file_checksum(conn, rel_path, checksum)
        conn.commit()

        indexed += 1
        total_chunks += len(chunks)

    print(f"\nDone: {indexed} files indexed ({total_chunks} chunks), {skipped} unchanged")
    conn.close()


def show_stats():
    """Show index statistics."""
    conn = get_connection()
    init_db(conn)

    total_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    total_files = conn.execute("SELECT COUNT(DISTINCT file_path) FROM chunks").fetchone()[0]
    tracked_files = conn.execute("SELECT COUNT(*) FROM file_checksums").fetchone()[0]

    print(f"Index Statistics:")
    print(f"  Tracked files: {tracked_files}")
    print(f"  Indexed files: {total_files}")
    print(f"  Total chunks:  {total_chunks}")

    # Top files by chunk count
    rows = conn.execute(
        "SELECT file_path, COUNT(*) as cnt FROM chunks GROUP BY file_path ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    if rows:
        print(f"\nTop files by chunk count:")
        for path, count in rows:
            print(f"  {path}: {count} chunks")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Index vault markdown files for memory search")
    parser.add_argument("--force", action="store_true", help="Force full re-index")
    parser.add_argument("--stats", action="store_true", help="Show index statistics")
    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    vault = find_vault()
    print(f"Vault: {vault}")
    index_vault(vault, force=args.force)


if __name__ == "__main__":
    main()
