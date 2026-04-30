# Project Brief: Finance Data Engineering Stack

## Purpose

Demonstrate a production-style finance data engineering pipeline in Python, covering ingestion from public market data sources, transformation into SQL-ready tables, data quality validation, and output to a queryable warehouse — packaged as a GitHub portfolio project targeting finance, risk, analytics, and fintech roles in the Philippines and globally.

## Target Roles

- Data engineer (finance / fintech)
- Quantitative analyst
- Risk analytics analyst
- Financial data analyst
- Fintech analytics engineer
- Applied economics research analyst

## Target Companies

ING Hubs Philippines, GCash, Maya, UnionBank, MSCI, PwC Philippines, JPMorgan Chase, Wells Fargo, BPI

## MVP Scope

Phase 0:
- Set up project structure with modular src/ package
- Ingest adjusted close prices for 9 equity tickers via yfinance
- Produce SQL-ready dimension and fact tables
- Save ingestion logs and summaries
- Build executable Jupyter notebook with clear narrative

Phase 1 (next):
- Data quality validation (missing values, staleness, outliers)
- DuckDB warehouse population
- Summary API or CLI export
- Data quality report

Phase 2 (next):
- GitHub polish
- Career-facing reports (resume bullets, interview Q&A, company positioning, LinkedIn post)

## Non-MVP Scope

- Real-time or streaming data feeds
- Proprietary data sources or paid APIs
- Production deployment or orchestration (Airflow, Prefect)
- Machine learning models or factor models
- Portfolio optimisation or backtesting engine

## Expected Outputs

- notebooks/01_ingestion_pipeline.ipynb (executed)
- data/processed/ — adjusted_close_prices.csv, daily_returns.csv, dim_assets.csv, fact_prices.csv, fact_returns.csv
- data/raw/ — market_prices_raw.csv
- outputs/logs/ — ingestion_log.csv
- outputs/summaries/ — ingestion_summary.csv
- sql/ — create_tables.sql, sample_queries.sql
