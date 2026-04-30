-- Finance Data Engineering Stack
-- Sample SQL queries for analyst use
-- Compatible with DuckDB and standard ANSI SQL
-- Phase 1: expanded to 8 queries

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
-- 2. Daily return history by ticker (most recent 30 trading days)
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
-- 3. Best single-day returns (top 10 across all assets)
-- ============================================================
SELECT
    fr.date,
    fr.ticker,
    da.asset_type,
    ROUND(fr.daily_return * 100, 4) AS daily_return_pct
FROM fact_returns fr
JOIN dim_assets da ON fr.ticker = da.ticker
ORDER BY fr.daily_return DESC
LIMIT 10;


-- ============================================================
-- 4. Worst single-day returns (bottom 10 across all assets)
-- ============================================================
SELECT
    fr.date,
    fr.ticker,
    da.asset_type,
    ROUND(fr.daily_return * 100, 4) AS daily_return_pct
FROM fact_returns fr
JOIN dim_assets da ON fr.ticker = da.ticker
ORDER BY fr.daily_return ASC
LIMIT 10;


-- ============================================================
-- 5. Average return and annualised volatility by ticker
-- ============================================================
SELECT
    fr.ticker,
    da.asset_type,
    COUNT(*)                                             AS trading_days,
    ROUND(AVG(fr.daily_return) * 100, 4)                 AS avg_daily_return_pct,
    ROUND(AVG(fr.daily_return) * 252 * 100, 2)           AS approx_annualised_return_pct,
    ROUND(STDDEV(fr.daily_return) * SQRT(252) * 100, 2)  AS annualised_volatility_pct
FROM fact_returns fr
JOIN dim_assets da ON fr.ticker = da.ticker
GROUP BY fr.ticker, da.asset_type
ORDER BY approx_annualised_return_pct DESC;


-- ============================================================
-- 6. Missing price check: dates present for some tickers but not all
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
    tt.total                              AS expected_tickers,
    tt.total - dtc.tickers_with_data      AS missing_count
FROM date_ticker_counts dtc
CROSS JOIN total_tickers tt
WHERE dtc.tickers_with_data < tt.total
ORDER BY dtc.date DESC
LIMIT 20;


-- ============================================================
-- 7. Joined price and return table (sample: last 5 trading days)
-- ============================================================
SELECT
    fp.date,
    fp.ticker,
    da.asset_type,
    ROUND(fp.adj_close, 4)               AS adj_close,
    ROUND(fr.daily_return * 100, 4)      AS daily_return_pct
FROM fact_prices fp
JOIN fact_returns fr
    ON fp.date   = fr.date
   AND fp.ticker = fr.ticker
JOIN dim_assets da ON fp.ticker = da.ticker
WHERE fp.date >= (
    SELECT MAX(date) - INTERVAL '5 days' FROM fact_prices
)
ORDER BY fp.date DESC, fp.ticker;


-- ============================================================
-- 8. Top cumulative return approximation by ticker
--    Uses product of (1 + daily_return) over full history.
--    Approximation only — assumes no compounding across gaps.
-- ============================================================
SELECT
    fr.ticker,
    da.asset_type,
    COUNT(*)                                                     AS trading_days,
    ROUND((EXP(SUM(LN(1 + fr.daily_return))) - 1) * 100, 2)     AS cumulative_return_pct,
    ROUND(AVG(fr.daily_return) * 252 * 100, 2)                   AS approx_annualised_return_pct
FROM fact_returns fr
JOIN dim_assets da ON fr.ticker = da.ticker
WHERE fr.daily_return > -1   -- guard against log(0) on full-loss days
GROUP BY fr.ticker, da.asset_type
ORDER BY cumulative_return_pct DESC;
