"""
Philippines Macro Nowcasting and Policy Dashboard
Phase 5 — Streamlit Dashboard

Portfolio research project. Not an official BSP forecast.
Run from project root:  streamlit run dashboard/app.py
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Philippines Macro Nowcasting Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .kpi-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
    }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.25rem;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.2;
    }
    .kpi-sub { font-size: 0.8rem; color: #94a3b8; margin-top: 0.15rem; }
    .callout-info {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 4px;
        padding: 0.9rem 1.1rem;
        margin: 0.75rem 0;
        font-size: 0.9rem;
        color: #1e3a5f;
    }
    .callout-warn {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 4px;
        padding: 0.9rem 1.1rem;
        margin: 0.75rem 0;
        font-size: 0.9rem;
        color: #78350f;
    }
    .callout-disclaimer {
        background: #fafafa;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 0.9rem 1.1rem;
        margin: 0.75rem 0;
        font-size: 0.82rem;
        color: #64748b;
    }
    .section-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1e293b;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Path resolution — supports running from project root OR dashboard/ dir
# ---------------------------------------------------------------------------
_THIS_FILE = Path(__file__).resolve()
_PROJECT_ROOT = _THIS_FILE.parent
for _ in range(5):
    if (_PROJECT_ROOT / "src").is_dir():
        break
    _PROJECT_ROOT = _PROJECT_ROOT.parent

DATA_DIR      = _PROJECT_ROOT / "data" / "processed"
FORECASTS_DIR = _PROJECT_ROOT / "outputs" / "forecasts"
SCENARIOS_DIR = _PROJECT_ROOT / "outputs" / "scenarios"

# ---------------------------------------------------------------------------
# BSP constants
# ---------------------------------------------------------------------------
BSP_LOWER    = 2.0
BSP_UPPER    = 4.0
BSP_MIDPOINT = 3.0

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
@st.cache_data
def _load_csv(path: Path, label: str):
    if not path.exists():
        st.warning(f"Expected file not found: `{path.name}` ({label})")
        return None
    return pd.read_csv(path)


@st.cache_data
def load_monthly():
    df = _load_csv(DATA_DIR / "monthly_macro_indicators.csv", "monthly macro indicators")
    if df is not None:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
    return df


@st.cache_data
def load_latest_forecast():
    df = _load_csv(FORECASTS_DIR / "latest_inflation_forecast.csv", "latest inflation forecast")
    if df is not None:
        df["forecast_origin_date"] = pd.to_datetime(df["forecast_origin_date"])
        df["forecast_target_date"] = pd.to_datetime(df["forecast_target_date"])
    return df


@st.cache_data
def load_metrics():
    return _load_csv(FORECASTS_DIR / "forecast_metrics.csv", "forecast metrics")


@st.cache_data
def load_test_predictions():
    df = _load_csv(
        FORECASTS_DIR / "inflation_forecast_test_predictions.csv",
        "test predictions",
    )
    if df is not None:
        df["target_date"] = pd.to_datetime(df["target_date"])
    return df


@st.cache_data
def load_band_summary():
    return _load_csv(
        SCENARIOS_DIR / "inflation_target_band_summary.csv",
        "inflation target band summary",
    )


@st.cache_data
def load_policy_summary():
    return _load_csv(
        SCENARIOS_DIR / "policy_interpretation_summary.csv",
        "policy interpretation summary",
    )


@st.cache_data
def load_dashboard_notes():
    path = SCENARIOS_DIR / "dashboard_policy_notes.md"
    if not path.exists():
        st.warning(f"Expected file not found: `{path.name}`")
        return {}
    text = path.read_text(encoding="utf-8")
    sections = {}
    current_key = None
    buf = []
    skip_prefixes = ("## Generated", "## Source", "## Disclaimer")
    for line in text.splitlines():
        if line.startswith("## ") and not any(line.startswith(p) for p in skip_prefixes):
            if current_key:
                sections[current_key] = "\n".join(buf).strip()
            current_key = line[3:].strip()
            buf = []
        elif line.strip() == "---":
            continue
        elif current_key:
            buf.append(line)
    if current_key:
        sections[current_key] = "\n".join(buf).strip()
    return sections


# ---------------------------------------------------------------------------
# Load data once
# ---------------------------------------------------------------------------
monthly      = load_monthly()
latest_fc    = load_latest_forecast()
metrics      = load_metrics()
test_preds   = load_test_predictions()
band_summary = load_band_summary()
policy_df    = load_policy_summary()
notes        = load_dashboard_notes()

# Scalar KPIs
_obs_inf    = float(latest_fc.iloc[0]["latest_observed_inflation_rate"]) if latest_fc is not None else None
_fcast_inf  = float(latest_fc.iloc[0]["forecast_inflation_rate"])        if latest_fc is not None else None
_fcast_date = latest_fc.iloc[0]["forecast_target_date"].strftime("%b %Y")  if latest_fc is not None else "N/A"
_obs_date   = latest_fc.iloc[0]["forecast_origin_date"].strftime("%b %Y")  if latest_fc is not None else "N/A"
_best_rmse  = float(metrics.loc[metrics["model"] == "linear_regression", "rmse"].values[0]) if metrics is not None else None
_best_mae   = float(metrics.loc[metrics["model"] == "linear_regression", "mae"].values[0])  if metrics is not None else None

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
PAGES = [
    "Overview",
    "Inflation and Target Band",
    "Forecast Performance",
    "Policy Interpretation",
    "Data and Limitations",
]
st.sidebar.title("Navigation")
page = st.sidebar.radio("", PAGES, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size:0.78rem; color:#64748b; line-height:1.6;">
    <strong>Philippines Macro Nowcasting</strong><br>
    Portfolio research project.<br>
    Not an official BSP forecast.<br><br>
    Data: BSP, PSA, World Bank<br>
    Model: Linear regression baseline<br>
    </div>
    """,
    unsafe_allow_html=True,
)


