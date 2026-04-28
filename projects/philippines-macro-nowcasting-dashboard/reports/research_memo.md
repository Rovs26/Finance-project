# Philippines Macro Nowcasting: Research Memo

**Date:** April 2026 (portfolio project)
**Disclaimer:** This is a portfolio research project. Nothing in this document constitutes an official economic forecast, investment advice, or guidance from the Bangko Sentral ng Pilipinas (BSP), the Philippine Statistics Authority (PSA), or any official institution.

---

## Executive Summary

Philippines headline inflation reached 4.1% in March 2026, marginally above the upper bound of the BSP's 2025–2028 inflation target band of 2.0%–4.0%. A simple linear regression baseline model, trained on historical Philippines monthly inflation and USD/PHP exchange rate data, forecasts April 2026 inflation at approximately 5.02%—approximately 1.0 percentage point above the target band upper bound.

The baseline model has limited scope (no policy rate, rice prices, or commodity inputs) and meaningful forecast uncertainty (RMSE of 0.49pp on the test set). These results are interpreted as analytical reference points, not as prescriptions for policy or investment decisions. The BSP is likely in a monitoring posture given the above-band inflation trajectory, and financial sector participants should stress-test their planning assumptions against scenarios ranging from continued elevated inflation to a swift disinflation reversal.

---

## 1. Data Sources

| Source | Series | Frequency | Coverage |
|---|---|---|---|
| BSP (via Excel download) | Headline inflation rate | Monthly | 1958–March 2026 |
| BSP (via Excel download) | USD/PHP exchange rate | Monthly | ~2000–2026 |
| World Bank API | GDP growth (annual), unemployment (annual), inflation backup, remittances as % of GDP | Annual | ~1960–2023 |

**Primary source:** The BSP historical inflation Excel file (`infrate2018.xls` from BSP additional sources) was parsed as the main monthly inflation series. PSA is the official source of CPI and inflation data in the Philippines. BSP historical data aligns with PSA-reported CPI.

**Limitations:** BSP policy rate, BSP prices data, and PSA CPI detail (e.g., food, core, bottom 30%) are referenced in the source inventory but not parsed in this project. World Bank data is annual-frequency only and is not used in the forecasting pipeline.

---

## 2. Cleaned Indicators

The Phase 2 pipeline produced four processed datasets:

- **`monthly_inflation.csv`** — Monthly Philippines headline inflation rate, 1958–March 2026.
- **`monthly_usd_php.csv`** — Monthly USD/PHP exchange rate (peso per US dollar).
- **`annual_macro_context.csv`** — World Bank annual indicators (GDP growth, unemployment, remittances) merged by year.
- **`monthly_macro_indicators.csv`** — Combined monthly table with inflation-first feature engineering.

The monthly macro indicators table includes 13 columns: date, year, month, inflation_rate, usd_php, inflation_rate_lag_1, inflation_rate_lag_3, inflation_rate_lag_6, inflation_rate_rolling_3, inflation_rate_rolling_6, inflation_rate_change_1, usd_php_lag_1, and usd_php_change_1.

The full dataset spans approximately 819 monthly observations from January 1958 to March 2026. USD/PHP data is available from approximately 2000 onward. Lag and rolling features create expected null values at the start of the series.

---

## 3. Forecasting Method Summary

**Target:** One-month-ahead Philippines headline inflation rate.

**Models compared:**

| Model | Description |
|---|---|
| Naive last-value | Predicts next month using current observed inflation (no change assumption) |
| 3-month moving average | Predicts using trailing 3-month average |
| Simple linear regression | Uses 8 features: inflation lags (1, 3, 6m), rolling averages (3, 6m), month-over-month change, USD/PHP lag and change |

**Evaluation method:** Chronological 80/20 train/test split. No random splitting, no rolling-origin validation.

**Implementation note:** The local Python environment has a NumPy/sklearn compatibility issue. The Phase 3 linear regression utility used a transparent NumPy least-squares fallback. Results are mathematically equivalent to sklearn `LinearRegression`.

---

## 4. Latest Forecast Result

| Metric | Value |
|---|---|
| Forecast origin | March 2026 |
| Forecast target | April 2026 |
| Latest observed inflation (March 2026) | 4.1% |
| Model forecast (April 2026) | 5.0198% |
| Model | Linear regression (NumPy least-squares) |
| BSP target band | 2.0%–4.0% (3.0% midpoint) |
| Observed position vs band | Above band (+0.1pp above upper bound) |
| Forecast position vs band | Above band (+1.02pp above upper bound) |

