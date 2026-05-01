# Methodology Notes

## Source Files

Phase 1 uses local prototype files copied into `data/raw/`:

- `sentiment_log.csv`
- `merged_data.json`
- `scraped_news.csv`

The scraped news CSV exists but is empty. The sentiment log and merged JSON are the main usable inputs.

## Script Audit Result

The `legacy/` folder now contains recovered prototype scripts rather than Phase 0 placeholders. Two additional legacy files are also present:

- `step5_dynamic_filtering.py`
- `step9_visualize.py`

The new Phase 1 notebook does not run heavy scraping or interactive legacy prompts. It uses the copied raw data as the source of truth.

## Sentiment Scoring Assumptions

Sentiment is classified with fixed thresholds:

- negative: score less than or equal to `-0.15`
- neutral: score between `-0.15` and `0.15`
- positive: score greater than or equal to `0.15`

The existing `action` column is preserved. If no action exists, the project can derive a simple signal label from sentiment, but this remains a research label only.

## Merge Assumptions

Sentiment is aggregated by normalized date, then merged to the recovered market data on date. Wide market columns such as `Close AMZN`, `Open AMZN`, and `Volume AMZN` are standardized to lower snake case.

## Connectedness Assumptions

Formal GFEVD requires enough complete time-series observations for VAR-style modeling. The recovered data has only two merged rows, so formal GFEVD is not valid in this phase.

## Fallback Method

Phase 1 uses an absolute-correlation connectedness fallback. It creates:

- a connectedness matrix
- an edge list above the threshold
- a compact connectedness summary

This fallback is transparent and useful for checking the workflow shape, but it should not be interpreted as a statistically reliable spillover model.
