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
| Phase 1 | Complete | Sentiment cleaning, market merge, and connectedness analysis |
| Phase 2 | Not started | GitHub polish and final reports |

## Current Status

Phase 1B is complete. The project loads the recovered prototype files, safely reads local OpenAI settings from `.env`, scores available headlines with structured sentiment output when possible, creates signal summaries, builds a clean sentiment-market merge, and produces a transparent correlation-based connectedness fallback because the recovered dataset is too small for formal GFEVD.

## How to Run Phase 0

```bash
cd projects/news-sentiment-market-connectedness-engine
pip install -r requirements.txt
python3 -m jupyter nbconvert --to notebook --execute notebooks/01_project_audit_and_data_review.ipynb --output 01_project_audit_and_data_review_executed.ipynb
python3 -m jupyter nbconvert --to notebook --execute notebooks/02_sentiment_market_merge_and_connectedness.ipynb --output 02_sentiment_market_merge_and_connectedness_executed.ipynb
```

## Generated Outputs

Phase 0:

- `outputs/audit/file_inventory.csv`
- `outputs/audit/legacy_script_inventory.csv`
- `outputs/audit/data_schema_summary.csv`
- `outputs/audit/data_coverage_summary.csv`
- `outputs/audit/company_coverage_summary.csv`
- `reports/figures/audit_records_by_source.png`

Phase 1:

- `outputs/sentiment/standardized_sentiment_log.csv`
- `outputs/sentiment/sentiment_by_date.csv`
- `outputs/sentiment/sentiment_by_company.csv`
- `outputs/sentiment/signal_summary.csv`
- `outputs/sentiment/openai_sentiment_scores.csv` when OpenAI scoring runs
- `outputs/merged/clean_merged_sentiment_market.csv`
- `outputs/connectedness/connectedness_matrix.csv`
- `outputs/connectedness/connectedness_edges.csv`
- `outputs/connectedness/connectedness_summary.csv`
- `reports/figures/sentiment_distribution.png`
- `reports/figures/sentiment_by_company.png`
- `reports/figures/sentiment_over_time.png`
- `reports/figures/signal_summary.png`
- `reports/figures/connectedness_heatmap.png`

## Phase 1 Findings

- `sentiment_log.csv` contains 11 usable sentiment records.
- `merged_data.json` contains 2 merged daily records with AMZN market columns.
- `scraped_news.csv` exists but is empty.
- OpenAI structured scoring ran for the 11 available headlines in the latest local run.
- Simple signal labels are research tags only: 6 `SELL`, 3 `HOLD`, and 2 `BUY`.
- Formal GFEVD is not statistically valid from the small recovered dataset, so the project uses a documented correlation-based connectedness fallback.

## Limitations

- Prototype files were added after Phase 0 and processed in Phase 1.
- The recovered sample is small and incomplete.
- `scraped_news.csv` is empty.
- No heavy scraping was run.
- No trading backtest or performance claim is made.
- GFEVD is not used because the available data is too small for a reliable VAR/GFEVD estimate.
