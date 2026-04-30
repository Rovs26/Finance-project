"""
Data validation utilities — Phase 1 placeholder.

Stubs defined here so imports work from Phase 0 notebooks;
full implementation built in Phase 1.
"""

from __future__ import annotations

import pandas as pd


def check_missing_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Return a summary of missing value counts per ticker."""
    missing = prices.isnull().sum().reset_index()
    missing.columns = ["ticker", "missing_count"]
    missing["total_rows"] = len(prices)
    missing["missing_pct"] = (missing["missing_count"] / missing["total_rows"] * 100).round(2)
    return missing


def check_price_staleness(prices: pd.DataFrame, max_gap_days: int = 5) -> pd.DataFrame:
    """Flag tickers whose latest date lags the most recent date in the panel."""
    latest_overall = prices.index.max()
    records = []
    for ticker in prices.columns:
        col = prices[ticker].dropna()
        latest_ticker = col.index.max() if not col.empty else None
        gap = (latest_overall - latest_ticker).days if latest_ticker else None
        records.append(
            {
                "ticker":        ticker,
                "latest_date":   latest_ticker,
                "panel_max_date": latest_overall,
                "gap_days":      gap,
                "stale":         gap is not None and gap > max_gap_days,
            }
        )
    return pd.DataFrame(records)


def check_return_outliers(returns: pd.DataFrame, z_threshold: float = 5.0) -> pd.DataFrame:
    """Return rows where the absolute z-score of daily_return exceeds threshold."""
    long = (
        returns.reset_index()
        .melt(id_vars="date", var_name="ticker", value_name="daily_return")
        .dropna(subset=["daily_return"])
    )
    mean = long["daily_return"].mean()
    std  = long["daily_return"].std()
    long["z_score"] = ((long["daily_return"] - mean) / std).abs()
    return long[long["z_score"] > z_threshold].reset_index(drop=True)
