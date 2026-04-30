"""Visualization helpers for fixed-income Phase 0 outputs."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def _apply_style(ax, title, xlabel=None, ylabel=None):
    """Apply a simple report-friendly chart style."""
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    return ax


def plot_bond_prices_by_rating(pricing_results):
    """Plot average clean price per 100 by credit rating."""
    summary = (
        pricing_results.groupby("credit_rating", as_index=False)["clean_price_per_100"]
        .mean()
        .sort_values("clean_price_per_100", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(summary["credit_rating"], summary["clean_price_per_100"], color="#2563eb")
    _apply_style(ax, "Average Bond Price by Rating", "Clean price per 100")
    fig.tight_layout()
    return fig


def plot_portfolio_market_value_by_sector(pricing_results):
    """Plot total market value by sector."""
    summary = (
        pricing_results.groupby("sector", as_index=False)["market_value"]
        .sum()
        .sort_values("market_value", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(summary["sector"], summary["market_value"], color="#059669")
    _apply_style(ax, "Portfolio Market Value by Sector", "Market value")
    fig.tight_layout()
    return fig


def plot_cashflow_schedule(cashflow_table):
    """Plot aggregate portfolio cash flows by year."""
    data = cashflow_table.copy()
    data["cashflow_year"] = pd.to_datetime(data["cashflow_date"]).dt.year
    summary = data.groupby("cashflow_year", as_index=False)["total_cashflow"].sum()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(summary["cashflow_year"].astype(str), summary["total_cashflow"], color="#7c3aed")
    _apply_style(ax, "Aggregate Bond Cash Flow Schedule", "Year", "Total cash flow")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def plot_price_vs_yield(yield_grid, price_grid):
    """Plot one bond's price sensitivity across yield levels."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pd.Series(yield_grid) * 100, price_grid, color="#dc2626", linewidth=2)
    _apply_style(ax, "Price vs Yield Example", "Yield (%)", "Model price")
    fig.tight_layout()
    return fig
