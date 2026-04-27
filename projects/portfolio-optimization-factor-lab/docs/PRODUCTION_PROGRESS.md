# Production Progress

## Phase 0: Setup

Status: Done

- Created starter repository structure.
- Added placeholder notebooks.
- Added placeholder source modules.
- Added starter reports and docs.

## Phase 1: Market Data and Returns

Status: Done

- Used ticker universe: AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA.
- Used SPY as benchmark.
- Downloaded adjusted close prices from Yahoo Finance through `yfinance`.
- Calculated daily returns, monthly returns, annualized performance metrics, drawdowns, and correlations.
- Saved Phase 1 CSV outputs and figure files.

## Phase 2: CAPM and Factor Research

Status: Done

- Estimated CAPM beta and alpha against SPY.
- Ran single-index regression workflow with NumPy fallback because statsmodels is unavailable in the local environment.
- Calculated 126-day rolling beta.
- Saved CAPM metrics, regression output, rolling beta, factor summary, and Phase 2 figures.

## Phase 3: Portfolio Optimization

Status: Done

- Built equal-weight, minimum-volatility, and maximum-Sharpe portfolios.
- Excluded SPY from optimized asset portfolios.
- Generated random long-only portfolios for efficient frontier-style analysis.
- Saved portfolio weights, portfolio summary, random portfolios, and Phase 3 figures.
- Used deterministic random-search fallback because local `scipy.optimize` is unavailable.

## Phase 4: Backtesting and Interpretation

Status: Done

- Backtested fixed Phase 3 strategy weights over the full available return period.
- Compared equal-weight, minimum-volatility, maximum-Sharpe, and SPY.
- Calculated cumulative return, annualized return, volatility, Sharpe ratio, drawdown, best day, worst day, and correlation to SPY.
- Saved backtest outputs, figures, and research memo.

## Phase 5: GitHub Polish

Status: Next

- Clean README and reports.
- Prepare career-facing materials.
- Keep assumptions and limitations visible.
