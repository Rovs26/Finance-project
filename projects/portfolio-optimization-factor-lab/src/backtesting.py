"""Fixed-weight portfolio backtesting utilities."""

import numpy as np
import pandas as pd


def load_returns(path):
    """Load saved daily return data with a date index."""
    return pd.read_csv(path, parse_dates=["date"], index_col="date")


def load_portfolio_weights(path):
    """Load portfolio weights with assets as rows and strategy names as columns."""
    return pd.read_csv(path)


def calculate_portfolio_returns(asset_returns, weights):
    """Calculate daily portfolio returns for a fixed-weight strategy."""
    aligned_weights = pd.Series(weights, index=asset_returns.columns).astype(float)
    return asset_returns.dot(aligned_weights)


def calculate_cumulative_returns(returns):
    """Calculate cumulative returns from simple periodic returns."""
    return (1 + returns.fillna(0)).cumprod() - 1


def calculate_drawdown_series(returns):
    """Calculate drawdown series from simple periodic returns."""
    wealth_index = (1 + returns.fillna(0)).cumprod()
    running_peak = wealth_index.cummax()
    return wealth_index / running_peak - 1


def calculate_backtest_metrics(returns, benchmark_returns=None, periods_per_year=252):
    """Calculate return, risk, drawdown, and benchmark-relative metrics."""
    clean_returns = returns.dropna()
    if clean_returns.empty:
        raise ValueError("Returns series is empty after dropping missing values.")

    cumulative_return = (1 + clean_returns).prod() - 1
    annualized_return = (1 + cumulative_return) ** (
        periods_per_year / len(clean_returns)
    ) - 1
    annualized_volatility = clean_returns.std() * np.sqrt(periods_per_year)
    sharpe_ratio = (
        annualized_return / annualized_volatility
        if not np.isclose(annualized_volatility, 0.0)
        else np.nan
    )
    drawdown = calculate_drawdown_series(clean_returns)

    metrics = {
        "cumulative_return": cumulative_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": drawdown.min(),
        "best_day": clean_returns.max(),
        "worst_day": clean_returns.min(),
        "correlation_to_spy": np.nan,
    }

    if benchmark_returns is not None:
        aligned = pd.concat(
            [clean_returns.rename("strategy"), benchmark_returns.rename("benchmark")],
            axis=1,
        ).dropna()
        if not aligned.empty:
            metrics["correlation_to_spy"] = aligned["strategy"].corr(aligned["benchmark"])

    return metrics


def build_strategy_return_table(asset_returns, weights_df, benchmark="SPY"):
    """Build daily returns for each fixed-weight strategy and optional benchmark."""
    if benchmark in asset_returns.columns:
        benchmark_returns = asset_returns[benchmark]
        investable_returns = asset_returns.drop(columns=[benchmark])
    else:
        benchmark_returns = None
        investable_returns = asset_returns

    strategy_returns = pd.DataFrame(index=investable_returns.index)
    for strategy in weights_df.columns:
        if strategy == "asset":
            continue
        weights = weights_df.set_index("asset")[strategy].reindex(investable_returns.columns)
        if weights.isna().any():
            missing_assets = weights[weights.isna()].index.tolist()
            raise ValueError(f"Missing weights for assets: {missing_assets}")
        strategy_returns[strategy] = calculate_portfolio_returns(
            investable_returns, weights
        )

    if benchmark_returns is not None:
        strategy_returns[benchmark] = benchmark_returns

    return strategy_returns.dropna(how="all")


def summarize_backtests(strategy_returns, benchmark_col="SPY"):
    """Summarize backtest metrics for each strategy and benchmark column."""
    benchmark_returns = (
        strategy_returns[benchmark_col] if benchmark_col in strategy_returns.columns else None
    )

    rows = []
    for strategy in strategy_returns.columns:
        comparison_benchmark = None if strategy == benchmark_col else benchmark_returns
        metrics = calculate_backtest_metrics(
            strategy_returns[strategy],
            benchmark_returns=comparison_benchmark,
        )
        metrics["strategy"] = strategy
        rows.append(metrics)

    columns = [
        "strategy",
        "cumulative_return",
        "annualized_return",
        "annualized_volatility",
        "sharpe_ratio",
        "max_drawdown",
        "best_day",
        "worst_day",
        "correlation_to_spy",
    ]
    return pd.DataFrame(rows)[columns].sort_values(
        "sharpe_ratio", ascending=False, na_position="last"
    )
