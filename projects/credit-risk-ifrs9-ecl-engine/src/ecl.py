"""IFRS 9-style Expected Credit Loss utilities.

These functions implement transparent portfolio analytics assumptions. They are
not a regulatory IFRS 9 model.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_pd_predictions(path: str | Path) -> pd.DataFrame:
    """Load Phase 2 PD predictions."""
    prediction_path = Path(path)
    if not prediction_path.exists():
        raise FileNotFoundError(f"PD prediction file not found: {prediction_path}")
    df = pd.read_csv(prediction_path, low_memory=False)
    required_columns = {"default_flag", "pd_score"}
    missing = required_columns - set(df.columns)
    if missing:
        raise KeyError(f"PD prediction file is missing required columns: {sorted(missing)}")
    return df


def assign_ead(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Assign exposure at default using available fields and return the method."""
    ecl_df = df.copy()
    if "loan_amnt" in ecl_df.columns:
        ecl_df["ead"] = pd.to_numeric(ecl_df["loan_amnt"], errors="coerce")
        method = "loan_amnt"
    elif "installment" in ecl_df.columns:
        ecl_df["ead"] = pd.to_numeric(ecl_df["installment"], errors="coerce") * 36
        method = "installment_times_36"
    else:
        ecl_df["ead"] = 10_000.0
        method = "fixed_10000"

    ecl_df["ead"] = ecl_df["ead"].fillna(10_000.0).clip(lower=0)
    return ecl_df, method


def assign_lgd(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Assign simplified loss given default using fixed portfolio assumptions."""
    ecl_df = df.copy()
    if "home_ownership" in ecl_df.columns:
        mapping = {
            "MORTGAGE": 0.35,
            "OWN": 0.40,
            "RENT": 0.50,
        }
        home_ownership = ecl_df["home_ownership"].astype("string").str.upper().str.strip()
        ecl_df["lgd"] = home_ownership.map(mapping).fillna(0.45).astype(float)
        method = "home_ownership_adjusted"
    else:
        ecl_df["lgd"] = 0.45
        method = "fixed_45_percent"
    return ecl_df, method


def assign_ifrs9_stage(df: pd.DataFrame) -> pd.DataFrame:
    """Assign simplified IFRS 9-style stages from PD score and default flag."""
    ecl_df = df.copy()
    pd_score = pd.to_numeric(ecl_df["pd_score"], errors="coerce").fillna(0).clip(0, 1)
    default_flag = pd.to_numeric(ecl_df["default_flag"], errors="coerce").fillna(0)

    ecl_df["ifrs9_stage"] = "Stage 1"
    ecl_df.loc[(pd_score >= 0.20) & (pd_score < 0.50), "ifrs9_stage"] = "Stage 2"
    ecl_df.loc[(pd_score >= 0.50) | (default_flag == 1), "ifrs9_stage"] = "Stage 3"
    return ecl_df


def calculate_ecl(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate expected credit loss as PD x LGD x EAD."""
    ecl_df = df.copy()
    ecl_df["pd_score"] = pd.to_numeric(ecl_df["pd_score"], errors="coerce").fillna(0).clip(0, 1)
    ecl_df["lgd"] = pd.to_numeric(ecl_df["lgd"], errors="coerce").fillna(0.45).clip(0, 1)
    ecl_df["ead"] = pd.to_numeric(ecl_df["ead"], errors="coerce").fillna(10_000.0).clip(lower=0)
    ecl_df["ecl"] = ecl_df["pd_score"] * ecl_df["lgd"] * ecl_df["ead"]
    return ecl_df


def summarize_ecl(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Summarize exposure and ECL by a grouping column."""
    if group_col not in df.columns:
        raise KeyError(f"Group column '{group_col}' is not available.")
    summary = (
        df.groupby(group_col, dropna=False, observed=False)
        .agg(
            row_count=("ecl", "size"),
            total_exposure=("ead", "sum"),
            total_ecl=("ecl", "sum"),
            average_pd=("pd_score", "mean"),
            average_lgd=("lgd", "mean"),
            average_ecl=("ecl", "mean"),
        )
        .reset_index()
    )
    summary["ecl_rate"] = summary["total_ecl"] / summary["total_exposure"]
    return summary.sort_values("total_ecl", ascending=False)


def apply_scenario(
    df: pd.DataFrame,
    scenario_name: str,
    pd_multiplier: float = 1.0,
    lgd_multiplier: float = 1.0,
) -> pd.DataFrame:
    """Apply a PD and LGD stress scenario with caps at 100 percent."""
    scenario_df = df.copy()
    scenario_df["scenario"] = scenario_name
    scenario_df["scenario_pd"] = (scenario_df["pd_score"] * pd_multiplier).clip(0, 1)
    scenario_df["scenario_lgd"] = (scenario_df["lgd"] * lgd_multiplier).clip(0, 1)
    scenario_df["scenario_ecl"] = (
        scenario_df["scenario_pd"] * scenario_df["scenario_lgd"] * scenario_df["ead"]
    )
    scenario_df["pd_multiplier"] = pd_multiplier
    scenario_df["lgd_multiplier"] = lgd_multiplier
    return scenario_df


def create_scenario_summary(df: pd.DataFrame, scenarios: list[dict]) -> pd.DataFrame:
    """Create a portfolio-level ECL summary for multiple scenarios."""
    rows = []
    base_exposure = df["ead"].sum()
    for scenario in scenarios:
        scenario_df = apply_scenario(
            df,
            scenario_name=scenario["scenario_name"],
            pd_multiplier=scenario.get("pd_multiplier", 1.0),
            lgd_multiplier=scenario.get("lgd_multiplier", 1.0),
        )
        rows.append(
            {
                "scenario": scenario["scenario_name"],
                "pd_multiplier": scenario.get("pd_multiplier", 1.0),
                "lgd_multiplier": scenario.get("lgd_multiplier", 1.0),
                "total_exposure": base_exposure,
                "total_ecl": scenario_df["scenario_ecl"].sum(),
                "average_pd": scenario_df["scenario_pd"].mean(),
                "average_lgd": scenario_df["scenario_lgd"].mean(),
                "ecl_rate": scenario_df["scenario_ecl"].sum() / base_exposure,
            }
        )
    return pd.DataFrame(rows)
