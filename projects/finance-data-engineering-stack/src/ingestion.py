"""
Ingestion utilities for the Finance Data Engineering Stack.

All functions are pure (no side-effects beyond explicit file saves)
so they can be used from both notebooks and the CLI.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import pandas as pd

logger = logging.getLogger(__name__)


def download_market_data(
    tickers: Sequence[str],
    start_date: str,
    end_date: str | None = None,
) -> pd.DataFrame:
    """
    Download OHLCV market data via yfinance for a list of tickers.

    Parameters
    ----------
    tickers : list of str
        Ticker symbols (e.g. ['AAPL', 'MSFT']).
    start_date : str
        ISO date string, e.g. '2020-01-01'.
    end_date : str or None
        ISO date string. Defaults to today if None.

    Returns
    -------
    pd.DataFrame
        MultiIndex columns: (field, ticker). Index: date.
    """
    try:
        import yfinance as yf
    except ImportError as exc:
        raise ImportError("yfinance is required: pip install yfinance") from exc

    if end_date is None:
        end_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    logger.info("Downloading %d tickers from %s to %s", len(tickers), start_date, end_date)
    raw = yf.download(
        list(tickers),
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )
    if raw.empty:
        raise ValueError("yfinance returned no data. Check tickers and date range.")
    return raw


def extract_adjusted_close(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the Adj Close panel from the raw MultiIndex yfinance download.

    Returns a DataFrame with dates as index and tickers as columns.
    """
    if "Adj Close" in raw_data.columns.get_level_values(0):
        prices = raw_data["Adj Close"].copy()
    elif "Close" in raw_data.columns.get_level_values(0):
        logger.warning("'Adj Close' not found — falling back to 'Close'.")
        prices = raw_data["Close"].copy()
    else:
        raise KeyError("Neither 'Adj Close' nor 'Close' found in raw data columns.")

    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "date"
    prices.columns.name = "ticker"
    return prices.dropna(how="all")


def save_raw_market_data(df: pd.DataFrame, path: Path) -> None:
    """Save the raw MultiIndex DataFrame to CSV (flattened column names)."""
    flat = df.copy()
    flat.columns = ["_".join(col).strip() for col in flat.columns.to_flat_index()]
    flat.to_csv(path)
    logger.info("Raw market data saved: %s (%d rows)", path.name, len(flat))


def save_processed_market_data(df: pd.DataFrame, path: Path) -> None:
    """Save a processed (wide or long) DataFrame to CSV."""
    df.to_csv(path)
    logger.info("Processed data saved: %s (%d rows)", path.name, len(df))


def create_ingestion_log(records: list[dict], path: Path) -> pd.DataFrame:
    """
    Persist an ingestion log and return it as a DataFrame.

    Each record should contain at minimum:
        ticker, start_date, end_date, rows_downloaded, status, timestamp
    """
    log_df = pd.DataFrame(records)
    log_df.to_csv(path, index=False)
    logger.info("Ingestion log saved: %s (%d records)", path.name, len(log_df))
    return log_df
