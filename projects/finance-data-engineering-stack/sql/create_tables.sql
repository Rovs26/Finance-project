-- Finance Data Engineering Stack
-- Table definitions for DuckDB or any ANSI-SQL warehouse
-- Generated from Phase 0 ingestion pipeline

-- ============================================================
-- dim_assets: asset dimension table
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_assets (
    asset_id    INTEGER PRIMARY KEY,
    ticker      VARCHAR(10) NOT NULL UNIQUE,
    asset_type  VARCHAR(50),
    loaded_at   TIMESTAMP
);

-- ============================================================
-- fact_prices: daily adjusted close prices
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_prices (
    price_id  INTEGER PRIMARY KEY,
    date      DATE        NOT NULL,
    ticker    VARCHAR(10) NOT NULL,
    adj_close DOUBLE,
    FOREIGN KEY (ticker) REFERENCES dim_assets(ticker)
);

CREATE INDEX IF NOT EXISTS idx_fact_prices_date   ON fact_prices(date);
CREATE INDEX IF NOT EXISTS idx_fact_prices_ticker ON fact_prices(ticker);

-- ============================================================
-- fact_returns: daily simple returns
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_returns (
    return_id    INTEGER PRIMARY KEY,
    date         DATE        NOT NULL,
    ticker       VARCHAR(10) NOT NULL,
    daily_return DOUBLE,
    FOREIGN KEY (ticker) REFERENCES dim_assets(ticker)
);

CREATE INDEX IF NOT EXISTS idx_fact_returns_date   ON fact_returns(date);
CREATE INDEX IF NOT EXISTS idx_fact_returns_ticker ON fact_returns(ticker);
