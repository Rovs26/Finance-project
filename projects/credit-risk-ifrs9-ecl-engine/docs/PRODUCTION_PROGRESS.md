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

Status: Done

- Built reusable feature and modeling utilities.
- Trained a baseline logistic regression PD model.
- Evaluated ROC AUC, accuracy, precision, recall, F1, confusion matrix, and classification report.
- Saved Phase 2 figures to `reports/figures/`.
- Saved model artifact to `outputs/model/pd_logistic_regression.joblib`.
- Saved PD predictions to `outputs/predictions/pd_predictions.csv`.

## Phase 3: ECL Engine

Status: Next

- Define starter LGD and EAD assumptions.
- Use PD predictions as input to a basic ECL calculation.
- Keep IFRS 9 staging out of scope until the simple ECL engine is correct.