**Test set performance:**

| Model | MAE | RMSE | MAPE | Directional Accuracy |
|---|---|---|---|---|
| Linear regression | 0.3785 | 0.4889 | 19.13% | 62.33% |
| Naive last-value | 0.3828 | 0.5002 | 18.21% | 0.00% |
| 3-month moving average | 0.6039 | 0.7570 | 28.57% | 36.30% |

The linear regression model outperforms both benchmarks on RMSE and MAE. The naive model has a lower MAPE, which reflects MAPE sensitivity to the denominator at low absolute inflation values — not a sign of better forecasting. Linear regression directional accuracy (62.3%) meaningfully exceeds the naive benchmark (0%).

---

## 5. BSP Target Band Interpretation

The BSP uses an inflation targeting framework. For 2025 to 2028, the target is 3.0% with a tolerance band of ±1.0 percentage point (effective range: 2.0%–4.0%).

- March 2026 observed inflation (4.1%) is 0.1pp above the upper bound — a marginal breach.
- April 2026 model forecast (5.02%) is approximately 1.02pp above the upper bound — a more pronounced above-band reading if the forecast materialises.

A single month above the target band does not automatically trigger BSP policy action. The BSP Monetary Board evaluates a broad set of factors including core inflation, output gap, global commodity conditions, exchange rate developments, and inflation expectations. However, two consecutive above-band readings with an accelerating trajectory would typically warrant a more hawkish monitoring posture.

---

## 6. Business Interpretation

**Scenario A — BSP holds or tightens (elevated inflation persists):** If inflation remains above the 4.0% upper bound into Q2 2026, the BSP is likely to maintain its policy rate or tighten. Banks benefit from NIM support on variable-rate loan books; fintechs face higher funding costs and potential delinquency risk; corporates should model refinancing assumptions at higher rates.

**Scenario B — BSP eases (inflation reverts to target):** If inflation decelerates sharply toward 3.0% — driven by lower rice prices, peso appreciation, or demand moderation — the BSP may resume its easing cycle. This creates a favorable refinancing environment for corporates and lower funding costs for fintechs.

**Scenario C — External shock amplifies upside (FX or commodity):** Peso depreciation or a commodity price spike could push inflation well above the model forecast. Corporates with USD-denominated inputs or liabilities face simultaneous FX and rate pressure.

**Banks:** NIM expansion risk/opportunity; credit quality monitoring as consumer prices compress household capacity.

**Fintechs:** Stress-test funding cost assumptions; monitor early delinquency signals; evaluate FX funding exposure.

**Corporate finance:** Stress-test refinancing at 4.5%–5.5% inflation scenarios for H1 2026; account for USD/PHP at ~59.4 in import cost models.

---

## 7. Limitations

- The model is a simple linear regression baseline, not an advanced nowcasting or structural macroeconomic model.
- Inputs are limited to historical inflation lags, rolling averages, and USD/PHP features. Rice prices, oil prices, core inflation, BSP policy rate, fiscal variables, and survey expectations are not included.
- Test MAPE of 19.1% implies typical absolute forecast errors that may be material for policy or business decisions. Plausible April 2026 range given model RMSE: approximately 4.5%–5.5%.
- Directional accuracy of 62.3% is above the naive baseline but is not reliable for calling turning points or sharp reversals.
- The chronological 80/20 split does not simulate real-time rolling-origin forecasting. Reported test metrics likely overstate live out-of-sample performance.
- This is a portfolio research project. All interpretations are analytical only.

---

## 8. Next Improvements

1. **Rolling-origin validation** — Replace the single 80/20 split with a walk-forward evaluation to better simulate live forecasting.
2. **Add policy rate data** — Parse BSP key rates page to include lagged policy rate as a feature.
3. **Add rice and food price features** — Rice prices are a key driver of Philippines headline inflation; they are referenced but not parsed in Phase 1.
4. **Core inflation decomposition** — Separate core from food-and-energy components to improve signal quality.
5. **Ensemble or regularised models** — Consider Ridge regression or a simple ensemble to reduce overfitting on short feature sets.
6. **Phase 5 dashboard** — Build a Streamlit dashboard in `dashboard/app.py` consuming pre-computed outputs from Phases 3 and 4.
