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


def standardize_market_columns(df):
    """Standardize common market data fields while preserving ticker suffixes."""
    standardized = df.copy()
    new_columns = []
    seen = {}
    for col in standardized.columns:
        base = str(col).strip().replace(" ", "_").lower()
        seen[base] = seen.get(base, 0) + 1
        new_columns.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
    standardized.columns = new_columns
    for col in list(standardized.columns):
        if col in {"date", "datetime"} or col.startswith("date"):
            values = standardized[col]
            numeric_like = pd.to_numeric(values, errors="coerce")
            if not numeric_like.dropna().empty and numeric_like.dropna().median() > 10_000_000:
                standardized[col] = pd.to_datetime(numeric_like, unit="ms", errors="coerce").dt.normalize()
            else:
                standardized[col] = pd.to_datetime(values, errors="coerce").dt.normalize()
    return standardized


def calculate_market_returns(df):
    """Calculate percentage returns for detected close price columns."""
    returns_df = df.copy()
    if "date" in returns_df.columns:
        returns_df = returns_df.sort_values("date")
    close_cols = [col for col in returns_df.columns if str(col).lower().startswith("close")]
    for col in close_cols:
        returns_df[f"{col}_return"] = pd.to_numeric(returns_df[col], errors="coerce").pct_change(fill_method=None)
    return returns_df
