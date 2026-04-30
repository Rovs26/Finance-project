"""
Visualization utilities for the Finance Data Engineering Stack.

Uses Plotly only (no Matplotlib dependency).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def plot_price_history(
    prices: pd.DataFrame,
    title: str = "Adjusted Close Prices",
    save_path: Path | None = None,
) -> go.Figure:
    """Line chart of adjusted close prices for all tickers."""
    fig = go.Figure()
    for ticker in prices.columns:
        fig.add_trace(
            go.Scatter(
                x=prices.index,
                y=prices[ticker],
                mode="lines",
                name=ticker,
                line=dict(width=1.5),
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Adjusted Close (USD)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=440,
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
    )
    if save_path is not None:
        fig.write_html(str(save_path))
    return fig


def plot_return_distribution(
    returns: pd.DataFrame,
    title: str = "Daily Return Distribution",
    save_path: Path | None = None,
) -> go.Figure:
    """Box plot of daily return distributions per ticker."""
    long = (
        returns.reset_index()
        .melt(id_vars="date", var_name="ticker", value_name="daily_return")
        .dropna(subset=["daily_return"])
    )
    fig = px.box(
        long,
        x="ticker",
        y="daily_return",
        title=title,
        labels={"daily_return": "Daily Return", "ticker": "Ticker"},
        color="ticker",
    )
    fig.update_layout(
        showlegend=False,
        height=400,
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
    )
    if save_path is not None:
        fig.write_html(str(save_path))
    return fig


def plot_missing_heatmap(
    prices: pd.DataFrame,
    title: str = "Price Data Missingness",
    save_path: Path | None = None,
) -> go.Figure:
    """Heatmap showing missing values across tickers and time."""
    missing_matrix = prices.isnull().astype(int)
    fig = px.imshow(
        missing_matrix.T,
        aspect="auto",
        color_continuous_scale=["#f0f4ff", "#dc2626"],
        title=title,
        labels=dict(x="Date", y="Ticker", color="Missing"),
    )
    fig.update_layout(height=300, paper_bgcolor="white")
    if save_path is not None:
        fig.write_html(str(save_path))
    return fig
