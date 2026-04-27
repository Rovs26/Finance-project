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
