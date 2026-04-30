# Data Quality Report

## Summary

The Phase 1 validation suite checks whether the finance data tables created by the ingestion pipeline are usable for SQL analysis. The latest run completed `15` checks with no failures or warnings.

## Validation Checks Performed

- Required columns in `dim_assets`, `fact_prices`, and `fact_returns`
- Unique ticker values in `dim_assets`
- No duplicate `(date, ticker)` keys in `fact_prices`
- No duplicate `(date, ticker)` keys in `fact_returns`
- Valid date ranges in price and return fact tables
- Missing value checks for all core tables
- Positive adjusted close prices
- Daily returns inside a broad reasonableness range of `-1` to `1`
- Referential integrity from fact table tickers back to `dim_assets`

## Result

- Total checks: `15`
- Passed: `15`
- Failed: `0`
- Warnings: `0`
- Overall status: `PASS`

Date coverage:

- `fact_prices`: 2020-01-02 to 2026-04-29
- `fact_returns`: 2020-01-03 to 2026-04-29

## Key Findings

- The processed tables have the expected schema.
- The asset dimension has one row per ticker.
- Price and return fact tables have no duplicate ticker-date keys.
- No missing values were found in the core dimension or fact tables.
- All adjusted close prices are positive.
- All daily return values fall inside the configured range.
- All fact table tickers match the asset dimension.

## What This Means for Data Reliability

The dataset is clean enough for the next layer of analysis: SQL queries, warehouse reads, and simple downstream analytics. The checks are basic but important. They catch common pipeline problems like missing columns, duplicate keys, broken joins, null values, and unreasonable numeric values.

For a real finance data platform, these checks would be automated and monitored over time. For this portfolio version, they show the pipeline has a clear quality gate before data reaches the warehouse layer.

## Limitations

- The validation suite runs in batch after ingestion.
- It does not yet track quality trends across pipeline runs.
- Return bounds are broad and should not be treated as a full anomaly detection system.
- yfinance adjusted close values may differ from paid market data vendors.
- The generated quality CSVs are ignored by Git and should be regenerated after cloning.

## Next Improvements

- Add ticker-level freshness checks.
- Add warning thresholds for large return moves.
- Add CI tests for validation functions.
- Store validation history across runs.
- Add alerting for failed checks if the pipeline is scheduled.
