# Model Notes

## CAPM Assumptions

- Benchmark: SPY.
- Asset universe: AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA.
- Input data: `outputs/returns/daily_returns.csv`.
- Risk-free rate: 0.0 for the current portfolio research version.
- Beta is estimated from daily covariance versus SPY divided by SPY variance.
- Alpha is interpreted as historical return above the CAPM-implied return under the simplified assumptions.
- Rolling beta uses a 126-trading-day window.

## Optimization Assumptions

- SPY is excluded from optimized portfolios and used only as a benchmark.
- Expected returns are historical annualized compounded returns.
- Risk is based on the historical annualized covariance matrix.
- Strategies are long-only with 0 percent to 100 percent asset bounds.
- Portfolio weights sum to 100 percent.
- Strategies compared: equal-weight, minimum-volatility, and maximum-Sharpe.

## Backtest Assumptions

- Backtests use fixed Phase 3 weights over the full available return period.
- Strategy returns are calculated from daily asset returns and fixed weights.
- SPY is included as benchmark reference.
- No rebalancing schedule is modeled.
- No transaction costs, taxes, liquidity constraints, or turnover limits are included.
- The backtest is descriptive and not a production investment process.

## Environment Limitations

- The local Matplotlib installation has a NumPy compatibility issue, so plotting relies on Plotly helpers and Pillow fallback PNG exports.
- `statsmodels` could not be used because the local SciPy/statsmodels stack is incompatible with the installed NumPy version.
- `scipy.optimize` could not be imported because the local SciPy package expects older NumPy APIs.
- The optimization module attempts SciPy SLSQP first, then uses deterministic random-search fallback when SciPy is unavailable.
- Because of the statsmodels fallback, regression p-values and residual volatility are not available in the current outputs.

## Interpretation Cautions

- Historical returns do not imply future performance.
- Optimized portfolios can overfit unusually strong historical winners.
- Fixed-weight backtests are not walk-forward or out-of-sample validation.
- SPY is a practical benchmark proxy, not a complete multi-factor risk model.
- Results are research outputs for portfolio analytics demonstration, not investment advice.
