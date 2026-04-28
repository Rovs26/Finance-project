"""Cleaning utilities for macroeconomic time series."""

from pathlib import Path

import pandas as pd


MONTH_MAP = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "sept": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def list_excel_files(raw_dir):
    """List Excel files under a raw data directory, including nested folders."""
    raw_path = Path(raw_dir)
    return sorted(
        [
            path
            for path in raw_path.rglob("*")
            if path.is_file() and path.suffix.lower() in {".xls", ".xlsx"}
        ]
    )


def inspect_excel_workbook(path):
    """Inspect workbook sheet names and return an inventory record."""
    workbook_path = Path(path)
    try:
        workbook = pd.ExcelFile(workbook_path)
        sheet_names = workbook.sheet_names
        return {
            "file_path": str(workbook_path),
            "file_name": workbook_path.name,
            "file_type": workbook_path.suffix.lower(),
            "sheet_count": len(sheet_names),
            "sheet_names": "; ".join(sheet_names),
            "status": "inspectable",
            "notes": "Workbook opened successfully.",
        }
    except Exception as exc:
        return {
            "file_path": str(workbook_path),
            "file_name": workbook_path.name,
            "file_type": workbook_path.suffix.lower(),
            "sheet_count": 0,
            "sheet_names": "",
            "status": "inspection_failed",
            "notes": f"{type(exc).__name__}: {exc}",
        }


def _month_to_number(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)) and 1 <= int(value) <= 12:
        return int(value)
    return MONTH_MAP.get(str(value).strip().lower())


def parse_bsp_inflation(path):
    """Parse BSP monthly inflation workbook into date, year, month, inflation_rate."""
    raw = pd.read_excel(path, sheet_name="Monthly", header=None)
    rows = raw.iloc[:, [2, 3, 5]].copy()
    rows.columns = ["year", "month", "inflation_rate"]
    rows["year"] = pd.to_numeric(rows["year"], errors="coerce").ffill()
    rows["month_num"] = rows["month"].map(_month_to_number)
    rows["inflation_rate"] = pd.to_numeric(rows["inflation_rate"], errors="coerce")
    rows = rows.dropna(subset=["year", "month_num", "inflation_rate"])
    rows["year"] = rows["year"].astype(int)
    rows["month"] = rows["month_num"].astype(int)
    rows["date"] = pd.to_datetime(
        {"year": rows["year"], "month": rows["month"], "day": 1}
    )
    output = rows[["date", "year", "month", "inflation_rate"]]
    return output.sort_values("date").drop_duplicates("date").reset_index(drop=True)


def parse_bsp_peso_dollar(path):
    """Parse BSP monthly peso-dollar workbook into date, year, month, usd_php."""
    raw = pd.read_excel(path, sheet_name="monthly", header=None)
    rows = raw.iloc[:, [1, 2, 3]].copy()
    rows.columns = ["year", "month", "usd_php"]
    rows["year"] = pd.to_numeric(rows["year"], errors="coerce").ffill()
    rows["month_num"] = rows["month"].map(_month_to_number)
    rows["usd_php"] = pd.to_numeric(rows["usd_php"], errors="coerce")
    rows = rows.dropna(subset=["year", "month_num", "usd_php"])
    rows["year"] = rows["year"].astype(int)
    rows["month"] = rows["month_num"].astype(int)
    rows["date"] = pd.to_datetime(
        {"year": rows["year"], "month": rows["month"], "day": 1}
    )
    output = rows[["date", "year", "month", "usd_php"]]
    return output.sort_values("date").drop_duplicates("date").reset_index(drop=True)


def parse_world_bank_csv(path, value_name):
    """Parse a World Bank indicator CSV into year and a named value column."""
    df = pd.read_csv(path)
    output = df[["year", "value"]].copy()
    output["year"] = pd.to_numeric(output["year"], errors="coerce").astype("Int64")
    output[value_name] = pd.to_numeric(output["value"], errors="coerce")
    output = output.drop(columns=["value"]).dropna(subset=["year"])
    output["year"] = output["year"].astype(int)
    return output.sort_values("year").reset_index(drop=True)


def standardize_monthly_date(df, year_col=None, month_col=None, date_col=None):
    """Add or standardize monthly date, year, and month columns."""
    output = df.copy()
    if date_col:
        output["date"] = pd.to_datetime(output[date_col])
        output["date"] = output["date"].dt.to_period("M").dt.to_timestamp()
    elif year_col and month_col:
        month_values = output[month_col].map(_month_to_number).fillna(output[month_col])
        output["date"] = pd.to_datetime(
            {
                "year": pd.to_numeric(output[year_col], errors="coerce"),
                "month": pd.to_numeric(month_values, errors="coerce"),
                "day": 1,
            }
        )
    else:
        raise ValueError("Provide either date_col or both year_col and month_col.")

    output["year"] = output["date"].dt.year
    output["month"] = output["date"].dt.month
    return output


def clean_column_names(df):
    """Standardize DataFrame column names to snake_case."""
    output = df.copy()
    output.columns = (
        pd.Index(output.columns)
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return output


def save_clean_dataset(df, path):
    """Save a cleaned dataset to CSV."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path
