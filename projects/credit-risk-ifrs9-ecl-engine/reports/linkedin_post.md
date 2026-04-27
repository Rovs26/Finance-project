# LinkedIn Post Drafts

## Short Post

I built a credit risk and IFRS 9-style expected credit loss portfolio project using Python.

The project covers data understanding, baseline PD modeling, simplified ECL calculation, scenario analysis, and business-ready reporting. It is a portfolio project, not a production bank system, but it helped me connect financial economics, risk analytics, machine learning, and business communication in one workflow.

## Medium Post

I recently built a portfolio project: Credit Risk and IFRS 9 Expected Credit Loss Engine.

The goal was to create a practical finance and risk analytics workflow using Python. The project starts with LendingClub-style loan data, builds a baseline probability of default model, calculates simplified expected credit loss using PD, LGD, and EAD assumptions, and produces business-ready summaries for dashboard development.

This is not a production bank model or official IFRS 9 system. I kept the assumptions transparent and documented the limitations clearly. The main value of the project is showing how finance, analytics, machine learning, and communication can fit together in a reproducible workflow.

## Technical Post

I built a Python portfolio project focused on credit risk analytics and simplified IFRS 9-style expected credit loss.

Workflow:
- Data understanding and schema review on LendingClub-style loan data
- Target mapping from loan status to default flag
- Baseline logistic regression PD model using scikit-learn
- PD score bands and model documentation
- Simplified ECL calculation using `PD x LGD x EAD`
- IFRS 9-style staging proxy for portfolio analytics
- Base, mild stress, and severe stress scenario summaries
- Dashboard-ready CSV tables and a Streamlit dashboard for portfolio review

Important caveat: this is a portfolio project, not a production bank system. It does not include regulatory validation, macroeconomic overlays, lifetime PD curves, discounting, or official IFRS 9 compliance logic.
