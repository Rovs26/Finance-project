# LinkedIn Post Drafts

## Short Post

I finished a portfolio project called News Sentiment and Market Connectedness Engine.

It cleans a recovered financial news sentiment prototype, scores headlines, merges sentiment with market data, and documents why the current dataset is too small for formal GFEVD.

The main lesson: good research analytics is partly about knowing when not to overclaim.

## Medium Post

I finished another finance analytics portfolio project: News Sentiment and Market Connectedness Engine.

This project started as a rough prototype with sentiment logs, market merge output, and legacy scripts. I cleaned it into a more reproducible workflow:

- audited the raw files and legacy scripts
- standardized sentiment records
- added safe `.env` handling
- used structured OpenAI scoring when available
- kept a transparent fallback scoring method
- created research signal labels
- merged sentiment with recovered AMZN market fields
- used a correlation-based connectedness fallback because the data was too small for formal GFEVD

This is not a trading system and not investment advice. It is a research analytics project focused on data quality, methodology, and honest limitations.

## Technical Post

Project completed: News Sentiment and Market Connectedness Engine.

Tech stack and workflow:

- Python and pandas for cleaning
- OpenAI structured outputs for optional sentiment scoring
- python-dotenv for local environment configuration
- Matplotlib for selected visuals
- JSON-lines and CSV loading utilities
- sentiment score thresholds for research labels
- correlation-based connectedness fallback when GFEVD is not valid

The dataset is intentionally described as limited: 11 sentiment records, 2 merged market rows, and an empty scraped news file. I kept that limitation visible instead of pretending the connectedness result is stronger than it is.

Future work would be a larger news dataset, complete market returns, manual label validation, and formal GFEVD only after the time series is usable.
