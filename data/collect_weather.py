import os
import requests
from .config import WEATHER_API_URL, WEATHER_API_KEY

def fetch_weather(location: str) -> dict:
    """Fetch current weather data for a given location.
    Returns mock data if API key is not configured.
    """
    # Check if using placeholder API key
    if WEATHER_API_KEY == "YOUR_WEATHER_API_KEY":
        return get_mock_weather_data(location)
    
    try:
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, Exception):
        # Fallback to mock data on any API error
        return get_mock_weather_data(location)

def get_mock_weather_data(location: str) -> dict:
    """Return mock weather data for demonstration."""
    return {
        "main": {"temp": 28.5, "humidity": 75},
        "wind": {"speed": 4.2},
        "rain": {"1h": 2.5},
        "clouds": {"all": 45},
        "name": location.split(",")[0]
    }

if __name__ == "__main__":
    # Example usage
    print(fetch_weather(os.getenv("DEFAULT_LOCATION", "Kochi,IN")))
