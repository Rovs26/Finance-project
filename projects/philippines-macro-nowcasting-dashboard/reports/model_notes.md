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
