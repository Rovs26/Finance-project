"""Streamlit dashboard for the Credit Risk and IFRS 9-style ECL project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS_DIR = PROJECT_ROOT / "outputs" / "predictions"
ECL_RESULTS_PATH = PROJECT_ROOT / "outputs" / "ecl_results.csv"

REQUIRED_FILES = {
    "dashboard_summary": PREDICTIONS_DIR / "dashboard_summary.csv",
    "ecl_by_stage": PREDICTIONS_DIR / "ecl_by_stage.csv",
    "ecl_by_score_band": PREDICTIONS_DIR / "ecl_by_score_band.csv",
    "scenario_summary": PREDICTIONS_DIR / "ecl_scenario_summary.csv",
    "ecl_results": ECL_RESULTS_PATH,
}

OPTIONAL_FILES = {
    "ecl_by_grade": PREDICTIONS_DIR / "ecl_by_grade.csv",
    "ecl_by_purpose": PREDICTIONS_DIR / "ecl_by_purpose.csv",
}

CHART_COLOR = "#4F8EF7"
CHART_ACCENT = "#8AB4F8"
TEXT_MUTED = "#9CA3AF"


def apply_custom_css() -> None:
    """Apply dashboard-level styling."""
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1 {
            font-size: 2.15rem;
            font-weight: 720;
            letter-spacing: 0;
            margin-bottom: 0.35rem;
        }
        h2, h3 {
            letter-spacing: 0;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            padding: 0.35rem 0.25rem;
            border-radius: 6px;
        }
        .project-subtitle {
            color: #9CA3AF;
            max-width: 920px;
            font-size: 1.02rem;
            line-height: 1.55;
            margin-bottom: 0.75rem;
        }
        .disclaimer-box {
            border: 1px solid rgba(245, 158, 11, 0.35);
            background: rgba(245, 158, 11, 0.08);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            color: #FDE68A;
            margin: 0.8rem 0 1.2rem 0;
        }
        .kpi-card {
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: rgba(15, 23, 42, 0.45);
            border-radius: 8px;
            padding: 1rem 1rem 0.9rem 1rem;
            min-height: 116px;
        }
        .kpi-label {
            color: #9CA3AF;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.35rem;
        }
        .kpi-value {
            color: #F8FAFC;
            font-size: 1.35rem;
            font-weight: 700;
            line-height: 1.25;
            margin-bottom: 0.35rem;
            overflow-wrap: anywhere;
        }
        .kpi-helper {
            color: #9CA3AF;
            font-size: 0.82rem;
            line-height: 1.35;
        }
        .insight-box {
            border-left: 4px solid #4F8EF7;
            background: rgba(79, 142, 247, 0.10);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            margin: 0.85rem 0 1.1rem 0;
            color: #DDEAFE;
        }
        .insight-label {
            color: #8AB4F8;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.78rem;
            letter-spacing: 0.06em;
            margin-bottom: 0.25rem;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 8px;
            overflow: hidden;
        }
        div[data-testid="stDownloadButton"] button {
            border-radius: 6px;
            border: 1px solid rgba(148, 163, 184, 0.30);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_currency(value: float) -> str:
    """Format a numeric value as compact currency."""
    if pd.isna(value):
        return "N/A"
    value = float(value)
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"
    if abs_value >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if abs_value >= 1_000:
        return f"${value / 1_000:,.2f}K"
    return f"${value:,.2f}"


def format_percent(value: float) -> str:
    """Format a decimal value as a percentage."""
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.2%}"


def render_key_insight(text: str) -> None:
    """Render a styled page-level key insight."""
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-label">Key insight</div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_csv(path: Path, required: bool = True) -> pd.DataFrame:
    """Load a CSV file with clear Streamlit errors."""
    if not path.exists():
        if required:
            st.error(f"Required file is missing: `{path.relative_to(PROJECT_ROOT)}`")
            st.stop()
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.error(f"Could not load `{path.relative_to(PROJECT_ROOT)}`: {exc}")
        st.stop()


def render_kpi_row(summary: pd.Series) -> None:
    """Render the portfolio KPI row."""
    cols = st.columns(6)
    cards = [
        ("Loans", f"{int(summary['total_loans']):,}", "Portfolio sample"),
        ("Exposure", format_currency(summary["total_exposure"]), "EAD proxy"),
        ("Expected Loss", format_currency(summary["total_ecl"]), "Base scenario"),
        ("ECL Rate", format_percent(summary["ecl_rate"]), "ECL / exposure"),
        ("Average PD", format_percent(summary["average_pd"]), "Model score mean"),
        ("Average LGD", format_percent(summary["average_lgd"]), "Assumption mean"),
    ]
    for col, (label, value, helper) in zip(cols, cards):
        col.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-helper">{helper}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _format_chart_value(value: float, y_col: str) -> str:
    """Format chart hover and text values."""
    if "rate" in y_col or y_col in {"average_pd", "average_lgd", "pd_multiplier", "lgd_multiplier"}:
        return format_percent(value)
    if any(token in y_col for token in ["ecl", "exposure", "ead", "loan_amnt"]):
        return format_currency(value)
    if pd.isna(value):
        return "N/A"
    return f"{float(value):,.2f}"


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    labels: dict | None = None,
) -> None:
    """Render a Plotly bar chart."""
    if df.empty:
        st.info("No data available for this chart.")
        return
    chart_df = df.copy()
    chart_df["_display_value"] = chart_df[y].apply(lambda value: _format_chart_value(value, y))
    chart = px.bar(
        chart_df,
        x=x,
        y=y,
        color=color,
        title=title,
        text="_display_value",
        labels=labels,
        template="plotly_dark",
        color_discrete_sequence=[CHART_COLOR, CHART_ACCENT, "#7DD3FC", "#A78BFA"],
    )
    hover_label = labels.get(y, y) if labels else y
    chart.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=18, r=18, t=58, b=28),
        font=dict(color="#E5E7EB", size=13),
        title=dict(font=dict(size=17), x=0.01, xanchor="left"),
        xaxis_title=labels.get(x, x) if labels else x,
        yaxis_title=labels.get(y, y) if labels else y,
        showlegend=bool(color),
        bargap=0.28,
    )
    chart.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color="#CBD5E1"))
    chart.update_yaxes(gridcolor="rgba(148, 163, 184, 0.18)", zeroline=False, tickfont=dict(color="#CBD5E1"))
    chart.update_traces(
        marker_line_width=0,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>" + hover_label + ": %{customdata[0]}<extra></extra>",
        customdata=chart_df[["_display_value"]],
    )
    st.plotly_chart(chart, use_container_width=True)


def _table_formatters(df: pd.DataFrame) -> dict:
    """Build display formatters for summary tables."""
    currency_cols = {
        "total_exposure",
        "total_ecl",
        "ecl",
        "ead",
        "loan_amnt",
        "installment",
        "annual_inc",
        "stage_1_ecl",
        "stage_2_ecl",
        "stage_3_ecl",
    }
    percent_cols = {
        "ecl_rate",
        "average_pd",
        "average_lgd",
        "pd_score",
        "lgd",
    }
    formatters = {}
    for col in df.columns:
        if col in currency_cols:
            formatters[col] = format_currency
        elif col in percent_cols:
            formatters[col] = format_percent
        elif col in {"pd_multiplier", "lgd_multiplier"}:
            formatters[col] = "{:.2f}x"
        elif pd.api.types.is_float_dtype(df[col]):
            formatters[col] = "{:,.2f}"
        elif pd.api.types.is_integer_dtype(df[col]):
            formatters[col] = "{:,}"
    return formatters


def safe_table(df: pd.DataFrame, max_rows: int = 500) -> None:
    """Display a bounded, copy-safe table."""
    if df.empty:
        st.info("No rows available.")
        return
    display_df = df.head(max_rows).copy()
    styled = display_df.style.format(_table_formatters(display_df)).hide(axis="index")
    st.dataframe(styled, use_container_width=True)
    if len(df) > max_rows:
        st.caption(f"Showing first {max_rows:,} of {len(df):,} rows.")


def page_portfolio_overview(
    dashboard_summary: pd.DataFrame,
    ecl_by_stage: pd.DataFrame,
    ecl_by_score_band: pd.DataFrame,
) -> None:
    """Render the portfolio overview page."""
    st.header("Portfolio Overview")
    summary = dashboard_summary.iloc[0]
    render_kpi_row(summary)
    render_key_insight(
        "The sample portfolio contains 50,000 loans. Under the simplified ECL "
        "assumptions, expected loss is concentrated in Stage 3 and higher PD score bands."
    )

    left, right = st.columns(2)
    with left:
        bar_chart(
            ecl_by_stage,
            x="group_value",
            y="total_ecl",
            title="ECL by IFRS 9-style Stage",
            labels={"group_value": "Stage", "total_ecl": "Total ECL"},
        )
    with right:
        bar_chart(
            ecl_by_score_band,
            x="group_value",
            y="total_ecl",
            title="ECL by PD Score Band",
            labels={"group_value": "PD score band", "total_ecl": "Total ECL"},
        )


def page_ifrs9_staging(ecl_by_stage: pd.DataFrame) -> None:
    """Render the simplified staging page."""
    st.header("IFRS 9 Staging")
    render_key_insight(
        "Stage 3 carries the largest ECL share because it captures records with high PD scores or observed default flags."
    )
    st.markdown(
        "Simplified staging rules: Stage 1 uses `pd_score < 0.20`; Stage 2 uses "
        "`0.20 <= pd_score < 0.50`; Stage 3 uses `pd_score >= 0.50` or `default_flag == 1`."
    )

    safe_table(ecl_by_stage)

    left, right = st.columns(2)
    with left:
        bar_chart(
            ecl_by_stage,
            x="group_value",
            y="total_exposure",
            title="Exposure by Stage",
            labels={"group_value": "Stage", "total_exposure": "Total exposure"},
        )
    with right:
        bar_chart(
            ecl_by_stage,
            x="group_value",
            y="total_ecl",
            title="ECL by Stage",
            labels={"group_value": "Stage", "total_ecl": "Total ECL"},
        )


def page_risk_segments(ecl_by_grade: pd.DataFrame, ecl_by_purpose: pd.DataFrame) -> None:
    """Render grade and purpose segment views."""
    st.header("Risk Segments")
    render_key_insight(
        "Grade and purpose views help identify where expected loss is concentrated before opening loan-level detail."
    )
    st.markdown(
        "These views identify concentration risk by available portfolio segments. "
        "They are useful for business review, not for standalone credit decisions."
    )

    if not ecl_by_grade.empty:
        st.subheader("Grade")
        bar_chart(
            ecl_by_grade,
            x="group_value",
            y="total_ecl",
            title="ECL by Grade",
            labels={"group_value": "Grade", "total_ecl": "Total ECL"},
        )
        safe_table(ecl_by_grade)
    else:
        st.info("Grade summary file is not available.")

    if not ecl_by_purpose.empty:
        st.subheader("Purpose")
        bar_chart(
            ecl_by_purpose.head(12),
            x="group_value",
            y="total_ecl",
            title="ECL by Purpose",
            labels={"group_value": "Purpose", "total_ecl": "Total ECL"},
        )
        safe_table(ecl_by_purpose)
    else:
        st.info("Purpose summary file is not available.")


def page_scenario_analysis(scenarios: pd.DataFrame) -> None:
    """Render scenario analysis page."""
    st.header("Scenario Analysis")
    render_key_insight(
        "Stress scenarios show how portfolio ECL changes when PD and LGD assumptions are increased together."
    )
    st.markdown(
        "Stress scenarios apply transparent PD and LGD multipliers. Stressed PD and LGD "
        "are capped at 100% in the Phase 3 ECL engine."
    )

    bar_chart(
        scenarios,
        x="scenario",
        y="total_ecl",
        title="Scenario Total ECL Comparison",
        labels={"scenario": "Scenario", "total_ecl": "Total ECL"},
    )
    safe_table(scenarios)

    multiplier_cols = [col for col in ["scenario", "pd_multiplier", "lgd_multiplier"] if col in scenarios.columns]
    if multiplier_cols:
        st.subheader("Stress Multipliers")
        safe_table(scenarios[multiplier_cols])


def page_loan_level_explorer(ecl_results: pd.DataFrame) -> None:
    """Render filterable loan-level ECL explorer."""
    st.header("Loan-Level Explorer")
    render_key_insight(
        "Use the filters to move from portfolio-level concentration to individual loans driving the ECL estimate."
    )
    st.markdown("Filter row-level ECL output and download the current filtered view.")

    filtered = ecl_results.copy()
    filter_cols = {
        "ifrs9_stage": "IFRS 9 stage",
        "pd_score_band": "PD score band",
        "grade": "Grade",
        "purpose": "Purpose",
    }

    for col, label in filter_cols.items():
        if col in filtered.columns:
            values = sorted(filtered[col].dropna().astype(str).unique().tolist())
            selected = st.multiselect(label, values, default=values)
            filtered = filtered[filtered[col].astype(str).isin(selected)]

    safe_cols = [
        "row_id",
        "default_flag",
        "pd_score",
        "pd_score_band",
        "ead",
        "lgd",
        "ifrs9_stage",
        "ecl",
        "loan_amnt",
        "term",
        "int_rate",
        "grade",
        "sub_grade",
        "home_ownership",
        "annual_inc",
        "verification_status",
        "purpose",
        "dti",
        "revol_util",
        "total_acc",
    ]
    display_cols = [col for col in safe_cols if col in filtered.columns]
    st.caption(f"Filtered rows: {len(filtered):,}")
    safe_table(filtered[display_cols], max_rows=500)
    st.download_button(
        "Download filtered rows",
        filtered[display_cols].to_csv(index=False).encode("utf-8"),
        file_name="filtered_ecl_rows.csv",
        mime="text/csv",
    )


def page_methodology_limitations() -> None:
    """Render methodology and limitations page."""
    st.header("Methodology and Limitations")
    render_key_insight(
        "The dashboard is designed for transparent portfolio analytics, not regulatory reporting or credit approval."
    )
    st.subheader("Plain-English Methodology")
    st.write(
        "PD estimates the likelihood of default. LGD estimates the share of exposure lost "
        "if default happens. EAD estimates exposure at default. ECL combines them as "
        "`PD x LGD x EAD`."
    )

    st.subheader("Simplified Assumptions")
    st.markdown(
        """
        - EAD uses `loan_amnt`.
        - LGD uses a home ownership adjustment.
        - Staging uses PD thresholds and `default_flag`.
        - Scenarios use PD and LGD multipliers.
        - This dashboard is a portfolio analytics project, not a regulatory production IFRS 9 model.
        """
    )

    st.subheader("Next Improvements")
    st.markdown(
        """
        - Lifetime PD
        - Macroeconomic overlays
        - Discounting
        - Model validation
        - Monitoring
        - Data quality checks
        """
    )


def main() -> None:
    """Run the dashboard."""
    st.set_page_config(
        page_title="Credit Risk IFRS 9 ECL Engine",
        layout="wide",
    )
    apply_custom_css()

    st.title("Credit Risk and IFRS 9-style Expected Credit Loss Engine")
    st.markdown(
        """
        <div class="project-subtitle">
        A portfolio analytics dashboard for reviewing PD scores, simplified IFRS 9-style
        stages, ECL concentration, stress scenarios, and row-level ECL outputs.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="disclaimer-box">
        Portfolio project only: this is not a regulatory IFRS 9 production model,
        not a bank decision engine, and not a validated credit approval system.
        </div>
        """,
        unsafe_allow_html=True,
    )
    for name, path in REQUIRED_FILES.items():
        if not path.exists():
            st.error(f"Missing required dashboard input `{name}`: `{path.relative_to(PROJECT_ROOT)}`")
            st.stop()

    dashboard_summary = load_csv(REQUIRED_FILES["dashboard_summary"])
    ecl_by_stage = load_csv(REQUIRED_FILES["ecl_by_stage"])
    ecl_by_score_band = load_csv(REQUIRED_FILES["ecl_by_score_band"])
    scenarios = load_csv(REQUIRED_FILES["scenario_summary"])
    ecl_results = load_csv(REQUIRED_FILES["ecl_results"])
    ecl_by_grade = load_csv(OPTIONAL_FILES["ecl_by_grade"], required=False)
    ecl_by_purpose = load_csv(OPTIONAL_FILES["ecl_by_purpose"], required=False)

    page = st.sidebar.radio(
        "Dashboard page",
        [
            "Portfolio Overview",
            "IFRS 9 Staging",
            "Risk Segments",
            "Scenario Analysis",
            "Loan-Level Explorer",
            "Methodology and Limitations",
        ],
    )
    st.sidebar.caption("Data source: generated Phase 3 and Phase 4A CSV outputs.")

    if page == "Portfolio Overview":
        page_portfolio_overview(dashboard_summary, ecl_by_stage, ecl_by_score_band)
    elif page == "IFRS 9 Staging":
        page_ifrs9_staging(ecl_by_stage)
    elif page == "Risk Segments":
        page_risk_segments(ecl_by_grade, ecl_by_purpose)
    elif page == "Scenario Analysis":
        page_scenario_analysis(scenarios)
    elif page == "Loan-Level Explorer":
        page_loan_level_explorer(ecl_results)
    else:
        page_methodology_limitations()


if __name__ == "__main__":
    main()
