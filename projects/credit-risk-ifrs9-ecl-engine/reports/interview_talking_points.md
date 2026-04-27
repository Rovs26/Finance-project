# Interview Talking Points

## 1. What problem does this project solve?

It shows how loan-level data can be converted into a credit risk analytics workflow: PD scoring, simplified ECL estimation, stress scenarios, and business reporting.

## 2. Why did you use logistic regression?

I used logistic regression as an interpretable baseline. It is easier to explain in risk and banking interviews than a black-box model, and it gives coefficients that can be reviewed.

## 3. What was the target variable?

The target was `default_flag`, mapped from LendingClub-style loan statuses. Charged off, default, and serious delinquency statuses were mapped to default.

## 4. How did you calculate ECL?

The simplified formula was `ECL = PD x LGD x EAD`. PD came from the Phase 2 model, EAD used loan amount, and LGD used a simple home-ownership rule.

## 5. Is this official IFRS 9?

No. It is IFRS 9-style portfolio analytics. It does not include lifetime PD curves, discounting, macroeconomic overlays, or regulatory validation.

## 6. What were the key results?

The portfolio sample had total exposure of 750,967,975.00 and base ECL of 146,297,248.66. Stage 3 accounted for the largest ECL concentration.

## 7. What did scenario analysis show?

Base ECL was 146,297,248.66. Mild stress increased ECL to 200,746,300.69, and severe stress increased it to 255,838,508.12.

## 8. What are the main limitations?

The model is a baseline, the data is public LendingClub-style data, EAD and LGD are simplified, and staging is based on PD thresholds rather than full IFRS 9 rules.

## 9. How is this relevant to early-career roles?

It connects finance theory, Python, machine learning, risk analytics, documentation, and business communication, which are useful across banking, fintech, advisory, and research roles.

## 10. What would you improve next?

I would add dashboard screenshots, improve PD calibration, add time-aware validation, refine LGD and EAD assumptions, and add stronger monitoring and data quality checks.
