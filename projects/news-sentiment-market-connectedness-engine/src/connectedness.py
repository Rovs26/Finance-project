"""Connectedness audit placeholders for Phase 0."""


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
