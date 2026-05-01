# News Sentiment and Market Connectedness Research Memo

## Executive Summary

Phase 1B improved the recovered prototype pipeline by adding environment-based OpenAI structured scoring with a rule-based fallback. The usable sentiment log contains 11 records across Apple, Amazon, and Tesla. OpenAI structured scoring ran successfully for the available headlines, while the pipeline still preserves a local fallback path for reproducibility.

The available merged market file remains too small for formal GFEVD analysis. The notebook therefore uses an absolute-correlation connectedness fallback and clearly treats it as exploratory.

## Data Used

- `data/raw/sentiment_log.csv`: 11 sentiment records.
- `data/raw/merged_data.json`: 2 daily merged records with AMZN market columns.
- `data/raw/scraped_news.csv`: file exists but is empty and could not be parsed.

## Sentiment Method

The pipeline can score headlines with OpenAI structured JSON output when a local `.env` key is available. The output includes company, ticker, sentiment score, label, confidence, rationale, risk flags, and a research signal label. If the OpenAI call fails or the key is missing, the pipeline falls back to transparent keyword rules.

Sentiment labels use these thresholds:

- `sentiment_score <= -0.15`: negative
- `-0.15 < sentiment_score < 0.15`: neutral
- `sentiment_score >= 0.15`: positive

The improved run produced OpenAI structured scores for all 11 available headlines.

## Signal Labeling Method

The existing `action` column is preserved. The improved pipeline also creates `recommended_signal` using stricter thresholds:

- `SELL` if sentiment score is less than or equal to `-0.25`
- `HOLD` if sentiment score is between `-0.25` and `0.25`
- `BUY` if sentiment score is greater than or equal to `0.25`

These labels are research tags only. They are not trading advice.

## Market Merge Method

The pipeline standardizes dates, aggregates sentiment by date, and merges daily sentiment with the recovered market fields. The merged output includes two dates, but only the first date has AMZN close, high, low, open, and volume values.

## Connectedness Method

Formal GFEVD requires a longer time series and enough complete numeric observations for VAR-style estimation. The recovered data has only two rows, so Phase 1 uses an absolute-correlation connectedness fallback. This creates a connectedness matrix and edge list for workflow demonstration, not a statistically reliable spillover estimate.

## Key Findings

- Sentiment coverage is concentrated on two dates: 2025-06-06 and 2025-10-20.
- Company coverage is Apple with 5 records, Amazon with 5 records, and Tesla with 1 record.
- Improved signal labels are 6 `SELL`, 3 `HOLD`, and 2 `BUY`.
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
