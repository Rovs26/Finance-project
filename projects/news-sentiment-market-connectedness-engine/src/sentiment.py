"""Sentiment data helpers for the audit phase."""

from __future__ import annotations

import pandas as pd


def standardize_sentiment_log(df):
    """Return a lightly standardized sentiment log without changing source meaning."""
    standardized = df.copy()
    standardized.columns = [str(col).strip().lower().replace(" ", "_") for col in standardized.columns]
    for col in standardized.columns:
        if "date" in col or "time" in col:
            standardized[col] = pd.to_datetime(standardized[col], errors="coerce")
    return standardized


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
        return pd.DataFrame(columns=["date", "record_count"])
    date_col = date_cols[0]
    dated = df.copy()
    dated["date"] = pd.to_datetime(dated[date_col], errors="coerce").dt.date
    return dated.groupby("date", dropna=True).size().reset_index(name="record_count")
