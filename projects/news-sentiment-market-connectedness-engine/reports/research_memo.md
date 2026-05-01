# News Sentiment and Market Connectedness Research Memo

## Executive Summary

Phase 1 recovered and processed the local prototype files for a small news sentiment and market connectedness workflow. The usable sentiment log contains 11 records across Apple, Amazon, and Tesla. Most sentiment scores are negative under the project's simple thresholds, and the signal labels are split between `SELL` and `HOLD`.

The available merged market file is too small for formal GFEVD analysis. The notebook therefore uses an absolute-correlation connectedness fallback and clearly treats it as exploratory.

## Data Used

- `data/raw/sentiment_log.csv`: 11 sentiment records.
- `data/raw/merged_data.json`: 2 daily merged records with AMZN market columns.
- `data/raw/scraped_news.csv`: file exists but is empty and could not be parsed.

## Sentiment Method

Sentiment scores are classified using transparent thresholds:

- `sentiment_score <= -0.15`: negative
- `-0.15 < sentiment_score < 0.15`: neutral
- `sentiment_score >= 0.15`: positive

The recovered data produced 9 negative records and 2 neutral records.

## Signal Labeling Method

The existing `action` column is preserved. If the action column is unavailable in a future run, the pipeline can create simple labels from sentiment:

- negative: `SELL`
- neutral: `HOLD`
- positive: `BUY`

These labels are research tags only. They are not trading advice.

## Market Merge Method

The pipeline standardizes dates, aggregates sentiment by date, and merges daily sentiment with the recovered market fields. The merged output includes two dates, but only the first date has AMZN close, high, low, open, and volume values.

## Connectedness Method

Formal GFEVD requires a longer time series and enough complete numeric observations for VAR-style estimation. The recovered data has only two rows, so Phase 1 uses an absolute-correlation connectedness fallback. This creates a connectedness matrix and edge list for workflow demonstration, not a statistically reliable spillover estimate.

## Key Findings

- Sentiment coverage is concentrated on two dates: 2025-06-06 and 2025-10-20.
- Company coverage is Apple with 5 records, Amazon with 5 records, and Tesla with 1 record.
- Simple signal labels are 6 `SELL` and 5 `HOLD`.
- AMZN market fields exist in the merged data, but only one row has complete market values.
- Connectedness output is limited by sample size and should be interpreted only as an exploratory fallback.

## Limitations

- Very small sample size.
- Empty scraped news file.
- Missing market values in the merged data.
- No heavy scraping was run.
- No trading backtest or trading recommendation is included.
- GFEVD is not statistically valid from the available data.

## Next Improvements

- Recover or rebuild a larger scraped news file.
- Extend the sentiment log across more dates and tickers.
- Rebuild the market merge with complete price data.
- Validate sentiment scoring assumptions.
- Run formal VAR/GFEVD only after enough clean observations exist.
