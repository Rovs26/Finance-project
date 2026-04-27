# Credit Risk and IFRS 9 Expected Credit Loss Engine

## Business Problem

Financial institutions need practical tools to estimate credit risk, assess borrower default probability, and translate model outputs into Expected Credit Loss (ECL) estimates under IFRS 9. This project is designed as a portfolio-ready analytics system that connects credit risk modeling, financial economics, and business interpretation.

## Project Goal

Build a clear, reproducible Python project that will eventually:

- Prepare and analyze loan-level credit data.
- Develop a probability of default (PD) modeling workflow.
- Estimate IFRS 9-style Expected Credit Loss using PD, LGD, and EAD assumptions.
- Present model outputs through business-facing reports and a dashboard.

## Planned Methodology

1. Data understanding and exploratory analysis.
2. Data cleaning and feature preparation.
3. PD model development and validation.
4. ECL calculation engine design.
5. Business interpretation and risk analytics reporting.
6. Streamlit dashboard development after ECL outputs are available.

## Planned Repo Structure

```text
credit-risk-ifrs9-ecl-engine/
  README.md
  requirements.txt
  .gitignore
  data/
    raw/
    processed/
    external/
  notebooks/
    01_data_understanding.ipynb
    02_pd_modeling.ipynb
    03_ecl_engine.ipynb
    04_business_interpretation.ipynb
  src/
    config.py
    data_prep.py
    features.py
    modeling.py
    ecl.py
    visualization.py
  reports/
    business_memo.md
    model_card.md
    figures/
  dashboard/
    app.py
  outputs/
    model/
    predictions/
    ecl_results.csv
  docs/
    PROJECT_BRIEF.md
    DECISION_LOG.md
    KNOWN_ISSUES.md
    AGENT_HANDOFF.md
    PRODUCTION_PROGRESS.md
```

## How To Run Later

Create an environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the Phase 1 data understanding notebook:

```bash
jupyter notebook
```

Open:

```text
notebooks/01_data_understanding.ipynb
```

The dashboard placeholder can be opened later with:

```bash
streamlit run dashboard/app.py
```

## Data Placement

Datasets are not included in this repository. Place the selected loan-level dataset manually inside:

```text
data/raw/
```

Phase 1 detects CSV-style files in `data/raw/`, including `.csv` and `.csv.gz`. If multiple CSV-style files exist, the largest file is selected for exploration.

## Generated Phase 1 Outputs

Phase 1 creates:

- `data/processed/modeling_sample.csv`
- `reports/figures/missing_values_top20.png`
- `reports/figures/target_distribution.png`
- `reports/figures/default_rate_by_grade.png`
- `reports/figures/default_rate_by_purpose.png`
- Additional available category and numeric EDA figures based on dataset columns
- `notebooks/01_data_understanding_executed.ipynb` when notebook execution tooling is available

## Current Status

Phase 1 data understanding is completed using the manually added LendingClub-style raw dataset. No PD model, ECL engine, dashboard logic, or fake results have been implemented.
