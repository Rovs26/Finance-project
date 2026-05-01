"""Merged dataset inspection helpers."""

from __future__ import annotations

import pandas as pd


def standardize_date_column(df, candidate_cols):
    """Create a normalized `date` column from the first usable candidate column."""
    standardized = df.copy()
    for col in candidate_cols:
        if col not in standardized.columns:
            continue
        values = standardized[col]
        numeric_like = pd.to_numeric(values, errors="coerce")
        if numeric_like.notna().mean() > 0.8 and numeric_like.dropna().median() > 10_000_000:
            parsed = pd.to_datetime(numeric_like, unit="ms", errors="coerce")
        else:
            parsed = pd.to_datetime(values, errors="coerce")
        if parsed.notna().sum() > 0:
            standardized["date"] = parsed.dt.normalize()
            return standardized
    if "date" not in standardized.columns:
        standardized["date"] = pd.NaT
    return standardized


def merge_sentiment_market(sentiment_df, market_df):
    """Merge daily sentiment with market data on date."""
    sentiment = standardize_date_column(sentiment_df, ["date", "datetime", "published_at"])
    market = standardize_date_column(market_df, ["date", "Date", "datetime"])

    if "sentiment_score" in sentiment.columns:
        agg_spec = {
            "avg_sentiment_score": ("sentiment_score", "mean"),
            "news_count": ("sentiment_score", "size"),
        }
    else:
        agg_spec = {"news_count": ("date", "size")}
    if "company" in sentiment.columns:
        agg_spec["companies"] = ("company", lambda x: ", ".join(sorted(set(map(str, x.dropna())))))
    if "action" in sentiment.columns:
        agg_spec["dominant_action"] = (
            "action",
            lambda x: x.mode().iat[0] if not x.mode().empty else "HOLD",
        )
    daily_sentiment = sentiment.groupby("date", dropna=True).agg(**agg_spec).reset_index()
    return daily_sentiment.merge(market, on="date", how="left")


def inspect_merged_dataset(df):
    """Inspect a candidate sentiment-market merged dataset."""
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "missing_values_total": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def identify_join_keys(df):
    """Identify likely join keys used to merge news, sentiment, and market data."""
    lower_map = {col: str(col).lower() for col in df.columns}
    return {
        "date_keys": [col for col, name in lower_map.items() if "date" in name or "time" in name],
        "company_keys": [col for col, name in lower_map.items() if name in {"company", "ticker", "symbol", "stock"}],
        "article_keys": [col for col, name in lower_map.items() if "url" in name or "article" in name or "headline" in name],
    }


def create_modeling_dataset(df):
    """Create a numeric dataset for exploratory connectedness analysis."""
    modeling = df.copy()
    if "date" in modeling.columns:
        modeling = modeling.sort_values("date")
    numeric_cols = list(modeling.select_dtypes(include="number").columns)
    keep_cols = ["date"] if "date" in modeling.columns else []
    keep_cols.extend(numeric_cols)
    return modeling[keep_cols].dropna(axis=1, how="all")
