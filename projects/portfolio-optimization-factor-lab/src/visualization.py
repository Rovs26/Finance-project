"""Plotly visualization helpers for market research outputs."""

import plotly.express as px


DEFAULT_TEMPLATE = "plotly_white"


def plot_price_history(prices):
    """Create a line chart of adjusted close prices."""
    fig = px.line(
        prices,
        x=prices.index,
        y=prices.columns,
        title="Adjusted Close Price History",
        labels={"value": "Adjusted close price", "variable": "Ticker", "date": "Date"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(legend_title_text="Ticker", margin=dict(l=40, r=20, t=60, b=40))
    return fig


def plot_cumulative_returns(returns):
    """Create a line chart of cumulative returns."""
    cumulative_returns = (1 + returns.fillna(0)).cumprod() - 1
    fig = px.line(
        cumulative_returns,
        x=cumulative_returns.index,
        y=cumulative_returns.columns,
        title="Cumulative Returns",
        labels={"value": "Cumulative return", "variable": "Ticker", "date": "Date"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(legend_title_text="Ticker", margin=dict(l=40, r=20, t=60, b=40))
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_correlation_heatmap(returns):
    """Create a heatmap of return correlations."""
    correlation_matrix = returns.corr()
    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Daily Return Correlation Matrix",
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    return fig


def plot_risk_return_scatter(summary_df):
    """Create a risk-return scatter plot from an asset performance summary."""
    plot_df = summary_df.reset_index()
    plot_df = plot_df.rename(columns={plot_df.columns[0]: "ticker"})
    fig = px.scatter(
        plot_df,
        x="annualized_volatility",
        y="annualized_return",
        text="ticker",
        hover_name="ticker",
        title="Annualized Risk and Return",
        labels={
            "annualized_volatility": "Annualized volatility",
            "annualized_return": "Annualized return",
        },
        template=DEFAULT_TEMPLATE,
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_factor_bar(factor_df, value_col, title, y_axis_title=None):
    """Create a bar chart for a factor metric by asset."""
    plot_df = factor_df.reset_index()
    plot_df = plot_df.rename(columns={plot_df.columns[0]: "ticker"})
    fig = px.bar(
        plot_df,
        x="ticker",
        y=value_col,
        title=title,
        labels={"ticker": "Ticker", value_col: y_axis_title or value_col},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40), showlegend=False)
    return fig


def plot_rolling_beta(rolling_beta, selected_assets=None):
    """Create a line chart of rolling beta by asset."""
    if selected_assets is not None:
        available_assets = [asset for asset in selected_assets if asset in rolling_beta.columns]
        plot_data = rolling_beta[available_assets]
    else:
        plot_data = rolling_beta

    fig = px.line(
        plot_data,
        x=plot_data.index,
        y=plot_data.columns,
        title="126-Day Rolling Beta vs SPY",
        labels={"value": "Rolling beta", "variable": "Ticker", "date": "Date"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(legend_title_text="Ticker", margin=dict(l=40, r=20, t=60, b=40))
    return fig


def plot_portfolio_weights(weights_df):
    """Create a grouped bar chart comparing portfolio weights by asset."""
    plot_df = weights_df.melt(
        id_vars="asset", var_name="portfolio", value_name="weight"
    )
    fig = px.bar(
        plot_df,
        x="asset",
        y="weight",
        color="portfolio",
        barmode="group",
        title="Portfolio Weight Comparison",
        labels={"asset": "Asset", "weight": "Weight", "portfolio": "Portfolio"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_efficient_frontier_simulation(random_portfolios, portfolio_summary=None):
    """Create a risk-return scatter plot for simulated random portfolios."""
    fig = px.scatter(
        random_portfolios,
        x="annualized_volatility",
        y="annualized_return",
        color="sharpe_ratio",
        color_continuous_scale="Viridis",
        title="Random Portfolio Risk-Return Simulation",
        labels={
            "annualized_volatility": "Annualized volatility",
            "annualized_return": "Annualized return",
            "sharpe_ratio": "Sharpe ratio",
        },
        template=DEFAULT_TEMPLATE,
    )
    if portfolio_summary is not None:
        fig.add_scatter(
            x=portfolio_summary["annualized_volatility"],
            y=portfolio_summary["annualized_return"],
            mode="markers+text",
            text=portfolio_summary["portfolio"],
            textposition="top center",
            marker=dict(size=12, color="red", symbol="diamond"),
            name="Selected portfolios",
        )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_portfolio_risk_return(summary_df):
    """Create a risk-return comparison chart for named portfolios."""
    fig = px.scatter(
        summary_df,
        x="annualized_volatility",
        y="annualized_return",
        text="portfolio",
        hover_name="portfolio",
        size="sharpe_ratio",
        title="Portfolio Risk-Return Comparison",
        labels={
            "annualized_volatility": "Annualized volatility",
            "annualized_return": "Annualized return",
            "sharpe_ratio": "Sharpe ratio",
        },
        template=DEFAULT_TEMPLATE,
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_allocation_pie_or_bar(weights_df, portfolio_col):
    """Create a bar chart for one portfolio allocation."""
    fig = px.bar(
        weights_df.sort_values(portfolio_col, ascending=False),
        x="asset",
        y=portfolio_col,
        title=f"{portfolio_col.replace('_', ' ').title()} Allocation",
        labels={"asset": "Asset", portfolio_col: "Weight"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40), showlegend=False)
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_backtest_cumulative_returns(cumulative_returns):
    """Create a cumulative return comparison chart for backtested strategies."""
    fig = px.line(
        cumulative_returns,
        x=cumulative_returns.index,
        y=cumulative_returns.columns,
        title="Backtest Cumulative Returns",
        labels={"value": "Cumulative return", "variable": "Strategy", "date": "Date"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(legend_title_text="Strategy", margin=dict(l=40, r=20, t=60, b=40))
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_backtest_drawdowns(drawdowns):
    """Create a drawdown comparison chart for backtested strategies."""
    fig = px.line(
        drawdowns,
        x=drawdowns.index,
        y=drawdowns.columns,
        title="Backtest Drawdown Comparison",
        labels={"value": "Drawdown", "variable": "Strategy", "date": "Date"},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(legend_title_text="Strategy", margin=dict(l=40, r=20, t=60, b=40))
    fig.update_yaxes(tickformat=".0%")
    return fig


def plot_backtest_metric_comparison(metrics_df, metric_col, title):
    """Create a bar chart comparing one backtest metric across strategies."""
    fig = px.bar(
        metrics_df,
        x="strategy",
        y=metric_col,
        title=title,
        labels={"strategy": "Strategy", metric_col: metric_col.replace("_", " ").title()},
        template=DEFAULT_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40), showlegend=False)
    if metric_col != "sharpe_ratio":
        fig.update_yaxes(tickformat=".0%")
    return fig
