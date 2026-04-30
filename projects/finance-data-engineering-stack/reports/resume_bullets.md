# Resume Bullets

## General Finance Data Engineering

- Built a finance data engineering pipeline in Python that ingests public market data, transforms price and return data into SQL-ready tables, validates data quality, and loads a local DuckDB warehouse.

## Banking Data Pipeline

- Designed a banking-style market data pipeline with ingestion logs, dimension and fact tables, validation checks, and analyst-ready SQL outputs for downstream reporting.

## Fintech Analytics

- Created a reproducible fintech analytics data stack using Python, DuckDB, SQL, and FastAPI to support clean market data access through warehouse tables and lightweight API endpoints.

## Data Quality and Validation

- Implemented 15 validation checks covering schema completeness, duplicate ticker-date keys, missing values, numeric ranges, date coverage, and referential integrity across finance tables.

## SQL and Warehouse

- Modeled adjusted close prices and daily returns into `dim_assets`, `fact_prices`, and `fact_returns`, then queried them through DuckDB using analyst-ready SQL for latest prices, volatility, and return summaries.

## API and Data Product

- Added a small read-only FastAPI layer with `/health`, `/assets`, `/latest-prices`, and `/return-stats` endpoints to demonstrate how validated warehouse outputs can be served as a simple data product.
