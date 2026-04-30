"""
Warehouse utilities — Phase 1 placeholder.

DuckDB and SQLAlchemy integration built in Phase 1.
Stubs here so imports work from Phase 0.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_to_duckdb(df: pd.DataFrame, table_name: str, db_path: Path) -> None:
    """Write a DataFrame to a DuckDB file database (Phase 1)."""
    try:
        import duckdb
    except ImportError as exc:
        raise ImportError("duckdb is required: pip install duckdb") from exc

    con = duckdb.connect(str(db_path))
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    con.close()


def read_from_duckdb(table_name: str, db_path: Path) -> pd.DataFrame:
    """Read a table from a DuckDB file database (Phase 1)."""
    try:
        import duckdb
    except ImportError as exc:
        raise ImportError("duckdb is required: pip install duckdb") from exc

    con = duckdb.connect(str(db_path), read_only=True)
    df = con.execute(f"SELECT * FROM {table_name}").df()
    con.close()
    return df


def list_warehouse_tables(db_path: Path) -> list[str]:
    """List all tables in the DuckDB warehouse (Phase 1)."""
    try:
        import duckdb
    except ImportError as exc:
        raise ImportError("duckdb is required: pip install duckdb") from exc

    con = duckdb.connect(str(db_path), read_only=True)
    tables = con.execute("SHOW TABLES").fetchall()
    con.close()
    return [t[0] for t in tables]
