# Known Issues

## Phase 1

- No blocking issue found in Phase 1.
- BSP inflation and peso-dollar files downloaded successfully, but workbook parsing is deferred to Phase 2.
- BSP key rates page requires manual handling or later parser development.
- BSP prices page is included as a reference source but not parsed yet.
- PSA CPI and inflation page is included as a primary reference but not parsed yet.
- World Bank indicators are annual and useful for backup context, not high-frequency nowcasting by themselves.

## Phase 2

- No blocking issue found in Phase 2.
- Legacy `.xls` parsing required installing `xlrd` in the local Python environment.
- The original BSP inflation file was parsed successfully but only runs through 2018; `additional_sources/infrate2018.xls` was used for the cleaned inflation series because it extends through March 2026.
- Additional local Excel files were inspected but not merged into the core table unless clearly parseable for the inflation-first MVP.
- Inspected but not used in the core table: `API_PHL_DS2_en_excel_v2_6947.xls`, `RERB.xlsx`, `Statistical Tables on March 2026 CPI for All Income Households (2018=100)_k4r8j.xlsx`, `inf_bottom30_2018.xls`, `infrate_comm2018.xls`, `pesodollar.xlsx`, and `prices2018.xls`.
- Policy rate data is still missing and requires manual handling or later parser development.
- Initial lag and rolling features create expected missing values at the start of the monthly series.

## Still Open for Future Phases

- No advanced nowcasting model has been built. Baseline linear regression only.
- Rolling-origin validation not yet implemented; single chronological holdout used throughout.

## Phase 3

- No blocking issue found in Phase 3.
- The system Python has a NumPy/SciPy/sklearn compatibility issue. The Phase 3 regression utility used a NumPy least-squares fallback instead of sklearn during execution.
- Forecasting is limited to one-month-ahead baseline models using the current inflation-first feature table.
- The model does not yet include policy rates, commodity prices, survey expectations, or additional high-frequency indicators.
- Evaluation uses a single chronological holdout period, not rolling-origin validation.
- Static Plotly image export was unavailable in the local environment, so the notebook saved PNG figure files using the built-in fallback path.

## Phase 4

- No blocking issue found in Phase 4.
- matplotlib 3.7.2 was incompatible with the installed NumPy 2.4.1 (compiled against NumPy 1.x). This caused an import error during initial notebook execution. Resolved by upgrading matplotlib to 3.10.9 via pip during Phase 4 setup. The notebook now executes cleanly.
- Policy rate data remains unparsed. BSP key rates page is referenced in the source inventory but manual handling is required. Policy rate is not included in the forecasting features.
- The model used in Phase 4 interpretation is the same baseline linear regression from Phase 3. No new modeling was done in Phase 4.
- Scenario descriptions are analytical frames. They do not constitute macroeconomic guidance, investment advice, or BSP guidance.
- This project is not an official BSP forecast. All outputs are portfolio research materials only.
- BSP target band constants (2.0%–4.0%, midpoint 3.0%, 2025–2028) are hardcoded in the Phase 4 notebook. If BSP announces a new target period, update the constants in notebook Cell 3 and re-execute before Phase 5 dashboard launch.

## Phase 5 and Phase 6

- No blocking issue found in Phases 5 or 6.
- Policy rate data remains unparsed across all phases. BSP key rates page is referenced in the source inventory but requires manual handling. Policy rate is not included in any forecasting features or dashboard inputs.
- The forecasting model is a simple linear regression baseline only. No advanced nowcasting, structural model, or machine-learning model has been built.
- This project is not an official BSP, PSA, or institutional forecast. All outputs are portfolio research materials only.
- Generated output files (outputs/forecasts/*.csv, outputs/scenarios/*.csv, outputs/scenarios/*.md, reports/figures/*.png) are committed to the repository for reproducibility. After a fresh clone, notebooks may be re-executed to regenerate them; matplotlib 3.10.9 and standard scientific Python packages are required.
- The Streamlit dashboard reads pre-computed output files. If output files are deleted or moved, the dashboard will show Streamlit warnings for each missing file rather than crashing.
- BSP target band constants (2.0%–4.0%, midpoint 3.0%, 2025–2028) are hardcoded in `dashboard/app.py` and in the Phase 4 notebook. Update both if BSP announces a new target period.
