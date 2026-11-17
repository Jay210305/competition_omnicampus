"""Unit tests for data loader and schema auditor (Sprint 0 Task S0-T1).

Validates:
- Loading train and test datasets from CSV
- File existence and error handling (FileNotFoundError)
- Schema and column validation (ValueError on missing required columns)
- Strict shape validation
- Memory optimization (float64 -> float32, int64 -> int32)
- Missingness audit function
- Real dataset dimensions and benchmark (< 5s)
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.data.loader import (
    EXPECTED_TRAIN_ROWS,
    EXPECTED_TRAIN_COLS,
    EXPECTED_TEST_ROWS,
    EXPECTED_TEST_COLS,
    REQUIRED_TRAIN_COLUMNS,
    REQUIRED_TEST_COLUMNS,
    load_data,
    optimize_dtypes,
    audit_missingness,
    validate_schema,
)


class TestDataLoaderUnit:
    """Unit tests using synthetic/fixture DataFrames."""

    def test_load_data_file_not_found(self, tmp_path):
        """Raises FileNotFoundError if train or test file does not exist."""
        non_existent_train = str(tmp_path / "non_existent_train.csv")
        non_existent_test = str(tmp_path / "non_existent_test.csv")

        with pytest.raises(FileNotFoundError):
            load_data(non_existent_train, non_existent_test)

        # Create valid train but invalid test
        train_file = tmp_path / "valid_train.csv"
        pd.DataFrame({"SK_ID_CURR": [1], "TARGET": [0]}).to_csv(train_file, index=False)
        with pytest.raises(FileNotFoundError):
            load_data(str(train_file), non_existent_test)

    def test_schema_missing_target_in_train(self, tmp_path):
        """Raises ValueError when train dataset is missing TARGET column."""
        train_file = tmp_path / "train_no_target.csv"
        test_file = tmp_path / "test.csv"
        pd.DataFrame({"SK_ID_CURR": [1, 2], "AMT_CREDIT": [100.0, 200.0]}).to_csv(train_file, index=False)
        pd.DataFrame({"SK_ID_CURR": [3, 4], "AMT_CREDIT": [300.0, 400.0]}).to_csv(test_file, index=False)

        with pytest.raises(ValueError, match="TARGET"):
            load_data(str(train_file), str(test_file))

    def test_schema_missing_sk_id_curr(self, tmp_path):
        """Raises ValueError when SK_ID_CURR is missing in train or test."""
        train_file = tmp_path / "train_no_id.csv"
        test_file = tmp_path / "test_no_id.csv"
        pd.DataFrame({"TARGET": [0, 1], "AMT_CREDIT": [100.0, 200.0]}).to_csv(train_file, index=False)
        pd.DataFrame({"AMT_CREDIT": [300.0, 400.0]}).to_csv(test_file, index=False)

        with pytest.raises(ValueError, match="SK_ID_CURR"):
            load_data(str(train_file), str(test_file))

    def test_schema_test_has_target_leak(self, tmp_path):
        """Raises ValueError when test dataset unexpectedly contains TARGET column."""
        train_file = tmp_path / "train.csv"
        test_file = tmp_path / "test_leaked.csv"
        pd.DataFrame({"SK_ID_CURR": [1], "TARGET": [0]}).to_csv(train_file, index=False)
        pd.DataFrame({"SK_ID_CURR": [2], "TARGET": [1]}).to_csv(test_file, index=False)

        with pytest.raises(ValueError, match="leak|TARGET"):
            load_data(str(train_file), str(test_file))

    def test_strict_shape_validation_mismatch(self, tmp_path):
        """Raises ValueError when strict_shape=True and row/column count differs from expected."""
        train_file = tmp_path / "train_small.csv"
        test_file = tmp_path / "test_small.csv"
        pd.DataFrame({"SK_ID_CURR": [1], "TARGET": [0]}).to_csv(train_file, index=False)
        pd.DataFrame({"SK_ID_CURR": [2]}).to_csv(test_file, index=False)

        with pytest.raises(ValueError, match="dimension|shape|row|column"):
            load_data(str(train_file), str(test_file), strict_shape=True)

    def test_optimize_dtypes(self):
        """Validates that float64 is cast to float32 and int64 is cast to int32."""
        df = pd.DataFrame({
            "id": np.array([1, 2, 3], dtype=np.int64),
            "amount": np.array([10.5, 20.3, 30.1], dtype=np.float64),
            "category": ["A", "B", "C"],
            "flag": np.array([1, 0, 1], dtype=np.int64),
        })

        optimized = optimize_dtypes(df)

        assert optimized["id"].dtype == np.int32
        assert optimized["amount"].dtype == np.float32
        assert optimized["flag"].dtype == np.int32
        assert pd.api.types.is_string_dtype(optimized["category"]) or optimized["category"].dtype == object
        # Ensure values are preserved
        np.testing.assert_allclose(optimized["amount"], [10.5, 20.3, 30.1], rtol=1e-5)
        np.testing.assert_array_equal(optimized["id"], [1, 2, 3])

    def test_audit_missingness(self):
        """Validates missingness audit calculations and sorting."""
        df = pd.DataFrame({
            "col_full": [1, 2, 3, 4],
            "col_half_null": [1.0, np.nan, 3.0, np.nan],
            "col_all_null": [np.nan, np.nan, np.nan, np.nan],
            "col_one_null": [1, 2, 3, np.nan],
        })

        audit = audit_missingness(df)

        assert list(audit.columns) == ["column", "null_count", "null_percentage", "dtype"]
        assert len(audit) == 4
        # Sorted by null_percentage descending
        assert audit.iloc[0]["column"] == "col_all_null"
        assert audit.iloc[0]["null_count"] == 4
        assert audit.iloc[0]["null_percentage"] == 100.0

        assert audit.iloc[1]["column"] == "col_half_null"
        assert audit.iloc[1]["null_count"] == 2
        assert audit.iloc[1]["null_percentage"] == 50.0

        assert audit.iloc[2]["column"] == "col_one_null"
        assert audit.iloc[2]["null_count"] == 1
        assert audit.iloc[2]["null_percentage"] == 25.0

        assert audit.iloc[3]["column"] == "col_full"
        assert audit.iloc[3]["null_count"] == 0
        assert audit.iloc[3]["null_percentage"] == 0.0


class TestDataLoaderRealData:
    """Integration tests on actual competition dataset."""

    @pytest.mark.skipif(not Path("input/train.csv").exists(), reason="input/train.csv missing")
    def test_load_real_datasets(self):
        """Loads actual train.csv and test.csv and verifies contract requirements."""
        start = time.perf_counter()
        train, test = load_data("input/train.csv", "input/test.csv", strict_shape=True)
        elapsed = time.perf_counter() - start

        # Shapes
        assert len(train) == EXPECTED_TRAIN_ROWS, f"Expected {EXPECTED_TRAIN_ROWS}, got {len(train)}"
        assert train.shape[1] == EXPECTED_TRAIN_COLS, f"Expected {EXPECTED_TRAIN_COLS}, got {train.shape[1]}"
        assert len(test) == EXPECTED_TEST_ROWS, f"Expected {EXPECTED_TEST_ROWS}, got {len(test)}"
        assert test.shape[1] == EXPECTED_TEST_COLS, f"Expected {EXPECTED_TEST_COLS}, got {test.shape[1]}"

        # Contract columns
        assert "SK_ID_CURR" in train.columns
        assert "TARGET" in train.columns
        assert "SK_ID_CURR" in test.columns
        assert "TARGET" not in test.columns

        # Check default rate
        default_rate = train["TARGET"].mean()
        assert 0.080 <= default_rate <= 0.082, f"Target rate {default_rate:.4f} outside ~8.07% expectation"

        # Check memory optimization
        for col in train.select_dtypes(include=["floating"]).columns:
            assert train[col].dtype == np.float32, f"Column {col} is not float32: {train[col].dtype}"
        for col in train.select_dtypes(include=["integer"]).columns:
            assert train[col].dtype in (np.int32, np.int8), f"Column {col} is not int32/int8: {train[col].dtype}"

        # Performance requirement <= 5 seconds
        assert elapsed <= 5.0, f"Loading took {elapsed:.2f}s (> 5.0s limit)"
