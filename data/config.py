# data/config.py
"""Configuration settings for the Smart Agriculture Intelligence System.
Replace placeholder values with actual API keys and endpoints before running.
"""
import os

# Weather API configuration (example using OpenWeatherMap)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "YOUR_WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5/weather")

# Soil data source configuration (could be a file path or API endpoint)
SOIL_DATA_PATH = os.getenv("SOIL_DATA_PATH", "data/soil_data.csv")
# If using an API, provide endpoint and key similarly

# Market price data configuration (example using a hypothetical API)
MARKET_API_KEY = os.getenv("MARKET_API_KEY", "YOUR_MARKET_API_KEY")
MARKET_BASE_URL = os.getenv("MARKET_BASE_URL", "https://api.agri-market.com/prices")

# Database configuration (choose between SQLite and MySQL)
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # or "mysql"
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "smart_agri.db")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "smart_agri")
