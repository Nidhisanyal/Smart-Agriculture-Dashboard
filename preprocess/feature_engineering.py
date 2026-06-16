# preprocess/feature_engineering.py
"""Feature engineering utilities for the Smart Agriculture Intelligence System.

This module provides functions to transform raw data from weather, soil, and market sources into
features suitable for machine‑learning models. Each function takes a pandas DataFrame and returns
a new DataFrame with added columns.
"""

import pandas as pd

def add_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived weather features.

    Expected columns: ['temp', 'humidity', 'wind_speed', 'rain']
    Adds:
        - 'temp_celsius' (if needed)
        - 'is_rainy' (binary)
        - 'wind_category' (low/medium/high)
    """
    df = df.copy()
    # Example conversion placeholder
    if 'temp' in df.columns:
        df['temp_celsius'] = df['temp'] - 273.15  # Kelvin to Celsius if needed
    if 'rain' in df.columns:
        df['is_rainy'] = (df['rain'] > 0).astype(int)
    if 'wind_speed' in df.columns:
        bins = [-1, 5, 15, 30, 100]
        labels = ['low', 'medium', 'high', 'extreme']
        df['wind_category'] = pd.cut(df['wind_speed'], bins=bins, labels=labels)
    return df

def add_soil_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived soil features.

    Expected columns: ['pH', 'nitrogen', 'phosphorus', 'potassium']
    Adds:
        - 'soil_fertility_score' (simple heuristic)
    """
    df = df.copy()
    if all(col in df.columns for col in ['nitrogen', 'phosphorus', 'potassium']):
        df['soil_fertility_score'] = (df['nitrogen'] + df['phosphorus'] + df['potassium']) / 3
    return df

def add_market_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived market features.

    Expected columns: ['price', 'volume']
    Adds:
        - 'price_change_7d' (placeholder for future implementation)
    """
    df = df.copy()
    # Placeholder: actual calculation would need historical data
    df['price_change_7d'] = 0.0
    return df

def engineer_features(weather_df: pd.DataFrame, soil_df: pd.DataFrame, market_df: pd.DataFrame) -> pd.DataFrame:
    """Combine all raw data sources and apply feature engineering.

    Returns a single DataFrame ready for model training/prediction.
    """
    df = pd.concat([weather_df, soil_df, market_df], axis=1)
    df = add_weather_features(df)
    df = add_soil_features(df)
    df = add_market_features(df)
    return df
