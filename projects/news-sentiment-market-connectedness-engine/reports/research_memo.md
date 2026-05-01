# News Sentiment and Market Connectedness Research Memo

## Executive Summary

This project cleans and documents a recovered financial news sentiment prototype. The improved workflow standardizes sentiment records, uses safe environment-based OpenAI structured scoring when available, preserves a rule-based fallback, merges sentiment with recovered market fields, and creates a connectedness view.

The current analytical result is limited by data size. The usable sentiment log has 11 records, the merged market file has 2 records, and the scraped news file is empty. Because of this, the connectedness output is exploratory and based on absolute correlations, not formal GFEVD.

## Data Used

- `sentiment_log.csv`: 11 sentiment records covering Apple, Amazon, and Tesla.
- `merged_data.json`: 2 daily merged records with AMZN price and volume columns.
- `scraped_news.csv`: present but empty.
- `legacy/`: recovered prototype scripts, preserved for review.

## Sentiment Findings

OpenAI structured scoring ran successfully for the 11 available headlines in the latest local run. The workflow returned standardized companies, tickers, sentiment scores, labels, confidence values, rationales, risk flags, and research signal labels.

The data is concentrated on two dates, so the results are useful for pipeline demonstration rather than market inference.

## Signal Findings

The improved signal labels are:

- 6 `SELL`
- 3 `HOLD`
- 2 `BUY`

These labels are research tags only. They are not trading advice, investment advice, or a backtested strategy.

## Market Merge Findings

The merged output links daily sentiment to recovered AMZN market fields. Only the first merged row has complete AMZN price and volume values, so the market side of the dataset remains incomplete.

## Connectedness Findings

Formal GFEVD was not used because two merged observations are not enough for a reliable VAR/GFEVD estimate. The project uses an absolute-correlation connectedness fallback to show the workflow structure while clearly documenting the statistical limitation.

## Business Interpretation

The project is most useful as a practical research engineering example: it shows how to clean a prototype, preserve legacy scripts, handle environment-based scoring safely, produce reproducible summaries, and avoid overstating results when data is thin.

For market research, the next meaningful improvement is not a more complex model; it is a larger and cleaner sentiment-market dataset.

## Limitations

- Small sentiment sample.
- Empty scraped news file.
- Two-row merged market dataset.
- Missing market values.
- No heavy scraping in the committed workflow.
- No backtest.
- No trading recommendation.
- Correlation connectedness fallback instead of formal GFEVD.

## Next Improvements

- Rebuild or recover a larger scraped news dataset.
- Add more tickers and dates.
- Recreate market data with complete returns.
- Validate sentiment scoring against manually reviewed labels.
- Run formal GFEVD only after the time series is statistically usable.
