# Known Issues

- No blocking issue found in Phase 1.
- The full raw accepted loan file is large, so Phase 1 uses a 50,000-row sample for exploration and the modeling-ready sample.
- No unknown `loan_status` values were found in the Phase 1 sample.
- All expected Phase 1 EDA columns were present in the detected dataset sample.
- Local notebook execution exposed a Matplotlib/NumPy binary compatibility issue, so Phase 1 figures are generated through Pillow-based plotting helpers.
- Model not yet built.
- ECL assumptions not yet finalized.
- Dashboard not yet implemented.
