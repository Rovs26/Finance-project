# Known Issues

## Phase 0

- No blocking issue found in Phase 0.
- The bond book is synthetic and should not be described as real bank, insurer, or market portfolio data.
- Day-count treatment is simplified with Actual/365 year fractions.
- Pricing uses a flat market yield per bond, not a real yield curve.
- Accrued interest, settlement calendars, holidays, and business-day conventions are not modeled yet.

## Phase 1

- No blocking issue found in Phase 1.
- Duration and convexity use simplified discounted cash flow formulas.
- Rate stress testing uses parallel shocks only.
- There is no real yield curve calibration.
- There is no liquidity spread, credit spread, migration, or default modeling.
- There is no callable bond, prepayment, amortization, or floating-rate instrument modeling.
- ALM interpretation is asset-side only and does not include liabilities, hedges, or deposit behavior.
