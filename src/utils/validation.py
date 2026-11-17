"""Cross-validation splitter and evaluation utilities for Home Credit Default Risk.

Sprint 1 Task S1-T1:
- Deterministic 5-fold Stratified K-Fold CV splitter
- Zero-overlap guarantee across folds and 100% dataset coverage
- Stratification preserving the ~8.07% target default rate across all folds
- Out-of-Fold (OOF) ROC-AUC calculation with optional bootstrap confidence interval
"""

from __future__ import annotations

import logging
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

logger = logging.getLogger(__name__)


def get_stratified_folds(
    df: pd.DataFrame,
    target_col: str = "TARGET",
    n_splits: int = 5,
    seed: int = 42,
) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Generates deterministic stratified cross-validation folds.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset containing features and the target column.
    target_col : str, default="TARGET"
        Name of the binary target column.
    n_splits : int, default=5
        Number of cross-validation folds.
    seed : int, default=42
        Random seed for shuffling to ensure strict reproducibility.

    Returns
    -------
    List[Tuple[np.ndarray, np.ndarray]]
        List of (train_indices, val_indices) numpy integer arrays for each fold.

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
    ValueError
        If df is empty, n_splits < 2, n_splits > len(df), or target has < 2 classes.
    KeyError
        If target_col is missing from df.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if len(df) == 0:
        raise ValueError("DataFrame is empty; cannot generate folds.")

    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame columns.")

    if n_splits < 2:
        raise ValueError(f"n_splits must be at least 2, got {n_splits}.")

    if n_splits > len(df):
        raise ValueError(
            f"n_splits cannot exceed number of samples ({len(df)}), got {n_splits}."
        )

    target_values = df[target_col].to_numpy()
    unique_classes = np.unique(target_values[~pd.isna(target_values)])
    if len(unique_classes) < 2:
        raise ValueError(
            f"Target column must contain at least 2 distinct classes, found: {unique_classes.tolist()}"
        )

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    folds: List[Tuple[np.ndarray, np.ndarray]] = []

    # X can be a dummy array since StratifiedKFold only uses y for stratifying
    dummy_x = np.zeros(len(df), dtype=np.int8)

    for fold_idx, (train_idx, val_idx) in enumerate(skf.split(dummy_x, target_values)):
        train_idx = np.asarray(train_idx, dtype=np.int64)
        val_idx = np.asarray(val_idx, dtype=np.int64)
        folds.append((train_idx, val_idx))

    logger.info(
        "Generated %d stratified folds (seed=%d, samples=%d, target_mean=%.5f)",
        n_splits,
        seed,
        len(df),
        float(np.mean(target_values)),
    )
    return folds


def compute_oof_roc_auc_ci(
    y_true: Union[np.ndarray, pd.Series, list],
    y_pred: Union[np.ndarray, pd.Series, list],
    ci_level: float = 0.95,
    n_bootstraps: int = 1000,
    seed: int = 42,
) -> Tuple[float, float, float]:
    """Computes OOF ROC-AUC along with bootstrap percentile confidence intervals.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary target values.
    y_pred : array-like of shape (n_samples,)
        Predicted probabilities or decision scores for the positive class.
    ci_level : float, default=0.95
        Confidence level for the two-sided confidence interval (e.g., 0.95 for 95% CI).
    n_bootstraps : int, default=1000
        Number of bootstrap iterations for estimating CI bounds.
    seed : int, default=42
        Random seed for the bootstrap generator.

    Returns
    -------
    Tuple[float, float, float]
        (point_estimate_auc, ci_lower, ci_upper)
    """
    y_t = _validate_and_sanitize_inputs(y_true, y_pred)
    y_p = np.asarray(y_pred, dtype=np.float64).ravel()

    if not (0.0 < ci_level < 1.0):
        raise ValueError(f"ci_level must be strictly between 0 and 1, got {ci_level}.")

    if n_bootstraps < 1:
        raise ValueError(f"n_bootstraps must be >= 1, got {n_bootstraps}.")

    point_auc = float(roc_auc_score(y_t, y_p))

    rng = np.random.default_rng(seed)
    n_samples = len(y_t)
    bootstrapped_scores: List[float] = []

    # Perform bootstrap sampling
    attempts = 0
    max_attempts = n_bootstraps * 3
    while len(bootstrapped_scores) < n_bootstraps and attempts < max_attempts:
        attempts += 1
        indices = rng.integers(0, n_samples, size=n_samples)
        sample_y_true = y_t[indices]
        if len(np.unique(sample_y_true)) < 2:
            continue
        sample_auc = float(roc_auc_score(sample_y_true, y_p[indices]))
        bootstrapped_scores.append(sample_auc)

    if len(bootstrapped_scores) < n_bootstraps:
        # Fallback if too many degenerate samples
        ci_lower = point_auc
        ci_upper = point_auc
    else:
        alpha = (1.0 - ci_level) / 2.0
        lower_pct = alpha * 100.0
        upper_pct = (1.0 - alpha) * 100.0
        ci_lower = float(np.percentile(bootstrapped_scores, lower_pct))
        ci_upper = float(np.percentile(bootstrapped_scores, upper_pct))

    return point_auc, ci_lower, ci_upper


