"""Local evaluation and risk flag utilities for cited research outputs."""

from __future__ import annotations

import re

import pandas as pd


RISK_KEYWORDS = {
    "credit risk": [
        "credit risk",
        "default",
        "delinquency",
        "borrower",
        "collections",
        "restructured",
        "non-performing",
    ],
    "liquidity risk": [
        "liquidity",
        "cash",
        "funding",
        "deposit",
        "withdrawal",
        "rollover",
    ],
    "interest-rate risk": [
        "interest rate",
        "policy rate",
        "rate sensitivity",
        "repricing",
        "yield",
    ],
    "inflation risk": [
        "inflation",
        "consumer prices",
        "price pressure",
        "purchasing power",
    ],
    "market risk": [
        "market risk",
        "volatility",
        "portfolio",
        "drawdown",
        "equity",
        "rates",
    ],
    "operational risk": [
        "operational",
        "outage",
        "fraud",
        "process",
        "cyber",
        "compliance",
    ],
    "profitability risk": [
        "profitability",
        "margin",
        "net interest margin",
        "funding cost",
        "fee income",
        "credit costs",
    ],
    "adoption risk": [
        "adoption",
        "digital payments",
        "merchant",
        "wallet",
        "customer trust",
        "user",
    ],
}


def _contains_any(text, keywords):
    normalized = str(text).lower()
    return any(keyword in normalized for keyword in keywords)


def evaluate_retrieval_coverage(evidence_table, questions):
    """Evaluate whether each research question has retrieved evidence."""
    rows = []
    for question in questions:
        subset = evidence_table[evidence_table["query"] == question]
        rows.append(
            {
                "question": question,
                "evidence_count": int(len(subset)),
                "unique_documents": int(subset["document_id"].nunique()) if not subset.empty else 0,
                "max_retrieval_score": float(subset["retrieval_score"].max()) if not subset.empty else 0.0,
                "status": "covered" if len(subset) > 0 else "not covered",
            }
        )
    return pd.DataFrame(rows)


def evaluate_source_traceability(evidence_table):
    """Check whether evidence rows contain source fields needed for citation tracing."""
    required_fields = ["citation", "document_id", "title", "chunk_id", "evidence_snippet"]
    rows = []
    for _, row in evidence_table.iterrows():
        missing = [field for field in required_fields if not str(row.get(field, "")).strip()]
        rows.append(
            {
                "query": row.get("query", ""),
                "citation": row.get("citation", ""),
                "document_id": row.get("document_id", ""),
                "chunk_id": row.get("chunk_id", ""),
                "is_traceable": len(missing) == 0,
                "missing_fields": ", ".join(missing),
            }
        )
    return pd.DataFrame(rows)


def evaluate_answer_grounding(memo_sections, evidence_table):
    """Check whether memo sections cite evidence included in the evidence table."""
    valid_citations = set(evidence_table["citation"].dropna().astype(str))
    rows = []
    for section, text in memo_sections.items():
        citations = re.findall(r"\[[A-Z0-9]+(?:-[A-Z0-9]+)*-CHUNK\d{3}\]", str(text))
        matched = [citation for citation in citations if citation in valid_citations]
        rows.append(
            {
                "section": section,
                "citation_count": len(citations),
                "matched_citation_count": len(matched),
                "grounded": len(citations) > 0 and len(citations) == len(matched),
                "citations": ", ".join(citations),
            }
        )
    return pd.DataFrame(rows)


def extract_risk_flags(evidence_table):
    """Extract transparent keyword-based risk flags from retrieved evidence."""
    rows = []
    for _, row in evidence_table.iterrows():
        text = " ".join(
            [
                str(row.get("query", "")),
                str(row.get("title", "")),
                str(row.get("evidence_snippet", "")),
            ]
        )
        for category, keywords in RISK_KEYWORDS.items():
            matched_keywords = [keyword for keyword in keywords if keyword in text.lower()]
            if matched_keywords:
                rows.append(
                    {
                        "risk_category": category,
                        "citation": row.get("citation", ""),
                        "query": row.get("query", ""),
                        "document_id": row.get("document_id", ""),
                        "chunk_id": row.get("chunk_id", ""),
                        "matched_keywords": ", ".join(sorted(set(matched_keywords))),
                        "evidence_snippet": row.get("evidence_snippet", ""),
                    }
                )
    return pd.DataFrame(rows).drop_duplicates()


def build_evaluation_summary(coverage_df, traceability_df, grounding_df):
    """Build a compact summary of retrieval, traceability, and grounding checks."""
    rows = [
        {
            "check": "retrieval_coverage",
            "total_items": int(len(coverage_df)),
            "passed_items": int((coverage_df["status"] == "covered").sum()),
            "status": "pass" if (coverage_df["status"] == "covered").all() else "review",
        },
        {
            "check": "source_traceability",
            "total_items": int(len(traceability_df)),
            "passed_items": int(traceability_df["is_traceable"].sum()),
            "status": "pass" if traceability_df["is_traceable"].all() else "review",
        },
        {
            "check": "answer_grounding",
            "total_items": int(len(grounding_df)),
            "passed_items": int(grounding_df["grounded"].sum()),
            "status": "pass" if grounding_df["grounded"].all() else "review",
        },
    ]
    return pd.DataFrame(rows)
