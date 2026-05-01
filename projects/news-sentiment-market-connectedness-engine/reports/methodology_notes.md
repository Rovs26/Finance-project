# Methodology Notes

## Source Files

The project uses local files copied into `data/raw/`:

- `sentiment_log.csv`
- `merged_data.json`
- `scraped_news.csv`

`scraped_news.csv` is empty. The usable analysis comes from `sentiment_log.csv` and `merged_data.json`.

## Legacy Script Review

Recovered scripts are preserved under `legacy/`. They document the original prototype flow: sentiment testing, scraping, filtering, keyword generation, daily sentiment aggregation, market merging, GFEVD analysis, and visualization.

The final workflow does not run heavy scraping or interactive legacy prompts. It uses the recovered raw files as the source of truth.

## Security Cleanup Summary

Recovered legacy scripts previously contained direct credential assignment. Those values were removed and replaced with environment-variable usage. `.env` is ignored by Git, and `.env.example` contains placeholders only.

## Environment Handling

The pipeline reads these local settings when present:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

Default model: `gpt-4o-mini`.

If the local key or package is unavailable, the scoring workflow falls back to transparent keyword rules.

## OpenAI Structured Scoring Method

When available, OpenAI scoring returns structured JSON fields:

- company
- ticker
- sentiment score
- sentiment label
- confidence
- rationale
- risk flags
- recommended research signal

Company/ticker outputs are constrained back to the approved map used in the project.

## Fallback Scoring Method

The fallback uses positive and negative finance keyword lists to create a score between `-1` and `1`. It also extracts simple risk flags from headline text.

This fallback is not a substitute for a validated sentiment model. It is included so the notebook can run without external model access.

## Sentiment Scoring Thresholds

- negative: score <= `-0.15`
- neutral: `-0.15 < score < 0.15`
- positive: score >= `0.15`

## Signal Label Method

- `SELL`: score <= `-0.25`
- `HOLD`: `-0.25 < score < 0.25`
- `BUY`: score >= `0.25`

Signals are research labels only and should not be used as trading advice.

## Market Merge Method

Sentiment records are normalized by date and aggregated to daily sentiment. The recovered merged file contains AMZN market fields. Date fields and wide columns such as `Close AMZN` are standardized before merging.

## Connectedness Fallback Method

The project prepares numeric sentiment and market fields, then calculates absolute correlations as a connectedness fallback. It exports a matrix, edge list, and summary.

## Why Formal GFEVD Was Not Used

Formal GFEVD requires enough clean observations for VAR-style modeling. The recovered merged dataset has only two observations and incomplete market values, so GFEVD would be misleading.

## Limitations

- Small sample size.
- Incomplete market fields.
- Empty scraped news file.
- Optional OpenAI scoring depends on local environment setup.
- Fallback scoring is simple.
- Connectedness output is exploratory.
