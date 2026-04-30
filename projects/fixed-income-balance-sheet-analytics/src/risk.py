"""Fixed income risk analytics for duration, convexity, and DV01."""

from __future__ import annotations

import pandas as pd

from src.pricing import discount_cashflows


def calculate_macaulay_duration(cashflows, market_yield, coupon_frequency):
    """Calculate Macaulay duration in years from discounted cash flows."""
    discounted = discount_cashflows(cashflows, market_yield, coupon_frequency)
    price = discounted["present_value"].sum()
    if price == 0:
        return 0.0
    weighted_time = (
        discounted["year_fraction"] * discounted["present_value"]
    ).sum()
    return float(weighted_time / price)


def calculate_modified_duration(cashflows, market_yield, coupon_frequency):
    """Calculate modified duration from Macaulay duration."""
    macaulay_duration = calculate_macaulay_duration(
        cashflows=cashflows,
        market_yield=market_yield,
        coupon_frequency=coupon_frequency,
    )
    return float(macaulay_duration / (1 + market_yield / coupon_frequency))


def calculate_convexity(cashflows, market_yield, coupon_frequency):
    """Calculate approximate annual convexity for periodically compounded cash flows."""
    discounted = discount_cashflows(cashflows, market_yield, coupon_frequency)
    price = discounted["present_value"].sum()
    if price == 0:
        return 0.0
    t = discounted["year_fraction"]
    convexity_numerator = (
        discounted["present_value"] * t * (t + 1 / coupon_frequency)
    ).sum()
    convexity_denominator = price * (1 + market_yield / coupon_frequency) ** 2
    return float(convexity_numerator / convexity_denominator)


def calculate_dv01(price, modified_duration):
    """Calculate dollar value change for a one basis point yield move."""
    return float(price * modified_duration * 0.0001)


def estimate_price_change_duration_convexity(
    price,
    modified_duration,
    convexity,
    yield_change,
):
    """Estimate price change using duration and convexity approximation."""
    return float(
        price
        * (
            -modified_duration * yield_change
            + 0.5 * convexity * yield_change**2
        )
    )


def calculate_bond_risk_metrics(bond_pricing_results, cashflows):
    """Calculate duration, convexity, and DV01 for each bond."""
    rows = []
    for _, bond in bond_pricing_results.iterrows():
        bond_cashflows = cashflows[cashflows["bond_id"] == bond["bond_id"]].copy()
        if bond_cashflows.empty:
            continue
        macaulay_duration = calculate_macaulay_duration(
            cashflows=bond_cashflows,
            market_yield=float(bond["market_yield"]),
            coupon_frequency=int(bond["coupon_frequency"]),
        )
        modified_duration = calculate_modified_duration(
            cashflows=bond_cashflows,
            market_yield=float(bond["market_yield"]),
            coupon_frequency=int(bond["coupon_frequency"]),
        )
        convexity = calculate_convexity(
            cashflows=bond_cashflows,
            market_yield=float(bond["market_yield"]),
            coupon_frequency=int(bond["coupon_frequency"]),
        )
        dv01 = calculate_dv01(
            price=float(bond["market_value"]),
            modified_duration=modified_duration,
        )
        rows.append(
            {
                "bond_id": bond["bond_id"],
                "issuer_type": bond["issuer_type"],
                "sector": bond["sector"],
                "credit_rating": bond["credit_rating"],
                "market_value": float(bond["market_value"]),
                "market_yield": float(bond["market_yield"]),
                "macaulay_duration": macaulay_duration,
                "modified_duration": modified_duration,
                "convexity": convexity,
                "dv01": dv01,
            }
        )
    return pd.DataFrame(rows)


def summarize_portfolio_risk(risk_results):
    """Summarize portfolio-level fixed income risk metrics."""
    total_market_value = float(risk_results["market_value"].sum())
    if total_market_value == 0:
        weights = pd.Series(0.0, index=risk_results.index)
    else:
        weights = risk_results["market_value"] / total_market_value
    return pd.DataFrame(
        [
            {
                "bond_count": int(len(risk_results)),
                "total_market_value": total_market_value,
                "portfolio_macaulay_duration": float(
                    (weights * risk_results["macaulay_duration"]).sum()
                ),
                "portfolio_modified_duration": float(
                    (weights * risk_results["modified_duration"]).sum()
                ),
                "portfolio_convexity": float(
                    (weights * risk_results["convexity"]).sum()
                ),
                "portfolio_dv01": float(risk_results["dv01"].sum()),
                "largest_single_bond_dv01": float(risk_results["dv01"].max()),
            }
        ]
    )
