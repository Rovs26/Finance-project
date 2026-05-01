"""Ingestion and audit helpers for prototype data files."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def load_csv(path):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(path)


def load_json_records(path):
    """Load JSON records from a JSON array, object, or JSON-lines file."""
    path = Path(path)
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return pd.DataFrame()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return pd.DataFrame(data)
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    return pd.DataFrame(value)
            return pd.DataFrame([data])
    except json.JSONDecodeError:
        records = [json.loads(line) for line in text.splitlines() if line.strip()]
        return pd.DataFrame(records)
    return pd.DataFrame()


def load_json_lines_or_records(path):
    """Backward-compatible wrapper for JSON record loading."""
    return load_json_records(path)


def load_available_raw_datasets(raw_dir):
    """Load expected raw datasets that are available in a raw directory."""
    raw_dir = Path(raw_dir)
    datasets = {}
    for path in sorted(raw_dir.glob("*")):
        if not path.is_file():
            continue
        try:
            if path.suffix.lower() == ".csv":
                datasets[path.name] = load_csv(path)
            elif path.suffix.lower() == ".json":
                datasets[path.name] = load_json_records(path)
        except Exception as exc:
            datasets[path.name] = pd.DataFrame(
                [{"load_error": str(exc), "source_file": path.name}]
            )
    return datasets


def inspect_dataframe(df, name):
    """Return a compact schema and coverage summary for a DataFrame."""
    summary = {
        "dataset": name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": ", ".join(map(str, df.columns)),
        "missing_values_total": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }
    date_cols = [col for col in df.columns if "date" in str(col).lower() or "time" in str(col).lower()]
    if date_cols:
        parsed = pd.to_datetime(df[date_cols[0]], errors="coerce")
        summary["date_column"] = date_cols[0]
        summary["start_date"] = parsed.min()
        summary["end_date"] = parsed.max()
        summary["valid_date_rows"] = int(parsed.notna().sum())
    else:
        summary["date_column"] = ""
        summary["start_date"] = pd.NaT
        summary["end_date"] = pd.NaT
        summary["valid_date_rows"] = 0
    return summary


def save_audit_summary(summary, path):
    """Save a list of audit dictionaries to CSV."""
    df = pd.DataFrame(summary)
    df.to_csv(path, index=False)
    return df


def save_dataframe(df, path):
    """Save a DataFrame to CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df
