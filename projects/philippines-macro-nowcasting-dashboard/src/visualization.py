"""Plotly visualization helpers for macroeconomic outputs."""

import plotly.express as px
import plotly.graph_objects as go


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


def plot_actual_vs_forecast(df, date_col, actual_col, forecast_cols, title):
    """Plot actual inflation against one or more forecast series."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[date_col],
            y=df[actual_col],
            mode="lines",
            name="Actual",
            line=dict(color="#111827", width=3),
        )
    )
    colors = ["#2563eb", "#16a34a", "#dc2626", "#7c3aed"]
    for index, forecast_col in enumerate(forecast_cols):
        if forecast_col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df[date_col],
                    y=df[forecast_col],
                    mode="lines",
                    name=forecast_col.replace("_", " ").title(),
                    line=dict(color=colors[index % len(colors)], width=2),
                )
            )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Inflation rate",
        template=DEFAULT_TEMPLATE,
        margin=dict(l=40, r=20, t=60, b=40),
        legend_title_text="Series",
    )
    return fig


def plot_forecast_errors(df, date_col, error_cols, title):
    """Plot forecast errors over time."""
    fig = go.Figure()
    colors = ["#2563eb", "#16a34a", "#dc2626", "#7c3aed"]
    for index, error_col in enumerate(error_cols):
        if error_col in df.columns:
            fig.add_trace(
                go.Bar(
                    x=df[date_col],
                    y=df[error_col],
                    name=error_col.replace("_", " ").title(),
                    marker_color=colors[index % len(colors)],
                )
            )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Forecast error",
        template=DEFAULT_TEMPLATE,
        barmode="group",
        margin=dict(l=40, r=20, t=60, b=40),
        legend_title_text="Model",
    )
    return fig


def plot_forecast_metrics(metrics_df, metric_col="rmse"):
    """Compare forecast models by a selected metric."""
    fig = px.bar(
        metrics_df,
        x="model",
        y=metric_col,
        title=f"Forecast Model Comparison by {metric_col.upper()}",
        labels={"model": "Model", metric_col: metric_col.upper()},
        template=DEFAULT_TEMPLATE,
        color_discrete_sequence=["#2563eb"],
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=80), showlegend=False)
    return fig


def plot_latest_forecast_context(history_df, date_col, value_col, forecast_date, forecast_value):
    """Show recent inflation history with the latest one-month-ahead forecast."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=history_df[date_col],
            y=history_df[value_col],
            mode="lines+markers",
            name="Historical inflation",
            line=dict(color="#111827", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[forecast_date],
            y=[forecast_value],
            mode="markers",
            name="Latest forecast",
            marker=dict(color="#dc2626", size=12, symbol="diamond"),
        )
    )
    fig.update_layout(
        title="Latest One-Month-Ahead Inflation Forecast Context",
        xaxis_title="Date",
        yaxis_title="Inflation rate",
        template=DEFAULT_TEMPLATE,
        margin=dict(l=40, r=20, t=60, b=40),
        legend_title_text="Series",
    )
    return fig
