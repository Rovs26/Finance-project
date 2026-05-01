# Known Issues

## Final Project Limitations

- No blocking final issue found after Phase 2 checks.
- `scraped_news.csv` exists but is empty.
- `sentiment_log.csv` has only 11 records.
- `merged_data.json` has only two merged daily records.
- Market fields are incomplete; only one merged row has AMZN price and volume values.
- Formal GFEVD is not statistically valid from the available data.
- The project uses correlation fallback instead of formal GFEVD.
- Signal labels are research labels only and are not trading advice.
- OpenAI scoring reruns require a local `.env` file.
- No heavy scraping was run in the committed workflow.
- No trading recommendation system is built.

## Practical Notes

- `.env` must remain local and untracked.
- `data/raw/`, `data/processed/`, and `outputs/` are ignored by Git.
- Figures and reports are committed for portfolio review.
