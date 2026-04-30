# Research Memo

## Executive Summary

This project builds a synthetic fixed income portfolio and walks through the core analytics used to understand bond value and interest-rate sensitivity. It covers cash flow modeling, discounted cash flow pricing, yield-to-maturity, duration, convexity, DV01, and parallel rate stress testing.

The latest outputs show a modeled portfolio market value of about `7.23 million`, weighted modified duration of `3.31`, and portfolio DV01 of about `2,393`. A `+100 bps` parallel rate shock produces an estimated market value loss of about `233,124`, or `3.23%`.

## Portfolio Setup

The bond book contains 10 synthetic fixed-rate bullet bonds across government, financials, utilities, property, consumer, telecom, infrastructure, and government-linked sectors. Ratings include `AA`, `A`, and `BBB`.

The book is synthetic and should not be read as a real portfolio, market recommendation, or confidential balance sheet.

## Pricing Results

Bonds are priced by discounting scheduled coupon and principal cash flows using a flat bond-level market yield. The project also calculates yield-to-maturity from the modeled price.

Portfolio summary:

- Total face value: `7.50 million`
- Total book value: `7.30 million`
- Total market value: `7.23 million`
- Market-to-book ratio: `0.991`
- Weighted average coupon: `5.37%`
- Weighted average yield: `5.96%`

## Duration and Convexity Findings

- Portfolio Macaulay duration: `3.40`
- Portfolio modified duration: `3.31`
- Portfolio convexity: `17.37`
- Portfolio DV01: `2,392.63`
- Largest single-bond DV01: `413.94`

The longest-duration exposures are mainly longer-maturity BBB bonds. This is intuitive: bonds with later cash flows have more sensitivity to discount-rate changes.

## Stress Testing Findings

Parallel shock results:

- `-100 bps`: market value gain of about `245,685`
- `-50 bps`: market value gain of about `121,219`
- `+50 bps`: market value loss of about `118,080`
- `+100 bps`: market value loss of about `233,124`
- `+200 bps`: market value loss of about `454,506`

For the `+100 bps` stress, Financials has the largest sector loss. By rating, BBB bonds show the largest modeled loss because the synthetic book includes several longer-duration BBB positions.

## ALM Interpretation

The asset portfolio has positive duration exposure. If rates rise, modeled bond market value falls; if rates decline, modeled market value rises.

For a bank, insurer, or treasury team, this type of output is a starting point for balance sheet sensitivity. It is not a full ALM model because it does not include liabilities, repricing gaps, insurance reserves, hedges, or behavioral assumptions.

## Business Relevance

This project demonstrates the mechanics behind fixed income risk conversations:

- How coupon cash flows translate into bond value
- Why yield changes affect longer-duration bonds more
- How DV01 helps summarize rate sensitivity
- How scenario analysis can frame potential balance sheet gains or losses
- Why limitations matter before using outputs for decisions

## Limitations

- Synthetic data only.
- Flat bond-level yields instead of a calibrated yield curve.
- Simplified Actual/365 timing.
- No accrued interest or settlement calendar.
- Parallel rate shocks only.
- No credit spread, liquidity, default, prepayment, or optionality modeling.
- No liability-side ALM model.

## Next Improvements

- Add real yield curve construction.
- Add key-rate duration.
- Add spread shock scenarios.
- Add liability cash flows for ALM gap analysis.
- Add callable or amortizing bond examples.
- Add a dashboard only after the analytics and documentation are stable.
