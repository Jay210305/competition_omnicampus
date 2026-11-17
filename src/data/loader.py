"""Data loader and schema auditor module for Home Credit competition.

Implements Sprint 0 Task S0-T1:
- Efficient memory loading (float32, int32)
- Strict and flexible schema validation
- Missingness reporting per column
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

EXPECTED_TRAIN_ROWS: int = 171_202
EXPECTED_TRAIN_COLS: int = 34
EXPECTED_TEST_ROWS: int = 61_500
EXPECTED_TEST_COLS: int = 33

REQUIRED_COMMON_COLUMNS: list[str] = [
    "SK_ID_CURR",
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "CNT_CHILDREN",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "REGION_POPULATION_RELATIVE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "DAYS_REGISTRATION",
    "DAYS_ID_PUBLISH",
    "OWN_CAR_AGE",
    "FLAG_MOBIL",
    "FLAG_EMP_PHONE",
    "FLAG_WORK_PHONE",
    "OCCUPATION_TYPE",
    "CNT_FAM_MEMBERS",
    "REGION_RATING_CLIENT",
    "ORGANIZATION_TYPE",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "DAYS_LAST_PHONE_CHANGE",
    "AMT_REQ_CREDIT_BUREAU_HOUR",
    "AMT_REQ_CREDIT_BUREAU_MON",
    "AMT_REQ_CREDIT_BUREAU_QRT",
    "AMT_REQ_CREDIT_BUREAU_YEAR",
]

REQUIRED_TRAIN_COLUMNS: list[str] = REQUIRED_COMMON_COLUMNS + ["TARGET"]
REQUIRED_TEST_COLUMNS: list[str] = REQUIRED_COMMON_COLUMNS.copy()


def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Downcasts numeric columns to float32 and int32 to minimize memory usage.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to optimize.

    Returns
    -------
    pd.DataFrame
        Optimized DataFrame with reduced memory footprint.
    """
    df = df.copy()
    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = df[col].astype(np.float32)

    for col in df.select_dtypes(include=["int64"]).columns:
        df[col] = df[col].astype(np.int32)

    return df


def validate_schema(df: pd.DataFrame, is_train: bool = True, strict_shape: bool = False) -> None:
    """Validates schema and integrity constraints on train or test dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to validate.
    is_train : bool, default True
        Whether this is the training split.
    strict_shape : bool, default False
        Whether to enforce exact production row and column dimensions.

    Raises
    ------
    ValueError
        If schema invariants, required columns, or expected dimensions are violated.
    """
    dataset_name = "train" if is_train else "test"

    if df.empty:
        raise ValueError(f"{dataset_name} DataFrame is empty.")

    if "SK_ID_CURR" not in df.columns:
        raise ValueError(f"Required identifier column 'SK_ID_CURR' missing in {dataset_name} dataset.")

    if is_train:
        if "TARGET" not in df.columns:
            raise ValueError("Required target column 'TARGET' missing in train dataset.")
    else:
        if "TARGET" in df.columns:
            raise ValueError("Data leakage detected: 'TARGET' column present in test dataset.")

    if strict_shape:
        expected_rows = EXPECTED_TRAIN_ROWS if is_train else EXPECTED_TEST_ROWS
        expected_cols = EXPECTED_TRAIN_COLS if is_train else EXPECTED_TEST_COLS

        if len(df) != expected_rows or df.shape[1] != expected_cols:
            raise ValueError(
                f"Strict shape mismatch for {dataset_name}: expected ({expected_rows}, {expected_cols}), "
                f"found ({len(df)}, {df.shape[1]})."
            )

        required_cols = REQUIRED_TRAIN_COLUMNS if is_train else REQUIRED_TEST_COLUMNS
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns in {dataset_name}: {sorted(missing_cols)}")


def audit_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Computes missing value count, percentage, and dtype for each column.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to audit.

    Returns
    -------
    pd.DataFrame
        Table sorted by null percentage descending, with columns:
        ['column', 'null_count', 'null_percentage', 'dtype'].
    """
    total_rows = len(df)
    null_counts = df.isnull().sum()
    null_pct = (null_counts / total_rows * 100.0) if total_rows > 0 else 0.0

    audit_df = pd.DataFrame({
        "column": df.columns,
        "null_count": null_counts.values,
        "null_percentage": null_pct.values if hasattr(null_pct, "values") else [0.0] * len(df.columns),
        "dtype": [str(df[col].dtype) for col in df.columns],
    })

    return audit_df.sort_values(by="null_percentage", ascending=False).reset_index(drop=True)


def load_data(
    train_path: str = "input/train.csv",
    test_path: str = "input/test.csv",
    strict_shape: bool = False,
    optimize_memory: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads and validates train and test datasets from CSV files.

    Parameters
    ----------
    train_path : str, default 'input/train.csv'
        Path to train CSV file.
    test_path : str, default 'input/test.csv'
        Path to test CSV file.
    strict_shape : bool, default False
        Whether to enforce exact row and column dimensions.
    optimize_memory : bool, default True
        Whether to cast float64->float32 and int64->int32.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        Tuple of (train_df, test_df).

    Raises
    ------
    FileNotFoundError
        If either train or test file cannot be found.
    ValueError
        If schema invariants or required columns are violated.
    """
    train_p = Path(train_path)
    test_p = Path(test_path)

    if not train_p.is_file():
        raise FileNotFoundError(f"Train dataset file not found at: {train_path}")
    if not test_p.is_file():
        raise FileNotFoundError(f"Test dataset file not found at: {test_path}")

    logger.info("Reading train data from %s...", train_path)
    train_df = pd.read_csv(train_p)

    logger.info("Reading test data from %s...", test_path)
    test_df = pd.read_csv(test_p)

    validate_schema(train_df, is_train=True, strict_shape=strict_shape)
    validate_schema(test_df, is_train=False, strict_shape=strict_shape)

    if optimize_memory:
        logger.info("Optimizing memory footprint (float32, int32)...")
        train_df = optimize_dtypes(train_df)
        test_df = optimize_dtypes(test_df)

    logger.info(
        "Successfully loaded train shape %s and test shape %s.",
        train_df.shape,
        test_df.shape,
    )
    return train_df, test_df
