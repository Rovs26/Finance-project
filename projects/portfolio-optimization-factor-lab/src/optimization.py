"""Portfolio optimization utilities."""

import contextlib
import io
import warnings

import numpy as np
import pandas as pd


LAST_OPTIMIZATION_STATUS = {
    "minimum_volatility": "not_run",
    "maximum_sharpe": "not_run",
}


def load_returns(path):
    """Load saved daily return data with a date index."""
    return pd.read_csv(path, parse_dates=["date"], index_col="date")


def select_asset_returns(returns, benchmark="SPY"):
    """Select asset return columns and exclude the benchmark if present."""
    if benchmark in returns.columns:
        return returns.drop(columns=[benchmark]).dropna(how="all")
    return returns.dropna(how="all")


def annualize_expected_returns(returns, periods_per_year=252):
    """Calculate annualized compounded expected returns from daily returns."""
    clean_returns = returns.dropna(how="all")
    periods = clean_returns.count()
    compounded = (1 + clean_returns).prod(skipna=True)
    return compounded.pow(periods_per_year / periods) - 1


def annualize_covariance(returns, periods_per_year=252):
    """Calculate annualized covariance matrix from daily returns."""
    return returns.cov() * periods_per_year


def portfolio_return(weights, expected_returns):
    """Calculate portfolio expected return."""
    return float(np.dot(np.asarray(weights), np.asarray(expected_returns)))


def portfolio_volatility(weights, covariance_matrix):
    """Calculate portfolio volatility."""
    weights = np.asarray(weights)
    covariance_values = np.asarray(covariance_matrix)
    return float(np.sqrt(weights.T @ covariance_values @ weights))


def portfolio_sharpe(weights, expected_returns, covariance_matrix, risk_free_rate=0.0):
    """Calculate portfolio Sharpe ratio."""
    volatility = portfolio_volatility(weights, covariance_matrix)
    if np.isclose(volatility, 0.0):
        return np.nan
    return (portfolio_return(weights, expected_returns) - risk_free_rate) / volatility


def equal_weight_portfolio(asset_names):
    """Create equal weights for a list of asset names."""
    n_assets = len(asset_names)
    if n_assets == 0:
        raise ValueError("At least one asset is required.")
    return np.repeat(1 / n_assets, n_assets)


