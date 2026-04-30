# Known Issues

## Phase 0

- No blocking issue found in Phase 0.

- **API availability risk:** yfinance depends on the Yahoo Finance data service. If Yahoo Finance changes its API or rate-limits requests, downloads may fail. A CSV fallback can be added in Phase 1.

- **yfinance data quality:** yfinance adjusted close prices may differ slightly from Bloomberg or Refinitiv due to dividend and split adjustment methodology. For a portfolio project, this is acceptable. For production use, a paid data source should be used.

- **Generated files ignored by Git:** All files under data/raw/, data/processed/, data/warehouse/, outputs/logs/, and outputs/summaries/ are in .gitignore. A fresh clone requires re-executing the notebooks to regenerate these files.

- **No validation layer yet:** Phase 0 does not run data quality checks. Missing values, stale prices, and return outliers are not flagged. This is Phase 1 work.

- **No API or warehouse yet:** DuckDB population and any query API are Phase 1 deliverables. Phase 0 produces only CSV outputs.

- **No rolling or live execution:** The notebook downloads a full historical batch on each run. Incremental ingestion is a future improvement.

## Still Open for Phase 1

- Data quality validation (missing values, staleness, outlier detection)
- DuckDB warehouse population from fact/dim CSVs
- Ingestion summary API or CLI
- Data quality report document
