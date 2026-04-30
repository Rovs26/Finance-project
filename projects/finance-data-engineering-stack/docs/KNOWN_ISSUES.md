# Known Issues

## Final Status

- No blocking final issue found in Phase 2.

## Data and Generated Artifacts

- Raw data, processed data, warehouse files, logs, and summary CSV outputs are ignored by Git.
- A fresh clone requires rerunning the notebooks to regenerate:
  - `data/raw/**`
  - `data/processed/**`
  - `data/warehouse/finance_data.duckdb`
  - `outputs/logs/**`
  - `outputs/summaries/**`

## Data Source Risk

- yfinance depends on Yahoo Finance availability and response formats.
- Adjusted close values from yfinance may differ from paid institutional feeds.
- This is acceptable for a portfolio project but should not be treated as a production market data source.

## Validation and Monitoring

- Validation checks run in batch through the notebook.
- There is no scheduler, alerting, or validation history table yet.
- The daily return range check is a broad reasonableness test, not full anomaly detection.

## Warehouse and API

- DuckDB is local and file-based.
- The optional API requires FastAPI and uvicorn.
- The API is not deployed, authenticated, or production-hardened.

## Production Gaps

- No Airflow or Prefect orchestration yet.
- No cloud deployment yet.
- No CI pipeline yet.
- No secrets management is needed for the current public-data workflow, but it would be required for private data sources.
