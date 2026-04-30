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

Status: Next

- Implement validation.py (missing values, staleness, outlier checks).
- Populate DuckDB warehouse from fact/dim CSVs.
- Run sample_queries.sql against the warehouse.
- Generate data_quality_report.md.
- Optional: simple CLI or API for querying the warehouse.

## Phase 2: GitHub Polish

Status: Not started

- Finalise README with outputs and screenshots.
- Write career-facing reports: resume_bullets, interview_talking_points, company_positioning, linkedin_post.
- architecture_notes.md.
- Final commit and GitHub push.
