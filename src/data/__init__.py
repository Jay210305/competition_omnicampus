"""Data processing package for Competition solution."""

from src.data.loader import (
    load_data,
    optimize_dtypes,
    audit_missingness,
    validate_schema,
    EXPECTED_TRAIN_ROWS,
    EXPECTED_TRAIN_COLS,
    EXPECTED_TEST_ROWS,
    EXPECTED_TEST_COLS,
    REQUIRED_TRAIN_COLUMNS,
    REQUIRED_TEST_COLUMNS,
)
from src.data.cleaner import (
    clean_anomalies,
    ANOMALY_SENTINEL_DAYS_EMPLOYED,
)

__all__ = [
    "load_data",
    "optimize_dtypes",
    "audit_missingness",
    "validate_schema",
    "clean_anomalies",
    "ANOMALY_SENTINEL_DAYS_EMPLOYED",
    "EXPECTED_TRAIN_ROWS",
    "EXPECTED_TRAIN_COLS",
    "EXPECTED_TEST_ROWS",
    "EXPECTED_TEST_COLS",
    "REQUIRED_TRAIN_COLUMNS",
    "REQUIRED_TEST_COLUMNS",
]
