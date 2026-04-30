# LinkedIn Post Drafts

## Short Post

I finished a finance data engineering portfolio project focused on the data layer behind analytics.

The project ingests public market data, transforms it into SQL-ready price and return tables, runs data quality checks, loads a local DuckDB warehouse, and adds a small optional API for summary outputs.

It is not a production platform or investment advice. The goal was to practice the kind of data foundations that finance, banking, fintech, and analytics teams need before any dashboard or model can be trusted.

## Medium Post

I wrapped up a finance data engineering portfolio project: **Finance Data Engineering Stack**.

The project focuses on a practical workflow:

- ingest public market data with Python
- calculate adjusted close prices and daily returns
- reshape data into dimension and fact tables
- run validation checks for schema, duplicates, missing values, numeric ranges, and referential integrity
- load the cleaned tables into DuckDB
- write analyst-ready SQL queries
- expose a small optional FastAPI layer for local summaries

The latest validation run passed 15 out of 15 checks.

This is a portfolio project, not a production enterprise platform or investment system. I built it to show the data engineering work that sits underneath finance analytics: clean tables, quality checks, SQL access, and clear documentation.

## Technical Post

I completed a finance data engineering portfolio project using Python, DuckDB, SQL, and FastAPI.

The pipeline:

1. Downloads public adjusted close market data through yfinance.
2. Builds wide price and return tables.
3. Creates SQL-ready tables: `dim_assets`, `fact_prices`, and `fact_returns`.
4. Runs 15 validation checks across schema, duplicate keys, missing values, numeric ranges, dates, and referential integrity.
5. Loads the validated tables into a local DuckDB warehouse.
6. Exports analyst-style query outputs for latest prices, return statistics, best/worst returns, and joined price-return samples.
7. Adds optional local API endpoints for `/health`, `/assets`, `/latest-prices`, and `/return-stats`.

This project is intentionally modest and honest: no cloud deployment, no orchestrator yet, and no claim that public data is institutional-grade. The focus is on showing a clean, reproducible finance data workflow that can support later analytics.
