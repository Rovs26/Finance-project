"""Data loading utilities for Philippines macroeconomic indicators."""

from datetime import datetime
from pathlib import Path

import pandas as pd
import requests


BSP_INFLATION_URL = "https://www.bsp.gov.ph/statistics/excel/infrate.xls"
BSP_PESO_DOLLAR_URL = "https://www.bsp.gov.ph/statistics/external/pesodollar.xlsx"
WORLD_BANK_BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}"


def download_file(url, output_path):
    """Download a public file and save it to output_path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output_path.write_bytes(response.content)
    return output_path


def download_bsp_inflation(output_dir):
    """Download BSP historical inflation Excel file."""
    return download_file(BSP_INFLATION_URL, Path(output_dir) / "bsp_inflation_infrate.xls")


def download_bsp_peso_dollar(output_dir):
    """Download BSP peso-dollar historical Excel file."""
    return download_file(BSP_PESO_DOLLAR_URL, Path(output_dir) / "bsp_peso_dollar.xlsx")


def fetch_world_bank_indicator(
    indicator_code, country="PHL", start_year=2000, end_year=None
):
    """Fetch an annual World Bank indicator for a country and return a tidy DataFrame."""
    if end_year is None:
        end_year = datetime.now().year

    url = WORLD_BANK_BASE_URL.format(country=country, indicator_code=indicator_code)
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 20000,
    }
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected World Bank response for {indicator_code}.")

    rows = []
    for item in payload[1] or []:
        rows.append(
            {
                "country": item.get("country", {}).get("value"),
                "country_code": item.get("countryiso3code"),
                "indicator": item.get("indicator", {}).get("value"),
                "indicator_code": indicator_code,
                "year": int(item.get("date")) if item.get("date") else None,
                "value": item.get("value"),
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("year").reset_index(drop=True)
    return df


def save_dataframe(df, path):
    """Save a DataFrame to CSV."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def build_source_inventory():
    """Build the Phase 1 macro data source inventory."""
    rows = [
        {
            "indicator": "Inflation rate",
            "source": "Bangko Sentral ng Pilipinas",
            "frequency": "Monthly or periodic, source-defined",
            "url": BSP_INFLATION_URL,
            "collection_method": "Direct Excel download",
            "status": "planned",
            "notes": "Primary official source for Philippines inflation monitoring.",
        },
        {
            "indicator": "USD/PHP exchange rate",
            "source": "Bangko Sentral ng Pilipinas",
            "frequency": "Daily or periodic, source-defined",
            "url": BSP_PESO_DOLLAR_URL,
            "collection_method": "Direct Excel download",
            "status": "planned",
            "notes": "Official BSP external statistics file for peso-dollar data.",
        },
        {
            "indicator": "Key policy rates",
            "source": "Bangko Sentral ng Pilipinas",
            "frequency": "Policy update, source-defined",
            "url": "https://www.bsp.gov.ph/SitePages/Statistics/KeyRates.aspx",
            "collection_method": "Manual review or later parser",
            "status": "manual_review_required",
            "notes": "Page is included in inventory; automated parsing is deferred.",
        },
        {
            "indicator": "Prices and inflation reference page",
            "source": "Bangko Sentral ng Pilipinas",
            "frequency": "Source-defined",
            "url": "https://www.bsp.gov.ph/SitePages/Statistics/Prices.aspx",
            "collection_method": "Manual review or later parser",
            "status": "manual_review_required",
            "notes": "Reference page for validating inflation source links.",
        },
        {
            "indicator": "CPI and inflation",
            "source": "Philippine Statistics Authority",
            "frequency": "Monthly, source-defined",
            "url": "https://psa.gov.ph/price-indices/cpi-ir",
            "collection_method": "Manual review or later parser",
            "status": "manual_review_required",
            "notes": "Primary national statistics reference for CPI and inflation releases.",
        },
        {
            "indicator": "GDP growth annual percent",
            "source": "World Bank",
            "frequency": "Annual",
            "url": WORLD_BANK_BASE_URL.format(
                country="PHL", indicator_code="NY.GDP.MKTP.KD.ZG"
            ),
            "collection_method": "World Bank API",
            "status": "planned",
            "notes": "Annual macro backup and cross-country comparable indicator.",
        },
        {
            "indicator": "Unemployment annual percent",
            "source": "World Bank",
            "frequency": "Annual",
            "url": WORLD_BANK_BASE_URL.format(
                country="PHL", indicator_code="SL.UEM.TOTL.ZS"
            ),
            "collection_method": "World Bank API",
            "status": "planned",
            "notes": "Annual labor market backup indicator.",
        },
        {
            "indicator": "Inflation annual percent backup",
            "source": "World Bank",
            "frequency": "Annual",
            "url": WORLD_BANK_BASE_URL.format(
                country="PHL", indicator_code="FP.CPI.TOTL.ZG"
            ),
            "collection_method": "World Bank API",
            "status": "planned",
            "notes": "Annual inflation backup for cross-checking official series.",
        },
        {
            "indicator": "Personal remittances received percent of GDP",
            "source": "World Bank",
            "frequency": "Annual",
            "url": WORLD_BANK_BASE_URL.format(
                country="PHL", indicator_code="BX.TRF.PWKR.DT.GD.ZS"
            ),
            "collection_method": "World Bank API",
            "status": "planned",
            "notes": "External sector and household income relevance for Philippines macro context.",
        },
    ]
    return pd.DataFrame(rows)
