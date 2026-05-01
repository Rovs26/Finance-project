"""Project path configuration."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DOCS_DIR = DATA_DIR / "sample_docs"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHUNKS_DIR = OUTPUTS_DIR / "chunks"
RETRIEVAL_DIR = OUTPUTS_DIR / "retrieval"
EVIDENCE_DIR = OUTPUTS_DIR / "evidence"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

for directory in [
    SAMPLE_DOCS_DIR,
    PROCESSED_DATA_DIR,
    CHUNKS_DIR,
    RETRIEVAL_DIR,
    EVIDENCE_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
