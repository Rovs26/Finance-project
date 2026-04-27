# Model Notes

## Purpose of CAPM Analysis

Phase 2 estimates benchmark sensitivity for each asset in the project universe. The goal is to explain which securities behaved more aggressively or defensively relative to SPY before moving into portfolio optimization.

## Benchmark Used

- Benchmark: SPY
- Asset universe: AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA
- Input data: `outputs/returns/daily_returns.csv`
- Period: daily returns from 2019-01-03 through 2026-04-27

## Method Summary

- Calculated CAPM-style beta using daily covariance versus SPY divided by SPY variance.
- Calculated annualized return, annualized volatility, benchmark correlation, R-squared from correlation, CAPM expected return, alpha, and tracking error.
- Ran a single-index regression workflow for each asset against SPY.
- Used 126-trading-day rolling beta to review whether benchmark sensitivity was stable over time.

## Key Findings

- NVDA had the highest beta at approximately 1.82, making it the most aggressive asset relative to SPY in this sample.
- AAPL, MSFT, and JPM also had betas above 1.0, indicating above-market sensitivity.
- JNJ, PG, and KO had the lowest betas, making them more defensive relative to SPY in this single-index view.
- MSFT had the highest benchmark correlation among the selected assets, while JNJ had the lowest benchmark correlation.
- NVDA showed the highest annualized return and highest tracking error, meaning its return profile was meaningfully different from the benchmark.

## Limitations

- SPY is used as a broad market proxy, not a full multi-factor benchmark.
- The risk-free rate is set to zero for this phase.
- The local statsmodels/SciPy environment is incompatible with the installed NumPy version, so the notebook used the NumPy regression fallback.
- Because of the fallback, regression p-values and residual volatility were not produced in Phase 2.
- Results are historical and descriptive, not investment advice.

## Why This Matters for Finance Roles

This phase demonstrates benchmark-relative analysis, market sensitivity interpretation, and clear communication of risk drivers. These are useful skills for investment analytics, financial data analytics, market research, corporate finance, and risk analytics roles.

## Portfolio Optimization Purpose

Phase 3 builds simple portfolio construction outputs from the saved daily returns. The purpose is to compare transparent allocation approaches before moving into full backtesting.

## Portfolio Optimization Assumptions

- Input returns: `outputs/returns/daily_returns.csv`
- Asset universe: AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA
- Benchmark excluded from optimized portfolios: SPY
- Expected returns: historical annualized compounded returns
- Risk model: historical annualized covariance matrix
- Risk-free rate: 0.0
- Constraint: long-only weights
- Bounds: 0 percent to 100 percent per asset
- Weight sum: 100 percent

## Portfolio Definitions

- Equal-weight portfolio: allocates 12.5 percent to each of the eight assets.
- Minimum-volatility portfolio: searches for the long-only allocation with the lowest annualized volatility.
- Maximum-Sharpe portfolio: searches for the long-only allocation with the highest return-to-volatility ratio.
- Random portfolio simulation: generates random long-only portfolios to visualize the risk-return opportunity set.

## Phase 3 Key Findings

- Equal-weight portfolio: annualized return approximately 24.69 percent, annualized volatility approximately 19.38 percent, Sharpe ratio approximately 1.27.
- Minimum-volatility portfolio: annualized return approximately 13.80 percent, annualized volatility approximately 15.89 percent, Sharpe ratio approximately 0.87.
- Maximum-Sharpe portfolio: annualized return approximately 43.58 percent, annualized volatility approximately 27.89 percent, Sharpe ratio approximately 1.56.
- The minimum-volatility allocation leaned most heavily toward JNJ, KO, and PG.
- The maximum-Sharpe allocation leaned most heavily toward NVDA and JNJ, reflecting strong historical risk-adjusted behavior but also concentration risk.

## Phase 3 Limitations

- The local SciPy optimizer could not be imported because the installed SciPy package expects older NumPy APIs. The notebook used a deterministic random-search fallback.
- Historical expected returns are unstable and should not be treated as forecasts.
- No transaction costs, rebalancing rules, taxes, turnover constraints, or out-of-sample backtest are included yet.
- Optimization can overfit historical return assumptions, especially when one asset has unusually strong historical performance.

## Why Portfolio Optimization Matters for Finance Roles

This phase demonstrates allocation logic, risk-return tradeoff analysis, constraints, and interpretation of model limitations. These skills are relevant for investment analytics, corporate finance, financial data analytics, risk analytics, and market research roles.

## Backtesting Assumptions

- Input returns: `outputs/returns/daily_returns.csv`
- Input weights: `outputs/portfolios/portfolio_weights.csv`
- Strategies: equal_weight, minimum_volatility, maximum_sharpe
- Benchmark: SPY
- Method: fixed-weight historical backtest over the full available return period
- Rebalancing: not modeled
- Transaction costs: not modeled
- Taxes and turnover limits: not modeled

## Phase 4 Backtest Findings

- Maximum-Sharpe produced the highest fixed-weight historical cumulative return and Sharpe ratio.
- Equal-weight produced strong results with simpler diversification and the highest correlation to SPY among the portfolio strategies.
- Minimum-volatility produced the least severe drawdown among the portfolio strategies but had lower return than equal-weight and maximum-Sharpe.
- SPY was included as a benchmark reference only.

## Phase 4 Limitations

- The fixed-weight backtest is not a walk-forward or out-of-sample validation.
- Weights were estimated using the full sample, so results can overstate practical performance.
- No transaction costs, rebalancing assumptions, taxes, liquidity constraints, or live execution considerations are included.
- The backtest is intended for portfolio analytics demonstration, not investment recommendation.
