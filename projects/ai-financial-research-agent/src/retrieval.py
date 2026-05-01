"""TF-IDF retrieval utilities for document chunks."""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd


class SimpleTfidfVectorizer:
    """Small TF-IDF fallback with a sklearn-like transform interface."""

    def __init__(self):
        self.vocabulary_ = {}
        self.idf_ = np.array([])

    def _tokenize(self, text):
        return re.findall(r"[a-zA-Z][a-zA-Z0-9_]+", str(text).lower())

    def fit_transform(self, texts):
        tokenized = [self._tokenize(text) for text in texts]
        vocabulary = sorted({token for tokens in tokenized for token in tokens})
        self.vocabulary_ = {token: idx for idx, token in enumerate(vocabulary)}
        doc_count = len(tokenized)
        df_counts = Counter()
        for tokens in tokenized:
            df_counts.update(set(tokens))
        self.idf_ = np.array(
            [
                math.log((1 + doc_count) / (1 + df_counts[token])) + 1
                for token in vocabulary
            ]
        )
        return self._transform_tokenized(tokenized)

    def transform(self, texts):
        tokenized = [self._tokenize(text) for text in texts]
        return self._transform_tokenized(tokenized)

    def get_feature_names_out(self):
        return np.array(list(self.vocabulary_.keys()))

    def _transform_tokenized(self, tokenized):
        matrix = np.zeros((len(tokenized), len(self.vocabulary_)))
        for row_idx, tokens in enumerate(tokenized):
            if not tokens:
                continue
            counts = Counter(tokens)
            max_count = max(counts.values())
            for token, count in counts.items():
                col_idx = self.vocabulary_.get(token)
                if col_idx is not None:
                    matrix[row_idx, col_idx] = (count / max_count) * self.idf_[col_idx]
        norms = np.linalg.norm(matrix, axis=1)
        norms[norms == 0] = 1
        return matrix / norms[:, None]


def build_tfidf_index(chunks):
    """Build a TF-IDF index over chunk text."""
    texts = chunks["chunk_text"].fillna("").tolist()
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(texts)
    except Exception:
        vectorizer = SimpleTfidfVectorizer()
        matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix


def _cosine_scores(query_vector, matrix):
    """Calculate cosine-style scores for sparse or dense TF-IDF matrices."""
    if hasattr(matrix, "dot"):
        scores = matrix.dot(query_vector.T)
        if hasattr(scores, "toarray"):
            return scores.toarray().ravel()
        return np.asarray(scores).ravel()
    return np.asarray(matrix @ query_vector.T).ravel()


def search_chunks(query, vectorizer, matrix, chunks, top_k=5):
    """Search chunks for a query and return top ranked evidence rows."""
    query_vector = vectorizer.transform([query])
    scores = _cosine_scores(query_vector, matrix)
    ranked_indices = np.argsort(scores)[::-1][:top_k]
    rows = []
    for rank, idx in enumerate(ranked_indices, start=1):
        row = chunks.iloc[int(idx)].to_dict()
        row.update(
            {
                "query": query,
                "rank": rank,
                "retrieval_score": float(scores[int(idx)]),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def build_evidence_table(query_results):
    """Build a compact evidence table from retrieval results."""
    evidence = query_results.copy()
    evidence["evidence_snippet"] = evidence["chunk_text"].str.slice(0, 280)
    return evidence[
        [
            "query",
            "rank",
            "retrieval_score",
            "document_id",
            "title",
            "chunk_id",
            "evidence_snippet",
        ]
    ]


def save_retrieval_results(results, path):
    """Save retrieval results to CSV."""
    path = Path(path)
    results.to_csv(path, index=False)
    return results


def retrieve_evidence_for_questions(chunks, questions, top_k=5):
    """Retrieve top evidence chunks for a list of research questions."""
    vectorizer, matrix = build_tfidf_index(chunks)
    results = []
    for question in questions:
        question_results = search_chunks(question, vectorizer, matrix, chunks, top_k=top_k)
        results.append(question_results)
    if not results:
        return pd.DataFrame()
    return pd.concat(results, ignore_index=True)


def format_citation(chunk_id, document_id, document_title):
    """Create a compact citation label for a retrieved document chunk."""
    chunk_text = str(chunk_id)
    chunk_number = "000"
    if "_chunk_" in chunk_text:
        chunk_number = chunk_text.rsplit("_chunk_", 1)[1]
    elif "__chunk_" in chunk_text:
        chunk_number = chunk_text.rsplit("__chunk_", 1)[1]

    document_text = str(document_id)
    words = [word for word in re.split(r"[^a-zA-Z0-9]+", document_text) if word]
    if words:
        prefix = "".join(word[:3].upper() for word in words[:2])
    else:
        title_words = [word for word in re.split(r"[^a-zA-Z0-9]+", str(document_title)) if word]
        prefix = "".join(word[:3].upper() for word in title_words[:2]) or "DOC"
    return f"[{prefix}-CHUNK{int(chunk_number):03d}]"


def create_cited_evidence_table(retrieval_results):
    """Create evidence rows with citation labels and readable snippets."""
    evidence = retrieval_results.copy()
    if evidence.empty:
        return evidence
    evidence["citation"] = evidence.apply(
        lambda row: format_citation(
            row.get("chunk_id", ""),
            row.get("document_id", ""),
            row.get("title", ""),
        ),
        axis=1,
    )
    evidence["evidence_snippet"] = evidence["chunk_text"].fillna("").str.slice(0, 360)
    columns = [
        "query",
        "rank",
        "retrieval_score",
        "citation",
        "document_id",
        "title",
        "chunk_id",
        "evidence_snippet",
    ]
    return evidence[[column for column in columns if column in evidence.columns]]