def _get_scipy_minimize():
    """Return scipy.optimize.minimize if available in the local environment."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with contextlib.redirect_stderr(io.StringIO()):
                from scipy.optimize import minimize

        return minimize, None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def _normalize_weights(weights, bounds):
    """Clip and normalize weights to long-only bounds."""
    lower, upper = bounds
    clipped = np.clip(weights, lower, upper)
    total = clipped.sum()
    if np.isclose(total, 0.0):
        return np.repeat(1 / len(clipped), len(clipped))
    return clipped / total


def _random_search_weights(
    expected_returns,
    covariance_matrix,
    objective,
    n_portfolios=50000,
    risk_free_rate=0.0,
    random_state=42,
):
    """Find weights with a deterministic random search fallback."""
    random_portfolios = generate_random_portfolios(
        expected_returns,
        covariance_matrix,
        n_portfolios=n_portfolios,
        risk_free_rate=risk_free_rate,
        random_state=random_state,
    )
    if objective == "min_volatility":
        selected = random_portfolios.sort_values("annualized_volatility").iloc[0]
    elif objective == "max_sharpe":
        selected = random_portfolios.sort_values("sharpe_ratio", ascending=False).iloc[0]
    else:
        raise ValueError(f"Unsupported objective: {objective}")
    weight_columns = [col for col in random_portfolios.columns if col.startswith("weight_")]
    return selected[weight_columns].to_numpy(dtype=float)


def minimum_volatility_portfolio(
    expected_returns, covariance_matrix, bounds=(0.0, 1.0)
):
    """Calculate long-only minimum-volatility portfolio weights."""
    global LAST_OPTIMIZATION_STATUS

    expected_returns = pd.Series(expected_returns)
    n_assets = len(expected_returns)
    initial_weights = equal_weight_portfolio(expected_returns.index)
    constraints = ({"type": "eq", "fun": lambda weights: np.sum(weights) - 1},)
    scipy_bounds = tuple(bounds for _ in range(n_assets))

    minimize, import_error = _get_scipy_minimize()
    if minimize is not None:
        result = minimize(
            lambda weights: portfolio_volatility(weights, covariance_matrix),
            initial_weights,
            method="SLSQP",
            bounds=scipy_bounds,
            constraints=constraints,
        )
        if result.success:
            LAST_OPTIMIZATION_STATUS["minimum_volatility"] = "scipy_slsqp_success"
            return _normalize_weights(result.x, bounds)
        LAST_OPTIMIZATION_STATUS["minimum_volatility"] = (
            f"scipy_slsqp_failed: {result.message}; used random_search_fallback"
        )
    else:
        LAST_OPTIMIZATION_STATUS["minimum_volatility"] = (
            f"scipy_unavailable: {import_error}; used random_search_fallback"
        )

    return _random_search_weights(
        expected_returns,
        covariance_matrix,
        objective="min_volatility",
        risk_free_rate=0.0,
        random_state=42,
    )


def maximum_sharpe_portfolio(
    expected_returns,
    covariance_matrix,
    risk_free_rate=0.0,
    bounds=(0.0, 1.0),
):
    """Calculate long-only maximum-Sharpe portfolio weights."""
    global LAST_OPTIMIZATION_STATUS

    expected_returns = pd.Series(expected_returns)
    n_assets = len(expected_returns)
    initial_weights = equal_weight_portfolio(expected_returns.index)
    constraints = ({"type": "eq", "fun": lambda weights: np.sum(weights) - 1},)
    scipy_bounds = tuple(bounds for _ in range(n_assets))

    minimize, import_error = _get_scipy_minimize()
    if minimize is not None:
        result = minimize(
            lambda weights: -portfolio_sharpe(
                weights, expected_returns, covariance_matrix, risk_free_rate
            ),
            initial_weights,
            method="SLSQP",
            bounds=scipy_bounds,
            constraints=constraints,
        )
        if result.success:
            LAST_OPTIMIZATION_STATUS["maximum_sharpe"] = "scipy_slsqp_success"
            return _normalize_weights(result.x, bounds)
        LAST_OPTIMIZATION_STATUS["maximum_sharpe"] = (
            f"scipy_slsqp_failed: {result.message}; used random_search_fallback"
        )
    else:
        LAST_OPTIMIZATION_STATUS["maximum_sharpe"] = (
            f"scipy_unavailable: {import_error}; used random_search_fallback"
        )

    return _random_search_weights(
        expected_returns,
        covariance_matrix,
        objective="max_sharpe",
        risk_free_rate=risk_free_rate,
        random_state=99,
    )


def generate_random_portfolios(
    expected_returns,
    covariance_matrix,
    n_portfolios=5000,
    risk_free_rate=0.0,
    random_state=42,
):
    """Generate random long-only portfolios for risk-return analysis."""
    expected_returns = pd.Series(expected_returns)
    rng = np.random.default_rng(random_state)
    raw_weights = rng.dirichlet(np.ones(len(expected_returns)), size=n_portfolios)

    rows = []
    for weights in raw_weights:
        annual_return = portfolio_return(weights, expected_returns)
        annual_volatility = portfolio_volatility(weights, covariance_matrix)
        sharpe_ratio = portfolio_sharpe(
            weights, expected_returns, covariance_matrix, risk_free_rate
        )
        row = {
            "annualized_return": annual_return,
            "annualized_volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio,
        }
        row.update(
            {
                f"weight_{asset}": weight
                for asset, weight in zip(expected_returns.index, weights)
            }
        )
        rows.append(row)

    return pd.DataFrame(rows)


def summarize_portfolio(
    name, weights, expected_returns, covariance_matrix, risk_free_rate=0.0
):
    """Summarize return, volatility, and Sharpe ratio for a portfolio."""
    return {
        "portfolio": name,
        "annualized_return": portfolio_return(weights, expected_returns),
        "annualized_volatility": portfolio_volatility(weights, covariance_matrix),
        "sharpe_ratio": portfolio_sharpe(
            weights, expected_returns, covariance_matrix, risk_free_rate
        ),
    }
