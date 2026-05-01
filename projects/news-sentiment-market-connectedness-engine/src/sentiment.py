"""Sentiment data helpers for prototype scoring and summaries."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pandas as pd


COMPANY_TICKER_MAP = {
    "apple": ("Apple", "AAPL"),
    "amazon": ("Amazon", "AMZN"),
    "tesla": ("Tesla", "TSLA"),
    "microsoft": ("Microsoft", "MSFT"),
    "nvidia": ("Nvidia", "NVDA"),
    "jpmorgan": ("JPMorgan", "JPM"),
    "google": ("Google", "GOOGL"),
    "alphabet": ("Alphabet", "GOOGL"),
    "meta": ("Meta", "META"),
    "netflix": ("Netflix", "NFLX"),
}

POSITIVE_TERMS = {
    "soars",
    "growth",
    "beats",
    "record",
    "profit",
    "rally",
    "surge",
    "strong",
    "upgrade",
    "optimism",
}

NEGATIVE_TERMS = {
    "lawsuit",
    "tariff",
    "uncertainty",
    "shutdown",
    "threat",
    "bubble",
    "tensions",
    "warns",
    "pressure",
    "risk",
    "selloff",
}

RISK_TERMS = {
    "credit risk": ["credit", "loan", "default", "borrower", "delinquency"],
    "market risk": ["market", "volatility", "bubble", "selloff", "portfolio"],
    "policy risk": ["fed", "tariff", "policy", "shutdown", "regulation"],
    "legal risk": ["lawsuit", "sec", "probe", "legal"],
    "competitive risk": ["competitive", "threat", "rival"],
    "macro risk": ["inflation", "rates", "china", "tensions", "tariff"],
}


def standardize_sentiment_log(df):
    """Return a lightly standardized sentiment log without changing source meaning."""
    standardized = df.copy()
    standardized.columns = [str(col).strip().lower().replace(" ", "_") for col in standardized.columns]
    if "date" in standardized.columns:
        standardized["date"] = pd.to_datetime(standardized["date"], errors="coerce").dt.normalize()
    for col in ["sentiment_score", "score", "polarity"]:
        if col in standardized.columns:
            standardized["sentiment_score"] = pd.to_numeric(standardized[col], errors="coerce")
            break
    if "sentiment_score" in standardized.columns:
        standardized["sentiment_label"] = standardized["sentiment_score"].apply(classify_sentiment_score)
        standardized["recommended_signal"] = standardized["sentiment_score"].apply(create_signal_from_score)
    if "action" not in standardized.columns and "recommended_signal" in standardized.columns:
        standardized["action"] = standardized["recommended_signal"]
    if "action" in standardized.columns:
        standardized["action"] = standardized["action"].fillna("").astype(str).str.upper()
    return standardized


def standardize_scraped_news(df):
    """Standardize scraped news column names and date fields when available."""
    standardized = df.copy()
    standardized.columns = [str(col).strip().lower().replace(" ", "_") for col in standardized.columns]
    for col in standardized.columns:
        if "date" in col or "time" in col or "published" in col:
            standardized[col] = pd.to_datetime(standardized[col], errors="coerce")
    return standardized


def classify_sentiment_score(score):
    """Classify a numeric sentiment score into negative, neutral, or positive."""
    if pd.isna(score):
        return "unknown"
    if score <= -0.15:
        return "negative"
    if score >= 0.15:
        return "positive"
    return "neutral"


def create_signal_from_score(score):
    """Create a research signal label from sentiment score."""
    if pd.isna(score):
        return "HOLD"
    if score <= -0.25:
        return "SELL"
    if score >= 0.25:
        return "BUY"
    return "HOLD"


def infer_company_and_ticker(text, company=None):
    """Infer standardized company and ticker values from text or existing company field."""
    source = " ".join([str(company or ""), str(text or "")]).lower()
    for key, value in COMPANY_TICKER_MAP.items():
        if key in source:
            return value
    return (str(company).strip() if company else "", "")


def extract_risk_flags(text):
    """Extract simple keyword-based risk flags."""
    lowered = str(text).lower()
    flags = [
        category
        for category, keywords in RISK_TERMS.items()
        if any(keyword in lowered for keyword in keywords)
    ]
    return flags


def _rule_based_score(text):
    lowered = str(text).lower()
    positive_hits = sum(1 for term in POSITIVE_TERMS if term in lowered)
    negative_hits = sum(1 for term in NEGATIVE_TERMS if term in lowered)
    raw_score = (positive_hits - negative_hits) / max(positive_hits + negative_hits, 1)
    if positive_hits == 0 and negative_hits == 0:
        raw_score = 0.0
    return max(min(float(raw_score), 1.0), -1.0)


def _load_openai_settings(env_path=None):
    """Load OpenAI settings without printing or returning sensitive values in logs."""
    try:
        from dotenv import load_dotenv

        if env_path:
            load_dotenv(env_path)
        else:
            for parent in [Path.cwd(), *Path.cwd().parents]:
                candidate = parent / ".env"
                if candidate.exists():
                    load_dotenv(candidate)
                    break
    except Exception:
        pass
    return {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    }


def score_headline_or_text(text, company=None, ticker=None, use_openai=True, model=None):
    """Score one headline or text item using OpenAI if available, else a rule fallback."""
    standard_company, inferred_ticker = infer_company_and_ticker(text, company)
    final_ticker = ticker or inferred_ticker
    settings = _load_openai_settings()
    selected_model = model or settings["model"] or "gpt-4o-mini"

    if use_openai and settings["api_key"]:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings["api_key"], timeout=20)
            schema = {
                "name": "financial_sentiment",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "company": {"type": "string"},
                        "ticker": {"type": "string"},
                        "sentiment_score": {"type": "number", "minimum": -1, "maximum": 1},
                        "sentiment_label": {"type": "string", "enum": ["negative", "neutral", "positive"]},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "rationale": {"type": "string"},
                        "risk_flags": {"type": "array", "items": {"type": "string"}},
                        "recommended_signal": {"type": "string", "enum": ["BUY", "HOLD", "SELL"]},
                    },
                    "required": [
                        "company",
                        "ticker",
                        "sentiment_score",
                        "sentiment_label",
                        "confidence",
                        "rationale",
                        "risk_flags",
                        "recommended_signal",
                    ],
                },
            }
            response = client.chat.completions.create(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Return JSON only. Score finance news sentiment for research analytics, not trading advice.",
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Company: {standard_company or company or 'unknown'}\\n"
                            f"Ticker: {final_ticker or 'unknown'}\\n"
                            f"Text: {text}"
                        ),
                    },
                ],
                response_format={"type": "json_schema", "json_schema": schema},
            )
            parsed = json.loads(response.choices[0].message.content)
            score = max(min(float(parsed.get("sentiment_score", 0.0)), 1.0), -1.0)
            parsed["sentiment_score"] = score
            parsed["sentiment_label"] = classify_sentiment_score(score)
            parsed["recommended_signal"] = create_signal_from_score(score)
            parsed["company"] = standard_company
            parsed["ticker"] = final_ticker
            parsed["risk_flags"] = parsed.get("risk_flags") or []
            parsed["scoring_method"] = "openai_structured"
            return parsed
        except Exception:
            pass

    score = _rule_based_score(text)
    flags = extract_risk_flags(text)
    return {
        "company": standard_company,
        "ticker": final_ticker,
        "sentiment_score": score,
        "sentiment_label": classify_sentiment_score(score),
        "confidence": 0.55 if flags else 0.40,
        "rationale": "Rule-based fallback using positive and negative finance keywords.",
        "risk_flags": flags,
        "recommended_signal": create_signal_from_score(score),
        "scoring_method": "rule_based_fallback",
    }


def score_sentiment_dataframe(df, text_col="headline", use_openai=True):
    """Score rows with headline/text and append structured sentiment fields."""
    if df.empty or text_col not in df.columns:
        return df.copy()
    rows = []
    for _, row in df.iterrows():
        result = score_headline_or_text(
            row.get(text_col, ""),
            company=row.get("company", ""),
            ticker=row.get("ticker", ""),
            use_openai=use_openai,
        )
        rows.append(result)
    scored = pd.DataFrame(rows)
    output = df.reset_index(drop=True).copy()
    for col in [
        "company",
        "ticker",
        "sentiment_score",
        "sentiment_label",
        "confidence",
        "rationale",
        "risk_flags",
        "recommended_signal",
        "scoring_method",
    ]:
        if col in scored.columns:
            value = scored[col]
            if col == "risk_flags":
                value = value.apply(lambda flags: ", ".join(flags) if isinstance(flags, list) else str(flags))
            output[f"rescored_{col}" if col in output.columns else col] = value
    if "rescored_sentiment_score" in output.columns:
        output["sentiment_score"] = output["rescored_sentiment_score"]
        output["sentiment_label"] = output["sentiment_score"].apply(classify_sentiment_score)
        output["recommended_signal"] = output["sentiment_score"].apply(create_signal_from_score)
    return output


def summarize_sentiment_by_company(df):
    """Summarize sentiment records by available company or ticker column."""
    candidates = [col for col in df.columns if col in {"company", "ticker", "symbol", "stock"}]
    if not candidates:
        return pd.DataFrame(columns=["company_key", "record_count"])
    key = candidates[0]
    return (
        df.groupby(key, dropna=False)
        .size()
        .reset_index(name="record_count")
        .rename(columns={key: "company_key"})
        .sort_values("record_count", ascending=False)
    )


def summarize_sentiment_by_date(df):
    """Summarize sentiment records by the first available date-like column."""
    date_cols = [col for col in df.columns if "date" in col or "time" in col]
    if not date_cols:
        return pd.DataFrame(columns=["date", "record_count", "avg_sentiment_score"])
    date_col = date_cols[0]
    dated = df.copy()
    dated["date"] = pd.to_datetime(dated[date_col], errors="coerce").dt.normalize()
    agg = {"record_count": ("date", "size")}
    if "sentiment_score" in dated.columns:
        agg["avg_sentiment_score"] = ("sentiment_score", "mean")
    if "sentiment_label" in dated.columns:
        agg["negative_count"] = ("sentiment_label", lambda x: (x == "negative").sum())
        agg["neutral_count"] = ("sentiment_label", lambda x: (x == "neutral").sum())
        agg["positive_count"] = ("sentiment_label", lambda x: (x == "positive").sum())
    return dated.groupby("date", dropna=True).agg(**agg).reset_index()


def create_signal_summary(df):
    """Summarize simple BUY/HOLD/SELL labels."""
    signal_col = "recommended_signal" if "recommended_signal" in df.columns else "action"
    if signal_col not in df.columns:
        return pd.DataFrame(columns=["action", "record_count", "share"])
    summary = df[signal_col].fillna("UNKNOWN").astype(str).str.upper().value_counts().reset_index()
    summary.columns = ["action", "record_count"]
    total = summary["record_count"].sum()
    summary["share"] = summary["record_count"] / total if total else 0
    return summary
