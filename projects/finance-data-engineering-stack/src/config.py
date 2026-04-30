"""
Central path configuration for the Finance Data Engineering Stack.
Import from here so every module resolves paths consistently,
regardless of the working directory at runtime.
"""

from pathlib import Path

# Walk up from this file until we find a directory that contains 'src/'
_THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = _THIS_FILE.parent
for _ in range(5):
    if (PROJECT_ROOT / "src").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent

# Data directories
DATA_DIR           = PROJECT_ROOT / "data"
RAW_DATA_DIR       = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR      = DATA_DIR / "warehouse"

# Output directories
OUTPUTS_DIR    = PROJECT_ROOT / "outputs"
LOGS_DIR       = OUTPUTS_DIR / "logs"
SUMMARIES_DIR  = OUTPUTS_DIR / "summaries"

# Report directories
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Ensure all directories exist at import time (safe to call repeatedly)
for _d in [
    RAW_DATA_DIR, PROCESSED_DATA_DIR, WAREHOUSE_DIR,
    LOGS_DIR, SUMMARIES_DIR, FIGURES_DIR,
]:
    _d.mkdir(parents=True, exist_ok=True)

# Asset universe used across phases
ASSET_UNIVERSE = ["AAPL", "MSFT", "JPM", "PG", "XOM", "JNJ", "KO", "NVDA", "SPY"]

# Default date range for ingestion
DEFAULT_START_DATE = "2020-01-01"
