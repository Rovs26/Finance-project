# Agent Handoff

## Current State

Phase 4B Streamlit dashboard has been completed for the Credit Risk and IFRS 9 Expected Credit Loss Engine. The project now has an interactive dashboard that reads the existing ECL output tables and loan-level ECL results.

## Files Changed

- `README.md`
- `dashboard/app.py`
- `docs/PRODUCTION_PROGRESS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/AGENT_HANDOFF.md`

## Dashboard Pages Built

- Portfolio Overview
- IFRS 9 Staging
- Risk Segments
- Scenario Analysis
- Loan-Level Explorer
- Methodology and Limitations

## Dashboard Inputs

- `outputs/ecl_results.csv`
- `outputs/predictions/dashboard_summary.csv`
- `outputs/predictions/ecl_by_stage.csv`
- `outputs/predictions/ecl_by_score_band.csv`
- `outputs/predictions/ecl_by_grade.csv`
- `outputs/predictions/ecl_by_purpose.csv`
- `outputs/predictions/ecl_scenario_summary.csv`

## Run Command

```bash
streamlit run dashboard/app.py
```

## Dashboard Features

- KPI cards for portfolio summary.
- Plotly charts for stage, score band, segment, and scenario views.
- Filterable loan-level explorer with a 500-row display limit.
- Download button for filtered loan-level rows.
- Visible methodology and limitations page.

## Next Recommended Task

Start Phase 5 by polishing the GitHub presentation, deciding whether generated output artifacts should stay ignored or be committed, and adding final usage notes or screenshots.
