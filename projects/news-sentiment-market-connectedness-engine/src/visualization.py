"""Plotly visualization helpers for project audit outputs."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def _write_or_return(fig, output_path=None):
    if output_path is not None:
        fig.write_image(str(output_path))
    return fig


def plot_row_counts_by_source(summary_df, output_path=None):
    """Plot row counts by available data source."""
    fig = px.bar(
        summary_df,
        x="dataset",
        y="rows",
        color="status" if "status" in summary_df.columns else None,
        title="Audit Row Counts by Source",
        labels={"dataset": "Dataset", "rows": "Rows"},
    )
    fig.update_layout(template="plotly_white", xaxis_tickangle=-25, margin=dict(l=40, r=30, t=70, b=90))
    return _write_or_return(fig, output_path)


def plot_sentiment_distribution(df, output_path=None):
    """Plot distribution for a detected sentiment label or score column."""
    candidates = [col for col in df.columns if "sentiment" in str(col).lower()]
    if not candidates:
        return None
    col = candidates[0]
    if pd.api.types.is_numeric_dtype(df[col]):
        fig = px.histogram(df, x=col, nbins=20, title="Sentiment Score Distribution")
    else:
        counts = df[col].fillna("missing").value_counts().reset_index()
        counts.columns = [col, "count"]
        fig = px.bar(counts, x=col, y="count", title="Sentiment Label Distribution")
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=30, t=70, b=70))
    return _write_or_return(fig, output_path)


def plot_records_over_time(df, output_path=None):
    """Plot record counts over time using the first date-like column."""
    date_cols = [col for col in df.columns if "date" in str(col).lower() or "time" in str(col).lower()]
    if not date_cols:
        return None
    dated = df.copy()
    dated["audit_date"] = pd.to_datetime(dated[date_cols[0]], errors="coerce").dt.date
    counts = dated.groupby("audit_date", dropna=True).size().reset_index(name="record_count")
    if counts.empty:
        return None
    fig = px.line(counts, x="audit_date", y="record_count", markers=True, title="Records Over Time")
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=30, t=70, b=70))
    return _write_or_return(fig, output_path)
