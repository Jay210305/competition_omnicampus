"""Unit tests for data cleaner and anomaly handler (Sprint 0 Task S0-T2).

Validates:
- Detection and replacement of DAYS_EMPLOYED == 365243 sentinel with np.nan
- Creation of DAYS_EMPLOYED_ANOM binary indicator flag with dtype int8
- Preservation of normal negative DAYS_EMPLOYED values
- Handling edge cases (no anomalies, all anomalies, existing NaNs)
- Integration with real competition train and test datasets
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.data.cleaner import clean_anomalies, ANOMALY_SENTINEL_DAYS_EMPLOYED
from src.data.loader import load_data


class TestCleanerUnit:
    """Unit tests using controlled synthetic data."""

    def test_clean_anomalies_basic(self):
        """Replaces sentinel with np.nan and adds int8 DAYS_EMPLOYED_ANOM indicator."""
        df = pd.DataFrame({
            "SK_ID_CURR": [1, 2, 3, 4],
            "DAYS_EMPLOYED": [-1200, 365243, -450, 365243],
        })

        cleaned = clean_anomalies(df)

        # Invariants
        assert "DAYS_EMPLOYED_ANOM" in cleaned.columns
        assert cleaned["DAYS_EMPLOYED_ANOM"].dtype == np.int8
        assert cleaned["DAYS_EMPLOYED"].dtype == np.float32

        # Anomaly flag checks
        np.testing.assert_array_equal(cleaned["DAYS_EMPLOYED_ANOM"].values, [0, 1, 0, 1])

        # Value checks: 365243 must be completely gone
        assert (cleaned["DAYS_EMPLOYED"] == ANOMALY_SENTINEL_DAYS_EMPLOYED).sum() == 0
        assert cleaned["DAYS_EMPLOYED"].isna().sum() == 2
        np.testing.assert_allclose(cleaned["DAYS_EMPLOYED"].dropna().values, [-1200.0, -450.0])

    def test_clean_anomalies_no_anomalies(self):
        """When no anomalies are present, DAYS_EMPLOYED_ANOM is all zeros."""
        df = pd.DataFrame({
            "DAYS_EMPLOYED": [-3000, -1500, -200],
        })
        cleaned = clean_anomalies(df)

        assert (cleaned["DAYS_EMPLOYED_ANOM"] == 0).all()
        assert cleaned["DAYS_EMPLOYED"].isna().sum() == 0
        np.testing.assert_allclose(cleaned["DAYS_EMPLOYED"].values, [-3000.0, -1500.0, -200.0])

    def test_clean_anomalies_all_anomalies(self):
        """When all rows have sentinel, DAYS_EMPLOYED_ANOM is all ones and DAYS_EMPLOYED is all NaN."""
        df = pd.DataFrame({
            "DAYS_EMPLOYED": [365243, 365243, 365243],
        })
        cleaned = clean_anomalies(df)

        assert (cleaned["DAYS_EMPLOYED_ANOM"] == 1).all()
        assert cleaned["DAYS_EMPLOYED"].isna().sum() == 3

    def test_clean_anomalies_preserves_existing_nans(self):
        """Pre-existing NaNs should remain NaN and have DAYS_EMPLOYED_ANOM == 0."""
        df = pd.DataFrame({
            "DAYS_EMPLOYED": [-500.0, np.nan, 365243.0],
        })
        cleaned = clean_anomalies(df)

        np.testing.assert_array_equal(cleaned["DAYS_EMPLOYED_ANOM"].values, [0, 0, 1])
        assert cleaned["DAYS_EMPLOYED"].isna().sum() == 2
        assert cleaned.loc[0, "DAYS_EMPLOYED"] == -500.0

    def test_missing_days_employed_column_raises_error(self):
        """Raises KeyError if DAYS_EMPLOYED column is absent."""
        df = pd.DataFrame({"AMT_INCOME_TOTAL": [100000.0]})
        with pytest.raises(KeyError, match="DAYS_EMPLOYED"):
            clean_anomalies(df)

    def test_immutability_copy(self):
        """Ensure original dataframe is not mutated when copy=True (default)."""
        original = pd.DataFrame({"DAYS_EMPLOYED": [365243, -100]})
        copy_original = original.copy()

        cleaned = clean_anomalies(original, copy=True)

        pd.testing.assert_frame_equal(original, copy_original)
        assert "DAYS_EMPLOYED_ANOM" not in original.columns


class TestCleanerRealData:
    """Integration test with real dataset to verify exact anomaly counts."""

    @pytest.mark.skipif(not Path("input/train.csv").exists(), reason="input/train.csv missing")
    def test_clean_real_datasets(self):
        """Verifies anomaly detection and replacement on actual train and test datasets."""
        train_df, test_df = load_data("input/train.csv", "input/test.csv")

        # Counts before cleaning
        train_anom_count_pre = (train_df["DAYS_EMPLOYED"] == 365243).sum()
        test_anom_count_pre = (test_df["DAYS_EMPLOYED"] == 365243).sum()

        assert train_anom_count_pre == 30_898, f"Expected 30,898 anomalies in train, found {train_anom_count_pre}"
        assert test_anom_count_pre == 10_565, f"Expected 10,565 anomalies in test, found {test_anom_count_pre}"

        # Clean datasets
        clean_train = clean_anomalies(train_df)
        clean_test = clean_anomalies(test_df)

        # Zero occurrences after cleaning
        assert (clean_train["DAYS_EMPLOYED"] == 365243).sum() == 0
        assert (clean_test["DAYS_EMPLOYED"] == 365243).sum() == 0

        # Exact flag counts match pre-cleaning counts
        assert clean_train["DAYS_EMPLOYED_ANOM"].sum() == 30_898
        assert clean_test["DAYS_EMPLOYED_ANOM"].sum() == 10_565
        assert clean_train["DAYS_EMPLOYED_ANOM"].dtype == np.int8
        assert clean_test["DAYS_EMPLOYED_ANOM"].dtype == np.int8

        # Cleaned column is float32
        assert clean_train["DAYS_EMPLOYED"].dtype == np.float32
        assert clean_test["DAYS_EMPLOYED"].dtype == np.float32

        # Preserves all other columns and row counts
        assert len(clean_train) == len(train_df)
        assert len(clean_test) == len(test_df)
        assert clean_train.shape[1] == train_df.shape[1] + 1
        assert clean_test.shape[1] == test_df.shape[1] + 1
