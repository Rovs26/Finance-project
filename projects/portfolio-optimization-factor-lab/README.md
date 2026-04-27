# Portfolio Optimization and Factor Research Lab

Python research project for analyzing public market data, asset returns, benchmark-relative performance, factor relationships, portfolio construction, and backtesting workflows.

## Business Problem

Investment, research, and finance teams need clear tools to analyze return drivers, compare assets against a benchmark, understand risk and drawdown, and explain portfolio choices using defensible assumptions.

## Target Roles and Companies

Target roles include investment analyst, financial data analyst, market research analyst, corporate finance analyst, risk analytics analyst, quantitative research intern, and fintech analytics analyst.

Target companies include JPMorgan Chase, MSCI, Wells Fargo, P&G Philippines, BPI, First Metro, ING Hubs Philippines, PwC, and other finance or analytics employers.

## Current Status

Phase 2 CAPM and single-index factor research is completed.

- Phase 0 setup: completed
- Phase 1 market data and returns: completed
- Phase 2 CAPM and factor research: completed
- Phase 3 portfolio optimization: next
- Phase 4 backtesting and interpretation: not started
- Phase 5 GitHub polish: not started

## Ticker Universe and Benchmark

Phase 1 uses public Yahoo Finance data through `yfinance`.

- Asset universe: `AAPL`, `MSFT`, `JPM`, `PG`, `XOM`, `JNJ`, `KO`, `NVDA`
- Benchmark: `SPY`
- Period: `2019-01-01` to latest available data at notebook execution

## Generated Phase 1 Outputs

Market data and return outputs:

- `data/processed/adjusted_close_prices.csv`
- `outputs/returns/daily_returns.csv`
- `outputs/returns/monthly_returns.csv`
- `outputs/returns/asset_performance_summary.csv`
- `outputs/returns/correlation_matrix.csv`

Figures:

- `reports/figures/price_history.png`
- `reports/figures/cumulative_returns.png`
- `reports/figures/correlation_heatmap.png`
- `reports/figures/risk_return_scatter.png`

## Generated Phase 2 Outputs

CAPM and single-index research outputs:

- `outputs/factors/capm_metrics.csv`
- `outputs/factors/single_index_regression.csv`
- `outputs/factors/rolling_beta.csv`
- `outputs/factors/factor_summary.csv`

Figures:

- `reports/figures/capm_beta_by_asset.png`
- `reports/figures/capm_alpha_by_asset.png`
- `reports/figures/benchmark_correlation_by_asset.png`
- `reports/figures/rolling_beta_selected_assets.png`

Key Phase 2 findings:

- Highest beta: `NVDA`, approximately `1.82`
- Lowest beta: `JNJ`, approximately `0.42`
- Highest benchmark correlation: `MSFT`, approximately `0.79`
- Phase 2 used a NumPy regression fallback because the local statsmodels/SciPy stack is incompatible with the installed NumPy version.

## Planned Methodology

1. Load public or manually supplied market data.
2. Calculate daily and monthly returns, annualized return, volatility, Sharpe ratio, drawdown, and correlations.
3. Compare asset performance against SPY.
4. Research CAPM and factor exposures.
5. Build simple portfolio optimization workflows.
6. Backtest portfolio allocations.
7. Interpret results through a research memo and career-ready project documentation.

## How to Run

Install requirements first:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the Phase 1 notebook:

```bash
jupyter nbconvert --to notebook --execute notebooks/01_market_data_and_returns.ipynb --output 01_market_data_and_returns_executed.ipynb
```

Run the Phase 2 notebook:

```bash
jupyter nbconvert --to notebook --execute notebooks/02_capm_factor_research.ipynb --output 02_capm_factor_research_executed.ipynb
```

Or open the notebook interactively:

```bash
jupyter notebook notebooks/01_market_data_and_returns.ipynb
```

## Repo Structure

```text
portfolio-optimization-factor-lab/
  data/
    raw/
    processed/
    external/
  notebooks/
    01_market_data_and_returns.ipynb
    02_capm_factor_research.ipynb
    03_portfolio_optimization.ipynb
    04_backtesting_and_interpretation.ipynb
  src/
    config.py
    data_loader.py
    returns.py
    factors.py
    optimization.py
    backtesting.py
    visualization.py
  reports/
    figures/
  outputs/
    returns/
    factors/
    portfolios/
    backtests/
  docs/
```

## Notes

No portfolio optimization, backtest, dashboard, or investment recommendation is included through Phase 2. Historical market data and CAPM estimates are descriptive and do not imply future performance.
