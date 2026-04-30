"""
Data validation utilities for the Finance Data Engineering Stack.

Functions
---------
load_table                    Load a CSV table from disk.
validate_required_columns     Check that all required columns are present.
validate_no_duplicate_keys    Check that key columns form a unique composite key.
validate_date_range           Report min/max date coverage for a date column.
validate_missing_values       Summarise missing value counts across all columns.
validate_numeric_ranges       Check numeric columns against min/max bounds.
validate_referential_integrity  Check FK relationship between two tables.
run_validation_suite          Run predefined suite against dim/fact tables.
save_validation_results       Persist validation results to CSV.

Phase 0 stubs are preserved at the bottom for backward compatibility.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


# ── Core helpers ──────────────────────────────────────────────────────────────

def load_table(path: Path) -> pd.DataFrame:
    """Load a CSV table from disk into a DataFrame."""
    df = pd.read_csv(path)
    logger.info("Loaded %s: %d rows, %d columns", Path(path).name, len(df), len(df.columns))
    return df


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> dict:
    """Check that all required columns are present in the DataFrame."""
    missing = [c for c in required_columns if c not in df.columns]
    return {
        "check": "required_columns",
        "status": "PASS" if not missing else "FAIL",
        "details": (
            f"All {len(required_columns)} required columns present"
            if not missing
            else f"Missing columns: {missing}"
        ),
    }


def validate_no_duplicate_keys(
    df: pd.DataFrame,
    key_columns: list[str],
) -> dict:
    """Check that key_columns form a unique composite key (no duplicates)."""
    dup_count = int(df.duplicated(subset=key_columns).sum())
    return {
        "check": "no_duplicate_keys",
        "status": "PASS" if dup_count == 0 else "FAIL",
        "details": (
            f"No duplicates on {key_columns}"
            if dup_count == 0
            else f"{dup_count} duplicate rows on {key_columns}"
        ),
    }


def validate_date_range(df: pd.DataFrame, date_col: str) -> dict:
    """Check date column coverage and report min/max date."""
    if date_col not in df.columns:
        return {
            "check": "date_range",
            "status": "FAIL",
            "details": f"Column '{date_col}' not found",
        }
    dates = pd.to_datetime(df[date_col], errors="coerce")
    null_count = int(dates.isna().sum())
    min_date = dates.min()
    max_date = dates.max()
    return {
        "check": "date_range",
        "status": "PASS" if null_count == 0 else "WARN",
        "details": (
            f"Date range: {min_date.date()} to {max_date.date()}; "
            f"{null_count} unparseable dates"
        ),
    }


def validate_missing_values(df: pd.DataFrame) -> dict:
    """Summarise missing value counts across all columns."""
    missing = df.isnull().sum()
    total_missing = int(missing.sum())
    cols_with_missing = [
        (col, int(cnt)) for col, cnt in missing.items() if cnt > 0
    ]
    return {
        "check": "missing_values",
        "status": "PASS" if total_missing == 0 else "WARN",
        "details": (
            "No missing values"
            if total_missing == 0
            else f"{total_missing} total missing; affected: {cols_with_missing}"
        ),
    }


def validate_numeric_ranges(
    df: pd.DataFrame,
    rules: list[dict],
) -> list[dict]:
    """
    Check numeric columns against min/max bounds.

    Parameters
    ----------
    df : pd.DataFrame
    rules : list of dicts
        Each dict: {"column": str, "min": float|None, "max": float|None}

    Returns
    -------
    list of result dicts, one per rule
    """
    results = []
    for rule in rules:
        col = rule["column"]
        lo  = rule.get("min")
        hi  = rule.get("max")
        if col not in df.columns:
            results.append({
                "check": f"numeric_range:{col}",
                "status": "FAIL",
                "details": f"Column '{col}' not found",
            })
            continue
        series = df[col].dropna()
        violations = 0
        if lo is not None:
            violations += int((series < lo).sum())
        if hi is not None:
            violations += int((series > hi).sum())
        results.append({
            "check": f"numeric_range:{col}",
            "status": "PASS" if violations == 0 else "FAIL",
            "details": (
                f"No out-of-range values (checked [{lo}, {hi}])"
                if violations == 0
                else f"{violations} values outside [{lo}, {hi}]"
            ),
        })
    return results


def validate_referential_integrity(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    child_key: str,
    parent_key: str,
) -> dict:
    """Check that all child_key values exist in parent_key (FK check)."""
    child_vals  = set(child_df[child_key].dropna().unique())
    parent_vals = set(parent_df[parent_key].dropna().unique())
    orphans = child_vals - parent_vals
    return {
        "check": f"referential_integrity:{child_key}->{parent_key}",
        "status": "PASS" if not orphans else "FAIL",
        "details": (
            f"All {len(child_vals)} {child_key} values found in parent"
            if not orphans
            else f"{len(orphans)} orphan value(s): {sorted(orphans)[:10]}"
        ),
    }


# ── Validation suite ──────────────────────────────────────────────────────────

def run_validation_suite(tables: dict[str, pd.DataFrame]) -> list[dict]:
    """
    Run predefined validation checks against dim_assets, fact_prices, fact_returns.

    Parameters
    ----------
    tables : dict
        Keys: "dim_assets", "fact_prices", "fact_returns"

    Returns
    -------
    list of result dicts: {table, check, status, details}
    """
    results: list[dict] = []
    dim     = tables.get("dim_assets",   pd.DataFrame())
    prices  = tables.get("fact_prices",  pd.DataFrame())
    returns = tables.get("fact_returns", pd.DataFrame())

    def _add(table: str, result: dict) -> None:
        results.append({"table": table, **result})

    def _add_many(table: str, result_list: list[dict]) -> None:
        for r in result_list:
            results.append({"table": table, **r})

    # ── dim_assets ─────────────────────────────────────────────────────────────
    _add("dim_assets", validate_required_columns(
        dim, ["asset_id", "ticker", "asset_type", "loaded_at"]
    ))
    _add("dim_assets", validate_no_duplicate_keys(dim, ["ticker"]))
    _add("dim_assets", validate_missing_values(dim))

    # ── fact_prices ────────────────────────────────────────────────────────────
    _add("fact_prices", validate_required_columns(
        prices, ["price_id", "date", "ticker", "adj_close"]
    ))
    _add("fact_prices", validate_no_duplicate_keys(prices, ["date", "ticker"]))
    _add("fact_prices", validate_date_range(prices, "date"))
    _add("fact_prices", validate_missing_values(prices))
    _add_many("fact_prices", validate_numeric_ranges(prices, [
        {"column": "adj_close", "min": 0.0, "max": None},
    ]))
    _add("fact_prices", validate_referential_integrity(prices, dim, "ticker", "ticker"))

    # ── fact_returns ───────────────────────────────────────────────────────────
    _add("fact_returns", validate_required_columns(
        returns, ["return_id", "date", "ticker", "daily_return"]
    ))
    _add("fact_returns", validate_no_duplicate_keys(returns, ["date", "ticker"]))
    _add("fact_returns", validate_date_range(returns, "date"))
    _add("fact_returns", validate_missing_values(returns))
    _add_many("fact_returns", validate_numeric_ranges(returns, [
        {"column": "daily_return", "min": -1.0, "max": 1.0},
    ]))
    _add("fact_returns", validate_referential_integrity(returns, dim, "ticker", "ticker"))

    return results


def save_validation_results(results: list[dict], path: Path) -> pd.DataFrame:
    """Persist validation results list to CSV and return as DataFrame."""
    df = pd.DataFrame(results)
    df.to_csv(path, index=False)
    logger.info(
        "Validation results saved: %s (%d checks)", Path(path).name, len(df)
    )
    return df


# ── Phase 0 compatibility stubs ───────────────────────────────────────────────

def check_missing_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Return a summary of missing value counts per ticker (Phase 0 stub)."""
    missing = prices.isnull().sum().reset_index()
    missing.columns = ["ticker", "missing_count"]
    missing["total_rows"] = len(prices)
    missing["missing_pct"] = (
        missing["missing_count"] / missing["total_rows"] * 100
    ).round(2)
    return missing


