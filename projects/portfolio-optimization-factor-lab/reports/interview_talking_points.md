# Interview Talking Points

## 1. What is this project about?

It is a Python portfolio research project that analyzes market returns, CAPM sensitivity, portfolio optimization, and fixed-weight backtesting for eight large-cap U.S. equities versus SPY.

## 2. Why did you use SPY as the benchmark?

SPY is a practical broad U.S. equity market proxy. It provides a clear benchmark for beta, correlation, and strategy performance comparison.

## 3. What did CAPM add to the project?

CAPM helped explain market sensitivity. For example, NVDA had the highest beta, while JNJ behaved more defensively versus SPY.

## 4. What portfolio strategies did you compare?

I compared equal-weight, minimum-volatility, and maximum-Sharpe portfolios. Equal-weight is transparent, minimum-volatility focuses on risk control, and maximum-Sharpe maximizes historical risk-adjusted return.

## 5. Which strategy performed best?

The maximum-Sharpe strategy had the highest historical Sharpe ratio and cumulative return, but it was also more concentrated and should be interpreted cautiously.

## 6. What was the most defensive strategy?

The minimum-volatility strategy had the lowest volatility and least severe drawdown among the portfolio strategies.

## 7. What are the biggest limitations?

The backtest is fixed-weight and uses the same historical period that informed the optimization. It does not include walk-forward validation, transaction costs, taxes, or rebalancing.

## 8. How would you improve it?

I would add walk-forward optimization, periodic rebalancing, transaction costs, turnover analysis, and richer factor data beyond SPY.

## 9. What finance skills does this demonstrate?

It demonstrates market data handling, return analytics, CAPM interpretation, portfolio construction, backtesting, risk communication, and business-readable reporting.

## 10. What technical skills does this demonstrate?

It demonstrates Python, pandas, NumPy, Plotly, yfinance, notebook workflows, reusable modules, CSV outputs, and GitHub-ready documentation.
