# Decision Log

## Initial Decisions

**Use yfinance for Phase 0 market data ingestion**
yfinance provides free, reliable access to historical OHLCV and adjusted close prices for major equities and ETFs with no API key required. It is a well-known library in finance Python workflows and its limitations (unofficial Yahoo Finance wrapper, no tick data, no futures/options) are acceptable for a portfolio demonstration. A CSV fallback is documented as a known alternative.

**Use notebook-first workflow**
All pipeline phases are implemented first in Jupyter notebooks for reproducibility and narrative clarity, with shared logic extracted into src/ modules. This matches how finance analytics teams prototype workflows before productionising.

**Create SQL-ready tables before API or dashboard**
The data model (dim_assets, fact_prices, fact_returns) is established in Phase 0 so that Phase 1 can load them into DuckDB and Phase 2 can query them via a simple API or CLI without re-engineering the schema.

**Use DuckDB for the Phase 1 warehouse**
DuckDB runs embedded (no server), supports ANSI SQL, and handles analytical workloads well for a portfolio project scale. It can be swapped for PostgreSQL or BigQuery in a production setting without changing the SQL DDL materially.

**Asset universe: AAPL, MSFT, JPM, PG, XOM, JNJ, KO, NVDA, SPY**
Chosen to cover technology (AAPL, MSFT, NVDA), financials (JPM), consumer staples (PG, KO), energy (XOM), health care (JNJ), and a broad market ETF (SPY). This gives cross-sector coverage relevant to risk analytics and portfolio analytics use cases.

**Default date range: 2020-01-01 to present**
Starting from 2020 covers the COVID shock, recovery, 2022 rate cycle, and AI-driven rally — a rich multi-regime sample for demonstrating data engineering and quality checks.
