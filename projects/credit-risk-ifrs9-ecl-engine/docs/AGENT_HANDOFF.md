# Agent Handoff

## Current State

Phase 3 ECL engine has been completed for the Credit Risk and IFRS 9 Expected Credit Loss Engine. The project now has row-level ECL results, scenario summaries, ECL figures, and a business memo.

## Files Changed

- `README.md`
- `notebooks/03_ecl_engine.ipynb`
- `notebooks/03_ecl_engine_executed.ipynb`
- `src/ecl.py`
- `src/visualization.py`
- `reports/business_memo.md`
- `docs/PRODUCTION_PROGRESS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/AGENT_HANDOFF.md`

## Input Used

- `outputs/predictions/pd_predictions.csv`
- 50,000 rows

## EAD Method Used

EAD uses `loan_amnt`, because it is available in the PD prediction file.

## LGD Method Used

LGD uses a simplified home-ownership adjustment:

- MORTGAGE: 35%
- OWN: 40%
- RENT: 50%
- Other or missing: 45%

## Staging Rules Used

- Stage 1: `pd_score < 0.20`
- Stage 2: `0.20 <= pd_score < 0.50`
- Stage 3: `pd_score >= 0.50` or `default_flag == 1`

## Outputs Created

- `outputs/ecl_results.csv`
- `outputs/predictions/ecl_scenario_summary.csv`
- `reports/figures/ecl_by_stage.png`
- `reports/figures/exposure_by_stage.png`
- `reports/figures/ecl_by_score_band.png`
- `reports/figures/ecl_by_grade.png`
- `reports/figures/ecl_by_purpose.png`
- `reports/figures/scenario_ecl_comparison.png`
- `reports/figures/ecl_distribution.png`

## Key Results

- Base total exposure: 750,967,975.00
- Base total ECL: 146,297,248.66
- Mild stress total ECL: 200,746,300.69
- Severe stress total ECL: 255,838,508.12

## Next Recommended Task

Start Phase 4 by creating the business interpretation notebook and dashboard-ready summary tables, then build the Streamlit dashboard after the interpretation layer is clear.
