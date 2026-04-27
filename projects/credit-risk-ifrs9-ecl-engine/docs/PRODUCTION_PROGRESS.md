# Production Progress

## Phase 0: Setup

Status: Done

- Created starter repository structure.
- Added documentation placeholders.
- Added source module placeholders.
- Added notebook placeholders.

## Phase 1: Data Understanding

Status: Done

- Detected the largest CSV-style raw dataset in `data/raw/`.
- Loaded a 50,000-row Phase 1 exploration sample.
- Reviewed dataset shape, schema, missingness, loan statuses, and target mapping.
- Created `default_flag` from `loan_status`.
- Saved EDA figures to `reports/figures/`.
- Saved `data/processed/modeling_sample.csv`.

## Phase 2: PD Modeling

Status: Next

- Confirm target treatment before modeling.
- Build preprocessing for numeric and categorical candidate features.
- Train and evaluate a simple benchmark probability of default model.
