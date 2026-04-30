"""Cash flow utilities for fixed-income portfolio examples."""

from __future__ import annotations

import pandas as pd


def generate_coupon_dates(settlement_date, maturity_date, coupon_frequency):
    """Generate future coupon dates after settlement through maturity."""
    settlement = pd.to_datetime(settlement_date)
    maturity = pd.to_datetime(maturity_date)
    if coupon_frequency <= 0:
        raise ValueError("coupon_frequency must be positive.")
    if maturity <= settlement:
        return []

    months = int(12 / coupon_frequency)
    dates = []
    current = maturity
    while current > settlement:
        dates.append(current)
        current = current - pd.DateOffset(months=months)
    return sorted(pd.Timestamp(date) for date in dates)


def generate_bond_cashflows(
    face_value,
    coupon_rate,
    coupon_frequency,
    settlement_date,
    maturity_date,
):
    """Generate scheduled coupon and principal cash flows for one bond."""
    coupon_dates = generate_coupon_dates(
        settlement_date=settlement_date,
        maturity_date=maturity_date,
        coupon_frequency=coupon_frequency,
    )
    coupon_payment = face_value * coupon_rate / coupon_frequency
    rows = []
    for idx, cashflow_date in enumerate(coupon_dates, start=1):
        principal = face_value if idx == len(coupon_dates) else 0.0
        rows.append(
            {
                "cashflow_number": idx,
                "cashflow_date": cashflow_date,
                "coupon_cashflow": coupon_payment,
                "principal_cashflow": principal,
                "total_cashflow": coupon_payment + principal,
            }
        )
    return pd.DataFrame(rows)


def build_cashflow_table(bond_book, settlement_date):
    """Build a combined cash flow table for every bond in the bond book."""
    frames = []
    for _, bond in bond_book.iterrows():
        cashflows = generate_bond_cashflows(
            face_value=float(bond["face_value"]),
            coupon_rate=float(bond["coupon_rate"]),
            coupon_frequency=int(bond["coupon_frequency"]),
            settlement_date=settlement_date,
            maturity_date=bond["maturity_date"],
        )
        if cashflows.empty:
            continue
        for column in [
            "bond_id",
            "issuer_type",
            "sector",
            "credit_rating",
            "coupon_rate",
            "market_yield",
            "face_value",
        ]:
            cashflows[column] = bond[column]
        cashflows["settlement_date"] = pd.to_datetime(settlement_date)
        frames.append(cashflows)
    if not frames:
        return pd.DataFrame()
    output = pd.concat(frames, ignore_index=True)
    return output[
        [
            "bond_id",
            "issuer_type",
            "sector",
            "credit_rating",
            "settlement_date",
            "cashflow_number",
            "cashflow_date",
            "coupon_rate",
            "market_yield",
            "face_value",
            "coupon_cashflow",
            "principal_cashflow",
            "total_cashflow",
        ]
    ]
