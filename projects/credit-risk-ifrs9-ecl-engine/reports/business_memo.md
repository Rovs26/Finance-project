# Business Memo: Credit Risk and IFRS 9-style ECL Portfolio Engine

## Executive Summary

This project converts LendingClub-style loan data into a credit risk analytics workflow: data understanding, baseline PD modeling, simplified ECL calculation, scenario analysis, and dashboard-ready summaries. On the 50,000-row portfolio sample, base exposure is 750,967,975.00 and base ECL is 146,297,248.66, or a 19.48% ECL rate.

The work is a portfolio analytics prototype, not a production bank model or official IFRS 9 compliance system.

## Project Purpose

The project demonstrates how Python, data analytics, machine learning, and financial risk concepts can be combined into a practical credit risk workflow for banking, fintech, risk advisory, insurance, and research roles.

## Methodology

- Built a Phase 1 modeling sample from manually supplied LendingClub-style data.
- Trained a baseline logistic regression PD model in Phase 2.
- Calculated ECL in Phase 3 as `PD x LGD x EAD`.
- Prepared Phase 4A business interpretation and dashboard-ready summary tables.

## Key Findings

- Total loans analyzed: 50,000
- Total exposure: 750,967,975.00
- Total ECL: 146,297,248.66
- ECL rate: 19.48%
- Stage 3 has the largest ECL concentration at 100,320,531.46.
- The largest grade-level ECL concentration is Grade C.
- The largest purpose-level ECL concentration is debt consolidation.

## Business Interpretation

The portfolio risk is concentrated in higher PD accounts and Stage 3 accounts. This is expected because Stage 3 includes records with `pd_score >= 0.50` or observed default flags. For business users, the strongest dashboard views should focus on Stage 3, high score bands, grade concentration, purpose concentration, and stress scenario sensitivity.

## Scenario Analysis

| Scenario | Total ECL | ECL Rate |
| --- | ---: | ---: |
| Base | 146,297,248.66 | 19.48% |
| Mild stress | 200,746,300.69 | 26.73% |
| Severe stress | 255,838,508.12 | 34.07% |

The stress scenarios apply transparent PD and LGD multipliers and cap stressed PD and LGD at 100%.

## Recommendations

- Use Stage 3 and high score bands as primary dashboard filters.
- Show grade and purpose concentration to make portfolio risk easier to explain.
- Keep scenario comparison visible for business users.
- Clearly label EAD, LGD, and staging assumptions as simplified.
- Improve calibration, validation, LGD, and EAD assumptions before positioning this as more than a portfolio prototype.

## Limitations

- The dataset is public LendingClub-style data, not confidential bank data.
- The PD model is a baseline logistic regression benchmark.
- EAD uses loan amount as a proxy.
- LGD uses a simplified home-ownership rule.
- IFRS 9-style staging uses PD thresholds and default flag only.
- No lifetime PD curve, macroeconomic overlay, discounting, cure logic, or regulatory validation is included.

## Next Steps

Add dashboard screenshots or a short demo GIF, then refine the final GitHub presentation for internship and early-career applications.
