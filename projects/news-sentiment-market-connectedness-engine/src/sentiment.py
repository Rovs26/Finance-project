"""Sentiment data helpers for the audit phase."""

from __future__ import annotations

import pandas as pd


def standardize_sentiment_log(df):
    """Return a lightly standardized sentiment log without changing source meaning."""
    standardized = df.copy()
    standardized.columns = [str(col).strip().lower().replace(" ", "_") for col in standardized.columns]
    if "date" in standardized.columns:
        standardized["date"] = pd.to_datetime(standardized["date"], errors="coerce").dt.normalize()
    for col in ["sentiment_score", "score", "polarity"]:
        if col in standardized.columns:
            standardized["sentiment_score"] = pd.to_numeric(standardized[col], errors="coerce")
            break
    if "sentiment_score" in standardized.columns:
        standardized["sentiment_label"] = standardized["sentiment_score"].apply(classify_sentiment_score)
    if "action" not in standardized.columns and "sentiment_label" in standardized.columns:
        action_map = {"negative": "SELL", "neutral": "HOLD", "positive": "BUY"}
        standardized["action"] = standardized["sentiment_label"].map(action_map)
    if "action" in standardized.columns:
        standardized["action"] = standardized["action"].fillna("").astype(str).str.upper()
    return standardized


def standardize_scraped_news(df):
    """Standardize scraped news column names and date fields when available."""
    standardized = df.copy()
    standardized.columns = [str(col).strip().lower().replace(" ", "_") for col in standardized.columns]
    for col in standardized.columns:
        if "date" in col or "time" in col or "published" in col:
            standardized[col] = pd.to_datetime(standardized[col], errors="coerce")
    return standardized


def classify_sentiment_score(score):
    """Classify a numeric sentiment score into negative, neutral, or positive."""
    if pd.isna(score):
        return "unknown"
    if score <= -0.15:
        return "negative"
    if score >= 0.15:
        return "positive"
    return "neutral"


def summarize_sentiment_by_company(df):
    """Summarize sentiment records by available company or ticker column."""
    candidates = [col for col in df.columns if col in {"company", "ticker", "symbol", "stock"}]
    if not candidates:
        return pd.DataFrame(columns=["company_key", "record_count"])
    key = candidates[0]
    return (
        df.groupby(key, dropna=False)
        .size()
        .reset_index(name="record_count")
        .rename(columns={key: "company_key"})
        .sort_values("record_count", ascending=False)
    )


def summarize_sentiment_by_date(df):
    """Summarize sentiment records by the first available date-like column."""
    date_cols = [col for col in df.columns if "date" in col or "time" in col]
    if not date_cols:
        return pd.DataFrame(columns=["date", "record_count", "avg_sentiment_score"])
    date_col = date_cols[0]
    dated = df.copy()
    dated["date"] = pd.to_datetime(dated[date_col], errors="coerce").dt.normalize()
    agg = {"record_count": ("date", "size")}
    if "sentiment_score" in dated.columns:
        agg["avg_sentiment_score"] = ("sentiment_score", "mean")
    if "sentiment_label" in dated.columns:
        agg["negative_count"] = ("sentiment_label", lambda x: (x == "negative").sum())
        agg["neutral_count"] = ("sentiment_label", lambda x: (x == "neutral").sum())
        agg["positive_count"] = ("sentiment_label", lambda x: (x == "positive").sum())
    return dated.groupby("date", dropna=True).agg(**agg).reset_index()


def create_signal_summary(df):
    """Summarize simple BUY/HOLD/SELL labels."""
    if "action" not in df.columns:
        return pd.DataFrame(columns=["action", "record_count", "share"])
    summary = df["action"].fillna("UNKNOWN").astype(str).str.upper().value_counts().reset_index()
    summary.columns = ["action", "record_count"]
    total = summary["record_count"].sum()
    summary["share"] = summary["record_count"] / total if total else 0
    return summary
