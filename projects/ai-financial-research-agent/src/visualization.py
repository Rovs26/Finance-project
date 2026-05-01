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


def plot_risk_flags_by_category(risk_flags):
    """Plot risk flag counts by category."""
    summary = (
        risk_flags.groupby("risk_category", as_index=False)
        .size()
        .rename(columns={"size": "flag_count"})
        .sort_values("flag_count", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(summary["risk_category"], summary["flag_count"], color="#dc2626")
    _style_axis(ax, "Risk Flags by Category", "Flag count")
    fig.tight_layout()
    return fig


def plot_evidence_count_by_question(coverage):
    """Plot retrieved evidence counts by research question."""
    summary = coverage.sort_values("evidence_count", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(summary["question"], summary["evidence_count"], color="#2563eb")
    _style_axis(ax, "Evidence Count by Research Question", "Evidence count")
    fig.tight_layout()
    return fig


def plot_source_traceability_status(traceability):
    """Plot source traceability pass/review counts."""
    summary = (
        traceability.assign(status=traceability["is_traceable"].map({True: "traceable", False: "review"}))
        .groupby("status", as_index=False)
        .size()
        .rename(columns={"size": "row_count"})
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(summary["status"], summary["row_count"], color="#059669")
    _style_axis(ax, "Source Traceability Status", "Status", "Evidence rows")
    fig.tight_layout()
    return fig


def plot_grounding_check_summary(grounding):
    """Plot memo section grounding pass/review counts."""
    summary = (
        grounding.assign(status=grounding["grounded"].map({True: "grounded", False: "review"}))
        .groupby("status", as_index=False)
        .size()
        .rename(columns={"size": "section_count"})
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(summary["status"], summary["section_count"], color="#7c3aed")
    _style_axis(ax, "Grounding Check Summary", "Status", "Memo sections")
    fig.tight_layout()
    return fig
