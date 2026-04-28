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

Setup phase only. The repository structure and placeholder files are created, but no macro data collection, cleaning, forecasting, dashboard, or results have been implemented.