def _kpi(col, label, value, sub=""):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE: OVERVIEW
# ============================================================
if page == "Overview":
    st.title("Philippines Macro Nowcasting and Policy Dashboard")
    st.markdown(
        '<div class="callout-disclaimer">'
        "<strong>Disclaimer:</strong> This is a portfolio research project and is not affiliated "
        "with, endorsed by, or representative of the Bangko Sentral ng Pilipinas (BSP), the "
        "Philippine Statistics Authority (PSA), or any official institution. Nothing here "
        "constitutes an official economic forecast, investment advice, or policy recommendation."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-header">Key Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    _kpi(c1, "Latest Observed Inflation",
         f"{_obs_inf:.1f}%" if _obs_inf is not None else "N/A", f"{_obs_date}")
    _kpi(c2, "Model Forecast Inflation",
         f"{_fcast_inf:.2f}%" if _fcast_inf is not None else "N/A", f"{_fcast_date}")
    _kpi(c3, "BSP Target Midpoint", f"{BSP_MIDPOINT:.1f}%", "2025-2028")
    _kpi(c4, "BSP Target Band", f"{BSP_LOWER:.1f}%-{BSP_UPPER:.1f}%", "tolerance +/-1.0pp")
    _kpi(c5, "Best Model", "Linear Regression", "vs naive and MA-3m")
    _kpi(c6, "Model RMSE (test)",
         f"{_best_rmse:.4f}pp" if _best_rmse is not None else "N/A",
         f"MAE {_best_mae:.4f}pp" if _best_mae is not None else "")

    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(
        """
        This dashboard presents a portfolio research workflow for Philippines macroeconomic
        nowcasting and policy analytics. It covers data collection from BSP and World Bank
        sources, cleaning and feature engineering, baseline inflation forecasting, and
        policy interpretation.

        **Key findings:**
        - Philippines headline inflation reached **4.1%** in March 2026, marginally above the
          BSP 2025-2028 target band upper bound of 4.0%.
        - A simple linear regression model forecasts April 2026 inflation at approximately
          **5.02%**, roughly 1.0 percentage point above the band upper bound.
        - The baseline model outperforms both naive and 3-month moving-average benchmarks
          on RMSE (0.4889 vs 0.5002 and 0.7570).
        - Both the March observation and the April forecast are classified as **above-band**,
          suggesting the BSP is likely in a monitoring posture.

        **Coverage:** Monthly Philippines inflation from 1958 to March 2026 (~819 observations),
        USD/PHP exchange rate, and engineered lag, rolling, and change features.

        **Scope:** Baseline forecasting only. No policy-rate inputs, no commodity price data,
        no advanced nowcasting.
        """
    )

    st.markdown('<div class="section-header">Band Position at a Glance</div>', unsafe_allow_html=True)
    if band_summary is not None:
        row = band_summary.iloc[0]
        for label, value, position, date_str in [
            ("Observed", f"{_obs_inf:.1f}%",   row["observed_position_vs_target"],  _obs_date),
            ("Forecast", f"{_fcast_inf:.2f}%", row["forecast_position_vs_target"], _fcast_date),
        ]:
            color = "#dc2626" if position == "above_band" else "#16a34a" if position == "within_band" else "#2563eb"
            label_text = position.replace("_", " ").title()
            st.markdown(
                f'<div class="kpi-card" style="border-left-color:{color};">'
                f'<div class="kpi-label">{label} ({date_str})</div>'
                f'<div class="kpi-value">{value}</div>'
                f'<div class="kpi-sub" style="color:{color}; font-weight:600;">'
                f'{label_text}</div></div>',
                unsafe_allow_html=True,
            )


