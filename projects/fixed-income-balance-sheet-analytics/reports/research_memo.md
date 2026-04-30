# Research Memo

## Executive Summary

This project uses a synthetic fixed income portfolio to demonstrate bond pricing, cash flow modeling, duration, convexity, DV01, and simple interest-rate stress testing. The latest Phase 1 outputs show a modeled portfolio market value of `7.23 million`, weighted modified duration of `3.31`, and portfolio DV01 of about `2,393`.

Under a `+100 bps` parallel rate shock, the synthetic portfolio loses about `233,124`, or `3.23%` of market value. Under a `+200 bps` shock, the modeled loss is about `454,506`, or `6.29%`.

## Portfolio Description

The bond book contains 10 synthetic fixed-rate bullet bonds across government, financials, utilities, property, consumer, telecom, infrastructure, and government-linked sectors. Ratings include `AA`, `A`, and `BBB`.

The portfolio is synthetic and should not be interpreted as real market, bank, insurer, or client holdings.

## Pricing Method Summary

Phase 0 prices each bond by discounting scheduled coupon and principal cash flows using a flat bond-level market yield. Yield-to-maturity is recovered from the model price using a transparent root-solving approach.

## Duration and Convexity Findings

- Portfolio Macaulay duration: `3.40`
- Portfolio modified duration: `3.31`
- Portfolio convexity: `17.37`
- Portfolio DV01: `2,392.63`
- Largest single-bond DV01: `413.94`

The longest-duration exposures are concentrated in longer-maturity BBB bonds such as telecom and infrastructure names. These bonds contribute more to rate sensitivity because their cash flows are further in the future.

## Stress Test Findings

Parallel rate shock results:

- `-100 bps`: market value gain of about `245,685`
- `-50 bps`: market value gain of about `121,219`
- `+50 bps`: market value loss of about `118,080`
- `+100 bps`: market value loss of about `233,124`
- `+200 bps`: market value loss of about `454,506`

For a `+100 bps` shock, the largest sector loss comes from financials, followed by telecom and government exposure. By rating, BBB bonds produce the largest modeled stress loss because they include several longer-duration positions.

## ALM Interpretation

For a simple balance sheet view, the bond portfolio has positive interest-rate duration. Rising rates reduce asset market value, while falling rates increase it. The current outputs do not include liabilities, deposit behavior, insurance reserves, or repricing gaps, so this is an asset-side sensitivity view rather than a full ALM model.

## Limitations

- Synthetic data only.
- Flat bond-level yields instead of a calibrated yield curve.
- Parallel rate shocks only.
- No credit spread, liquidity, prepayment, optionality, or default modeling.
- No liability-side modeling.
- No regulatory capital, IFRS, or accounting classification treatment.

## Next Improvements

- Add key-rate duration.
- Add credit spread scenarios.
- Add simple liability cash flows for ALM gap analysis.
- Add reporting tables for treasury and risk review.
- Polish the project for final GitHub presentation in Phase 2.
