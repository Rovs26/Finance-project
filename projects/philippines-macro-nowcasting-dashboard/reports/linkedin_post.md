# LinkedIn Post Drafts

Portfolio project: Philippines Macro Nowcasting and Policy Dashboard
Three post options for different audiences and post lengths.

---

## Short Post (under 150 words)

Just completed a Philippines macro nowcasting and policy analytics portfolio project in Python.

The workflow covers data collection from BSP and World Bank sources, cleaning and feature engineering on 66 years of monthly inflation data, three baseline forecasting models evaluated on a chronological holdout, and policy interpretation relative to the BSP 3.0% inflation target.

Key output: a simple linear regression model forecasts April 2026 Philippines inflation at 5.02%, above the BSP 2025-2028 target band upper bound of 4.0%.

Results are presented in a five-page Streamlit dashboard covering inflation trends, forecast performance, scenario-based policy analysis, and business implications for banks, fintechs, and corporate finance.

Note: this is a portfolio research project, not an official BSP or institutional forecast.

---

## Medium Post (200-350 words)

Completed a Philippines macroeconomic nowcasting and policy analytics portfolio project.

**What I built:**
An end-to-end Python pipeline covering macro data collection (BSP, World Bank), monthly time-series cleaning and feature engineering, baseline inflation forecasting, policy interpretation, and a five-page Streamlit dashboard.

**Key findings:**
- Philippines headline inflation reached 4.1% in March 2026 — marginally above the BSP 2025-2028 target band upper bound of 4.0%.
- A simple linear regression baseline model forecasts April 2026 inflation at 5.02%, roughly 1 percentage point above the band.
- Linear regression outperforms both the naive and 3-month moving-average benchmarks on RMSE (0.4889pp vs 0.5002pp and 0.7570pp).

**Policy context:**
Both the latest observation and the model forecast are above the BSP band, suggesting a monitoring posture. The dashboard includes three analytical scenarios: BSP holds or tightens, BSP eases if inflation reverts, and an external shock scenario. Business implications for banks (NIM dynamics), fintechs (funding costs), and corporate finance (refinancing stress tests) are all covered.

**Technical stack:**
Python, pandas, NumPy, Plotly, Streamlit, Jupyter notebooks, modular source code in `src/`.

**Important note:**
This is a portfolio research project. It is not an official BSP forecast and does not represent any institutional view. The model is a simple baseline with meaningful limitations documented throughout.

---

## Technical Post (400-500 words)

Portfolio project: Philippines Macro Nowcasting and Policy Dashboard.

**Motivation:**
I wanted to build a complete macro analytics workflow from raw public data through forecasting and policy interpretation, packaged in a way that demonstrates both technical depth and business communication. The Philippines is an interesting case because the BSP has an explicit inflation targeting framework (3.0% +/-1.0pp, 2025-2028) that provides a clear analytical anchor for interpretation.

**Pipeline overview:**
The project runs in six phases. Phase 1 collects BSP inflation and USD/PHP Excel files and World Bank annual indicators. Phase 2 cleans the data and builds a monthly feature table with 8 features: inflation lags at 1, 3, and 6 months; rolling averages at 3 and 6 months; month-over-month change; and USD/PHP lag and change. Phase 3 compares three baselines on a chronological 80/20 split. Phase 4 interprets results relative to the BSP band. Phase 5 builds the Streamlit dashboard. Phase 6 packages career-facing materials.

**Modeling choices and tradeoffs:**
I chose a naive benchmark, 3-month moving average, and simple linear regression. Linear regression won on RMSE (0.4889pp) and MAE (0.3785pp). The naive model actually had lower MAPE — a known issue with MAPE when the denominator (observed inflation) is close to zero in some periods. Directional accuracy was 62.3% for linear regression vs 0% for the naive benchmark. The model uses a single chronological holdout, not rolling-origin validation — that is the most important methodological improvement for future work.

**Key numbers:**
- March 2026 observed inflation: 4.1% (above BSP band by 0.1pp)
- April 2026 model forecast: 5.02% (above BSP band by 1.02pp)
- Historical data: ~819 monthly observations (1958-2026)

**Dashboard design:**
I deliberately separated computation from presentation. All model outputs are pre-computed by the notebooks and saved as CSVs and markdown files. The Streamlit app reads those outputs without re-running any models. The dashboard_policy_notes.md file contains pre-authored narrative blocks that the app renders directly — this pattern avoids embedding business logic in the app layer.

**Limitations I documented:**
No policy rate, rice prices, oil prices, or survey expectations. Single-holdout evaluation. Test MAPE 19.1%. Directional accuracy reliable only for trend direction, not turning points. NumPy/sklearn compatibility issue in the local environment required a NumPy least-squares fallback (mathematically equivalent).

**Important note:**
This is a portfolio research project. It is not an official BSP forecast and does not represent any institutional view. All interpretations are analytical frameworks, not policy recommendations.

If you are working on similar macro analytics problems or have feedback on the methodology, I would welcome the conversation.
