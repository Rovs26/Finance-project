# Research Memo: Portfolio Optimization and Factor Research Lab

## Executive Summary

This project analyzes a large-cap U.S. equity universe, estimates market sensitivity versus SPY, builds simple long-only portfolios, and compares fixed-weight historical performance. The maximum-Sharpe portfolio produced the strongest historical risk-adjusted result, while the minimum-volatility portfolio produced the least severe drawdown among the portfolio strategies.

## Asset Universe

The asset universe includes AAPL, MSFT, JPM, PG, XOM, JNJ, KO, and NVDA.

## Benchmark

SPY is used as the benchmark for return comparison, CAPM-style sensitivity analysis, and backtest interpretation. SPY is excluded from optimized portfolios.

## Methods

- Downloaded public adjusted close prices using Yahoo Finance through `yfinance`.
- Calculated daily returns, monthly returns, cumulative returns, volatility, Sharpe ratio, drawdowns, and correlations.
- Estimated CAPM-style beta, alpha, benchmark correlation, tracking error, and 126-day rolling beta versus SPY.
- Built equal-weight, minimum-volatility, and maximum-Sharpe long-only portfolios.
- Ran a fixed-weight historical backtest using the Phase 3 strategy weights.

## CAPM and Factor Findings

- NVDA had the highest beta at approximately 1.82, indicating the strongest market sensitivity versus SPY.
- JNJ had the lowest beta at approximately 0.42, indicating more defensive behavior versus SPY.
- MSFT had the highest benchmark correlation at approximately 0.79.
- Local statsmodels/SciPy compatibility issues required a NumPy fallback for single-index regression, so p-values were not produced.

## Optimization Findings

- Equal-weight portfolio: approximately 24.69 percent annualized return and 1.27 Sharpe ratio in the Phase 3 summary.
- Minimum-volatility portfolio: approximately 15.89 percent annualized volatility.
- Maximum-Sharpe portfolio: approximately 43.58 percent annualized return and 1.56 Sharpe ratio in the Phase 3 summary.
- Minimum-volatility weights leaned toward JNJ, KO, and PG.
- Maximum-Sharpe weights leaned toward NVDA and JNJ, creating stronger concentration risk.

## Backtest Findings

- Maximum-Sharpe strategy: 1,427.59 percent cumulative return, 45.32 percent annualized return, 27.89 percent volatility, and 1.63 Sharpe ratio.
- Equal-weight strategy: 460.25 percent cumulative return, 26.65 percent annualized return, 19.38 percent volatility, and 1.37 Sharpe ratio.
- Minimum-volatility strategy: 177.08 percent cumulative return, 15.00 percent annualized return, 15.89 percent volatility, and 0.94 Sharpe ratio.
- SPY benchmark: 217.99 percent cumulative return, 17.19 percent annualized return, 19.57 percent volatility, and 0.88 Sharpe ratio.
- Minimum-volatility had the least severe drawdown among the portfolio strategies at approximately -30.26 percent.

## Business Interpretation

The project shows the tradeoff between growth exposure, diversification, and downside control. Maximum-Sharpe performed best historically but was more concentrated and more exposed to high-return assets. Equal-weight was simple, diversified, and performed strongly. Minimum-volatility reduced drawdown but gave up upside. For finance roles, the project demonstrates how to turn market data into risk metrics, portfolio decisions, and business-readable interpretation.

## Limitations

- The backtest uses fixed weights estimated from the full historical sample.
- No walk-forward validation, transaction costs, rebalancing schedule, taxes, or liquidity constraints are included.
- Historical returns and optimized weights can overfit past market behavior.
- Results are not investment advice.

## Next Improvements

- Add walk-forward optimization and periodic rebalancing.
- Include transaction costs, turnover, and active return metrics.
- Add richer factor data beyond SPY.
- Add optional screenshots or a lightweight dashboard after GitHub polish.
