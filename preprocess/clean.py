# preprocess/clean.py
"""Data cleaning utilities for the Smart Agriculture system.
Provides functions to handle missing values, outliers, and datatype casts.
"""
import pandas as pd
import numpy as np

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Perform basic cleaning on a DataFrame.
    Steps:
    - Fill missing numeric values with median.
    - Fill missing categorical values with mode.
    - Remove duplicate rows.
    - Clip extreme outliers to 1st and 99th percentiles.
    """
    df = df.copy()
    for col in df.select_dtypes(include=[np.number]).columns:
        median = df[col].median()
        df[col].fillna(median, inplace=True)
        lower, upper = df[col].quantile([0.01, 0.99])
        df[col] = np.clip(df[col], lower, upper)
    for col in df.select_dtypes(include=['object', 'category']).columns:
        mode = df[col].mode()[0] if not df[col].mode().empty else "unknown"
        df[col].fillna(mode, inplace=True)
    df.drop_duplicates(inplace=True)
    return df
