"""Return and risk metric utilities."""

import numpy as np
import pandas as pd


def calculate_daily_returns(prices):
    """Calculate simple daily returns from adjusted close prices."""
    return prices.sort_index().pct_change(fill_method=None).dropna(how="all")


def calculate_monthly_returns(prices):
    """Calculate month-end simple returns from adjusted close prices."""
    monthly_prices = prices.sort_index().resample("ME").last()
    return monthly_prices.pct_change(fill_method=None).dropna(how="all")


def calculate_annualized_return(returns, periods_per_year=252):
    """Calculate annualized compounded return for a return series or DataFrame."""
    clean_returns = returns.dropna(how="all")
    periods = clean_returns.count()
    compounded = (1 + clean_returns).prod(skipna=True)
    return compounded.pow(periods_per_year / periods) - 1


def calculate_annualized_volatility(returns, periods_per_year=252):
    """Calculate annualized volatility for a return series or DataFrame."""
    return returns.std(skipna=True) * np.sqrt(periods_per_year)


def calculate_sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
    """Calculate annualized Sharpe ratio using a constant annual risk-free rate."""
    annual_return = calculate_annualized_return(returns, periods_per_year=periods_per_year)
    annual_volatility = calculate_annualized_volatility(
        returns, periods_per_year=periods_per_year
    )
    excess_return = annual_return - risk_free_rate
    return excess_return / annual_volatility.replace(0, np.nan)


def calculate_max_drawdown(returns):
    """Calculate maximum drawdown for each return series."""
    cumulative_returns = (1 + returns.fillna(0)).cumprod()
    running_peak = cumulative_returns.cummax()
    drawdowns = cumulative_returns / running_peak - 1
    return drawdowns.min()


def summarize_asset_performance(returns):
    """Summarize annualized return, volatility, Sharpe ratio, and drawdown by asset."""
    summary = pd.DataFrame(
        {
            "annualized_return": calculate_annualized_return(returns),
            "annualized_volatility": calculate_annualized_volatility(returns),
            "sharpe_ratio": calculate_sharpe_ratio(returns),
            "max_drawdown": calculate_max_drawdown(returns),
        }
    )
    return summary.sort_values("annualized_return", ascending=False)
