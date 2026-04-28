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

- No advanced nowcasting model has been built yet.
- Dashboard not yet implemented.

## Phase 3

- No blocking issue found in Phase 3.
- The system Python has a NumPy/SciPy/sklearn compatibility issue. The Phase 3 regression utility used a NumPy least-squares fallback instead of sklearn during execution.
- Forecasting is limited to one-month-ahead baseline models using the current inflation-first feature table.
- The model does not yet include policy rates, commodity prices, survey expectations, or additional high-frequency indicators.
- Evaluation uses a single chronological holdout period, not rolling-origin validation.
- Static Plotly image export was unavailable in the local environment, so the notebook saved PNG figure files using the built-in fallback path.
