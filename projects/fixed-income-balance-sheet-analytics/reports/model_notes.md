# Model Notes

## Pricing Assumptions

- The bond book is synthetic.
- Bonds are fixed-rate bullet instruments.
- Principal is repaid at maturity.
- Coupon dates are generated backward from maturity based on coupon frequency.
- Cash flows are discounted with a flat market yield for each bond.
- Timing uses a simple Actual/365 year fraction.
- Accrued interest, settlement calendars, holidays, and business-day adjustments are not included.

## YTM Assumptions

Yield-to-maturity is calculated as the yield that equates the present value of scheduled cash flows to the modeled price.

The implementation uses a transparent root-solving approach with a fallback search. It is intended for learning and portfolio demonstration, not production bond analytics.

## Duration Assumptions

Macaulay duration is calculated as the present-value-weighted average time to receive cash flows.

Modified duration is calculated as:

```text
modified_duration = macaulay_duration / (1 + market_yield / coupon_frequency)
```

This is used as a first-order estimate of price sensitivity to yield changes.

## Convexity Assumptions

Convexity is calculated from discounted cash flows using a periodic-compounding approximation:

```text
sum(PV_cashflow * t * (t + 1 / coupon_frequency))
/ (price * (1 + yield / coupon_frequency)^2)
```

It helps explain why price-yield relationships are curved rather than perfectly linear.

## DV01 Assumptions

DV01 is calculated as:

```text
market_value * modified_duration * 0.0001
```

The report treats DV01 as a positive exposure amount. A one basis point rate increase would approximately reduce market value by this amount before convexity effects.

## Rate Shock Assumptions

The stress test applies parallel shifts to each bond's market yield:

- `-100 bps`
- `-50 bps`
- `0 bps`
- `+50 bps`
- `+100 bps`
- `+200 bps`

Each bond is repriced under the shocked yield. The model does not change curve shape, credit spreads, liquidity premiums, or issuer fundamentals.

## Synthetic Data Limitations

- The book is not calibrated to actual market holdings.
- Ratings, yields, sectors, and values are illustrative.
- There is no real yield curve.
- There are no callable bonds, amortizing bonds, floating-rate notes, or securitized instruments.
- There is no liability-side model.
- Results should be interpreted as fixed income mechanics, not market views.
