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

This repository is currently in setup phase only. After a dataset is manually added and implementation begins, the expected workflow will be:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
streamlit run dashboard/app.py
```

## Data Placement

Datasets are not included in this repository. Place the selected loan-level dataset manually inside:

```text
data/raw/
```

## Current Status

Setup phase only. The project structure and placeholder files have been created, but no dataset, model, ECL engine, dashboard logic, or results have been implemented.
