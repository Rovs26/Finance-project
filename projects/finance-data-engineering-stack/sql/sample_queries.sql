-- Finance Data Engineering Stack
-- Sample SQL queries for analyst use
-- Compatible with DuckDB and standard ANSI SQL

-- ============================================================
-- 1. Latest adjusted close price by asset
-- ============================================================
SELECT
    fp.ticker,
    da.asset_type,
    fp.date        AS latest_date,
    fp.adj_close   AS latest_price
FROM fact_prices fp
JOIN dim_assets da ON fp.ticker = da.ticker
WHERE fp.date = (
    SELECT MAX(date) FROM fact_prices
)
ORDER BY fp.ticker;


-- ============================================================
-- 2. Daily returns by asset (most recent 30 trading days)
-- ============================================================
SELECT
    fr.date,
    fr.ticker,
    da.asset_type,
    ROUND(fr.daily_return * 100, 4) AS daily_return_pct
FROM fact_returns fr
JOIN dim_assets da ON fr.ticker = da.ticker
WHERE fr.date >= (
    SELECT MAX(date) - INTERVAL '30 days' FROM fact_returns
)
ORDER BY fr.date DESC, fr.ticker;


-- ============================================================
-- 3. Best and worst single-day return across all assets
-- ============================================================
-- Best
SELECT
    'best'   AS label,
    fr.date,
    fr.ticker,
    ROUND(fr.daily_return * 100, 4) AS daily_return_pct
FROM fact_returns fr
ORDER BY fr.daily_return DESC
LIMIT 1

UNION ALL

-- Worst
SELECT
    'worst'  AS label,
    fr.date,
    fr.ticker,
    ROUND(fr.daily_return * 100, 4) AS daily_return_pct
FROM fact_returns fr
ORDER BY fr.daily_return ASC
LIMIT 1;


-- ============================================================
-- 4. Average daily return by asset (annualised approximation)
-- ============================================================
SELECT
    fr.ticker,
    da.asset_type,
    COUNT(*)                                        AS trading_days,
    ROUND(AVG(fr.daily_return) * 100, 4)            AS avg_daily_return_pct,
    ROUND(AVG(fr.daily_return) * 252 * 100, 2)      AS approx_annualised_return_pct,
    ROUND(STDDEV(fr.daily_return) * SQRT(252) * 100, 2) AS annualised_volatility_pct
FROM fact_returns fr
JOIN dim_assets da ON fr.ticker = da.ticker
GROUP BY fr.ticker, da.asset_type
ORDER BY approx_annualised_return_pct DESC;


-- ============================================================
-- 5. Missing price check: dates present for some tickers but not all
-- ============================================================
WITH date_ticker_counts AS (
    SELECT
        date,
        COUNT(DISTINCT ticker) AS tickers_with_data
    FROM fact_prices
    WHERE adj_close IS NOT NULL
    GROUP BY date
),
total_tickers AS (
    SELECT COUNT(DISTINCT ticker) AS total FROM dim_assets
)
SELECT
    dtc.date,
    dtc.tickers_with_data,
    tt.total              AS expected_tickers,
    tt.total - dtc.tickers_with_data AS missing_count
FROM date_ticker_counts dtc
CROSS JOIN total_tickers tt
WHERE dtc.tickers_with_data < tt.total
ORDER BY dtc.date DESC
LIMIT 20;