# ============================================================
# PAGE: INFLATION AND TARGET BAND
# ============================================================
elif page == "Inflation and Target Band":
    st.title("Inflation and BSP Target Band")
    st.markdown(
        '<div class="callout-info">'
        "The BSP 2025-2028 inflation target is <strong>3.0% +/-1.0pp</strong> "
        "(effective band: 2.0%-4.0%). The PSA is the official source for CPI and "
        "headline inflation data in the Philippines."
        "</div>",
        unsafe_allow_html=True,
    )

    if monthly is not None:
        valid = monthly[monthly["inflation_rate"].notna()].copy()
        recent_cutoff = pd.Timestamp("2016-01-01")
        recent = valid[valid["date"] >= recent_cutoff].copy()

        obs_inf    = _obs_inf
        obs_date   = latest_fc.iloc[0]["forecast_origin_date"] if latest_fc is not None else None
        fcast_inf  = _fcast_inf
        fcast_date = latest_fc.iloc[0]["forecast_target_date"] if latest_fc is not None else None

        # Full history chart
        fig = go.Figure()
        fig.add_hrect(
            y0=BSP_LOWER, y1=BSP_UPPER,
            fillcolor="#16a34a", opacity=0.08, line_width=0,
            annotation_text="BSP target band (2025-2028)",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#166534"),
        )
        fig.add_hline(
            y=BSP_MIDPOINT, line_dash="dash", line_color="#16a34a", line_width=1.2,
            annotation_text="3.0% midpoint", annotation_position="right",
            annotation_font=dict(size=9, color="#166534"),
        )
        fig.add_trace(go.Scatter(
            x=valid["date"], y=valid["inflation_rate"],
            mode="lines", name="Historical (pre-2016)",
            line=dict(color="#cbd5e1", width=0.8),
        ))
        fig.add_trace(go.Scatter(
            x=recent["date"], y=recent["inflation_rate"],
            mode="lines", name="2016-2026",
            line=dict(color="#1e3a5f", width=2),
        ))
        if obs_date is not None:
            fig.add_trace(go.Scatter(
                x=[obs_date], y=[obs_inf],
                mode="markers+text",
                marker=dict(color="#dc2626", size=10),
                text=[f"{_obs_date}: {obs_inf:.1f}%"],
                textposition="top center",
                name="Latest observed",
                textfont=dict(size=10, color="#dc2626"),
            ))
        if fcast_date is not None:
            fig.add_trace(go.Scatter(
                x=[fcast_date], y=[fcast_inf],
                mode="markers+text",
                marker=dict(color="#dc2626", size=10, symbol="diamond"),
                text=[f"{_fcast_date} forecast: {fcast_inf:.2f}%"],
                textposition="top center",
                name="Latest forecast",
                textfont=dict(size=10, color="#dc2626"),
            ))
        fig.update_layout(
            title="Philippines Headline Inflation Rate with BSP Target Band",
            xaxis_title="Date", yaxis_title="Inflation rate (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=440, margin=dict(l=40, r=40, t=60, b=40),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Recent 5-year zoom
        st.markdown(
            '<div class="section-header">Recent Inflation — Last 5 Years</div>',
            unsafe_allow_html=True,
        )
        recent5 = valid[valid["date"] >= pd.Timestamp("2021-01-01")].copy()
        fig2 = go.Figure()
        fig2.add_hrect(y0=BSP_LOWER, y1=BSP_UPPER, fillcolor="#16a34a", opacity=0.1, line_width=0)
        fig2.add_hline(y=BSP_MIDPOINT, line_dash="dash", line_color="#16a34a", line_width=1)
        fig2.add_trace(go.Scatter(
            x=recent5["date"], y=recent5["inflation_rate"],
            mode="lines+markers", name="Inflation rate",
            line=dict(color="#1e3a5f", width=2), marker=dict(size=4),
        ))
        if obs_date is not None and fcast_date is not None:
            fig2.add_trace(go.Scatter(
                x=[obs_date, fcast_date], y=[obs_inf, fcast_inf],
                mode="markers+text",
                marker=dict(color="#dc2626", size=10, symbol=["circle", "diamond"]),
                text=[f"{obs_inf:.1f}%", f"Forecast {fcast_inf:.2f}%"],
                textposition=["top center", "top center"],
                name="Current / Forecast",
                textfont=dict(size=10, color="#dc2626"),
            ))
        fig2.update_layout(
            title="Inflation Rate - Recent 5 Years vs BSP Target Band",
            xaxis_title="Date", yaxis_title="Inflation rate (%)",
            height=360, margin=dict(l=40, r=40, t=50, b=40),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Band summary table
    st.markdown(
        '<div class="section-header">Target Band Position Summary</div>',
        unsafe_allow_html=True,
    )
    if band_summary is not None:
        disp = band_summary.rename(columns={
            "latest_observed_date":      "Observed Date",
            "latest_observed_inflation": "Observed Inflation",
            "latest_forecast_date":      "Forecast Date",
            "latest_forecast_inflation": "Forecast Inflation",
            "target_midpoint":           "Target Midpoint",
            "target_lower_bound":        "Lower Bound",
            "target_upper_bound":        "Upper Bound",
            "observed_position_vs_target": "Observed Position",
            "forecast_position_vs_target": "Forecast Position",
        })
        st.dataframe(disp, hide_index=True, use_container_width=True)

    if "inflation_context" in notes:
        st.markdown(
            '<div class="section-header">Inflation Context</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="callout-info">{notes["inflation_context"]}</div>',
            unsafe_allow_html=True,
        )
    if "policy_target_context" in notes:
        st.markdown(
            '<div class="section-header">Policy Target Context</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="callout-warn">{notes["policy_target_context"]}</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE: FORECAST PERFORMANCE
# ============================================================
elif page == "Forecast Performance":
    st.title("Forecast Performance")
    st.markdown(
        '<div class="callout-info">'
        "Three baseline models evaluated on a chronological 80/20 train/test split. "
        "Linear regression uses eight features: inflation lags (1, 3, 6 months), "
        "rolling averages (3, 6 months), month-over-month change, and USD/PHP lag and change."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-header">Model Performance Metrics (Test Set)</div>',
        unsafe_allow_html=True,
    )
    if metrics is not None:
        m_disp = metrics.copy()
        m_disp["mae"]  = m_disp["mae"].round(4)
        m_disp["rmse"] = m_disp["rmse"].round(4)
        m_disp["mape"] = m_disp["mape"].round(2).astype(str) + "%"
        m_disp["directional_accuracy"] = (m_disp["directional_accuracy"] * 100).round(1).astype(str) + "%"
        m_disp.columns = ["Model", "MAE", "RMSE", "MAPE", "Directional Accuracy"]
        st.dataframe(m_disp, hide_index=True, use_container_width=True)

        rmse_df = metrics.sort_values("rmse")
        color_map = {
            "linear_regression": "#2563eb",
            "naive_last_value":  "#94a3b8",
            "moving_average_3m": "#cbd5e1",
        }
        fig_m = go.Figure(go.Bar(
            x=rmse_df["rmse"].round(4),
            y=rmse_df["model"],
            orientation="h",
            marker_color=[color_map.get(m, "#94a3b8") for m in rmse_df["model"]],
            text=rmse_df["rmse"].round(4),
            textposition="outside",
        ))
        fig_m.update_layout(
            title="Model RMSE Comparison (lower is better)",
            xaxis_title="RMSE (percentage points)",
            height=240, margin=dict(l=40, r=60, t=50, b=40),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
        )
        st.plotly_chart(fig_m, use_container_width=True)

    st.markdown(
        '<div class="section-header">Actual vs Forecast — Linear Regression (Test Set)</div>',
        unsafe_allow_html=True,
    )
    if test_preds is not None:
        fig_avf = go.Figure()
        fig_avf.add_hrect(y0=BSP_LOWER, y1=BSP_UPPER, fillcolor="#16a34a", opacity=0.07, line_width=0)
        fig_avf.add_trace(go.Scatter(
            x=test_preds["target_date"], y=test_preds["actual_inflation_1m_ahead"],
            mode="lines", name="Actual inflation",
            line=dict(color="#1e3a5f", width=2),
        ))
        fig_avf.add_trace(go.Scatter(
            x=test_preds["target_date"], y=test_preds["linear_regression_forecast"],
            mode="lines", name="Linear regression forecast",
            line=dict(color="#2563eb", width=1.5, dash="dash"),
        ))
        fig_avf.add_trace(go.Scatter(
            x=test_preds["target_date"], y=test_preds["naive_last_value_forecast"],
            mode="lines", name="Naive last-value",
            line=dict(color="#cbd5e1", width=1, dash="dot"),
        ))
        fig_avf.update_layout(
            title="One-Month-Ahead Inflation: Actual vs Model Forecasts",
            xaxis_title="Target date", yaxis_title="Inflation rate (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400, margin=dict(l=40, r=40, t=60, b=40),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
        )
        st.plotly_chart(fig_avf, use_container_width=True)

        st.markdown(
            '<div class="section-header">Forecast Errors Over Time — Linear Regression</div>',
            unsafe_allow_html=True,
        )
        fig_err = go.Figure()
        fig_err.add_hline(y=0, line_color="#64748b", line_width=1)
        fig_err.add_trace(go.Scatter(
            x=test_preds["target_date"],
            y=test_preds["linear_regression_forecast_error"],
            mode="lines", name="LR forecast error",
            line=dict(color="#2563eb", width=1.5),
            fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
        ))
        fig_err.update_layout(
            title="Forecast Error: Linear Regression (Forecast minus Actual)",
            xaxis_title="Target date", yaxis_title="Error (pp)",
            height=300, margin=dict(l=40, r=40, t=50, b=40),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
        )
        st.plotly_chart(fig_err, use_container_width=True)

    if "forecast_context" in notes:
        st.markdown(
            '<div class="section-header">Latest Forecast Context</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="callout-info">{notes["forecast_context"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="callout-warn">'
        "<strong>Interpretation note:</strong> Linear regression test MAPE is 19.1% and "
        "directional accuracy is 62.3%. The model outperforms naive and moving-average "
        "benchmarks but is not a production-grade nowcasting model. Forecast errors are "
        "non-trivial and turning points may be missed. The 80/20 chronological split does "
        "not simulate rolling-origin live forecasting."
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE: POLICY INTERPRETATION
# ============================================================
elif page == "Policy Interpretation":
    st.title("Policy Interpretation")
    st.markdown(
        '<div class="callout-disclaimer">'
        "All interpretations below are analytical frames only. They do not constitute "
        "official BSP guidance, investment recommendations, or professional macro forecasts."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-header">Scenario and Business Interpretation</div>',
        unsafe_allow_html=True,
    )
    if policy_df is not None:
        SECTION_LABELS = {
            "inflation_trend":             "Inflation Trend",
            "model_performance":           "Model Performance",
            "latest_forecast":             "Latest Forecast",
            "scenario_a_bsp_hold_tighten": "Scenario A: BSP Hold / Tighten",
            "scenario_b_bsp_ease":         "Scenario B: BSP Ease",
            "scenario_c_external_shock":   "Scenario C: External Shock",
            "business_banks":              "Banks",
            "business_fintechs":           "Fintechs",
            "business_corporate":          "Corporate Finance",
        }
        tabs = st.tabs(list(SECTION_LABELS.values()))
        for tab, (key, _tab_label) in zip(tabs, SECTION_LABELS.items()):
            with tab:
                row = policy_df[policy_df["section"] == key]
                if row.empty:
                    st.info(f"No data for section: {key}")
                    continue
                r = row.iloc[0]
                st.markdown(f"**Finding:** {r['finding']}")
                st.markdown(f"**Implication:** {r['implication']}")
                st.markdown(
                    f'<div class="callout-warn"><strong>Caveat:</strong> {r["caveat"]}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown(
        '<div class="section-header">Full Policy Interpretation Table</div>',
        unsafe_allow_html=True,
    )
    if policy_df is not None:
        disp_p = policy_df.copy()
        disp_p.columns = ["Section", "Finding", "Implication", "Caveat"]
        st.dataframe(disp_p, hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="section-header">Business Relevance</div>', unsafe_allow_html=True
    )
    if "business_relevance" in notes:
        st.markdown(
            f'<div class="callout-info">{notes["business_relevance"]}</div>',
            unsafe_allow_html=True,
        )

    col_b, col_f, col_c = st.columns(3)
    with col_b:
        st.markdown("**Banks**")
        st.markdown(
            """
            - BSP hold supports short-term NIM expansion on variable-rate books
            - Fixed-rate funding creates repricing risk if BSP tightens
            - Credit quality monitoring important as prices compress household capacity
            """
        )
    with col_f:
        st.markdown("**Fintechs**")
        st.markdown(
            """
            - Higher funding costs and potential delinquency uptick
            - Shorter repricing windows require proactive cost-of-funds analysis
            - FX funding exposure adds peso depreciation risk under Scenario C
            """
        )
    with col_c:
        st.markdown("**Corporate Finance**")
        st.markdown(
            """
            - Stress-test refinancing at 4.5%-5.5% inflation for H1 2026
            - USD/PHP at ~59.4 adds import cost pressure
            - Working capital models should include upside inflation sensitivity
            """
        )


# ============================================================
# PAGE: DATA AND LIMITATIONS
# ============================================================
elif page == "Data and Limitations":
    st.title("Data and Limitations")

    st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)
    sources_df = pd.DataFrame({
        "Source": [
            "BSP (via Excel download)",
            "BSP (via Excel download)",
            "World Bank API",
            "PSA (reference only)",
        ],
        "Series": [
            "Headline inflation rate",
            "USD/PHP exchange rate",
            "GDP growth, unemployment, remittances (annual)",
            "Official CPI and inflation data",
        ],
        "Frequency": ["Monthly", "Monthly", "Annual", "Monthly"],
        "Coverage": [
            "1958-March 2026",
            "~2000-2026",
            "~1960-2023",
            "Official source; not parsed in this project",
        ],
    })
    st.dataframe(sources_df, hide_index=True, use_container_width=True)

    st.markdown('<div class="section-header">Methodology</div>', unsafe_allow_html=True)
    st.markdown(
        """
        **Forecast target:** One-month-ahead Philippines headline inflation rate.

        **Feature engineering:** Inflation lags (1, 3, 6 months), rolling averages (3, 6 months),
        month-over-month change, USD/PHP lag and change.

        **Evaluation:** Chronological 80/20 train/test split. No random split, no rolling-origin
        validation.

        **Model implementation:** NumPy least-squares fallback was used due to a local NumPy/sklearn
        compatibility issue. Results are mathematically equivalent to sklearn `LinearRegression`.
        """
    )

    st.markdown('<div class="section-header">Known Limitations</div>', unsafe_allow_html=True)
    if "limitations" in notes:
        st.markdown(
            f'<div class="callout-warn">{notes["limitations"]}</div>',
            unsafe_allow_html=True,
        )

    limits_df = pd.DataFrame({
        "Limitation": [
            "Model scope",
            "Missing inputs",
            "Evaluation method",
            "Forecast uncertainty",
            "Directional accuracy",
            "Policy rate data",
            "Project scope",
        ],
        "Detail": [
            "Simple linear regression baseline; not advanced nowcasting",
            "No rice prices, oil prices, core inflation, BSP policy rate, survey expectations",
            "80/20 chronological holdout; not rolling-origin validation",
            "Test MAPE 19.1%; plausible April 2026 range approximately 4.5%-5.5%",
            "62.3% on test set; not reliable for sharp turning points",
            "BSP key rates page referenced but not parsed in this project",
            "Portfolio research project only; not affiliated with BSP, PSA, or any official institution",
        ],
    })
    st.dataframe(limits_df, hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="section-header">Future Improvements</div>', unsafe_allow_html=True
    )
    st.markdown(
        """
        1. **Rolling-origin validation** - Walk-forward evaluation to simulate live forecasting.
        2. **Policy rate features** - Parse BSP key rates page for lagged policy rate inputs.
        3. **Rice and food price data** - Rice prices are a key driver of Philippines CPI.
        4. **Core inflation decomposition** - Separate food-and-energy from core components.
        5. **Regularised models** - Ridge regression or simple ensembles to reduce overfitting.
        6. **Survey expectations** - BSP inflation expectations survey as a feature.
        """
    )

    st.markdown(
        '<div class="callout-disclaimer">'
        "<strong>Disclaimer:</strong> This dashboard is a portfolio research project. "
        "Forecasts are generated by a simple linear regression model trained on historical "
        "Philippines inflation and USD/PHP data. Nothing in this dashboard constitutes "
        "official economic analysis, investment advice, or guidance from BSP, PSA, or any "
        "official institution."
        "</div>",
        unsafe_allow_html=True,
    )
