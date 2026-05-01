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
