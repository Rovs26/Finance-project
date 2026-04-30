"""
Data transformation utilities for the Finance Data Engineering Stack.

Produces SQL-ready dimension and fact tables from raw price data.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate simple daily percentage returns from a wide price table.

    Parameters
    ----------
    prices : pd.DataFrame
        Wide table — index: date, columns: tickers.

    Returns
    -------
    pd.DataFrame
        Same shape as prices; first row is NaN (no prior day).
    """
    returns = prices.pct_change()
    returns.index.name = "date"
    returns.columns.name = "ticker"
    return returns


def reshape_prices_long(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Melt a wide price table into long format.

    Returns columns: date, ticker, price
    """
    long = prices.reset_index().melt(id_vars="date", var_name="ticker", value_name="price")
    long = long.dropna(subset=["price"]).reset_index(drop=True)
    long["date"] = pd.to_datetime(long["date"])
    return long.sort_values(["date", "ticker"]).reset_index(drop=True)


def create_asset_dimension(tickers: list[str]) -> pd.DataFrame:
    """
    Build a simple dim_assets table with a surrogate key.

    Columns: asset_id, ticker, asset_type, loaded_at
    """
    sector_map = {
        "AAPL": "Technology",
        "MSFT": "Technology",
        "NVDA": "Technology",
        "JPM":  "Financials",
        "PG":   "Consumer Staples",
        "XOM":  "Energy",
        "JNJ":  "Health Care",
        "KO":   "Consumer Staples",
        "SPY":  "ETF",
    }
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for i, ticker in enumerate(sorted(tickers), start=1):
        rows.append(
            {
                "asset_id":   i,
                "ticker":     ticker,
                "asset_type": sector_map.get(ticker, "Equity"),
                "loaded_at":  now,
            }
        )
    return pd.DataFrame(rows)


def create_price_fact_table(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Build fact_prices from a wide adjusted-close price table.

    Columns: price_id, date, ticker, adj_close
    """
    long = reshape_prices_long(prices)
    long = long.rename(columns={"price": "adj_close"})
    long.insert(0, "price_id", range(1, len(long) + 1))
    return long


def create_returns_fact_table(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Build fact_returns from a wide returns table.

    Columns: return_id, date, ticker, daily_return
    """
    long = (
        returns.reset_index()
        .melt(id_vars="date", var_name="ticker", value_name="daily_return")
        .dropna(subset=["daily_return"])
        .reset_index(drop=True)
    )
    long["date"] = pd.to_datetime(long["date"])
    long = long.sort_values(["date", "ticker"]).reset_index(drop=True)
    long.insert(0, "return_id", range(1, len(long) + 1))
    return long
