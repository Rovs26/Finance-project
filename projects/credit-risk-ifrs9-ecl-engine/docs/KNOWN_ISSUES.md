# Known Issues

- No blocking issue found in Phase 1.
- The full raw accepted loan file is large, so Phase 1 uses a 50,000-row sample for exploration and the modeling-ready sample.
- No unknown `loan_status` values were found in the Phase 1 sample.
- All expected Phase 1 EDA columns were present in the detected dataset sample.
- Local notebook execution exposed a Matplotlib/NumPy binary compatibility issue, so Phase 1 figures are generated through Pillow-based plotting helpers.
- No blocking issue found in Phase 2.
- The system Python also has a NumPy/SciPy/scikit-learn compatibility issue, so Phase 2 was executed using a project-local `.venv`.
- The first full `requirements.txt` installation attempt timed out on larger dashboard-related dependencies; the local `.venv` was completed with the minimal Phase 2 packages needed for notebook execution.
- `funded_amnt` and `loan_status` were requested for PD prediction exports if available, but they were not present in `data/processed/modeling_sample.csv`.
- The baseline model has moderate ROC AUC and low precision, so it should be treated as a benchmark rather than a production-ready PD model.
- No blocking issue found in Phase 3.
- Phase 3 uses `loan_amnt` as the EAD proxy because it is available in `outputs/predictions/pd_predictions.csv`.
- Phase 3 LGD is a simplified home-ownership rule, not a recovery model.
- Phase 3 staging is a simplified PD-threshold proxy, not official IFRS 9 compliance logic.
- Scenario analysis applies simple PD and LGD multipliers only; no macroeconomic model is included.
- Dashboard not yet implemented.
