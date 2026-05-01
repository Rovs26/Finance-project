"""Connectedness helpers for sentiment and market exploratory analysis."""

from __future__ import annotations

import pandas as pd


def inspect_connectedness_inputs(df):
    """Inspect whether a DataFrame has numeric inputs suitable for connectedness analysis."""
    numeric_columns = list(df.select_dtypes(include="number").columns)
    return {
        "rows": int(len(df)),
        "numeric_column_count": len(numeric_columns),
        "numeric_columns": numeric_columns,
        "has_minimum_inputs": len(numeric_columns) >= 2 and len(df) >= 30,
    }


def describe_gfevd_requirements():
    """Describe minimum inputs needed before repairing or running GFEVD analysis."""
    return {
        "required_shape": "Time-indexed panel with at least two numeric market or sentiment series.",
        "required_cleaning": "Consistent dates, no duplicated date-series keys, and handled missing values.",
        "required_validation": "Stationarity or transformation review, lag-order choice, and sensitivity checks.",
        "phase_0_status": "Inspection only. Full GFEVD repair is planned for Phase 1.",
    }


def prepare_connectedness_inputs(df):
    """Prepare numeric inputs for a simple connectedness matrix."""
    data = df.copy()
    if "date" in data.columns:
        data = data.sort_values("date").set_index("date")
    numeric = data.select_dtypes(include="number").copy()
    numeric = numeric.dropna(axis=1, how="all")
    numeric = numeric.loc[:, numeric.nunique(dropna=True) > 1]
    return numeric.dropna(how="all")


def calculate_correlation_connectedness(df):
    """Calculate absolute correlation matrix as transparent connectedness fallback."""
    if df.shape[1] < 2:
        return pd.DataFrame()
    return df.corr().abs().fillna(0.0)


def calculate_simple_variance_share(df):
    """Calculate simple variance shares for numeric series."""
    variances = df.var(numeric_only=True).dropna()
    total = variances.sum()
    if total == 0:
        shares = variances * 0
    else:
        shares = variances / total
    return shares.reset_index().rename(columns={"index": "series", 0: "variance_share"})


def build_connectedness_summary(df):
    """Build summary metrics for a connectedness matrix or input dataset."""
    if df.empty:
        return pd.DataFrame(
            [{"metric": "connectedness_status", "value": "not_enough_numeric_series"}]
        )
    matrix = calculate_correlation_connectedness(df)
    if matrix.empty:
        return pd.DataFrame(
            [{"metric": "connectedness_status", "value": "not_enough_numeric_series"}]
        )
    off_diag = matrix.copy()
    for col in off_diag.columns:
        off_diag.loc[col, col] = 0
    return pd.DataFrame(
        [
            {"metric": "method", "value": "absolute_correlation_fallback"},
            {"metric": "series_count", "value": int(matrix.shape[0])},
            {"metric": "observation_count", "value": int(len(df))},
            {"metric": "average_off_diagonal_connectedness", "value": float(off_diag.values.sum() / (matrix.shape[0] * (matrix.shape[0] - 1))) if matrix.shape[0] > 1 else 0.0},
            {"metric": "max_pairwise_connectedness", "value": float(off_diag.values.max()) if not off_diag.empty else 0.0},
        ]
    )


def create_connectedness_edges(matrix_df, threshold=0.2):
    """Create edge list from a connectedness matrix above a threshold."""
    rows = []
    if matrix_df.empty:
        return pd.DataFrame(columns=["source", "target", "connectedness"])
    for source in matrix_df.index:
        for target in matrix_df.columns:
            if source == target:
                continue
            value = float(matrix_df.loc[source, target])
            if value >= threshold:
                rows.append({"source": source, "target": target, "connectedness": value})
    return pd.DataFrame(rows).sort_values("connectedness", ascending=False)
