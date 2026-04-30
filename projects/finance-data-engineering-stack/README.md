# Finance Data Engineering Stack

Finance data engineering portfolio project that ingests public market data, validates it, loads it into DuckDB, and exposes analyst-ready SQL and API outputs.

**Disclaimer:** This is a portfolio data engineering project. It is not investment advice, an institutional research product, or a production trading platform.

## Business Problem

Finance, banking, and fintech teams need reliable pipelines before they can trust analytics, models, dashboards, or reporting. Raw price data has to be ingested, reshaped, validated, stored in queryable tables, and documented clearly enough for other analysts to use.

This project demonstrates that workflow using public equity market data.

## Target Roles and Companies

Target roles:

- Finance data analyst
- Data engineer
- Fintech analytics engineer
- Risk analytics analyst
- Banking data analyst
- Junior quantitative analyst

Target companies:

- ING Hubs Philippines
- GCash
- Maya
- UnionBank
- MSCI
- PwC Philippines
- JPMorgan Chase
- Wells Fargo
- BPI

## Pipeline Overview

1. Download adjusted close prices from yfinance.
2. Save raw and processed CSV outputs.
3. Calculate daily returns.
4. Create SQL-ready dimension and fact tables.
5. Run validation checks on schema, duplicates, missing values, ranges, and referential integrity.
6. Load validated tables into a local DuckDB warehouse.
7. Run sample analytical SQL queries.
8. Optionally serve warehouse summaries through a small FastAPI layer.

## Architecture Summary

```text
yfinance
  -> data/raw/market_prices_raw.csv
  -> data/processed/adjusted_close_prices.csv
  -> data/processed/daily_returns.csv
  -> data/processed/dim_assets.csv
  -> data/processed/fact_prices.csv
  -> data/processed/fact_returns.csv
  -> validation checks
  -> data/warehouse/finance_data.duckdb
  -> SQL query outputs
  -> optional FastAPI endpoints
```

## Data Sources

- Source: Yahoo Finance data accessed through `yfinance`
- Asset universe: `AAPL`, `MSFT`, `JPM`, `PG`, `XOM`, `JNJ`, `KO`, `NVDA`, `SPY`
- Date range: 2020-01-01 to latest available run date
- Main field used: adjusted close price

## Tables Created

- `dim_assets`: one row per ticker with asset metadata
- `fact_prices`: long-format adjusted close prices by date and ticker
- `fact_returns`: long-format daily returns by date and ticker
- `adjusted_close_prices.csv`: wide price table for analysis
- `daily_returns.csv`: wide returns table for analysis

## Validation Checks

The Phase 1 validation suite checks:

- Required columns in all core tables
- Unique ticker values in `dim_assets`
- No duplicate `(date, ticker)` keys in fact tables
- Date range validity
- Missing values
- Positive adjusted close prices
- Daily returns between `-1` and `1`
- Fact table tickers exist in `dim_assets`

Latest validation result:

- Total checks: `15`
- Passed: `15`
- Failed: `0`
- Warnings: `0`
- Overall status: `PASS`

## DuckDB Warehouse Layer

The notebook builds a local DuckDB warehouse at:

```text
data/warehouse/finance_data.duckdb
```

Warehouse tables:

- `dim_assets`
- `fact_prices`
- `fact_returns`

The DuckDB file is not committed because it is generated from reproducible notebook outputs.

## Optional API Layer

The project includes a lightweight read-only FastAPI app:

- `GET /health`
- `GET /assets`
- `GET /latest-prices`
- `GET /return-stats`

This is a small local demonstration layer, not a deployed service.

## SQL Examples

`sql/sample_queries.sql` includes analyst-style queries for:

- Latest price by ticker
- Daily return history by ticker
- Best daily returns
- Worst daily returns
- Average return and volatility by ticker
- Missing price checks
- Joined price and return table
- Cumulative return approximation by ticker

## Key Results

- Ingested market data for 9 tickers.
- Produced SQL-ready dimension and fact tables.
- Built a validation suite with 15 checks.
- Latest validation run passed all checks.
- Created a local DuckDB warehouse.
- Exported query summaries for latest prices, return statistics, best/worst returns, and joined price-return samples.
- Added a small optional API for local warehouse reads.

## How to Run

From the repository root:

```bash
cd projects/finance-data-engineering-stack
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run Phase 0 ingestion:

```bash
python3 -m jupyter nbconvert --to notebook --execute \
  notebooks/01_ingestion_pipeline.ipynb \
  --output 01_ingestion_pipeline_executed.ipynb
```

Run Phase 1 validation and warehouse build:

```bash
python3 -m jupyter nbconvert --to notebook --execute \
  notebooks/02_data_quality_and_warehouse.ipynb \
  --output 02_data_quality_and_warehouse_executed.ipynb
```

Run the optional API after the warehouse has been generated:

```bash
uvicorn api.app:app --host 127.0.0.1 --port 8011
```

## Generated Artifacts Policy

The following files are generated and intentionally ignored by Git:

- `data/raw/**`
- `data/processed/**`
- `data/warehouse/**`
- `outputs/logs/**`
- `outputs/summaries/**`

Run the notebooks in order to regenerate data, warehouse files, logs, and query summary CSVs after cloning.

Committed project materials include source code, notebooks, SQL, docs, reports, and selected report figures.

## Key Reports

- `reports/data_quality_report.md`
- `reports/architecture_notes.md`
- `reports/resume_bullets.md`
- `reports/interview_talking_points.md`
- `reports/company_positioning.md`
- `reports/linkedin_post.md`

## Limitations

- yfinance is a public data source and can change, fail, or differ from paid institutional feeds.
- The pipeline is batch-oriented and notebook-driven.
- There is no Airflow, Prefect, or cloud scheduler yet.
- The API is local and read-only.
- Validation checks are useful but not a full production monitoring system.
- No live deployment or CI pipeline is included in the MVP.

## Future Improvements

- Add scheduled orchestration with Airflow or Prefect.
- Add CI checks for validation functions and SQL queries.
- Add incremental ingestion.
- Add a data freshness dashboard or alerting layer.
- Add cloud warehouse deployment.
- Add authentication and deployment configuration for the API.

## Resume Bullet

Built a finance data engineering pipeline in Python that ingests public equity prices, transforms them into SQL-ready fact and dimension tables, validates data quality with 15 checks, loads a DuckDB warehouse, and exposes analyst-ready SQL/API outputs.
