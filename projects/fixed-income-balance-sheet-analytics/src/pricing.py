"""Bond pricing and yield-to-maturity utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.cashflows import generate_bond_cashflows


def _year_fraction(start_date, end_date):
    """Calculate a simple Actual/365 year fraction."""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    return max((end - start).days / 365.0, 0.0)


def discount_cashflows(cashflows, market_yield, coupon_frequency):
    """Discount scheduled cash flows with periodic compounding."""
    if cashflows.empty:
        return cashflows.copy()
    output = cashflows.copy()
    settlement = pd.to_datetime(output["settlement_date"].iloc[0])
    output["year_fraction"] = output["cashflow_date"].apply(
        lambda date: _year_fraction(settlement, date)
    )
    output["discount_factor"] = (
        1 + market_yield / coupon_frequency
    ) ** (-coupon_frequency * output["year_fraction"])
    output["present_value"] = output["total_cashflow"] * output["discount_factor"]
    return output


def price_bond(
    face_value,
    coupon_rate,
    market_yield,
    maturity_date,
    settlement_date,
    coupon_frequency,
):
    """Price one fixed-rate bullet bond from discounted cash flows."""
    cashflows = generate_bond_cashflows(
        face_value=face_value,
        coupon_rate=coupon_rate,
        coupon_frequency=coupon_frequency,
        settlement_date=settlement_date,
        maturity_date=maturity_date,
    )
    if cashflows.empty:
        return 0.0
    cashflows["settlement_date"] = pd.to_datetime(settlement_date)
    discounted = discount_cashflows(cashflows, market_yield, coupon_frequency)
    return float(discounted["present_value"].sum())


def calculate_ytm(
    price,
    face_value,
    coupon_rate,
    maturity_date,
    settlement_date,
    coupon_frequency,
):
    """Calculate yield to maturity using bisection with a grid fallback."""
    def objective(yield_guess):
        model_price = price_bond(
            face_value=face_value,
            coupon_rate=coupon_rate,
            market_yield=yield_guess,
            maturity_date=maturity_date,
            settlement_date=settlement_date,
            coupon_frequency=coupon_frequency,
        )
        return model_price - price

    low, high = -0.50, 1.00
    low_value = objective(low)
    high_value = objective(high)
    if low_value * high_value <= 0:
        for _ in range(100):
            midpoint = (low + high) / 2
            mid_value = objective(midpoint)
            if abs(mid_value) < 1e-8:
                return float(midpoint)
            if low_value * mid_value <= 0:
                high = midpoint
                high_value = mid_value
            else:
                low = midpoint
                low_value = mid_value
        return float((low + high) / 2)

    grid = np.linspace(-0.25, 0.75, 5001)
    errors = np.array([abs(objective(yield_guess)) for yield_guess in grid])
    return float(grid[errors.argmin()])


def price_bond_book(bond_book, settlement_date):
    """Price every bond in a synthetic bond book and calculate YTM."""
    rows = []
    for _, bond in bond_book.iterrows():
        price = price_bond(
            face_value=float(bond["face_value"]),
            coupon_rate=float(bond["coupon_rate"]),
            market_yield=float(bond["market_yield"]),
            maturity_date=bond["maturity_date"],
            settlement_date=settlement_date,
            coupon_frequency=int(bond["coupon_frequency"]),
        )
        ytm = calculate_ytm(
            price=price,
            face_value=float(bond["face_value"]),
            coupon_rate=float(bond["coupon_rate"]),
            maturity_date=bond["maturity_date"],
            settlement_date=settlement_date,
            coupon_frequency=int(bond["coupon_frequency"]),
        )
        market_value = price * float(bond["book_value"]) / float(bond["face_value"])
        rows.append(
            {
                **bond.to_dict(),
                "settlement_date": pd.to_datetime(settlement_date),
                "clean_price_per_100": price / float(bond["face_value"]) * 100,
                "model_price": price,
                "market_value": market_value,
                "calculated_ytm": ytm,
                "price_premium_discount": price - float(bond["face_value"]),
            }
        )
    return pd.DataFrame(rows)
