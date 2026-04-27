"""CAPM and single-index factor research utilities."""

import contextlib
import io

import numpy as np
import pandas as pd

from src.returns import calculate_annualized_volatility


def _annualized_return(return_series, periods_per_year=252):
    """Calculate annualized compounded return for one return series."""
    clean_returns = return_series.dropna()
    if clean_returns.empty:
        return np.nan
    compounded = (1 + clean_returns).prod()
    return compounded ** (periods_per_year / len(clean_returns)) - 1


def load_returns(path):
    """Load saved return data with a date index."""
    return pd.read_csv(path, parse_dates=["date"], index_col="date")


def split_assets_and_benchmark(returns, benchmark="SPY"):
    """Split a returns DataFrame into asset returns and benchmark returns."""
    if benchmark not in returns.columns:
        raise KeyError(f"Benchmark column '{benchmark}' was not found in returns data.")

    benchmark_returns = returns[benchmark].dropna()
    asset_returns = returns.drop(columns=[benchmark])
    aligned = asset_returns.join(benchmark_returns.rename(benchmark), how="inner")
    return aligned.drop(columns=[benchmark]), aligned[benchmark]


def calculate_capm_metrics(
    asset_returns, benchmark_returns, risk_free_rate=0.0, periods_per_year=252
):
    """Calculate CAPM-style beta, alpha, correlation, and tracking metrics."""
    rows = []
    benchmark_returns = benchmark_returns.dropna()
    benchmark_annual_return = _annualized_return(
        benchmark_returns, periods_per_year=periods_per_year
    )
    benchmark_excess = benchmark_returns - (risk_free_rate / periods_per_year)
    benchmark_variance = benchmark_excess.var()

    for ticker in asset_returns.columns:
        joined = pd.concat(
            [asset_returns[ticker].rename("asset"), benchmark_returns.rename("benchmark")],
            axis=1,
        ).dropna()
        asset_excess = joined["asset"] - (risk_free_rate / periods_per_year)
        benchmark_excess_aligned = joined["benchmark"] - (risk_free_rate / periods_per_year)

        beta = asset_excess.cov(benchmark_excess_aligned) / benchmark_variance
        annual_return = _annualized_return(
            joined["asset"], periods_per_year=periods_per_year
        )
        annual_volatility = calculate_annualized_volatility(
            joined["asset"], periods_per_year=periods_per_year
        )
        correlation = joined["asset"].corr(joined["benchmark"])
        expected_return_capm = risk_free_rate + beta * (
            benchmark_annual_return - risk_free_rate
        )
        tracking_error = calculate_annualized_volatility(
            joined["asset"] - joined["benchmark"], periods_per_year=periods_per_year
        )

        rows.append(
            {
                "ticker": ticker,
                "beta": beta,
                "alpha": annual_return - expected_return_capm,
                "annualized_return": annual_return,
                "annualized_volatility": annual_volatility,
                "correlation_to_benchmark": correlation,
                "r_squared": correlation**2,
                "expected_return_capm": expected_return_capm,
                "tracking_error": tracking_error,
            }
        )

    return pd.DataFrame(rows).set_index("ticker").sort_values("beta", ascending=False)


def run_single_index_regression(asset_returns, benchmark_returns):
    """Run daily single-index regressions of each asset against the benchmark."""
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            import statsmodels.api as sm

        use_statsmodels = True
    except Exception:
        sm = None
        use_statsmodels = False

    rows = []
    for ticker in asset_returns.columns:
        joined = pd.concat(
            [asset_returns[ticker].rename("asset"), benchmark_returns.rename("benchmark")],
            axis=1,
        ).dropna()

        if use_statsmodels:
            x = sm.add_constant(joined["benchmark"])
            model = sm.OLS(joined["asset"], x).fit()
            alpha = model.params.get("const", np.nan)
            beta = model.params.get("benchmark", np.nan)
            alpha_pvalue = model.pvalues.get("const", np.nan)
            beta_pvalue = model.pvalues.get("benchmark", np.nan)
            r_squared = model.rsquared
            residual_volatility = model.resid.std() * np.sqrt(252)
            method = "statsmodels_ols"
        else:
            x = joined["benchmark"].to_numpy()
            y = joined["asset"].to_numpy()
            beta, alpha = np.polyfit(x, y, 1)
            alpha_pvalue = np.nan
            beta_pvalue = np.nan
            r_squared = np.nan
            residual_volatility = np.nan
            method = "numpy_polyfit_fallback"

        rows.append(
            {
                "ticker": ticker,
                "alpha_daily": alpha,
                "alpha_annualized_simple": alpha * 252,
                "beta": beta,
                "alpha_pvalue": alpha_pvalue,
                "beta_pvalue": beta_pvalue,
                "r_squared": r_squared,
                "residual_volatility": residual_volatility,
                "method": method,
            }
        )

    return pd.DataFrame(rows).set_index("ticker").sort_values("beta", ascending=False)


def calculate_rolling_beta(asset_returns, benchmark_returns, window=126):
    """Calculate rolling beta for each asset using a rolling covariance approach."""
    rolling_betas = pd.DataFrame(index=asset_returns.index)
    benchmark_variance = benchmark_returns.rolling(window=window).var()

    for ticker in asset_returns.columns:
        rolling_covariance = asset_returns[ticker].rolling(window=window).cov(
            benchmark_returns
        )
        rolling_betas[ticker] = rolling_covariance / benchmark_variance

    return rolling_betas.dropna(how="all")


def summarize_factor_results(capm_df, regression_df):
    """Combine CAPM metrics and single-index regression results into one summary."""
    regression_cols = regression_df[
        [
            "alpha_daily",
            "alpha_annualized_simple",
            "beta",
            "alpha_pvalue",
            "beta_pvalue",
            "r_squared",
            "residual_volatility",
            "method",
        ]
    ].rename(
        columns={
            "beta": "regression_beta",
            "r_squared": "regression_r_squared",
        }
    )
    summary = capm_df.join(regression_cols, how="left")
    return summary.sort_values("beta", ascending=False)
