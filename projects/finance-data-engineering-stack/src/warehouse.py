"""
Warehouse utilities for the Finance Data Engineering Stack.

Functions
---------
create_duckdb_connection   Open a DuckDB connection to a file database.
load_csv_to_table          Load a CSV into a named DuckDB table.
create_warehouse           Create a full warehouse from a dict of CSV paths.
run_query                  Execute SQL and return result as DataFrame.
export_query_result        Execute SQL, save to CSV, and return DataFrame.
run_sample_queries         Run named queries dict and return results dict.

Phase 0 stubs (write_to_duckdb, read_from_duckdb, list_warehouse_tables)
are preserved at the bottom for backward compatibility.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def create_duckdb_connection(db_path: Path):
    """
    Open and return a DuckDB connection to a file database.

    Parameters
    ----------
    db_path : Path
        Path to the .duckdb file (created if it does not exist).

    Returns
    -------
    duckdb.DuckDBPyConnection
    """
    try:
        import duckdb
    except ImportError as exc:
        raise ImportError("duckdb is required: pip install duckdb") from exc
    return duckdb.connect(str(db_path))


def load_csv_to_table(conn, csv_path: Path, table_name: str) -> int:
    """
    Load a CSV file into a named DuckDB table (replace if exists).

    Parameters
    ----------
    conn : duckdb.DuckDBPyConnection
    csv_path : Path
    table_name : str

    Returns
    -------
    int  Row count loaded.
    """
    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT * FROM read_csv_auto('{csv_path}', header=True)
    """)
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    logger.info(
        "Loaded %s → %s: %d rows", Path(csv_path).name, table_name, row_count
    )
    return row_count


def create_warehouse(db_path: Path, table_paths: dict[str, Path]) -> None:
    """
    Create a DuckDB warehouse from a mapping of table_name → csv_path.

    The database file is created (or replaced) at db_path.

    Parameters
    ----------
    db_path : Path
        File path for the DuckDB database.
    table_paths : dict
        {table_name: csv_path}
    """
    import duckdb
    conn = duckdb.connect(str(db_path))
    try:
        for table_name, csv_path in table_paths.items():
            load_csv_to_table(conn, csv_path, table_name)
    finally:
        conn.close()
    logger.info("Warehouse created at %s with tables: %s", db_path.name, list(table_paths))


def run_query(conn, query: str) -> pd.DataFrame:
    """Execute a SQL query and return the result as a DataFrame."""
    return conn.execute(query).fetchdf()


def export_query_result(conn, query: str, output_path: Path) -> pd.DataFrame:
    """Execute a SQL query, save result to CSV, and return the DataFrame."""
    df = run_query(conn, query)
    df.to_csv(output_path, index=False)
    logger.info(
        "Query result saved: %s (%d rows)", Path(output_path).name, len(df)
    )
    return df


def run_sample_queries(
    db_path: Path,
    queries: dict[str, str],
) -> dict[str, pd.DataFrame]:
    """
    Run named SQL queries against the warehouse.

    Parameters
    ----------
    db_path : Path
    queries : dict
        {name: sql_string}

    Returns
    -------
    dict {name: DataFrame}
    """
    import duckdb
    conn = duckdb.connect(str(db_path), read_only=True)
    results: dict[str, pd.DataFrame] = {}
    try:
        for name, sql in queries.items():
            results[name] = run_query(conn, sql)
            logger.info("Query '%s': %d rows", name, len(results[name]))
    finally:
        conn.close()
    return results


# ── Phase 0 compatibility stubs ───────────────────────────────────────────────

def write_to_duckdb(df: pd.DataFrame, table_name: str, db_path: Path) -> None:
    """Write a DataFrame to a DuckDB file database (Phase 0 stub)."""
    import duckdb
    con = duckdb.connect(str(db_path))
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    con.close()


def read_from_duckdb(table_name: str, db_path: Path) -> pd.DataFrame:
    """Read a table from a DuckDB file database (Phase 0 stub)."""
    import duckdb
    con = duckdb.connect(str(db_path), read_only=True)
    df = con.execute(f"SELECT * FROM {table_name}").df()
    con.close()
    return df


def list_warehouse_tables(db_path: Path) -> list[str]:
    """List all tables in the DuckDB warehouse (Phase 0 stub)."""
    import duckdb
    con = duckdb.connect(str(db_path), read_only=True)
    tables = con.execute("SHOW TABLES").fetchall()
    con.close()
    return [t[0] for t in tables]
