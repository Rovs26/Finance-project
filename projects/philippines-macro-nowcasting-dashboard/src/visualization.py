"""Plotly visualization helpers for macroeconomic outputs."""

import plotly.express as px


DEFAULT_TEMPLATE = "plotly_white"


def plot_time_series(df, x_col, y_col, title):
    """Create a time-series line chart."""
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={x_col: "Date", y_col: y_col.replace("_", " ").title()},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    return fig


def plot_indicator_correlation(df):
    """Create a correlation heatmap for numeric indicators."""
    numeric_df = df.select_dtypes(include="number")
    correlation = numeric_df.corr()
    fig = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Macro Indicator Correlation",
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    return fig


def plot_missingness_summary(df):
    """Create a bar chart of missing values by column."""
    missing = (
        df.isna()
        .sum()
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_values"})
    )
    fig = px.bar(
        missing,
        x="column",
        y="missing_values",
        title="Missing Values by Column",
        labels={"column": "Column", "missing_values": "Missing values"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=80))
    return fig
