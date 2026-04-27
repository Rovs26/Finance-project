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

Run the Phase 2 PD modeling notebook:

```bash
jupyter notebook
```

Open:

```text
notebooks/02_pd_modeling.ipynb
```

Run the Phase 3 ECL engine notebook:

```bash
jupyter notebook
```

Open:

```text
notebooks/03_ecl_engine.ipynb
```

Run the Phase 4A business interpretation notebook:

```bash
jupyter notebook
```

Open:

```text
notebooks/04_business_interpretation.ipynb
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

## Generated Phase 2 Outputs

Phase 2 creates:

- `outputs/model/pd_logistic_regression.joblib`
- `outputs/predictions/pd_predictions.csv`
- `reports/figures/pd_roc_curve.png`
- `reports/figures/pd_confusion_matrix.png`
- `reports/figures/pd_score_distribution.png`
- `reports/figures/pd_default_rate_by_score_band.png`
- `reports/figures/pd_top_coefficients.png`
- `notebooks/02_pd_modeling_executed.ipynb` when notebook execution tooling is available

The Phase 2 model is a baseline logistic regression only. It does not include IFRS 9 staging, LGD, EAD, ECL calculations, or dashboard logic.

## Generated Phase 3 Outputs

Phase 3 creates:

- `outputs/ecl_results.csv`
- `outputs/predictions/ecl_scenario_summary.csv`
- `reports/figures/ecl_by_stage.png`
- `reports/figures/exposure_by_stage.png`
- `reports/figures/ecl_by_score_band.png`
- `reports/figures/ecl_by_grade.png`
- `reports/figures/ecl_by_purpose.png`
- `reports/figures/scenario_ecl_comparison.png`
- `reports/figures/ecl_distribution.png`
- `notebooks/03_ecl_engine_executed.ipynb` when notebook execution tooling is available

Scenario analysis includes Base, Mild stress, and Severe stress cases using PD and LGD multipliers. PD and LGD are capped at 100%.

Phase 3 uses simplified IFRS 9-style staging for portfolio analytics only:

- Stage 1: `pd_score < 0.20`
- Stage 2: `0.20 <= pd_score < 0.50`
- Stage 3: `pd_score >= 0.50` or `default_flag == 1`

This is not official IFRS 9 compliance logic.

## Generated Phase 4A Outputs

Phase 4A creates dashboard-ready tables:

- `outputs/predictions/dashboard_summary.csv`
- `outputs/predictions/ecl_by_stage.csv`
- `outputs/predictions/ecl_by_score_band.csv`
- `outputs/predictions/ecl_by_grade.csv`
- `outputs/predictions/ecl_by_purpose.csv`

Phase 4A also creates portfolio presentation materials:

- `reports/resume_bullets.md`
- `reports/interview_talking_points.md`
- `reports/company_positioning.md`
- `reports/linkedin_post.md`
- polished `reports/business_memo.md`
- updated `reports/model_card.md`

The dashboard-ready tables are prepared for the next Streamlit phase, but the dashboard has not been built yet.

## Current Status

Phase 4A business interpretation is completed using the Phase 3 ECL outputs. No Streamlit dashboard has been built yet. The project remains a portfolio analytics prototype, not a production bank system or official IFRS 9 model.
