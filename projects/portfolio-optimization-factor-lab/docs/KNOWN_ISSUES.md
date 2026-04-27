# Known Issues

## Phase 1

- No blocking issue found in Phase 1.
- `yfinance` was not initially installed in the system Python environment and was installed before notebook execution.
- The local Matplotlib install has a NumPy compatibility issue, so Phase 1 uses Plotly helpers and a Pillow-based PNG export fallback when Plotly static export is unavailable.
- Plotly static PNG export used the fallback path because Kaleido was not installed.
- Market data depends on Yahoo Finance availability and may change if the vendor revises historical prices or corporate action adjustments.

## Phase 2

- No blocking issue found in Phase 2.
- `statsmodels` could not be used because the local SciPy/statsmodels stack is incompatible with the installed NumPy version.
- Single-index regression used the NumPy fallback, so beta and alpha were produced but regression p-values and residual volatility were not available.
- Plotly static PNG export continued to use the Pillow fallback because Kaleido is not installed.

## Still Open for Future Phases

- Multi-factor dataset or factor source not yet finalized.
- Optimization assumptions not yet finalized.
- Dashboard not planned for MVP.
