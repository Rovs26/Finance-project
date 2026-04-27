"""Reusable modeling utilities for baseline probability of default modeling."""

from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def split_train_test(X, y, test_size: float = 0.2, random_state: int = 42):
    """Split feature matrix and target into stratified train and test samples."""
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def _build_one_hot_encoder() -> OneHotEncoder:
    """Create a OneHotEncoder across supported scikit-learn versions."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_logistic_regression_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
) -> Pipeline:
    """Build a preprocessing and logistic regression PD pipeline."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", _build_one_hot_encoder()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )
    classifier = LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        solver="lbfgs",
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def train_model(model, X_train, y_train):
    """Fit and return a scikit-learn model."""
    return model.fit(X_train, y_train)


def evaluate_binary_classifier(model, X_test, y_test) -> dict:
    """Evaluate a binary classifier using probability and class metrics."""
    y_pred = model.predict(X_test)
    y_score = generate_pd_scores(model, X_test)
    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    return {
        "roc_auc": roc_auc_score(y_test, y_score),
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
        "fpr": fpr,
        "tpr": tpr,
        "thresholds": thresholds,
    }


def generate_pd_scores(model, X):
    """Generate probability of default scores for the positive class."""
    return model.predict_proba(X)[:, 1]


def save_model(model, path: str | Path) -> Path:
    """Persist a fitted model artifact with joblib."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


def load_model(path: str | Path):
    """Load a persisted model artifact with joblib."""
    return joblib.load(path)
