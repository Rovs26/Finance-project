# Model Notes

## Pricing Assumptions

- Synthetic fixed-rate bond book.
- Bullet principal repayment at maturity.
- Coupon dates generated from maturity backwards based on coupon frequency.
- Actual/365 year fractions.
- Flat bond-level market yield.
- No accrued interest, settlement calendar, or holiday adjustment.

## Duration Method

Macaulay duration is calculated as the present-value-weighted average time to cash flow receipt.

Modified duration is calculated as:

```text
modified_duration = macaulay_duration / (1 + market_yield / coupon_frequency)
```

It estimates percentage price sensitivity to a small yield change.

## Convexity Method

Convexity is calculated from discounted cash flows using a periodic-compounding approximation:

```text
sum(PV_cashflow * t * (t + 1 / coupon_frequency))
/ (price * (1 + yield / coupon_frequency)^2)
```

Convexity is used to improve the duration-only estimate for larger rate moves.

## DV01 Method

DV01 is calculated as:

```text
price_or_market_value * modified_duration * 0.0001
```

The project reports DV01 as a positive exposure amount. A one basis point rate increase would approximately reduce market value by this amount before convexity adjustment.

## Stress Scenario Assumptions

Scenarios are parallel shocks to each bond's market yield:

- `-100 bps`
- `-50 bps`
- `0 bps`
- `+50 bps`
- `+100 bps`
- `+200 bps`

Each bond is repriced under the shocked yield. No curve shape changes, spread shocks, liquidity effects, or credit migration effects are included.

## Simplified ALM Assumptions

The ALM output is an asset-side interpretation of market value sensitivity. It does not model liabilities, deposit repricing, insurance liabilities, hedges, or behavioral assumptions.

## Limitations

- Synthetic data only.
- Simplified day count and compounding.
- No real yield curve calibration.
- Parallel shocks only.
- No liquidity or credit spread modeling.
- No optionality, callable bonds, amortization, or floating-rate instruments.
