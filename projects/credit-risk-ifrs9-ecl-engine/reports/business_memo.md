# Business Memo: Simplified IFRS 9-style ECL Engine

## Executive Summary

Phase 3 converts the Phase 2 PD predictions into a simplified IFRS 9-style Expected Credit Loss estimate. The base portfolio exposure is 750,967,975.00 and the base ECL estimate is 146,297,248.66, implying a simplified ECL rate of 19.48%.

This result should be interpreted as a portfolio analytics prototype, not as a regulatory IFRS 9 model.

## Methodology

The engine calculates row-level ECL using:

`ECL = PD x LGD x EAD`

The workflow assigns exposure at default, loss given default, simplified IFRS 9-style stage, base ECL, grouped ECL summaries, and stress scenario results.

## PD Model Input

The ECL engine uses `outputs/predictions/pd_predictions.csv` from Phase 2. The PD model is a baseline logistic regression model trained on the 50,000-row Phase 1 modeling sample.

## EAD Assumption

EAD uses `loan_amnt` because it is available in the PD prediction file. This is a transparent exposure proxy for portfolio analytics and does not represent contractual EAD modeling.

## LGD Assumption

LGD uses a simplified home-ownership adjustment:

- MORTGAGE: 35%
- OWN: 40%
- RENT: 50%
- Other or missing: 45%

This is a simplified portfolio assumption, not a regulatory recovery model.

## Staging Assumption

The IFRS 9-style stage proxy uses:

- Stage 1: `pd_score < 0.20`
- Stage 2: `0.20 <= pd_score < 0.50`
- Stage 3: `pd_score >= 0.50` or `default_flag == 1`

This staging is for portfolio analytics only and is not official IFRS 9 compliance logic.

## Base ECL Result

- Total exposure: 750,967,975.00
- Total ECL: 146,297,248.66
- ECL rate: 19.48%

## Risk Concentration Findings

Stage 3 has the largest ECL concentration:

- Stage 1 ECL: 3,819,344.09
- Stage 2 ECL: 42,157,373.11
- Stage 3 ECL: 100,320,531.46

Stage 3 contributes the majority of total ECL because it includes all records with `pd_score >= 0.50` and all observed default rows.

## Scenario Analysis

| Scenario | PD Multiplier | LGD Multiplier | Total ECL | ECL Rate |
| --- | ---: | ---: | ---: | ---: |
| Base | 1.00 | 1.00 | 146,297,248.66 | 19.48% |
| Mild stress | 1.25 | 1.10 | 200,746,300.69 | 26.73% |
| Severe stress | 1.50 | 1.20 | 255,838,508.12 | 34.07% |

Stress scenarios cap PD and LGD at 100%.

## Business Recommendations

- Use the Phase 3 output as a prototype risk analytics layer for business interpretation and dashboard development.
- Review Stage 3 concentration and high-PD score bands before designing dashboard views.
- Improve LGD and EAD assumptions before presenting the project as a serious IFRS 9 modeling workflow.
- Add documentation that clearly separates portfolio analytics assumptions from regulatory IFRS 9 compliance.

## Limitations

- EAD is proxied by loan amount.
- LGD is based on a simple home-ownership rule.
- Staging uses PD thresholds and default flag only.
- No lifetime PD curve, macroeconomic overlay, discounting, cure assumption, or regulatory validation is included.
- The PD model is a baseline model with known precision limitations.

## Next Improvements

- Build the Phase 4 business interpretation notebook.
- Add dashboard-ready summary tables.
- Improve EAD and LGD assumptions.
- Consider calibrated PD and time-aware validation before deeper IFRS 9 extensions.
