"""Merged dataset inspection helpers."""

from __future__ import annotations

import pandas as pd


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
