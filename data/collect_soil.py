# data/collect_soil.py
"""Collect soil data from a CSV file or API.
Provides a function `load_soil_data()` returning a pandas DataFrame.
"""

import pandas as pd
from . import config

def load_soil_data():
    """Load soil data from the configured CSV path.
    Returns mock data if file not found.
    Returns:
        pd.DataFrame: Soil dataset with appropriate columns.
    """
    path = config.SOIL_DATA_PATH
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        # Return mock soil data for demonstration
        return get_mock_soil_data()

def get_mock_soil_data() -> pd.DataFrame:
    """Return mock soil data for demonstration."""
    return pd.DataFrame({
        "pH": [6.8, 6.5, 7.0, 6.9, 6.7],
        "nitrogen": [45, 52, 48, 50, 46],
        "phosphorus": [18, 20, 19, 21, 17],
        "potassium": [180, 195, 185, 200, 175],
        "moisture": [35, 40, 38, 42, 36]
    })
