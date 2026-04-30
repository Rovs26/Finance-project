# Interview Talking Points

Portfolio project: Philippines Macro Nowcasting and Policy Dashboard
Prepared answers for likely interview questions about this project.

---

**Q1: Walk me through this project from start to finish.**

A: The project is a full-stack macro analytics workflow for the Philippines. I started by collecting public data from BSP Excel files and the World Bank API — monthly inflation from 1958 to March 2026 and USD/PHP exchange rate data. Phase 2 cleaned those series and built a feature table with inflation lags, rolling averages, and change features. Phase 3 compared three baseline forecasting models — a naive last-value benchmark, a 3-month moving average, and a simple linear regression — on a chronological 80/20 holdout. Linear regression won on RMSE. Phase 4 interpreted those results in the context of the BSP's 3.0% inflation target band, produced scenario analysis for banks, fintechs, and corporates, and generated dashboard-ready outputs. Phase 5 built a five-page Streamlit dashboard. Phase 6 packaged everything into portfolio-ready reports.

---

**Q2: Why did you choose inflation as the forecasting target?**

A: Inflation is central to Philippines macroeconomic policy. The BSP uses an explicit inflation targeting framework, so understanding the trajectory of CPI relative to the target band is the most direct lens for policy interpretation. It is also the variable where BSP historical monthly data goes back to 1958, giving a long time series for feature engineering and model evaluation. It connects directly to the business implications I wanted to illustrate — NIM for banks, funding costs for fintechs, and working capital planning for corporates.

---

**Q3: How did you evaluate your forecasting models?**

A: I used a chronological 80/20 train/test split — the last 20% of usable observations formed the holdout set. I evaluated four metrics: MAE, RMSE, MAPE, and directional accuracy. Linear regression had the lowest RMSE (0.4889pp) and MAE (0.3785pp). An important caveat: the naive model had lower MAPE than linear regression, which reflects MAPE's sensitivity to small denominators near zero inflation — it can penalise a better model when absolute inflation is low. The 80/20 single holdout is also a limitation; I documented that rolling-origin validation is the right next improvement.

---

**Q4: What are the main limitations of your model?**

A: Several. First, it is a simple linear regression with only lagged inflation and USD/PHP features — no policy rate, rice prices, oil prices, core inflation, or survey expectations. Second, the 80/20 split does not simulate live forecasting; rolling-origin validation would give a more realistic view of out-of-sample performance. Third, the test MAPE of 19.1% is non-trivial — the model is useful as a directional indicator but not precise enough for high-stakes decisions. Fourth, a NumPy/sklearn compatibility issue in the local environment required a NumPy least-squares fallback, though the results are mathematically equivalent.

---

**Q5: Both March 2026 inflation and your April forecast are above the BSP band. What does that mean?**

A: The BSP 2025-2028 target is 3.0% plus or minus 1.0 percentage point, so the band is 2.0% to 4.0%. March 2026 headline inflation came in at 4.1%, which is a marginal breach of 0.1pp. The model forecasts April 2026 at 5.02%, roughly 1pp above the upper bound. A single month above band does not automatically trigger policy action — the BSP evaluates core inflation, output gap, global conditions, and expectations. But two consecutive above-band readings with an accelerating trajectory would typically warrant a more hawkish monitoring posture. I was careful to frame this as a portfolio research interpretation, not a BSP forecast.

---

**Q6: How would you improve this project if you had more time?**

A: The highest-priority improvement is rolling-origin validation — re-running the model at each point in the test set using only data available at that time, rather than fitting once on the training set. Second, integrating BSP policy rate data, which is referenced in the source inventory but not yet parsed. Third, rice prices — rice is a key CPI driver in the Philippines and its exclusion is a meaningful gap. Fourth, exploring regularised models like Ridge regression or simple ensembles to reduce overfitting on a short feature set.

---

**Q7: Why did you build a Streamlit dashboard?**

A: The dashboard makes the analysis accessible to a non-technical audience and demonstrates the full analytics-to-delivery pipeline. The design deliberately separates concerns: the notebooks do all the computation and save pre-computed outputs, and the dashboard reads those outputs without re-running any models. This matches how production analytics systems typically work — the app layer consumes pre-built artifacts rather than running models on every page load. It also demonstrates I can communicate technical findings through a clean interface, which is relevant for roles that involve presenting to business stakeholders.

---

**Q8: How is this relevant to a role at BSP or PIDS?**

A: The project demonstrates a practical understanding of the BSP inflation targeting framework, the role of PSA as the official CPI data source, and how to connect model outputs to policy interpretation. The research memo is structured like an institutional policy note — data sourcing, methodology, results, limitations, and recommendations. For a research analyst role, the ability to build a reproducible pipeline, document decisions, and present findings with appropriate caveats is directly applicable.

---

**Q9: How is this relevant to a banking or fintech role?**

A: The policy interpretation section connects macro forecast outputs directly to banking and fintech business implications. NIM sensitivity to the BSP rate path, loan repricing dynamics for fintechs, and working-capital stress scenarios for corporates are all covered in the scenario analysis. The dashboard is designed to be used by business stakeholders, not just economists. For a banking analytics role, the ability to translate macro signals into business-relevant scenarios is the core skill this project demonstrates.

---

**Q10: What technical skills does this project demonstrate?**

A: Python data engineering (pandas, pathlib, data cleaning from Excel), time-series feature engineering (lags, rolling averages, changes), baseline ML evaluation (train/test splits, RMSE, MAE, MAPE, directional accuracy), Plotly and Streamlit for interactive analytics delivery, Jupyter notebooks for reproducible research, and markdown-based documentation. The project also demonstrates awareness of production constraints — using pre-computed outputs, graceful file-not-found warnings, modular source code in `src/`, and clear separation between computation (notebooks) and presentation (dashboard).
