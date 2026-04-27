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


def plot_roc_curve(fpr, tpr, roc_auc: float) -> Image.Image:
    """Plot a ROC curve from false-positive and true-positive rates."""
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title_font = _font(22)
    text_font = _font(14)
    left, top, right, bottom = 90, 70, 730, 510

    draw.text((40, 25), f"ROC Curve (AUC = {roc_auc:.3f})", fill="#1F2933", font=title_font)
    draw.rectangle((left, top, right, bottom), outline="#D0D7DE", width=1)
    draw.line((left, bottom, right, top), fill="#CBD5E1", width=2)

    points = []
    for x_value, y_value in zip(fpr, tpr):
        x = left + float(x_value) * (right - left)
        y = bottom - float(y_value) * (bottom - top)
        points.append((x, y))
    if len(points) >= 2:
        draw.line(points, fill="#2563EB", width=3)

    draw.text((left, bottom + 25), "False positive rate", fill="#334155", font=text_font)
    draw.text((15, top), "True positive rate", fill="#334155", font=text_font)
    return image


def plot_confusion_matrix(confusion_values) -> Image.Image:
    """Plot a 2x2 confusion matrix."""
    values = confusion_values.tolist() if hasattr(confusion_values, "tolist") else confusion_values
    width, height = 620, 520
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title_font = _font(22)
    text_font = _font(16)
    value_font = _font(24)
    labels = [["TN", "FP"], ["FN", "TP"]]
    max_value = max(max(row) for row in values) if values else 1

    draw.text((40, 25), "Confusion Matrix", fill="#1F2933", font=title_font)
    cell_size = 150
    start_x, start_y = 170, 120
    for row in range(2):
        for col in range(2):
            value = values[row][col]
            intensity = int(240 - 140 * (value / max_value)) if max_value else 240
            color = (intensity, intensity + 10 if intensity < 245 else 245, 255)
            x0 = start_x + col * cell_size
            y0 = start_y + row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            draw.rectangle((x0, y0, x1, y1), fill=color, outline="#334155", width=2)
            draw.text((x0 + 50, y0 + 42), labels[row][col], fill="#1F2933", font=text_font)
            draw.text((x0 + 45, y0 + 80), f"{value:,}", fill="#1F2933", font=value_font)

    draw.text((start_x + 25, start_y - 35), "Predicted 0", fill="#334155", font=text_font)
    draw.text((start_x + cell_size + 25, start_y - 35), "Predicted 1", fill="#334155", font=text_font)
    draw.text((40, start_y + 55), "Actual 0", fill="#334155", font=text_font)
    draw.text((40, start_y + cell_size + 55), "Actual 1", fill="#334155", font=text_font)
    return image


def plot_pd_score_distribution(scores, bins: int = 30) -> Image.Image:
    """Plot a distribution of PD scores."""
    score_series = pd.Series(scores).dropna().clip(lower=0, upper=1)
    if score_series.empty:
        labels: list[str] = []
        counts: list[int] = []
    else:
        binned = pd.cut(score_series, bins=bins, include_lowest=True, duplicates="drop")
        counts_series = binned.value_counts(sort=False)
        labels = [f"{interval.left:.2f} to {interval.right:.2f}" for interval in counts_series.index]
        counts = counts_series.astype(int).tolist()
    return _bar_chart(
        labels=labels,
        values=counts,
        title="PD Score Distribution",
        x_label="Row count",
        color="#7C3AED",
    )


def plot_default_rate_by_score_band(
    df: pd.DataFrame,
    band_col: str = "pd_score_band",
    target_col: str = "default_flag",
) -> Image.Image:
    """Plot observed default rate by PD score band."""
    rates = (df.groupby(band_col, observed=False)[target_col].mean() * 100).round(2)
    return _bar_chart(
        labels=rates.index.tolist(),
        values=rates.tolist(),
        title="Observed Default Rate by PD Score Band",
        x_label="Default rate (%)",
        color="#DC2626",
        height=460,
    )


def plot_top_coefficients(coefficients: pd.DataFrame, top_n: int = 20) -> Image.Image:
    """Plot top coefficients by absolute magnitude."""
    if coefficients.empty:
        labels: list[str] = []
        values: list[float] = []
    else:
        top = coefficients.reindex(coefficients["coefficient"].abs().sort_values(ascending=False).index).head(top_n)
        top = top.sort_values("coefficient")
        labels = top["feature"].tolist()
        values = top["coefficient"].round(4).tolist()
    return _bar_chart(
        labels=labels,
        values=[abs(value) for value in values],
        title="Top Logistic Regression Coefficients",
        x_label="Absolute coefficient value",
        color="#0F766E",
    )