def check_price_staleness(
    prices: pd.DataFrame, max_gap_days: int = 5
) -> pd.DataFrame:
    """Flag tickers whose latest date lags the panel maximum (Phase 0 stub)."""
    latest_overall = prices.index.max()
    records = []
    for ticker in prices.columns:
        col = prices[ticker].dropna()
        latest_ticker = col.index.max() if not col.empty else None
        gap = (latest_overall - latest_ticker).days if latest_ticker else None
        records.append({
            "ticker":         ticker,
            "latest_date":    latest_ticker,
            "panel_max_date": latest_overall,
            "gap_days":       gap,
            "stale":          gap is not None and gap > max_gap_days,
        })
    return pd.DataFrame(records)


def check_return_outliers(
    returns: pd.DataFrame, z_threshold: float = 5.0
) -> pd.DataFrame:
    """Return rows where |z-score| of daily_return exceeds threshold (Phase 0 stub)."""
    long = (
        returns.reset_index()
        .melt(id_vars="date", var_name="ticker", value_name="daily_return")
        .dropna(subset=["daily_return"])
    )
    mean = long["daily_return"].mean()
    std  = long["daily_return"].std()
    long["z_score"] = ((long["daily_return"] - mean) / std).abs()
    return long[long["z_score"] > z_threshold].reset_index(drop=True)
