"""Interest-rate scenario and simple ALM utilities."""

from __future__ import annotations

import pandas as pd

from src.pricing import price_bond, price_bond_book


def create_rate_scenarios():
    """Create the standard Phase 1 parallel rate shock scenarios."""
    return pd.DataFrame(
        [
            {"scenario": "-100 bps", "shock_bps": -100, "yield_change": -0.0100},
            {"scenario": "-50 bps", "shock_bps": -50, "yield_change": -0.0050},
            {"scenario": "base", "shock_bps": 0, "yield_change": 0.0000},
            {"scenario": "+50 bps", "shock_bps": 50, "yield_change": 0.0050},
            {"scenario": "+100 bps", "shock_bps": 100, "yield_change": 0.0100},
            {"scenario": "+200 bps", "shock_bps": 200, "yield_change": 0.0200},
        ]
    )


def apply_parallel_rate_shock(bond_book, shocks_bps, settlement_date):
    """Reprice every bond after a parallel yield shock."""
    shock_decimal = shocks_bps / 10000
    rows = []
    for _, bond in bond_book.iterrows():
        shocked_yield = max(float(bond["market_yield"]) + shock_decimal, -0.95)
        shocked_price = price_bond(
            face_value=float(bond["face_value"]),
            coupon_rate=float(bond["coupon_rate"]),
            market_yield=shocked_yield,
            maturity_date=bond["maturity_date"],
            settlement_date=settlement_date,
            coupon_frequency=int(bond["coupon_frequency"]),
        )
        shocked_market_value = (
            shocked_price * float(bond["book_value"]) / float(bond["face_value"])
        )
        rows.append(
            {
                "bond_id": bond["bond_id"],
                "issuer_type": bond["issuer_type"],
                "sector": bond["sector"],
                "credit_rating": bond["credit_rating"],
                "shock_bps": int(shocks_bps),
                "base_market_yield": float(bond["market_yield"]),
                "shocked_market_yield": shocked_yield,
                "shocked_price": shocked_price,
                "shocked_clean_price_per_100": shocked_price
                / float(bond["face_value"])
                * 100,
                "shocked_market_value": shocked_market_value,
            }
        )
    return pd.DataFrame(rows)


def run_stress_test(bond_book, shocks_bps, settlement_date):
    """Run parallel rate stress scenarios and compare against base values."""
    base_pricing = price_bond_book(bond_book, settlement_date=settlement_date)
    base_values = base_pricing[
        ["bond_id", "model_price", "market_value", "clean_price_per_100"]
    ].rename(
        columns={
            "model_price": "base_price",
            "market_value": "base_market_value",
            "clean_price_per_100": "base_clean_price_per_100",
        }
    )

    frames = []
    for shock in shocks_bps:
        scenario_results = apply_parallel_rate_shock(
            bond_book=bond_book,
            shocks_bps=shock,
            settlement_date=settlement_date,
        )
        scenario_results = scenario_results.merge(base_values, on="bond_id", how="left")
        scenario_results["market_value_change"] = (
            scenario_results["shocked_market_value"]
            - scenario_results["base_market_value"]
        )
        scenario_results["market_value_change_pct"] = (
            scenario_results["market_value_change"]
            / scenario_results["base_market_value"]
        )
        frames.append(scenario_results)
    return pd.concat(frames, ignore_index=True)


def summarize_stress_results(stress_results):
    """Summarize portfolio market value under each rate scenario."""
    summary = (
        stress_results.groupby("shock_bps", as_index=False)
        .agg(
            portfolio_market_value=("shocked_market_value", "sum"),
            base_market_value=("base_market_value", "sum"),
            market_value_change=("market_value_change", "sum"),
        )
        .sort_values("shock_bps")
    )
    summary["market_value_change_pct"] = (
        summary["market_value_change"] / summary["base_market_value"]
    )
    summary["scenario"] = summary["shock_bps"].map(
        lambda value: "base" if value == 0 else f"{value:+d} bps"
    )
    return summary[
        [
            "scenario",
            "shock_bps",
            "base_market_value",
            "portfolio_market_value",
            "market_value_change",
            "market_value_change_pct",
        ]
    ]


def create_simple_alm_summary(portfolio_market_value, stress_summary):
    """Create a simplified ALM interpretation summary from stress results."""
    base_row = stress_summary[stress_summary["shock_bps"] == 0].iloc[0]
    up_100 = stress_summary[stress_summary["shock_bps"] == 100].iloc[0]
    up_200 = stress_summary[stress_summary["shock_bps"] == 200].iloc[0]
    down_100 = stress_summary[stress_summary["shock_bps"] == -100].iloc[0]
    return pd.DataFrame(
        [
            {
                "measure": "base_portfolio_market_value",
                "value": float(base_row["portfolio_market_value"]),
                "interpretation": "Current modeled market value of the synthetic bond portfolio.",
            },
            {
                "measure": "plus_100_bps_market_value_change",
                "value": float(up_100["market_value_change"]),
                "interpretation": "Estimated loss from a 100 bps parallel upward rate shock.",
            },
            {
                "measure": "plus_200_bps_market_value_change",
                "value": float(up_200["market_value_change"]),
                "interpretation": "Larger rate shock loss proxy for balance sheet sensitivity.",
            },
            {
                "measure": "minus_100_bps_market_value_change",
                "value": float(down_100["market_value_change"]),
                "interpretation": "Estimated gain from a 100 bps downward rate shock.",
            },
            {
                "measure": "market_value_to_input_check",
                "value": float(portfolio_market_value),
                "interpretation": "Input portfolio market value used to anchor stress interpretation.",
            },
        ]
    )
