"""Data cleaner and anomaly handling module.

Implements Sprint 0 Task S0-T2:
- Detects DAYS_EMPLOYED == 365243 sentinel
- Replaces sentinel with np.nan
- Adds DAYS_EMPLOYED_ANOM flag (int8)
- Guarantees zero leakage across train and test splits
"""

from __future__ import annotations

import logging
from typing import Union
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

ANOMALY_SENTINEL_DAYS_EMPLOYED: int = 365_243


def clean_anomalies(
    df: pd.DataFrame,
    target_col: str = "DAYS_EMPLOYED",
    anom_col: str = "DAYS_EMPLOYED_ANOM",
    sentinel_val: Union[int, float] = ANOMALY_SENTINEL_DAYS_EMPLOYED,
    copy: bool = True,
) -> pd.DataFrame:
    """Replaces DAYS_EMPLOYED sentinel values with np.nan and creates an indicator flag.

    In Home Credit data, 365,243 days in employment is a known sentinel value representing
    unemployed, retired, or anomalous employment status (~18% of observations).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the target column.
    target_col : str, default 'DAYS_EMPLOYED'
        Name of the column containing sentinel values.
    anom_col : str, default 'DAYS_EMPLOYED_ANOM'
        Name of the indicator column to create.
    sentinel_val : int | float, default 365243
        Sentinel value representing anomaly/missing employment.
    copy : bool, default True
        Whether to copy df before modification.

    Returns
    -------
    pd.DataFrame
        DataFrame with sentinel values replaced by np.nan and anom_col added (int8).

    Raises
    ------
    KeyError
        If target_col is not present in df.
    """
    if target_col not in df.columns:
        raise KeyError(f"Column '{target_col}' not found in DataFrame.")

    if copy:
        df = df.copy()

    # Identify sentinel rows (NaNs evaluate to False)
    is_anom = df[target_col] == sentinel_val

    # Create binary indicator flag with int8 dtype
    df[anom_col] = is_anom.astype(np.int8)

    # Replace sentinel with np.nan and maintain float32 dtype
    df[target_col] = df[target_col].replace({sentinel_val: np.nan}).astype(np.float32)

    logger.debug(
        "Replaced %d occurrences of sentinel %s in '%s'. Added flag '%s'.",
        int(is_anom.sum()),
        sentinel_val,
        target_col,
        anom_col,
    )
    return df
