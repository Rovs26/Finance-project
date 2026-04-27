"""Simple visualization helpers for Phase 1 exploratory analysis.

The helpers use Pillow instead of Matplotlib so the notebook can still generate
PNG artifacts in lightweight or mismatched local Python environments.
"""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont
import pandas as pd


def _font(size: int = 14):
    """Load a default bitmap font."""
    return ImageFont.load_default(size=size)


def _truncate(value: object, max_length: int = 32) -> str:
    """Shorten long labels for compact charts."""
    text = str(value)
    return text if len(text) <= max_length else f"{text[: max_length - 3]}..."


def _bar_chart(
    labels: list[object],
    values: list[float],
    title: str,
    x_label: str,
    color: str,
    width: int = 1100,
    height: int = 700,
) -> Image.Image:
    """Draw a horizontal bar chart and return it as a Pillow image."""
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title_font = _font(22)
    text_font = _font(14)

    left = 300
    right = width - 70
    top = 80
    bottom = height - 80
    chart_width = right - left
    bar_area_height = bottom - top
    count = max(len(labels), 1)
    bar_gap = 8
    bar_height = max(12, int((bar_area_height - (count - 1) * bar_gap) / count))
    max_value = max(values) if values else 0
    scale = chart_width / max_value if max_value else 0

    draw.text((40, 28), title, fill="#1F2933", font=title_font)
    draw.line((left, top - 10, left, bottom + 10), fill="#D0D7DE", width=1)
    draw.line((left, bottom + 10, right, bottom + 10), fill="#D0D7DE", width=1)

    for idx, (label, value) in enumerate(zip(labels, values)):
        y = top + idx * (bar_height + bar_gap)
        bar_width = int(value * scale) if scale else 0
        draw.text((40, y + max(0, bar_height // 2 - 7)), _truncate(label), fill="#334155", font=text_font)
        draw.rectangle((left, y, left + bar_width, y + bar_height), fill=color)
        value_label = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
        draw.text((left + bar_width + 8, y + max(0, bar_height // 2 - 7)), value_label, fill="#334155", font=text_font)

    draw.text((left, height - 45), x_label, fill="#334155", font=text_font)
    return image


def plot_missing_values(df: pd.DataFrame, top_n: int = 20) -> Image.Image:
    """Plot the columns with the highest missing-value percentages."""
    missing_pct = (df.isna().mean().sort_values(ascending=False).head(top_n) * 100).sort_values()
    return _bar_chart(
        labels=missing_pct.index.tolist(),
        values=missing_pct.round(2).tolist(),
        title=f"Top {top_n} Columns by Missing Values",
        x_label="Missing values (%)",
        color="#5B8DEF",
    )


def plot_target_distribution(df: pd.DataFrame, target_col: str = "default_flag") -> Image.Image:
    """Plot the binary target distribution."""
    counts = df[target_col].value_counts(dropna=False).sort_index()
    labels = ["Non-default" if value == 0 else "Default" if value == 1 else value for value in counts.index]
    return _bar_chart(
        labels=labels,
        values=counts.astype(int).tolist(),
        title="Target Distribution",
        x_label="Row count",
        color="#2CA58D",
        height=360,
    )


def plot_default_rate_by_category(
    df: pd.DataFrame,
    category_col: str,
    target_col: str = "default_flag",
    top_n: int = 20,
) -> Image.Image:
    """Plot default rate by a categorical feature."""
    grouped = (
        df.groupby(category_col, dropna=False)[target_col]
        .agg(default_rate="mean", row_count="size")
        .sort_values("row_count", ascending=False)
        .head(top_n)
        .sort_values("default_rate")
    )
    rates = (grouped["default_rate"] * 100).round(2)
    return _bar_chart(
        labels=rates.index.tolist(),
        values=rates.tolist(),
        title=f"Default Rate by {category_col}",
        x_label="Default rate (%)",
        color="#F2B134",
    )


def plot_numeric_distribution(df: pd.DataFrame, numeric_col: str, bins: int = 40) -> Image.Image:
    """Plot a numeric feature distribution."""
    values = pd.to_numeric(df[numeric_col], errors="coerce").dropna()
    if values.empty:
        labels: list[str] = []
        counts: list[int] = []
    else:
        binned = pd.cut(values, bins=bins, duplicates="drop")
        counts_series = binned.value_counts(sort=False)
        labels = [f"{interval.left:.1f} to {interval.right:.1f}" for interval in counts_series.index]
        counts = counts_series.astype(int).tolist()
    return _bar_chart(
        labels=labels,
        values=counts,
        title=f"Distribution of {numeric_col}",
        x_label="Row count",
        color="#6C757D",
    )
