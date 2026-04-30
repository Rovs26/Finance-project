# Finance Data Engineering Stack

A Python portfolio project demonstrating a production-style finance data engineering pipeline — ingestion, transformation, data quality validation, and SQL-ready warehouse tables — built on publicly available market data.

**Disclaimer:** This is a portfolio data engineering project. It is not investment advice and does not represent any institutional view.

---

## Business Problem

Finance, risk, and analytics teams need reliable, auditable pipelines that ingest raw market data, standardise it into SQL-ready formats, validate quality, and serve clean tables to downstream models, dashboards, and APIs. This project demonstrates that end-to-end workflow using public equity data.

---

## Target Roles and Companies

**Roles:** Data engineer, quantitative analyst, risk analytics analyst, financial data analyst, fintech analytics engineer

**Companies:** ING Hubs Philippines, GCash, Maya, UnionBank, MSCI, PwC Philippines, JPMorgan Chase, Wells Fargo, BPI

---

## Phase Plan

| Phase | Status | Description |
|---|---|---|
| Phase 0: Setup + Ingestion | Done | Project structure, yfinance ingestion, SQL-ready tables |
| Phase 1: Validation + Warehouse | Next | Data quality checks, DuckDB warehouse, summary API |
| Phase 2: GitHub Polish | Not started | Reports, career materials, final packaging |

---

## Current Status

Phase 0 ingestion pipeline is complete.

- Asset universe ingested: AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA, SPY
- Date range: 2020-01-01 to present
- Adjusted close prices, daily returns, and SQL-ready dimension and fact tables produced
- Ingestion log and summary saved

---

## How to Run Phase 0

```bash
cd projects/finance-data-engineering-stack

# Install dependencies
pip install -r requirements.txt

# Execute the ingestion notebook
python3 -m jupyter nbconvert --to notebook --execute \
    notebooks/01_ingestion_pipeline.ipynb \
    --output 01_ingestion_pipeline_executed.ipynb
```

---

## Generated Outputs

### Processed data
- `data/processed/adjusted_close_prices.csv` — wide price table (date x ticker)
- `data/processed/daily_returns.csv` — wide returns table (date x ticker)
- `data/processed/dim_assets.csv` — asset dimension table
- `data/processed/fact_prices.csv` — long-format price fact table
- `data/processed/fact_returns.csv` — long-format returns fact table

### Raw data
- `data/raw/market_prices_raw.csv` — raw OHLCV download from yfinance (flattened)

### Logs
- `outputs/logs/ingestion_log.csv` — per-ticker ingestion metadata
- `outputs/summaries/ingestion_summary.csv` — overall pipeline run summary

### SQL
- `sql/create_tables.sql` — DDL for dim_assets, fact_prices, fact_returns
- `sql/sample_queries.sql` — 5 analyst-ready queries

---

## Project Structure

```
finance-data-engineering-stack/
  README.md
  requirements.txt
  .gitignore
  data/           raw/, processed/, warehouse/
  notebooks/      01_ingestion_pipeline.ipynb
  src/            config.py, ingestion.py, transforms.py,
                  validation.py, warehouse.py, visualization.py
  sql/            create_tables.sql, sample_queries.sql
  reports/        figures/, architecture_notes.md, data_quality_report.md
  outputs/        logs/, summaries/
  docs/           PROJECT_BRIEF.md, DECISION_LOG.md, KNOWN_ISSUES.md,
                  AGENT_HANDOFF.md, PRODUCTION_PROGRESS.md
```

---

## Disclaimer

This is a portfolio data engineering project. All data is sourced from publicly available market data via yfinance. Nothing in this repository constitutes investment advice, official financial analysis, or a production trading system.
