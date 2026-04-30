# Production Progress

## Phase 0: Setup and Ingestion

Status: Done

- Created project structure with src/ package, sql/, reports/, outputs/, docs/.
- Implemented ingestion.py, transforms.py, validation.py (stub), warehouse.py (stub), visualization.py, config.py.
- Built notebooks/01_ingestion_pipeline.ipynb and executed successfully.
- Ingested adjusted close prices for 9 tickers (AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA, SPY) from 2020-01-01 to present via yfinance.
- Saved raw, processed, dimension, and fact table CSVs.
- Saved ingestion log and summary.
- Created SQL DDL and sample queries.
- README, PROJECT_BRIEF, DECISION_LOG, KNOWN_ISSUES written.

## Phase 1: Data Validation and Warehouse

Status: Done

- Implemented reusable validation checks for schema, duplicate keys, date ranges, missing values, numeric ranges, and referential integrity.
- Populated local DuckDB warehouse from `dim_assets`, `fact_prices`, and `fact_returns`.
- Expanded `sample_queries.sql` to 8 analyst-ready SQL examples.
- Exported validation and SQL summary CSVs.
- Generated Phase 1 figures.
- Added optional FastAPI read layer for local warehouse summaries.
- Updated data quality and architecture reports.

## Phase 2: GitHub Polish

Status: Next

- Finalise README with outputs and screenshots.
- Write career-facing reports: resume_bullets, interview_talking_points, company_positioning, linkedin_post.
- architecture_notes.md.
- Final commit and GitHub push.
