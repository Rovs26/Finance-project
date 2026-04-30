-- Finance Data Engineering Stack
-- DDL for DuckDB warehouse (compatible with standard ANSI SQL)
-- Phase 1: updated with column descriptions and primary key notes
--
-- Tables:
--   dim_assets   — asset dimension (surrogate key + ticker + sector)
--   fact_prices  — daily adjusted close prices (long format)
--   fact_returns — daily simple returns (long format)
--
-- Note: DuckDB supports PRIMARY KEY constraints as documentation.
--       For production PostgreSQL or Snowflake, the same DDL applies.

-- ============================================================
-- dim_assets: asset dimension table
-- One row per unique ticker in the asset universe.
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_assets (
    -- asset_id: surrogate integer primary key
    asset_id    INTEGER PRIMARY KEY,
    -- ticker: exchange ticker symbol (e.g. AAPL, SPY) — must be unique
    ticker      VARCHAR(10) NOT NULL UNIQUE,
    -- asset_type: broad sector/category (Technology, ETF, Financials, etc.)
    asset_type  VARCHAR(50),
    -- loaded_at: UTC timestamp of when this row was created by the pipeline
    loaded_at   TIMESTAMP
);


-- ============================================================
-- fact_prices: daily adjusted close prices (long / normalised format)
-- One row per (date, ticker) combination.
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_prices (
    -- price_id: surrogate integer primary key
    price_id  INTEGER PRIMARY KEY,
    -- date: trading date (no time component)
    date      DATE        NOT NULL,
    -- ticker: foreign key to dim_assets.ticker
    ticker    VARCHAR(10) NOT NULL,
    -- adj_close: split- and dividend-adjusted closing price in USD
    adj_close DOUBLE,
    FOREIGN KEY (ticker) REFERENCES dim_assets(ticker)
);

-- Indexes for analytical query performance
CREATE INDEX IF NOT EXISTS idx_fact_prices_date   ON fact_prices(date);
CREATE INDEX IF NOT EXISTS idx_fact_prices_ticker ON fact_prices(ticker);


-- ============================================================
-- fact_returns: daily simple returns (long / normalised format)
-- One row per (date, ticker) combination.
-- daily_return = (price_t / price_t-1) - 1
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_returns (
    -- return_id: surrogate integer primary key
    return_id    INTEGER PRIMARY KEY,
    -- date: trading date (no time component)
    date         DATE        NOT NULL,
    -- ticker: foreign key to dim_assets.ticker
    ticker       VARCHAR(10) NOT NULL,
    -- daily_return: simple return as a decimal (0.05 = +5%)
    daily_return DOUBLE,
    FOREIGN KEY (ticker) REFERENCES dim_assets(ticker)
);

-- Indexes for analytical query performance
CREATE INDEX IF NOT EXISTS idx_fact_returns_date   ON fact_returns(date);
CREATE INDEX IF NOT EXISTS idx_fact_returns_ticker ON fact_returns(ticker);
