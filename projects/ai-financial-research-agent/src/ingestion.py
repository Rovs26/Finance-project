"""Document ingestion utilities for local text files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def list_text_documents(directory):
    """List text documents in a directory."""
    return sorted(Path(directory).glob("*.txt"))


def load_text_document(path):
    """Load one text document and return a metadata dictionary."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    title = path.stem.replace("_", " ").title()
    for line in text.splitlines():
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
            break
    return {
        "document_id": path.stem,
        "file_name": path.name,
        "title": title,
        "path": str(path),
        "text": text,
        "character_count": len(text),
        "word_count": len(text.split()),
    }


def load_document_corpus(directory):
    """Load all local text documents into a corpus list."""
    return [load_text_document(path) for path in list_text_documents(directory)]


def save_corpus_metadata(corpus, path):
    """Save document-level corpus metadata without full text."""
    metadata = [
        {key: value for key, value in document.items() if key != "text"}
        for document in corpus
    ]
    df = pd.DataFrame(metadata)
    df.to_csv(path, index=False)
    return df
