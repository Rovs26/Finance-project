# Interview Talking Points

## 1. What problem does this project solve?

It solves a common finance analytics problem: raw market data is not immediately useful until it is ingested, standardized, validated, and made queryable. I built a small pipeline that takes public price data and turns it into SQL-ready tables, validation outputs, and a local warehouse.

## 2. Why did you use DuckDB?

DuckDB is lightweight, fast for analytical queries, and easy to run locally without a server. For a portfolio project, it lets me demonstrate warehouse-style thinking without needing cloud infrastructure.

## 3. What tables did you create?

I created `dim_assets`, `fact_prices`, and `fact_returns`. The fact tables are long-format tables at the `(date, ticker)` grain, which makes them easier to query with SQL than wide spreadsheet-style data.

## 4. What data quality checks did you implement?

I checked required columns, duplicate keys, date ranges, missing values, positive prices, reasonable daily return ranges, and referential integrity between fact tables and the asset dimension.

## 5. What did the validation results show?

The latest run passed 15 out of 15 checks. That means the processed tables had the expected schema, no duplicate ticker-date keys, no missing values, valid ticker relationships, positive prices, and daily returns inside the configured bounds.

## 6. How does this relate to finance or banking work?

Finance teams depend on clean, traceable data before doing risk reporting, portfolio analytics, reconciliations, or model development. This project shows that I can build the data layer before jumping into analysis.

## 7. Why include SQL?

SQL is still the main language for querying finance and risk data. The sample queries show how an analyst could retrieve latest prices, return statistics, best and worst return days, and joined price-return views from the warehouse.

## 8. Why add an API?

The API is a small demonstration of serving warehouse outputs as a data product. It is not a full production service, but it shows the path from validated tables to reusable endpoints.

## 9. What are the main limitations?

The project uses public yfinance data, runs as a batch notebook workflow, and does not include orchestration, CI, cloud deployment, or production monitoring. Those would be the next steps.

## 10. What would you improve next?

I would add scheduled orchestration, CI tests for validation functions, incremental ingestion, validation history, and a deployment plan for the API if the project needed to become a real internal data service.
