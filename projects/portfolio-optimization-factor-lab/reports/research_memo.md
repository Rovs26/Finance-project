# Research Memo: Portfolio Optimization and Factor Research Lab

## Executive Summary

This project analyzes a large-cap U.S. equity universe, estimates benchmark-relative risk, builds simple optimized portfolios, and evaluates fixed-weight historical performance against SPY. The best historical Sharpe ratio came from the maximum-Sharpe portfolio, while the minimum-volatility portfolio produced the least severe drawdown among the portfolio strategies.

## Asset Universe

- AAPL
- MSFT
- JPM
- PG
- XOM
- JNJ
- KO
- NVDA

## Benchmark

SPY is used as the benchmark reference for return comparison, CAPM analysis, and backtesting. SPY is not included as an optimized portfolio asset.

## Methods Used

- Downloaded adjusted close prices from Yahoo Finance.
- Calculated daily returns, monthly returns, annualized return, volatility, Sharpe ratio, drawdown, and correlations.
- Estimated CAPM-style beta, alpha, benchmark correlation, and rolling beta versus SPY.
- Built equal-weight, minimum-volatility, and maximum-Sharpe portfolios.
- Backtested fixed Phase 3 portfolio weights over the full available daily return history.

## CAPM and Factor Findings

- NVDA had the highest beta, approximately 1.82, indicating the strongest market sensitivity versus SPY.
- JNJ had the lowest beta, approximately 0.42, indicating more defensive behavior versus SPY.
- MSFT had the highest benchmark correlation, approximately 0.79.
- The single-index regression used a NumPy fallback because the local statsmodels/SciPy environment is incompatible with the installed NumPy version.

## Portfolio Optimization Findings

- Equal-weight portfolio annualized return: approximately 24.69 percent.
- Minimum-volatility portfolio annualized volatility: approximately 15.89 percent.
- Maximum-Sharpe portfolio Sharpe ratio: approximately 1.56 in the Phase 3 optimization summary.
- Minimum-volatility weights leaned toward JNJ, KO, and PG.
- Maximum-Sharpe weights leaned toward NVDA and JNJ.

## Backtest Findings

- Maximum-Sharpe strategy: 1,427.59 percent cumulative return, 45.32 percent annualized return, 27.89 percent volatility, and 1.63 Sharpe ratio.
- Equal-weight strategy: 460.25 percent cumulative return, 26.65 percent annualized return, 19.38 percent volatility, and 1.37 Sharpe ratio.
- Minimum-volatility strategy: 177.08 percent cumulative return, 15.00 percent annualized return, 15.89 percent volatility, and 0.94 Sharpe ratio.
- SPY benchmark: 217.99 percent cumulative return, 17.19 percent annualized return, 19.57 percent volatility, and 0.88 Sharpe ratio.
- Minimum-volatility had the least severe drawdown among the portfolio strategies at approximately -30.26 percent.

## Business Interpretation

The results show a clear risk-return tradeoff. The maximum-Sharpe allocation delivered the strongest historical performance, but it was more concentrated and more volatile. Equal weight offered strong performance with simple diversification. Minimum volatility reduced drawdown risk but gave up upside. For finance and investment analytics roles, this project demonstrates how to connect return analysis, factor sensitivity, portfolio construction, and backtest interpretation in a transparent workflow.

## Limitations

- The backtest uses fixed weights estimated from the full sample, so it is not an out-of-sample validation.
- No walk-forward optimization, transaction costs, taxes, turnover constraints, liquidity constraints, or rebalancing schedule are included.
- Historical expected returns and optimized weights can overfit past market behavior.
- Results are descriptive research outputs, not investment advice.

## Next Improvements

- Add walk-forward optimization and periodic rebalancing.
- Include transaction costs and turnover.
- Add benchmark-relative active return and tracking error attribution.
- Add factor data beyond SPY.
- Polish the repository for GitHub and recruiter readability.
