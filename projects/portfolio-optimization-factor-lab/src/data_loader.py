"""Market data loading utilities."""

from pathlib import Path

import pandas as pd


def download_price_data(tickers, start_date, end_date=None):
    """Download historical market data from Yahoo Finance through yfinance."""
    try:
        import yfinance as yf
    except ImportError as exc:
        raise ImportError(
            "yfinance is required to download market data. Install project requirements first."
        ) from exc

    raw_data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
        group_by="column",
        threads=True,
    )

    if raw_data.empty:
        raise ValueError("No market data was returned by yfinance.")

    return raw_data


def extract_adjusted_close(raw_data):
    """Extract adjusted close prices from raw yfinance output."""
    if isinstance(raw_data.columns, pd.MultiIndex):
        if "Adj Close" in raw_data.columns.get_level_values(0):
            prices = raw_data["Adj Close"].copy()
        elif "Close" in raw_data.columns.get_level_values(0):
            prices = raw_data["Close"].copy()
        else:
            raise KeyError("Raw data does not contain an adjusted close or close price field.")
    elif "Adj Close" in raw_data.columns:
        prices = raw_data[["Adj Close"]].copy()
    elif "Close" in raw_data.columns:
        prices = raw_data[["Close"]].copy()
    else:
        prices = raw_data.copy()

    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()
    prices = prices.dropna(how="all")
    return prices


def save_price_data(prices, path):
    """Save adjusted close prices to a CSV file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(output_path, index_label="date")
    return output_path


def load_price_data(path):
    """Load adjusted close prices from a CSV file."""
    return pd.read_csv(path, parse_dates=["date"], index_col="date")