def compute_oof_roc_auc(
    y_true: Union[np.ndarray, pd.Series, list],
    y_pred: Union[np.ndarray, pd.Series, list],
    return_ci: bool = False,
    ci_level: float = 0.95,
    n_bootstraps: int = 1000,
    seed: int = 42,
) -> Union[float, Tuple[float, Tuple[float, float]]]:
    """Computes the Out-of-Fold ROC-AUC metric and optional confidence interval.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary target labels.
    y_pred : array-like of shape (n_samples,)
        Predicted probabilities for the positive class (TARGET=1).
    return_ci : bool, default=False
        If True, returns (auc, (ci_lower, ci_upper)). If False, returns float auc.
    ci_level : float, default=0.95
        Confidence level for bootstrap confidence interval.
    n_bootstraps : int, default=1000
        Number of bootstrap samples.
    seed : int, default=42
        Seed for reproducibility.

    Returns
    -------
    Union[float, Tuple[float, Tuple[float, float]]]
        Float ROC-AUC score, or tuple of (score, (ci_lower, ci_upper)).
    """
    y_t = _validate_and_sanitize_inputs(y_true, y_pred)
    y_p = np.asarray(y_pred, dtype=np.float64).ravel()

    if not return_ci:
        return float(roc_auc_score(y_t, y_p))

    auc, ci_lower, ci_upper = compute_oof_roc_auc_ci(
        y_t,
        y_p,
        ci_level=ci_level,
        n_bootstraps=n_bootstraps,
        seed=seed,
    )
    return auc, (ci_lower, ci_upper)


def _validate_and_sanitize_inputs(
    y_true: Union[np.ndarray, pd.Series, list],
    y_pred: Union[np.ndarray, pd.Series, list],
) -> np.ndarray:
    """Validates y_true and y_pred shapes, types, and values."""
    if isinstance(y_true, (pd.Series, pd.Index)):
        y_t = y_true.to_numpy()
    else:
        y_t = np.asarray(y_true)

    if isinstance(y_pred, (pd.Series, pd.Index)):
        y_p = y_pred.to_numpy()
    else:
        y_p = np.asarray(y_pred)

    y_t = y_t.ravel()
    y_p = y_p.ravel()

    if len(y_t) != len(y_p):
        raise ValueError(
            f"Length mismatch: len(y_true)={len(y_t)} != len(y_pred)={len(y_p)}"
        )

    if len(y_t) == 0:
        raise ValueError("Inputs cannot be empty.")

    if np.isnan(y_t).any() or np.isinf(y_t).any():
        raise ValueError("y_true contains NaN or Inf values.")

    if np.isnan(y_p).any() or np.isinf(y_p).any():
        raise ValueError("y_pred contains NaN or Inf values.")

    unique_classes = np.unique(y_t)
    if len(unique_classes) < 2:
        raise ValueError(
            f"y_true must contain at least 2 distinct classes, found: {unique_classes.tolist()}"
        )

    return y_t
