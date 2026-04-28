"""Baseline forecasting utilities for monthly Philippines inflation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class RegressionForecastModel:
    """Small prediction wrapper for linear regression forecasts."""

    model_type: str
    intercept: float
    coefficients: np.ndarray
    feature_cols: list[str]
    estimator: object | None = None

    def predict(self, X):
        """Predict using either a fitted sklearn estimator or NumPy coefficients."""
        X_df = pd.DataFrame(X, columns=self.feature_cols)
        if self.estimator is not None:
            return np.asarray(self.estimator.predict(X_df))
        values = X_df.to_numpy(dtype=float)
        return self.intercept + values @ self.coefficients


def load_monthly_indicators(path):
    """Load the processed monthly macro indicator table."""
    df = pd.read_csv(Path(path))
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
    return df


def create_forecast_target(df, target_col="inflation_rate", horizon=1):
    """Create a one-step-ahead target by shifting the target backward."""
    if target_col not in df.columns:
        raise KeyError(f"Missing target column: {target_col}")
    output = df.copy()
    forecast_target_col = (
        f"inflation_target_{horizon}m"
        if target_col == "inflation_rate"
        else f"{target_col}_target_{horizon}m"
    )
    output[forecast_target_col] = output[target_col].shift(-horizon)
    if "date" in output.columns:
        output["target_date"] = output["date"].shift(-horizon)
    return output


def chronological_train_test_split(df, test_size=0.2):
    """Split a time-ordered dataset by assigning the final rows to the test set."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")
    if len(df) < 5:
        raise ValueError("At least five observations are required for a time split.")
    split_index = int(np.floor(len(df) * (1 - test_size)))
    split_index = min(max(split_index, 1), len(df) - 1)
    train = df.iloc[:split_index].copy()
    test = df.iloc[split_index:].copy()
    return train, test


def naive_last_value_forecast(train, test, target_col="inflation_rate"):
    """Forecast next-month inflation using inflation observed at the forecast date."""
    if target_col not in train.columns or target_col not in test.columns:
        raise KeyError(f"Missing forecast origin column: {target_col}")
    return test[target_col].astype(float).to_numpy()


def moving_average_forecast(train, test, target_col="inflation_rate", window=3):
    """Forecast next-month inflation using a rolling average through the forecast date."""
    if target_col not in train.columns or target_col not in test.columns:
        raise KeyError(f"Missing forecast origin column: {target_col}")
    combined = pd.concat([train[[target_col]], test[[target_col]]], axis=0)
    rolling = combined[target_col].astype(float).rolling(window=window, min_periods=1).mean()
    return rolling.loc[test.index].to_numpy()


def regression_forecast(train, test, feature_cols, target_col="inflation_target_1m"):
    """Fit a simple linear regression model and return test predictions plus model."""
    if not feature_cols:
        raise ValueError("At least one usable feature is required for regression.")

    train_model = train.dropna(subset=[target_col, *feature_cols]).copy()
    test_model = test.dropna(subset=feature_cols).copy()
    if train_model.empty or test_model.empty:
        raise ValueError("Regression data is empty after dropping missing values.")

    X_train = train_model[feature_cols].astype(float)
    y_train = train_model[target_col].astype(float)
    X_test = test_model[feature_cols].astype(float)

    try:
        from sklearn.linear_model import LinearRegression

        estimator = LinearRegression()
        estimator.fit(X_train, y_train)
        predictions = estimator.predict(X_test)
        model = RegressionForecastModel(
            model_type="sklearn_linear_regression",
            intercept=float(estimator.intercept_),
            coefficients=np.asarray(estimator.coef_, dtype=float),
            feature_cols=list(feature_cols),
            estimator=estimator,
        )
    except Exception:
        X = np.column_stack([np.ones(len(X_train)), X_train.to_numpy(dtype=float)])
        coefficients, *_ = np.linalg.lstsq(X, y_train.to_numpy(dtype=float), rcond=None)
        intercept = float(coefficients[0])
        betas = np.asarray(coefficients[1:], dtype=float)
        predictions = intercept + X_test.to_numpy(dtype=float) @ betas
        model = RegressionForecastModel(
            model_type="numpy_linear_regression",
            intercept=intercept,
            coefficients=betas,
            feature_cols=list(feature_cols),
            estimator=None,
        )

    prediction_series = pd.Series(predictions, index=test_model.index, name="prediction")
    return prediction_series, model


def evaluate_forecast(y_true, y_pred, reference=None):
    """Evaluate a forecast with error and optional direction metrics."""
    aligned = pd.concat(
        [
            pd.Series(y_true, name="actual", dtype="float64"),
            pd.Series(y_pred, name="prediction", dtype="float64"),
        ],
        axis=1,
    ).dropna()
    if aligned.empty:
        raise ValueError("No aligned actual and predicted values are available.")

    errors = aligned["prediction"] - aligned["actual"]
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors**2)))

    nonzero_actual = aligned["actual"].abs() > 1e-12
    mape = np.nan
    if nonzero_actual.any():
        mape = float(
            np.mean(
                np.abs(
                    (aligned.loc[nonzero_actual, "actual"] - aligned.loc[nonzero_actual, "prediction"])
                    / aligned.loc[nonzero_actual, "actual"]
                )
            )
            * 100
        )

    directional_accuracy = np.nan
    if reference is not None:
        ref = pd.Series(reference, name="reference", dtype="float64")
        direction_df = pd.concat([aligned, ref], axis=1).dropna()
        direction_df = direction_df[direction_df["actual"].ne(direction_df["reference"])]
        if not direction_df.empty:
            actual_direction = np.sign(direction_df["actual"] - direction_df["reference"])
            predicted_direction = np.sign(direction_df["prediction"] - direction_df["reference"])
            directional_accuracy = float((actual_direction == predicted_direction).mean())

    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "directional_accuracy": directional_accuracy,
    }


def build_forecast_comparison(results):
    """Convert a dictionary of forecast metrics into a comparison table."""
    rows = []
    for model_name, metrics in results.items():
        row = {"model": model_name}
        row.update(metrics)
        rows.append(row)
    return pd.DataFrame(rows)


def create_next_month_forecast(model, latest_row, feature_cols):
    """Create a one-month-ahead forecast from the latest available feature row."""
    if not feature_cols:
        raise ValueError("At least one feature is required for the next-month forecast.")
    latest = pd.DataFrame([latest_row[feature_cols]], columns=feature_cols).astype(float)
    return float(model.predict(latest)[0])
