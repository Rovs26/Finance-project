"""Text cleaning and chunking utilities."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


def clean_text(text):
    """Normalize whitespace in document text."""
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text


def chunk_text(text, chunk_size=600, overlap=100):
    """Split text into overlapping character chunks."""
    cleaned = clean_text(text)
    if not cleaned:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size.")

    chunks = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = end - overlap
    return chunks


def build_chunk_table(corpus):
    """Build a chunk-level table from a loaded document corpus."""
    rows = []
    for document in corpus:
        chunks = chunk_text(document["text"])
        for chunk_index, chunk in enumerate(chunks, start=1):
            rows.append(
                {
                    "chunk_id": f"{document['document_id']}__chunk_{chunk_index:03d}",
                    "document_id": document["document_id"],
                    "file_name": document["file_name"],
                    "title": document["title"],
                    "chunk_index": chunk_index,
                    "chunk_text": chunk,
                    "character_count": len(chunk),
                    "word_count": len(chunk.split()),
                }
            )
    return pd.DataFrame(rows)


def save_chunks(chunks, path):
    """Save chunk table to CSV."""
    path = Path(path)
    chunks.to_csv(path, index=False)
    return chunks
