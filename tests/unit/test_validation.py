"""Unit tests for Stratified K-Fold CV splitter and OOF ROC-AUC evaluation.

Sprint 1 Task S1-T1:
- 5 stratified folds with fixed seed 42
- Identical target rate (~8.07% +/- 0.05%)
- Zero overlap within fold and across validation folds (100% data coverage)
- Deterministic behavior
- ROC-AUC evaluation with confidence intervals
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from src.utils.validation import (
    compute_oof_roc_auc,
    compute_oof_roc_auc_ci,
    get_stratified_folds,
)


@pytest.fixture
def synthetic_target_df():
    """Generates synthetic dataset of 10,000 samples with ~8.07% target rate.

    Matches Home Credit default rate distribution.
    """
    rng = np.random.default_rng(42)
    n_samples = 10_000
    n_pos = int(n_samples * 0.0807)  # 807 positives (~8.07%)
    targets = np.zeros(n_samples, dtype=int)
    pos_indices = rng.choice(n_samples, size=n_pos, replace=False)
    targets[pos_indices] = 1

    return pd.DataFrame({
        "SK_ID_CURR": np.arange(100_000, 100_000 + n_samples),
        "FEATURE_1": rng.standard_normal(n_samples),
        "TARGET": targets,
    })


class TestStratifiedFoldsSplitter:
    """Test suite for get_stratified_folds."""

    def test_fold_count(self, synthetic_target_df):
        """Must return exactly n_splits tuples (default 5)."""
        folds = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)
        assert len(folds) == 5, f"Expected 5 folds, got {len(folds)}"

    def test_determinism_with_same_seed(self, synthetic_target_df):
        """Identical seed must produce identical train and val index arrays."""
        folds_1 = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)
        folds_2 = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)

        for fold_idx, ((train_1, val_1), (train_2, val_2)) in enumerate(zip(folds_1, folds_2)):
            np.testing.assert_array_equal(
                train_1,
                train_2,
                err_msg=f"Train indices differ on fold {fold_idx} with identical seed.",
            )
            np.testing.assert_array_equal(
                val_1,
                val_2,
                err_msg=f"Val indices differ on fold {fold_idx} with identical seed.",
            )

    def test_different_seeds_produce_different_splits(self, synthetic_target_df):
        """Different seeds must yield different splits."""
        folds_42 = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)
        folds_99 = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=99)

        # At least one validation fold should differ
        has_difference = any(
            not np.array_equal(val_42, val_99)
            for (_, val_42), (_, val_99) in zip(folds_42, folds_99)
        )
        assert has_difference, "Different seeds should produce different splits."

    def test_zero_overlap_within_each_fold(self, synthetic_target_df):
        """Train and val sets within each fold must be mutually exclusive."""
        folds = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)

        for fold_idx, (train_idx, val_idx) in enumerate(folds):
            overlap = set(train_idx).intersection(set(val_idx))
            assert len(overlap) == 0, (
                f"Fold {fold_idx} has {len(overlap)} overlapping indices between train and val!"
            )
            assert len(train_idx) + len(val_idx) == len(synthetic_target_df), (
                f"Fold {fold_idx} train + val count does not match total DataFrame rows."
            )

    def test_total_coverage_and_zero_val_overlap_across_folds(self, synthetic_target_df):
        """The union of validation folds must cover exactly 100% of rows without overlap."""
        n_samples = len(synthetic_target_df)
        folds = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)

        seen_val_indices = []
        for fold_idx, (_, val_idx) in enumerate(folds):
            seen_val_indices.extend(val_idx.tolist())

        # Check total count
        assert len(seen_val_indices) == n_samples, (
            f"Total validation indices count ({len(seen_val_indices)}) != dataset size ({n_samples})"
        )

        # Check no duplicates across val folds
        unique_val_indices = set(seen_val_indices)
        assert len(unique_val_indices) == n_samples, (
            f"Validation folds contain duplicate indices across folds: {n_samples - len(unique_val_indices)} dupes"
        )

        # Check exact range coverage
        assert unique_val_indices == set(range(n_samples)), (
            "Validation indices do not cover the exact set of dataset positional indices [0..N-1]"
        )

    def test_stratification_target_rate_synthetic(self, synthetic_target_df):
        """Target rate across validation folds must not deviate by more than 0.05% (0.0005)."""
        folds = get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=5, seed=42)
        total_pos_rate = synthetic_target_df["TARGET"].mean()

        rates = []
        for fold_idx, (_, val_idx) in enumerate(folds):
            fold_val_rate = synthetic_target_df["TARGET"].iloc[val_idx].mean()
            rates.append(fold_val_rate)
            diff = abs(fold_val_rate - total_pos_rate)
            assert diff <= 0.0005, (
                f"Fold {fold_idx} target rate ({fold_val_rate:.5f}) deviates from total "
                f"({total_pos_rate:.5f}) by {diff:.5f} > 0.05% threshold!"
            )

        max_rate_diff = max(rates) - min(rates)
        assert max_rate_diff <= 0.0005 + 1e-7, (
            f"Max target rate difference between folds ({max_rate_diff:.5f}) exceeds 0.05%!"
        )

    def test_stratification_target_rate_real_train_data(self):
        """Verifies stratification on real input/train.csv (~171,202 rows, ~8.07% target)."""
        train_path = Path("input/train.csv")
        if not train_path.exists():
            pytest.skip("input/train.csv not found, skipping real data test.")

        # Read only TARGET column for speed
        df_target = pd.read_csv(train_path, usecols=["TARGET"])
        total_rate = df_target["TARGET"].mean()

        # Home Credit target rate is ~8.07%
        assert 0.075 <= total_rate <= 0.085, f"Expected target rate ~8.07%, got {total_rate:.4f}"

        folds = get_stratified_folds(df_target, target_col="TARGET", n_splits=5, seed=42)
        assert len(folds) == 5

        rates = []
        for fold_idx, (_, val_idx) in enumerate(folds):
            val_rate = df_target["TARGET"].iloc[val_idx].mean()
            rates.append(val_rate)
            diff = abs(val_rate - total_rate)
            assert diff <= 0.0005, (
                f"Real train fold {fold_idx} target rate ({val_rate:.5f}) differs from "
                f"dataset mean ({total_rate:.5f}) by {diff:.5f} > 0.05%!"
            )

        max_diff = max(rates) - min(rates)
        assert max_diff <= 0.0005, f"Real train max fold rate diff {max_diff:.5f} > 0.05%"

    def test_invalid_inputs_raise_errors(self, synthetic_target_df):
        """Contract violation tests for invalid inputs."""
        # Not a DataFrame
        with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
            get_stratified_folds([1, 2, 3], target_col="TARGET")

        # Empty DataFrame
        with pytest.raises(ValueError, match="DataFrame is empty"):
            get_stratified_folds(pd.DataFrame(), target_col="TARGET")

        # Missing target column
        with pytest.raises(KeyError, match="Target column 'NON_EXISTENT' not found"):
            get_stratified_folds(synthetic_target_df, target_col="NON_EXISTENT")

        # Invalid n_splits (< 2)
        with pytest.raises(ValueError, match="n_splits must be at least 2"):
            get_stratified_folds(synthetic_target_df, target_col="TARGET", n_splits=1)

        # n_splits greater than number of samples
        with pytest.raises(ValueError, match="n_splits cannot exceed number of samples"):
            get_stratified_folds(synthetic_target_df.head(3), target_col="TARGET", n_splits=5)

        # Single class in target column
        single_class_df = pd.DataFrame({"TARGET": [0, 0, 0, 0, 0]})
        with pytest.raises(ValueError, match="Target column must contain at least 2 distinct classes"):
            get_stratified_folds(single_class_df, target_col="TARGET", n_splits=2)


class TestOofRocAucMetric:
    """Test suite for compute_oof_roc_auc and confidence intervals."""

    def test_matches_sklearn_roc_auc_score(self):
        """Metric must match sklearn.metrics.roc_auc_score exactly."""
        rng = np.random.default_rng(42)
        y_true = rng.integers(0, 2, size=1000)
        y_pred = rng.uniform(0.0, 1.0, size=1000)

        expected_auc = roc_auc_score(y_true, y_pred)
        computed_auc = compute_oof_roc_auc(y_true, y_pred)

        assert isinstance(computed_auc, float)
        assert np.isclose(computed_auc, expected_auc, atol=1e-7)

    def test_perfect_and_worst_predictions(self):
        """Perfect predictions must yield 1.0; inverted must yield 0.0."""
        y_true = np.array([0, 0, 0, 1, 1, 1])
        y_perfect = np.array([0.1, 0.2, 0.3, 0.7, 0.8, 0.9])
        y_inverted = np.array([0.9, 0.8, 0.7, 0.3, 0.2, 0.1])

        assert np.isclose(compute_oof_roc_auc(y_true, y_perfect), 1.0)
        assert np.isclose(compute_oof_roc_auc(y_true, y_inverted), 0.0)

    def test_confidence_interval_computation(self):
        """Bootstrap CI must bracket the point estimate: ci_lower <= auc <= ci_upper."""
        rng = np.random.default_rng(42)
        y_true = rng.binomial(1, 0.2, size=1000)
        # Add informative signal
        y_pred = np.clip(y_true * 0.4 + rng.uniform(0.1, 0.5, size=1000), 0.0, 1.0)

        # Using return_ci=True
        auc, (ci_lower, ci_upper) = compute_oof_roc_auc(
            y_true, y_pred, return_ci=True, ci_level=0.95, n_bootstraps=200, seed=42
        )
        assert 0.0 <= ci_lower <= auc <= ci_upper <= 1.0
        assert ci_upper - ci_lower > 0

        # Using compute_oof_roc_auc_ci helper
        auc_res, ci_low, ci_high = compute_oof_roc_auc_ci(
            y_true, y_pred, ci_level=0.95, n_bootstraps=200, seed=42
        )
        assert np.isclose(auc, auc_res)
        assert np.isclose(ci_lower, ci_low)
        assert np.isclose(ci_upper, ci_high)

    def test_accepts_pandas_series_and_lists(self):
        """Must handle pandas.Series and Python lists seamlessly."""
        y_true_list = [0, 0, 1, 1]
        y_pred_list = [0.1, 0.2, 0.8, 0.9]

        auc_list = compute_oof_roc_auc(y_true_list, y_pred_list)
        auc_series = compute_oof_roc_auc(pd.Series(y_true_list), pd.Series(y_pred_list))
        auc_numpy = compute_oof_roc_auc(np.array(y_true_list), np.array(y_pred_list))

        assert np.isclose(auc_list, 1.0)
        assert np.isclose(auc_series, 1.0)
        assert np.isclose(auc_numpy, 1.0)

    def test_invalid_metric_inputs_raise_errors(self):
        """Must reject length mismatches, NaNs, missing classes, and invalid parameters."""
        # Length mismatch
        with pytest.raises(ValueError, match="Length mismatch"):
            compute_oof_roc_auc([0, 1], [0.5])

        # Single class
        with pytest.raises(ValueError, match="y_true must contain at least 2 distinct classes"):
            compute_oof_roc_auc([0, 0, 0], [0.1, 0.2, 0.3])

        # NaN values in y_true
        with pytest.raises(ValueError, match="NaN or Inf"):
            compute_oof_roc_auc([0, np.nan, 1], [0.1, 0.5, 0.9])

        # NaN values in y_pred
        with pytest.raises(ValueError, match="NaN or Inf"):
            compute_oof_roc_auc([0, 1, 1], [0.1, np.nan, 0.9])

        # Invalid ci_level
        with pytest.raises(ValueError, match="ci_level must be strictly between 0 and 1"):
            compute_oof_roc_auc([0, 1], [0.2, 0.8], return_ci=True, ci_level=1.5)

        # Invalid n_bootstraps
        with pytest.raises(ValueError, match="n_bootstraps must be >= 1"):
            compute_oof_roc_auc([0, 1], [0.2, 0.8], return_ci=True, n_bootstraps=0)
