"""Feature utilities for probability of default modeling."""

from __future__ import annotations

import math

import pandas as pd


DEFAULT_MODEL_FEATURES = [
    "loan_amnt",
    "funded_amnt",
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


def get_default_candidate_features(df: pd.DataFrame) -> list[str]:
    """Return the default PD candidate features available in the DataFrame."""
    return [column for column in DEFAULT_MODEL_FEATURES if column in df.columns]


def clean_feature_values(df: pd.DataFrame) -> pd.DataFrame:
    """Apply lightweight value cleaning for common LendingClub-style fields."""
    cleaned = df.copy()

    for column in ["int_rate", "revol_util"]:
        if column in cleaned.columns:
            cleaned[column] = (
                cleaned[column]
                .astype("string")
                .str.replace("%", "", regex=False)
                .str.strip()
            )
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    numeric_candidates = [
        "loan_amnt",
        "funded_amnt",
        "installment",
        "annual_inc",
        "dti",
        "delinq_2yrs",
        "fico_range_low",
        "fico_range_high",
        "inq_last_6mths",
        "open_acc",
        "pub_rec",
        "revol_bal",
        "total_acc",
        "mort_acc",
        "pub_rec_bankruptcies",
    ]
    for column in numeric_candidates:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    categorical_candidates = [
        "term",
        "grade",
        "sub_grade",
        "emp_length",
        "home_ownership",
        "verification_status",
        "purpose",
        "application_type",
    ]
    for column in categorical_candidates:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip().replace("", pd.NA)
            cleaned[column] = cleaned[column].astype("object").where(cleaned[column].notna(), math.nan)

    return cleaned


def identify_feature_types(
    df: pd.DataFrame,
    target_col: str = "default_flag",
) -> tuple[list[str], list[str]]:
    """Identify numeric and categorical feature columns for modeling."""
    feature_columns = [column for column in get_default_candidate_features(df) if column != target_col]
    numeric_features = [
        column
        for column in feature_columns
        if pd.api.types.is_numeric_dtype(df[column])
    ]
    categorical_features = [
        column
        for column in feature_columns
        if column not in numeric_features
    ]
    return numeric_features, categorical_features


def build_feature_matrix(
    df: pd.DataFrame,
    target_col: str = "default_flag",
) -> tuple[pd.DataFrame, pd.Series]:
    """Return X and y using available default candidate features."""
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' is missing.")

    cleaned = clean_feature_values(df)
    feature_columns = get_default_candidate_features(cleaned)
    X = cleaned[feature_columns].copy()
    y = cleaned[target_col].astype(int).copy()
    return X, y
