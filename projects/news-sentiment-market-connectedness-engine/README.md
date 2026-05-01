# News Sentiment and Market Connectedness Engine

Research portfolio project that audits an existing financial news sentiment prototype and prepares it for sentiment-market merging and connectedness analysis.

**Disclaimer:** This is a research portfolio project, not trading advice, investment advice, or a live trading recommendation system.

## Business Problem

Market research teams often want to connect financial news sentiment with market movements, but prototype scripts can become hard to inspect and reproduce. This project turns an existing news-sentiment prototype into a cleaner research repo with documented data inputs, legacy scripts, audit outputs, and a staged path toward connectedness analysis.

## Target Roles and Companies

Target roles include market research analyst, finance analytics analyst, risk analytics analyst, investment data analyst, fintech analytics analyst, and data analyst.

Target companies include JPMorgan Chase, MSCI, ING Hubs Philippines, Wells Fargo, First Metro, BPI, PwC Philippines, KPMG Philippines, fintech analytics teams, and market research teams.

## Current Prototype Files

Phase 0 checks for:

- `merged_data.json`
- `scraped_news.csv`
- `sentiment_log.csv`
- `step1_sentiment_test.py`
- `step2_scraper.py`
- `step3_stock_filter.py`
- `step4_keyword_generator.py`
- `step6_daily_sentiment.py`
- `step7_merge_data.py`
- `step8_gfevd_analysis.py`

No matching prototype files were found in the current workspace during the initial audit. Placeholder legacy files document this status and can be replaced if the original scripts are added later.

## Phase Plan

| Phase | Status | Description |
|---|---|---|
| Phase 0 | Complete | Audit and restructure existing project |
| Phase 1 | Next | Sentiment cleaning, market merge, and connectedness analysis |
| Phase 2 | Not started | GitHub polish and final reports |

## Current Status

Phase 0 creates the project structure, preserves the expected legacy layout, builds audit utilities, and executes a notebook that records file availability, schema coverage, data coverage, company coverage, and current limitations.

## How to Run Phase 0

```bash
cd projects/news-sentiment-market-connectedness-engine
pip install -r requirements.txt
python3 -m jupyter nbconvert --to notebook --execute notebooks/01_project_audit_and_data_review.ipynb --output 01_project_audit_and_data_review_executed.ipynb
```

## Generated Outputs

- `outputs/audit/file_inventory.csv`
- `outputs/audit/legacy_script_inventory.csv`
- `outputs/audit/data_schema_summary.csv`
- `outputs/audit/data_coverage_summary.csv`
- `outputs/audit/company_coverage_summary.csv`
- `reports/figures/audit_records_by_source.png`

Additional sentiment and time-series figures will be generated in Phase 1 once usable sentiment and market files are available.

## Limitations

- Prototype files were not found in the workspace during Phase 0.
- Placeholder legacy scripts are included only to preserve the expected project structure.
- No heavy scraping was run.
- No trading backtest or performance claim is made.
- GFEVD and connectedness logic is inspection-only until Phase 1.
