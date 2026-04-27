# Model Card: Baseline PD Logistic Regression

## Model Purpose

Estimate a baseline probability of default (PD) score for loan-level records using the Phase 1 modeling sample. The model is intended to provide an interpretable benchmark for Phase 3 Expected Credit Loss work.

## Data Used

- Source file: `data/processed/modeling_sample.csv`
- Rows used: 50,000
- Train-test split: 80% train and 20% test, stratified on `default_flag`
- Raw source lineage: manually provided LendingClub-style accepted loan data

## Target Definition

Target column: `default_flag`

- `1`: default status mapped from Phase 1 loan-status rules
- `0`: non-default status mapped from Phase 1 loan-status rules

Phase 2 preserves the Phase 1 assumption that `Current`, `In Grace Period`, and `Late (16-30 days)` are mapped to non-default for this starter benchmark.

## Features Used

Available candidate features from the processed modeling sample were used, including:

- Loan terms and amount fields: `loan_amnt`, `term`, `int_rate`, `installment`
- Credit grade fields: `grade`, `sub_grade`
- Borrower and application fields: `emp_length`, `home_ownership`, `annual_inc`, `verification_status`, `purpose`, `application_type`
- Credit history fields: `dti`, `delinq_2yrs`, `fico_range_low`, `fico_range_high`, `inq_last_6mths`, `open_acc`, `pub_rec`, `revol_bal`, `revol_util`, `total_acc`, `mort_acc`, `pub_rec_bankruptcies`

## Model Type

Baseline logistic regression using a scikit-learn `Pipeline` and `ColumnTransformer`.

- Numeric preprocessing: median imputation and standard scaling
- Categorical preprocessing: most-frequent imputation and one-hot encoding
- Class handling: `class_weight="balanced"`
- Solver: logistic regression with increased `max_iter`

## Evaluation Metrics

Test set metrics:

| Metric | Value |
| --- | ---: |
| ROC AUC | 0.701 |
| Accuracy | 0.632 |
| Precision | 0.285 |
| Recall | 0.651 |
| F1 Score | 0.396 |

Confusion matrix on 10,000 test rows:

|  | Predicted 0 | Predicted 1 |
| --- | ---: | ---: |
| Actual 0 | 5,107 | 3,038 |
| Actual 1 | 647 | 1,208 |

## Interpretation

The model shows moderate discriminatory power for a starter PD benchmark. The balanced class weighting improves default recall, which is useful for risk screening, but this comes with a relatively high false-positive count and low precision. The score bands should be treated as ordinal risk segments, not as final calibrated regulatory PD estimates.

## Limitations

- Trained on a 50,000-row sample, not the full raw dataset.
- Current and early delinquency statuses are treated as non-default based on Phase 1 rules.
- No time-based validation has been performed yet.
- No probability calibration has been performed yet.
- No macroeconomic variables, IFRS 9 staging, LGD, EAD, or ECL calculation is included.
- The local system Python has a NumPy/SciPy/scikit-learn compatibility issue, so Phase 2 was executed in a project-local `.venv`.

## Intended Use

- Portfolio demonstration of baseline credit risk modeling.
- Input candidate for Phase 3 ECL engine development.
- Educational analysis for early-career risk analytics, fintech analytics, and financial data analytics roles.

## Not Intended Use

- Production credit approval or decline decisions.
- Regulatory model submission.
- Customer-level lending actions.
- IFRS 9 reporting without further validation, calibration, staging logic, LGD, and EAD assumptions.

## Next Improvements

- Confirm target treatment for `Current`, `In Grace Period`, and `Late (16-30 days)` accounts.
- Add time-aware validation using issue dates if available.
- Review coefficient stability and feature leakage risk.
- Calibrate PD scores before ECL use.
- Compare against additional models only after the baseline workflow is fully documented.
