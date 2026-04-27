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

Status: Done

- Defined starter EAD and LGD assumptions.
- Assigned simplified IFRS 9-style stages.
- Calculated row-level ECL using PD x LGD x EAD.
- Created Base, Mild stress, and Severe stress scenario summaries.
- Saved ECL results to `outputs/ecl_results.csv`.
- Saved scenario summary to `outputs/predictions/ecl_scenario_summary.csv`.
- Saved Phase 3 ECL figures to `reports/figures/`.

## Phase 4A: Business Interpretation

Status: Done

- Build business interpretation notebook using ECL outputs.
- Prepare dashboard-ready summary views.
- Created resume bullets, interview talking points, company positioning, and LinkedIn post drafts.
- Polished the business memo and aligned the model card with downstream use.
- Saved dashboard-ready tables to `outputs/predictions/`.

## Phase 4B: Streamlit Dashboard

Status: Done

- Build Streamlit dashboard from the Phase 4A dashboard-ready tables.
- Include portfolio overview, stage analysis, score band analysis, grade/purpose views, and scenario comparison.
- Keep limitations visible in the dashboard.
- Completed dashboard UI polish with custom CSS, styled KPI cards, key insight callouts, cleaner Plotly charts, and formatted tables.

## Phase 5: Polish and GitHub Cleanup

Status: Done

- Review README and report links for GitHub presentation.
- Decide which ignored generated artifacts should remain reproducible only versus committed.
- Add usage notes for regenerated artifacts and dashboard inputs.
- Clean up local environment notes and final limitations.

## Optional: Screenshots and Live Demo

Status: In Progress

- Added dashboard overview and scenario analysis screenshots to the README.
- Add more dashboard screenshots or a short demo GIF if useful.
- Consider a lightweight demo dataset if sharing without raw LendingClub-style data.
- Add final GitHub release notes if desired.
