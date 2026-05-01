# Known Issues

## Phase 1

- No blocking issue found in Phase 1.
- `scraped_news.csv` exists but is empty.
- `sentiment_log.csv` has only 11 records.
- `merged_data.json` has only two merged daily records.
- Market fields are incomplete; only one merged row has AMZN price and volume values.
- Formal GFEVD is not statistically valid from the available data, so Phase 1 uses a correlation-based connectedness fallback.
- Signal labels are research tags only and are not trading advice.
- No heavy scraping was run.
- OpenAI structured scoring ran locally in Phase 1B, but the project keeps a fallback path because API availability should not be assumed.
- `.env` must remain local and untracked.

## Phase 0

- Phase 0 initially did not find the prototype files. They were manually copied into the project afterward and processed in Phase 1.
- Prototype scripts may still need refactoring before production-style use.
- Sentiment scoring is simple and needs validation on a larger sample.
- No trading recommendation system is built.
