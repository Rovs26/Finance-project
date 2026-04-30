# Philippines Macro Nowcasting and Policy Dashboard

A Python portfolio project demonstrating an end-to-end macroeconomic nowcasting and policy analytics workflow for the Philippines, built on publicly available BSP, PSA, and World Bank data.

---

## Business Problem

Economic research, banking, policy, and business analytics teams need clear, reproducible workflows for collecting macro indicators, monitoring inflation against policy targets, building transparent baseline forecasts, and explaining results to financial sector audiences.

---

## Target Roles and Companies

**Roles:** Economic research analyst, macro research analyst, finance analytics analyst, banking analytics analyst, policy research analyst, fintech analytics analyst

**Companies:** BSP, PIDS, JPMorgan Chase, ING Hubs Philippines, PwC Philippines, P&G Philippines, MSCI, BPI, Wells Fargo

---

## Data Sources

| Source | Series | Frequency |
|---|---|---|
| BSP (Excel download) | Headline inflation rate | Monthly (1958-2026) |
| BSP (Excel download) | USD/PHP exchange rate | Monthly (~2000-2026) |
| World Bank API | GDP growth, unemployment, remittances | Annual |
| PSA | Official CPI and inflation (reference) | Monthly |

---

## Methodology

1. Collect public Philippines macro data from BSP Excel files and World Bank API
2. Clean and standardize monthly time series
3. Engineer lag (1, 3, 6 months), rolling average (3, 6 months), and change features
4. Compare three one-month-ahead inflation forecasting baselines on a chronological 80/20 split
5. Interpret forecast outputs relative to BSP inflation target band (3.0% +/-1.0pp, 2025-2028)
6. Produce scenario-style policy and business interpretation
7. Present in a Streamlit dashboard

---

## Key Results

| Metric | Value |
|---|---|
| Latest observed inflation (March 2026) | 4.1% — above BSP band |
| April 2026 model forecast | 5.02% — above BSP band |
| BSP target band (2025-2028) | 2.0%-4.0% (midpoint 3.0%) |
| Best model | Linear regression |
| Linear regression RMSE (test) | 0.4889 pp |
| Linear regression MAE (test) | 0.3785 pp |
| Directional accuracy | 62.3% |
| Historical data | ~819 monthly observations (1958-2026) |

---

## Dashboard

Five-page Streamlit dashboard built in `dashboard/app.py`:

| Page | Content |
|---|---|
| Overview | KPI cards, executive summary, band position at a glance |
| Inflation and Target Band | Full history + 5-year zoom charts, BSP band overlay, target band position table |
| Forecast Performance | Metrics table, RMSE comparison, actual vs forecast chart, error chart |
| Policy Interpretation | Tabbed scenario analysis, full interpretation table, business relevance by sector |
| Data and Limitations | Data sources, methodology, limitations table, future improvements |

### Run the dashboard

```bash
cd projects/philippines-macro-nowcasting-dashboard
streamlit run dashboard/app.py
```

---

## How to Run Notebooks

Re-execute any phase notebook:

```bash
cd projects/philippines-macro-nowcasting-dashboard

# Phase 2: Cleaning and features
python3 -m jupyter nbconvert --to notebook --execute notebooks/02_cleaning_and_features.ipynb --output 02_cleaning_and_features_executed.ipynb

# Phase 3: Baseline forecasting
python3 -m jupyter nbconvert --to notebook --execute notebooks/03_baseline_forecasting.ipynb --output 03_baseline_forecasting_executed.ipynb

# Phase 4: Policy interpretation
python3 -m jupyter nbconvert --to notebook --execute notebooks/04_policy_interpretation.ipynb --output 04_policy_interpretation_executed.ipynb
```

**Note:** matplotlib 3.10.9+ required (NumPy 2.x compatibility).

---

## Outputs Generated

### Processed data
- `data/processed/monthly_macro_indicators.csv` — 819-row monthly feature table (1958-2026)
- `data/processed/monthly_inflation.csv` — cleaned BSP monthly inflation series
- `data/processed/monthly_usd_php.csv` — cleaned BSP USD/PHP series
- `data/processed/annual_macro_context.csv` — World Bank annual context indicators

### Forecasts
- `outputs/forecasts/latest_inflation_forecast.csv` — April 2026 forecast (5.02%)
- `outputs/forecasts/forecast_metrics.csv` — test set metrics for all three models
- `outputs/forecasts/inflation_forecast_test_predictions.csv` — full test set predictions

### Policy interpretation
- `outputs/scenarios/inflation_target_band_summary.csv` — BSP band position (observed + forecast)
- `outputs/scenarios/policy_interpretation_summary.csv` — 9-row scenario and business table
- `outputs/scenarios/dashboard_policy_notes.md` — pre-authored narrative for the dashboard

### Figures
- `reports/figures/inflation_trend_with_bsp_band.png`
- `reports/figures/inflation_actual_vs_forecast.png`
- `reports/figures/forecast_metrics_comparison.png`
- `reports/figures/latest_forecast_context.png`
- `reports/figures/phase4_metrics_bar.png`

---

## Reports

| File | Description |
|---|---|
| `reports/research_memo.md` | Full macro research memo (8 sections) |
| `reports/model_notes.md` | Model documentation and limitations across all phases |
| `reports/resume_bullets.md` | Resume bullets for target roles |
| `reports/interview_talking_points.md` | Interview Q&A for common questions |
| `reports/company_positioning.md` | Company-specific application angles |
| `reports/linkedin_post.md` | LinkedIn post drafts |

---

## Project Phases

| Phase | Status |
|---|---|
| Phase 0: Setup | Done |
| Phase 1: Macro data collection | Done |
| Phase 2: Cleaning and feature engineering | Done |
| Phase 3: Baseline forecasting | Done |
| Phase 4: Policy interpretation | Done |
| Phase 5: Streamlit dashboard | Done |
| Phase 6: GitHub polish | Done |

---

## Limitations

- Model is a simple linear regression baseline, not advanced nowcasting
- No BSP policy rate, rice prices, oil prices, core inflation, or survey expectations
- Chronological 80/20 split only; no rolling-origin validation
- Test MAPE 19.1%; forecast errors are non-trivial for policy decisions
- This is a portfolio research project — not an official BSP, PSA, or institutional forecast

---

## Future Improvements

1. Rolling-origin validation for realistic out-of-sample performance measurement
2. BSP policy rate data integration
3. Rice and food price features (key CPI driver in the Philippines)
4. Core inflation decomposition
5. Regularised or ensemble models
6. BSP inflation expectations survey as a feature

---

## Resume Bullet

Built an end-to-end Philippines macroeconomic nowcasting and policy analytics pipeline in Python — collecting BSP and World Bank data, engineering 66 years of monthly inflation features, comparing three baseline forecasting models (best RMSE 0.4889pp), interpreting results against BSP's 3.0% inflation target, and delivering findings in a five-page Streamlit dashboard with scenario-based business implications for banks, fintechs, and corporate finance.

---

## Disclaimer

This is a portfolio research project. It is not affiliated with, endorsed by, or representative of the Bangko Sentral ng Pilipinas (BSP), the Philippine Statistics Authority (PSA), or any official institution. Nothing in this repository constitutes an official economic forecast, investment advice, or policy recommendation.
