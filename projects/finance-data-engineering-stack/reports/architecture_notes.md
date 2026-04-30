# Architecture Notes

## Overview

This project is a small finance data engineering stack built around a realistic data flow: ingest market data, transform it into usable tables, validate quality, load a warehouse, and expose simple query outputs.

It is intentionally compact. The point is to show clear engineering structure without pretending to be a full enterprise platform.

## Raw to Processed to Warehouse Flow

```text
yfinance download
  -> raw market data CSV
  -> adjusted close price panel
  -> daily returns panel
  -> dim_assets
  -> fact_prices
  -> fact_returns
  -> validation suite
  -> DuckDB warehouse
  -> SQL query outputs
  -> optional local API
```

## Data Model

The data model is simple and analyst-friendly:

- `dim_assets`: ticker-level metadata
- `fact_prices`: adjusted close prices by date and ticker
- `fact_returns`: daily returns by date and ticker

The fact tables use `(date, ticker)` as the natural analytical key. Surrogate IDs are included for a familiar warehouse-style layout, but the validation checks focus on the ticker-date grain.

## Validation Layer

The validation layer is implemented in `src/validation.py`. It checks:

- Schema completeness
- Duplicate keys
- Date coverage
- Missing values
- Numeric ranges
- Referential integrity

The latest run passed all checks. This gives downstream users a cleaner starting point for SQL analysis and API reads.

## SQL Layer

`sql/create_tables.sql` documents the intended DuckDB table structure.

`sql/sample_queries.sql` includes examples for:

- Latest prices
- Return history
- Best and worst daily returns
- Return and volatility summaries
- Missing-price checks
- Joined price and return samples
- Cumulative return approximation

This makes the project useful for both data engineering and finance analytics interviews.

## Optional API Layer

`api/app.py` provides a small FastAPI read layer over the local DuckDB warehouse.

Endpoints:

- `/health`
- `/assets`
- `/latest-prices`
- `/return-stats`

The API is deliberately modest. It shows how the warehouse can be served as a data product, but it is not deployed or secured.

## How This Maps to Production Data Engineering

This portfolio version mirrors the shape of a production workflow:

- Clear separation between ingestion, transformation, validation, and serving
- SQL-ready dimensional tables
- Reproducible notebooks for pipeline runs
- Data quality checks before warehouse use
- Query outputs for analytics consumers
- Small API layer for service-style access

What is missing for production:

- Scheduler or orchestrator
- Cloud storage or warehouse deployment
- CI/CD
- Monitoring and alerting
- Secrets management
- Authentication and access control
- Formal data contracts

## Future Improvements

- Move notebook execution into scheduled jobs.
- Add Airflow or Prefect orchestration.
- Add CI tests for Python modules and SQL queries.
- Add incremental ingestion instead of full historical refreshes.
- Add validation history tables.
- Deploy the API behind authentication if it becomes more than a local demo.
