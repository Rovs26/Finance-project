# Data Quality Report

## Executive Summary

Phase 1 added a reusable validation suite for the processed finance data tables created by the ingestion pipeline. The latest run completed `15` checks with `15` passes, `0` failures, and `0` warnings.

## Tables Validated

- `dim_assets`: asset dimension table with ticker metadata.
- `fact_prices`: long-format adjusted close price table.
- `fact_returns`: long-format daily return table.

## Validation Checks Performed

- Required column checks for all core tables.
- Unique ticker check for `dim_assets`.
- Duplicate composite key checks for `(date, ticker)` in price and return facts.
- Date range checks for fact tables.
- Missing value summaries for each table.
- Numeric range checks:
  - `fact_prices.adj_close > 0`
  - `fact_returns.daily_return` between `-1` and `1`
- Referential integrity checks:
  - `fact_prices.ticker` exists in `dim_assets.ticker`
  - `fact_returns.ticker` exists in `dim_assets.ticker`

## Latest Results

- Total checks: `15`
- Passed: `15`
- Failed: `0`
- Warnings: `0`
- Overall status: `PASS`

Date coverage:

- `fact_prices`: 2020-01-02 to 2026-04-29
- `fact_returns`: 2020-01-03 to 2026-04-29

## Key Findings

- All required schema fields are present.
- No duplicate ticker-date rows were found in the fact tables.
- No missing values were found in the dimension or fact tables.
- All price values are positive.
- Daily returns stayed within the configured reasonableness range.
- All fact table tickers are valid members of the asset dimension.

## Known Limitations

- Validation is batch-oriented and runs after ingestion, not as streaming or scheduled checks.
- Return thresholds are broad reasonableness rules, not market microstructure anomaly detection.
- Corporate action accuracy still depends on yfinance adjusted close methodology.
- The generated CSV summaries and DuckDB warehouse are ignored by Git and should be regenerated after cloning.

## Next Improvements

- Add data freshness checks by ticker.
- Add configurable warning thresholds for return outliers.
- Add schema tests in CI.
- Add validation trend logs across pipeline runs.
