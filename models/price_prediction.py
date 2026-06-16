"""Price forecasting utilities for Streamlit dashboard.

This module provides a simple Prophet-based forecasting helper
for historical commodity price data.
"""

import pandas as pd
from prophet import Prophet


def load_price_data(csv_path: str) -> pd.DataFrame:
    """Load historical price data from a CSV file.

    The CSV must contain columns `ds` and `y` for Prophet.
    """
    df = pd.read_csv(csv_path)
    if "ds" not in df.columns or "y" not in df.columns:
        raise ValueError("Price CSV must include 'ds' and 'y' columns.")
    df = df.copy()
    df["ds"] = pd.to_datetime(df["ds"])
    return df


def train_prophet(df: pd.DataFrame) -> Prophet:
    """Train a Prophet model on historical price data."""
    model = Prophet()
    model.fit(df)
    return model


def forecast(model: Prophet, periods: int = 30) -> pd.DataFrame:
    """Generate a future forecast for the given Prophe model."""
    future = model.make_future_dataframe(periods=periods)
    forecast_df = model.predict(future)
    return forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]]
