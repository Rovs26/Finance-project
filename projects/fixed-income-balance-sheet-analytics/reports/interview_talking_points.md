# Interview Talking Points

## 1. What does this project do?

It prices a synthetic fixed-rate bond portfolio, generates cash flows, calculates YTM, measures duration, convexity, and DV01, then runs simple parallel interest-rate stress scenarios.

## 2. Why did you use synthetic data?

Fixed income portfolio holdings can be confidential. Synthetic data lets me show the mechanics clearly without pretending I have access to real bank, insurer, or client positions.

## 3. How are the bonds priced?

Each bond is priced by discounting its future coupon and principal cash flows using a flat bond-level market yield. It is a transparent discounted cash flow model.

## 4. What is yield-to-maturity?

YTM is the yield that makes the present value of the bond's scheduled cash flows equal to its price. In the project, I solve for YTM from the modeled price.

## 5. What is duration?

Macaulay duration is the present-value-weighted average time to receive cash flows. Modified duration translates that into approximate price sensitivity to a change in yield.

## 6. What is convexity?

Convexity captures the curvature in the price-yield relationship. It improves the rate sensitivity estimate when yield changes are larger.

## 7. What is DV01?

DV01 estimates the market value change for a one basis point yield move. In this project, portfolio DV01 is about `2,393`.

## 8. What did the stress test show?

A `+100 bps` parallel rate shock reduced modeled market value by about `233,124`, or `3.23%`. A `+200 bps` shock reduced value by about `454,506`, or `6.29%`.

## 9. What are the main limitations?

The project uses synthetic bonds, flat yields, simple day count, and parallel shocks only. It does not include credit spreads, liquidity, callable bonds, prepayment, default, or liability-side ALM.

## 10. How would you improve it?

I would add real yield curve construction, key-rate duration, spread shocks, liability cash flows, and a small dashboard after the analytics layer is stable.
