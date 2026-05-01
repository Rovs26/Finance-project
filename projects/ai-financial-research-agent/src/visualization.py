"""Visualization helpers for document ingestion and retrieval outputs."""

from __future__ import annotations

from collections import Counter
import re

import matplotlib.pyplot as plt
import pandas as pd


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "are",
    "can",
    "not",
    "but",
    "into",
    "when",
    "may",
    "should",
    "portfolio",
    "prototype",
    "sample",
    "document",
}


def _style_axis(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(axis="x", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    return ax


def plot_chunks_by_document(chunks):
    """Plot number of chunks per document."""
    summary = (
        chunks.groupby("title", as_index=False)["chunk_id"]
        .count()
        .rename(columns={"chunk_id": "chunk_count"})
        .sort_values("chunk_count", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(summary["title"], summary["chunk_count"], color="#2563eb")
    _style_axis(ax, "Chunks by Document", "Chunk count")
    fig.tight_layout()
    return fig


def plot_top_terms_overall(chunks, top_n=15):
    """Plot most frequent non-stopword terms across chunks."""
    text = " ".join(chunks["chunk_text"].fillna("").tolist()).lower()
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_]+", text)
    counts = Counter(token for token in tokens if token not in STOPWORDS and len(token) > 2)
    summary = pd.DataFrame(counts.most_common(top_n), columns=["term", "count"])
    summary = summary.sort_values("count", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(summary["term"], summary["count"], color="#059669")
    _style_axis(ax, "Top Terms Across Sample Documents", "Term count")
    fig.tight_layout()
    return fig


def plot_retrieval_score_distribution(results):
    """Plot retrieval score distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(results["retrieval_score"], bins=12, color="#7c3aed", edgecolor="white")
    _style_axis(ax, "Retrieval Score Distribution", "Retrieval score", "Result count")
    fig.tight_layout()
    return fig
