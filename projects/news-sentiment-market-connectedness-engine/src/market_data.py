"""Market data audit helpers."""

from __future__ import annotations

import pandas as pd


def identify_market_columns(df):
    """Identify columns that look like price, return, volume, ticker, or date fields."""
    lower_map = {col: str(col).lower() for col in df.columns}
    return {
        "date_columns": [col for col, name in lower_map.items() if "date" in name or "time" in name],
        "ticker_columns": [col for col, name in lower_map.items() if name in {"ticker", "symbol", "stock"}],
        "price_columns": [col for col, name in lower_map.items() if any(term in name for term in ["price", "close", "open", "high", "low"])],
        "return_columns": [col for col, name in lower_map.items() if "return" in name or name in {"ret", "returns"}],
        "volume_columns": [col for col, name in lower_map.items() if "volume" in name],
    }


def summarize_market_data(df):
    """Summarize market-like fields in a DataFrame."""
    columns = identify_market_columns(df)
    numeric = df.select_dtypes(include="number")
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "market_column_groups": columns,
        "numeric_columns": list(numeric.columns),
        "numeric_missing_total": int(numeric.isna().sum().sum()) if not numeric.empty else 0,
    }
