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

Status: Next

- Define return and risk assumptions.
- Build initial portfolio optimization workflow.
- Compare equal weight, minimum volatility, and risk-return efficient allocations.

## Phase 4: Backtesting and Interpretation

Status: Not started

- Backtest allocation strategies.
- Interpret results in a research memo.

## Phase 5: GitHub Polish

Status: Not started

- Clean README and reports.
- Prepare career-facing materials.
