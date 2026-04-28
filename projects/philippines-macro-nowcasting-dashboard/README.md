# Philippines Macro Nowcasting and Policy Dashboard

Python research project for building a Philippines-focused macroeconomic nowcasting and policy analytics workflow.

## Business Problem

Economic research, banking, policy, and business analytics teams need clear workflows for collecting macro indicators, monitoring inflation and policy conditions, building transparent baseline forecasts, and explaining results in a policy-relevant way.

## Target Roles and Companies

Target roles:

- Economic research analyst
- Macro research analyst
- Finance analytics analyst
- Banking analytics analyst
- Policy research analyst
- Business analytics analyst
- Fintech analytics analyst

Target companies include BSP, PIDS, JPMorgan Chase, ING Hubs Philippines, PwC Philippines, P&G Philippines, MSCI, Wells Fargo, BPI, and other finance or research employers.

## Planned Indicators

- Philippines inflation and CPI indicators
- BSP policy rate
- Exchange rate
- Interest rates or yield indicators
- GDP or production indicators
- Labor market indicators
- External trade or balance indicators
- Selected global or regional reference indicators if useful

## Planned Methodology

1. Collect or manually place transparent public macro data.
2. Clean and standardize time-series indicators.
3. Engineer lag, growth, momentum, and policy-relevant features.
4. Build simple baseline forecasting or nowcasting models.
5. Interpret results through policy and business context.
6. Build a Streamlit dashboard only after clean outputs exist.
7. Package findings into recruiter-readable reports.

## Planned Repo Structure

```text
philippines-macro-nowcasting-dashboard/
  README.md
  requirements.txt
  .gitignore
  data/
    raw/
    processed/
    external/
  notebooks/
    01_macro_data_collection.ipynb
    02_cleaning_and_features.ipynb
    03_baseline_forecasting.ipynb
    04_policy_interpretation.ipynb
  src/
    config.py
    data_loader.py
    cleaning.py
    features.py
    forecasting.py
    visualization.py
  dashboard/
    app.py
  reports/
    research_memo.md
    model_notes.md
    resume_bullets.md
    interview_talking_points.md
    company_positioning.md
    linkedin_post.md
    figures/
  outputs/
    indicators/
    forecasts/
    scenarios/
  docs/
    PROJECT_BRIEF.md
    DECISION_LOG.md
    KNOWN_ISSUES.md
    AGENT_HANDOFF.md
    PRODUCTION_PROGRESS.md
```

## Data Plan

Macro data will be collected from public sources or manually placed later. No macro data is included in the setup phase.

## Current Status

Phase 4 policy interpretation is complete. Dashboard is next.

- Phase 0 setup: completed
- Phase 1 macro data collection: completed
- Phase 2 cleaning and feature engineering: completed
- Phase 3 baseline forecasting: completed
- Phase 4 policy interpretation: completed
- Phase 5 dashboard: next
- Phase 6 GitHub polish: not started

**Disclaimer:** This is a portfolio research project. Nothing in this repository constitutes an official economic forecast, investment advice, or guidance from the BSP, PSA, or any official institution.

## Collected Phase 1 Sources

Raw files collected:

- `data/raw/bsp_inflation_infrate.xls`
- `data/raw/bsp_peso_dollar.xlsx`
- `data/raw/world_bank_gdp_growth.csv`
- `data/raw/world_bank_unemployment.csv`
- `data/raw/world_bank_inflation_backup.csv`
- `data/raw/world_bank_remittances_pct_gdp.csv`

Inventory and summary outputs:

- `outputs/indicators/source_inventory.csv`
- `outputs/indicators/data_collection_summary.csv`

Phase 1 only collects raw source files and records availability.

## Processed Phase 2 Datasets

Processed datasets created:

- `data/processed/monthly_inflation.csv`
- `data/processed/monthly_usd_php.csv`
- `data/processed/annual_macro_context.csv`
- `data/processed/monthly_macro_indicators.csv`

Indicator and quality outputs:

- `outputs/indicators/raw_excel_inventory.csv`
- `outputs/indicators/data_quality_summary.csv`

Figures:

- `reports/figures/inflation_time_series.png`
- `reports/figures/usd_php_time_series.png`
- `reports/figures/inflation_features_missingness.png`
- `reports/figures/macro_indicator_correlation.png`

The monthly macro table is inflation-first and includes inflation lags, rolling averages, changes, and USD/PHP features where available.

## Phase 3 Baseline Forecasting

Forecast target:

- One-month-ahead Philippines inflation rate.

Models compared:

- Naive last-value benchmark
- 3-month moving-average benchmark
- Simple linear regression using available lag, rolling, change, and USD/PHP features

Generated outputs:

- `outputs/forecasts/inflation_forecast_test_predictions.csv`
- `outputs/forecasts/forecast_metrics.csv`
- `outputs/forecasts/latest_inflation_forecast.csv`

Figures:

- `reports/figures/inflation_actual_vs_forecast.png`
- `reports/figures/forecast_error_by_model.png`
- `reports/figures/forecast_metrics_comparison.png`
- `reports/figures/latest_forecast_context.png`

Current best baseline by RMSE is the simple linear regression model. Forecasting remains intentionally simple: no advanced nowcasting, policy-rate parser, macro scenario model, or dashboard has been built yet.

## Phase 4 Policy Interpretation

Policy context and scenario outputs:

- `outputs/scenarios/inflation_target_band_summary.csv` — BSP band position for latest observation and forecast
- `outputs/scenarios/policy_interpretation_summary.csv` — Nine-row policy and business interpretation table
- `outputs/scenarios/dashboard_policy_notes.md` — Pre-authored narrative blocks for Phase 5 dashboard

Figures:

- `reports/figures/inflation_trend_with_bsp_band.png` — Full inflation history with BSP target band
- `reports/figures/phase4_metrics_bar.png` — Model RMSE comparison

Research outputs:

- `reports/research_memo.md` — Full macro research memo with data, forecasting, and policy narrative
- `reports/model_notes.md` — Updated with Phase 4 policy interpretation limitations

## Run the Phase 4 Notebook

```bash
cd projects/philippines-macro-nowcasting-dashboard
python3 -m jupyter nbconvert --to notebook --execute notebooks/04_policy_interpretation.ipynb --output 04_policy_interpretation_executed.ipynb
```

## Run the Phase 3 Notebook

```bash
cd projects/philippines-macro-nowcasting-dashboard
python3 -m jupyter nbconvert --to notebook --execute notebooks/03_baseline_forecasting.ipynb --output 03_baseline_forecasting_executed.ipynb
```
