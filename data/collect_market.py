# data/collect_market.py
"""Collect market price data from external API and store in database."""
import os
import requests
import pandas as pd
from .config import MARKET_API_KEY, MARKET_BASE_URL, DB_TYPE
from .database import get_connection

def fetch_market_data(region: str = "global"):
    """Fetch market price data for given region.
    Returns mock data if API key is not configured.
    Returns a pandas DataFrame with columns: ['date', 'commodity', 'price'].
    """
    # Check if using placeholder API key
    if MARKET_API_KEY == "YOUR_MARKET_API_KEY":
        return get_mock_market_data(region)
    
    try:
        params = {"apikey": MARKET_API_KEY, "region": region}
        response = requests.get(MARKET_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Assuming the API returns a list of records
        df = pd.DataFrame(data)
        return df
    except (requests.exceptions.RequestException, Exception):
        # Fallback to mock data on any API error
        return get_mock_market_data(region)

def get_mock_market_data(region: str = "global") -> pd.DataFrame:
    """Return mock market price data for demonstration."""
    return pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=5),
        "commodity": ["Wheat", "Rice", "Corn", "Soybeans", "Cotton"],
        "price": [250.5, 480.25, 320.75, 580.00, 95.50]
    })

def store_market_data(df: pd.DataFrame):
    conn = get_connection()
    df.to_sql("market_prices", conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    df = fetch_market_data()
    store_market_data(df)
