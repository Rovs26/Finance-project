# Known Issues

## Final Status

- No blocking final issue found in Phase 2.

## Data Limitations

- The bond book is synthetic.
- Ratings, yields, sectors, book values, and issuer types are illustrative.
- The project should not be described as using real bank, insurer, or client portfolio data.

## Modeling Limitations

- Day-count treatment is simplified with Actual/365 year fractions.
- Pricing uses flat bond-level yields, not a real calibrated yield curve.
- Accrued interest, settlement calendars, holidays, and business-day conventions are not modeled.
- Duration and convexity use simplified discounted cash flow formulas.
- Stress testing uses parallel rate shocks only.
- There is no key-rate duration.
- There is no credit spread, liquidity spread, credit migration, or default modeling.
- There is no callable bond, prepayment, amortization, or floating-rate instrument modeling.
- ALM interpretation is asset-side only and does not include liabilities, hedges, or deposit behavior.

## Optional Future Work

- Real market yield curve construction.
- Key-rate duration.
- Credit spread scenarios.
- Liability cash flow modeling.
- Dashboard or reporting app.
