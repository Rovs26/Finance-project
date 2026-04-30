"""
Finance Data Engineering Stack — optional REST API.

Endpoints
---------
GET /health         Liveness check; reports warehouse availability.
GET /assets         Asset dimension table (dim_assets).
GET /latest-prices  Latest adjusted close price per ticker.
GET /return-stats   Average and annualised return/volatility per ticker.

Queries run directly against the DuckDB warehouse at runtime.

Run with:
    uvicorn api.app:app --host 127.0.0.1 --port 8011

Requires:
    pip install fastapi uvicorn duckdb
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# ── Path resolution ───────────────────────────────────────────────────────────
_THIS_FILE = Path(__file__).resolve()
_PROJECT_ROOT = _THIS_FILE.parent
for _ in range(5):
    if (_PROJECT_ROOT / "src").is_dir():
        break
    _PROJECT_ROOT = _PROJECT_ROOT.parent

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import WAREHOUSE_DIR  # noqa: E402

DB_PATH = WAREHOUSE_DIR / "finance_data.duckdb"

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Finance Data Engineering Stack API",
    description=(
        "Read-only REST API for the DuckDB finance data warehouse. "
        "Portfolio project — not investment advice."
    ),
    version="1.0.0",
)


def _query_db(sql: str) -> list[dict]:
    """Execute a SQL query against the warehouse and return list of records."""
    try:
        import duckdb
    except ImportError:
        raise HTTPException(status_code=500, detail="duckdb not installed")
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Warehouse not found at {DB_PATH}. Run notebook 02 first.",
        )
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = conn.execute(sql).fetchdf()
    finally:
        conn.close()
    # Convert non-serialisable types (Timestamp, Decimal, etc.) to str
    return df.astype(str).to_dict(orient="records")


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health", summary="Liveness check")
def health():
    """Return API status and whether the DuckDB warehouse file exists."""
    return {
        "status": "ok",
        "warehouse_exists": DB_PATH.exists(),
        "warehouse_path": str(DB_PATH),
    }


@app.get("/assets", summary="Asset dimension table")
def get_assets():
    """Return all assets in the dim_assets dimension table."""
    records = _query_db(
        "SELECT asset_id, ticker, asset_type, loaded_at "
        "FROM dim_assets ORDER BY ticker"
    )
    return JSONResponse(content=records)


@app.get("/latest-prices", summary="Latest adjusted close by ticker")
def get_latest_prices():
    """Return the most recent adjusted close price for each ticker."""
    sql = """
        SELECT
            fp.ticker,
            da.asset_type,
            CAST(fp.date AS VARCHAR)            AS latest_date,
            ROUND(fp.adj_close, 4)              AS latest_price
        FROM fact_prices fp
        JOIN dim_assets da ON fp.ticker = da.ticker
        WHERE fp.date = (SELECT MAX(date) FROM fact_prices)
        ORDER BY fp.ticker
    """
    records = _query_db(sql)
    return JSONResponse(content=records)


@app.get("/return-stats", summary="Return and volatility statistics by ticker")
def get_return_stats():
    """Return average daily return and annualised volatility for each ticker."""
    sql = """
        SELECT
            fr.ticker,
            da.asset_type,
            COUNT(*)                                             AS trading_days,
            ROUND(AVG(fr.daily_return) * 100, 4)                AS avg_daily_return_pct,
            ROUND(AVG(fr.daily_return) * 252 * 100, 2)          AS approx_annualised_return_pct,
            ROUND(STDDEV(fr.daily_return) * SQRT(252) * 100, 2) AS annualised_volatility_pct
        FROM fact_returns fr
        JOIN dim_assets da ON fr.ticker = da.ticker
        GROUP BY fr.ticker, da.asset_type
        ORDER BY approx_annualised_return_pct DESC
    """
    records = _query_db(sql)
    return JSONResponse(content=records)
