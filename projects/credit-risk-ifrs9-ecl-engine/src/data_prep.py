"""Data preparation utilities for Phase 1 data understanding."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_DIR


DEFAULT_STATUSES = {
    "Charged Off",
    "Default",
    "Late (31-120 days)",
    "Does not meet the credit policy. Status:Charged Off",
}

NON_DEFAULT_STATUSES = {
    "Fully Paid",
    "Current",
    "In Grace Period",
    "Late (16-30 days)",
    "Does not meet the credit policy. Status:Fully Paid",
}

CANDIDATE_FEATURES = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "annual_inc",
    "verification_status",
    "purpose",
    "dti",
    "delinq_2yrs",
    "earliest_cr_line",
    "fico_range_low",
    "fico_range_high",
    "inq_last_6mths",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc",
    "application_type",
    "mort_acc",
    "pub_rec_bankruptcies",
]


def _is_csv_like(path: Path) -> bool:
    """Return True for plain or compressed CSV files."""
    return path.suffix == ".csv" or path.name.endswith(".csv.gz")


def find_raw_dataset(raw_data_dir: Path = RAW_DATA_DIR) -> Path:
    """Find the preferred raw dataset file, choosing the largest CSV-like file."""
    candidates = [
        path
        for path in raw_data_dir.iterdir()
        if path.is_file() and _is_csv_like(path)
    ]
    if not candidates:
        raise FileNotFoundError(f"No CSV or CSV.GZ dataset found in {raw_data_dir}")
    return max(candidates, key=lambda path: path.stat().st_size)


def load_raw_data(sample_size: int | None = None) -> pd.DataFrame:
    """Load the selected raw dataset, optionally limiting rows for exploration."""
    dataset_path = find_raw_dataset()
    return pd.read_csv(dataset_path, nrows=sample_size, low_memory=False)


def summarize_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Return a column-level schema summary with data types and missingness."""
    summary = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(dtype) for dtype in df.dtypes],
            "non_null_count": df.notna().sum().to_numpy(),
            "missing_count": df.isna().sum().to_numpy(),
            "missing_pct": (df.isna().mean() * 100).round(2).to_numpy(),
            "unique_count": df.nunique(dropna=True).to_numpy(),
        }
    )
    return summary.sort_values(["missing_pct", "column"], ascending=[False, True])


def map_loan_status_to_target(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Map LendingClub loan statuses to a binary default target.

    Returns a modeling-ready DataFrame excluding rows with unknown target status,
    plus a sorted list of unknown statuses found in the input.
    """
    if "loan_status" not in df.columns:
        raise KeyError("Expected column 'loan_status' was not found.")

    mapped = df.copy()
    mapped["loan_status"] = mapped["loan_status"].astype("string").str.strip()
    target_map = {status: 1 for status in DEFAULT_STATUSES}
    target_map.update({status: 0 for status in NON_DEFAULT_STATUSES})
    mapped["default_flag"] = mapped["loan_status"].map(target_map)

    observed_statuses = set(mapped["loan_status"].dropna().unique())
    known_statuses = DEFAULT_STATUSES | NON_DEFAULT_STATUSES
    unknown_statuses = sorted(observed_statuses - known_statuses)

    modeling_ready = mapped[mapped["default_flag"].notna()].copy()
    modeling_ready["default_flag"] = modeling_ready["default_flag"].astype(int)
    return modeling_ready, unknown_statuses


def get_candidate_features(df: pd.DataFrame) -> list[str]:
    """Return candidate credit risk features that exist in the dataset."""
    return [column for column in CANDIDATE_FEATURES if column in df.columns]
