# LinkedIn Post Drafts

## Short Post

I finished a fixed income analytics portfolio project focused on bond pricing and interest-rate risk.

It uses a synthetic bond book to model coupon cash flows, price bonds, calculate YTM, duration, convexity, DV01, and run parallel rate shock scenarios.

This is not investment advice or a production treasury system. It is a practical portfolio project to show fixed income mechanics and risk analytics in Python.

## Medium Post

I completed a new portfolio project: **Fixed Income and Balance Sheet Analytics Platform**.

The project uses a synthetic bond book to work through:

- coupon and principal cash flow modeling
- discounted cash flow bond pricing
- yield-to-maturity calculation
- Macaulay and modified duration
- convexity
- DV01
- parallel interest-rate stress testing
- simple balance sheet / ALM interpretation

The current synthetic portfolio has a modeled market value of about `7.23 million`, modified duration of `3.31`, and portfolio DV01 of about `2,393`. A `+100 bps` parallel shock produces an estimated market value loss of about `3.23%`.

The project is intentionally honest about limitations: synthetic data, flat bond-level yields, no real yield curve, no credit spread modeling, and no liability-side ALM yet.

## Technical Post

I built a fixed income analytics project in Python around a synthetic bond portfolio.

The workflow:

1. Create a synthetic fixed-rate bond book.
2. Generate coupon and principal cash flows.
3. Price bonds using discounted cash flows.
4. Recover yield-to-maturity from model price.
5. Calculate Macaulay duration, modified duration, convexity, and DV01.
6. Reprice the portfolio under `-100 bps` to `+200 bps` parallel rate shocks.
7. Summarize stress losses by sector and rating.

The goal was to practice the core mechanics behind fixed income and balance sheet analytics, not to claim a production treasury platform. Future improvements would include yield curve calibration, key-rate duration, credit spread scenarios, and liability cash flows.
