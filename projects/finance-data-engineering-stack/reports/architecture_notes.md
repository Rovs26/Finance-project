# Architecture Notes

## Pipeline Architecture

The project follows a simple finance data engineering flow:

1. Ingest public adjusted close market data with `yfinance`.
2. Save raw and processed CSV files.
3. Transform wide price and return panels into SQL-ready dimension and fact tables.
4. Validate processed tables before warehouse loading.
5. Load clean tables into a local DuckDB warehouse.
6. Run analyst-style SQL queries and export summary outputs.
7. Optionally serve warehouse summaries through a small FastAPI layer.

## Raw to Processed to Warehouse Flow

- `data/raw/market_prices_raw.csv`: flattened raw market data download.
- `data/processed/adjusted_close_prices.csv`: wide adjusted close price table.
- `data/processed/daily_returns.csv`: wide daily returns table.
- `data/processed/dim_assets.csv`: ticker metadata.
- `data/processed/fact_prices.csv`: long-format adjusted close prices.
- `data/processed/fact_returns.csv`: long-format daily returns.
- `data/warehouse/finance_data.duckdb`: local DuckDB warehouse generated from processed CSVs.

The warehouse file is intentionally ignored by Git because it is generated from reproducible processed inputs.

## Validation Layer

`src/validation.py` provides reusable checks for schema, duplicate keys, date ranges, missing values, numeric ranges, and referential integrity. The Phase 1 notebook saves:

- `outputs/summaries/data_quality_results.csv`
- `outputs/summaries/data_quality_summary.csv`

The latest validation run passed all configured checks.

## SQL Layer

`sql/create_tables.sql` documents DuckDB-compatible table definitions for:

- `dim_assets`
- `fact_prices`
- `fact_returns`

`sql/sample_queries.sql` includes analyst-ready examples for latest prices, return history, best and worst returns, return statistics, missing-price checks, joined price/return views, and cumulative return approximation.

The notebook exports selected query results to `outputs/summaries/`.

## Optional API Layer

`api/app.py` adds a small read-only FastAPI service with:

- `GET /health`
- `GET /assets`
- `GET /latest-prices`
- `GET /return-stats`

The API reads from the generated DuckDB warehouse. It is optional and should be run only after executing the Phase 1 notebook.

## Production Improvements

- Move from notebook execution to scheduled jobs.
- Add CI tests for validation functions and SQL queries.
- Add incremental ingestion and idempotent partition updates.
- Add structured logging and run metadata tables.
- Add data contracts for downstream consumers.
- Add deployment configuration for the API if it becomes a real service.
