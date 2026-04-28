# Model Notes

## Phase 1 Data Sources Used

- BSP historical inflation Excel: `https://www.bsp.gov.ph/statistics/excel/infrate.xls`
- BSP USD/PHP historical Excel: `https://www.bsp.gov.ph/statistics/external/pesodollar.xlsx`
- BSP key rates page: `https://www.bsp.gov.ph/SitePages/Statistics/KeyRates.aspx`
- BSP prices page: `https://www.bsp.gov.ph/SitePages/Statistics/Prices.aspx`
- PSA CPI and inflation page: `https://psa.gov.ph/price-indices/cpi-ir`
- World Bank API indicators for GDP growth, unemployment, inflation backup, and remittances as percent of GDP.

## Source Rationale

BSP and PSA are the primary sources for Philippines macro data because they are official domestic institutions responsible for monetary, price, and national statistics. For an inflation-first MVP, BSP inflation data and BSP policy-rate references are the most relevant starting points.

World Bank data is used as annual backup and cross-country comparable context. It is useful for GDP growth, unemployment, inflation backup, and remittances, but it may lag official domestic releases.

## Known Source Limitations

- BSP Excel workbooks are downloaded as raw files and still need sheet-level inspection before cleaning.
- BSP key rates, BSP prices, and PSA CPI pages are included in the inventory but require manual handling or later parser development.
- World Bank indicators are annual and not enough for high-frequency nowcasting by themselves.
- Phase 1 only collects and inventories sources; it does not finalize the forecasting target or build modeling features.

## Phase 2 Parsing Decisions

- All `.xls` and `.xlsx` files under `data/raw/` were inventoried in `outputs/indicators/raw_excel_inventory.csv`.
- The original BSP inflation file `bsp_inflation_infrate.xls` was parsed successfully but ends in 2018.
- The additional local BSP file `additional_sources/infrate2018.xls` was parseable and extends through March 2026, so it was used for `monthly_inflation.csv`.
- BSP peso-dollar data was parsed from the monthly sheet in `bsp_peso_dollar.xlsx`.
- World Bank annual CSV files were merged by year into `annual_macro_context.csv`.

## Cleaned Datasets Created

- `data/processed/monthly_inflation.csv`
- `data/processed/monthly_usd_php.csv`
- `data/processed/annual_macro_context.csv`
- `data/processed/monthly_macro_indicators.csv`

## Feature Engineering Choices

- Inflation is the first forecasting target candidate because it is central to Philippines macro policy analysis and BSP monitoring.
- The monthly feature table includes `inflation_lag_1`, `inflation_lag_3`, `inflation_lag_6`, `inflation_rolling_3`, `inflation_rolling_6`, and `inflation_change_1`.
- USD/PHP is included as an external macro-financial indicator with `usd_php_lag_1` and `usd_php_change_1`.
- World Bank annual indicators are retained as context and are not forced into the monthly table in Phase 2.

## Phase 2 Limitations

- Policy rate data is not yet parsed.
- Some additional local Excel files were inspected but not used because they require separate layout-specific parsers.
- Feature engineering is intentionally simple and no forecasting model has been trained yet.
- Legacy `.xls` parsing requires `xlrd` in the local Python environment.

## Phase 3 Forecasting Target

The Phase 3 target is one-month-ahead Philippines `inflation_rate`. The notebook creates `inflation_target_1m` by shifting monthly inflation forward one month and evaluates forecasts on the final 20 percent of usable observations.

## Models Used

- Naive last-value benchmark: predicts next-month inflation using the current observed inflation rate.
- 3-month moving-average benchmark: predicts next-month inflation using the latest three-month average.
- Simple linear regression: uses available inflation lag, rolling, change, and USD/PHP features.

## Split and Metrics

- Split method: chronological train/test split only; no random split.
- Metrics: MAE, RMSE, MAPE where safe, and directional accuracy where safe.
- Best model by RMSE: linear regression.
- Linear regression test metrics: MAE `0.3785`, RMSE `0.4889`, MAPE `19.13%`, directional accuracy `62.33%`.
- Naive benchmark test metrics: MAE `0.3828`, RMSE `0.5002`, MAPE `18.21%`.
- Moving-average benchmark test metrics: MAE `0.6039`, RMSE `0.7570`, MAPE `28.57%`.

## Latest Forecast

The latest available forecast origin is March 2026. The baseline linear regression forecast for April 2026 inflation is `5.0198`, compared with latest observed March 2026 inflation of `4.1`.

## Phase 3 Limitations

- The system Python has a NumPy/SciPy/sklearn compatibility issue, so the regression utility used the transparent NumPy least-squares fallback during notebook execution.
- The model is a baseline linear forecast, not an advanced nowcasting model.
- No policy-rate, commodity, survey, or high-frequency indicators are included yet.
- Evaluation uses one chronological holdout period; rolling-origin validation is a future improvement.
- These outputs are for macro research portfolio analysis, not official policy forecasting.

## Why This Matters

Phase 3 demonstrates a practical macro research workflow: define a forecast target, compare simple benchmarks, evaluate out-of-sample forecast error, and translate results into policy-relevant limitations before attempting more complex models.

## Phase 4 Policy Interpretation

Phase 4 produced three outputs in `outputs/scenarios/`:

- `inflation_target_band_summary.csv` — BSP band position summary for the latest observation and forecast (1 row, 9 columns).
- `policy_interpretation_summary.csv` — Nine-row policy and business interpretation table with columns: section, finding, implication, caveat.
- `dashboard_policy_notes.md` — Pre-authored narrative text blocks for the Phase 5 Streamlit dashboard.

Phase 4 also produced two figures in `reports/figures/`:

- `inflation_trend_with_bsp_band.png` — Full historical inflation series with BSP target band overlay and latest forecast point.
- `phase4_metrics_bar.png` — Horizontal bar chart comparing model RMSE across the three Phase 3 baselines.

The baseline linear regression model is not designed for policy prescription. The Phase 4 interpretation documents what the model output implies analytically, subject to the caveats documented in Phase 3 and reinforced here.

## Phase 4 Limitations

- Scenario descriptions are analytical frames, not forward-looking policy guidance.
- The model does not include rice prices, oil prices, core inflation, or BSP policy rate.
- Band breach classification uses strict greater-than/less-than logic against the stated BSP target bounds (2.0%–4.0%, 2025–2028). Any future change to the BSP target period would require updating the constants in the notebook Cell 3.
- matplotlib 3.10.9 was installed during Phase 4 execution to resolve a NumPy 2.x compatibility issue with the previously installed matplotlib 3.7.2. This resolves the Phase 3 documented NumPy/matplotlib conflict.
