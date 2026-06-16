# Smart Agriculture Intelligence System

## Overview
This repository implements an AI‑powered decision support platform for precision agriculture. It automatically collects real‑time weather, soil, and market data, runs machine‑learning models to generate crop recommendations, yield forecasts, irrigation schedules, fertilizer advice, and commodity price predictions, and visualises the results in an interactive Streamlit dashboard.

## Features
- Data collection from configurable APIs (weather, soil, market)
- Modular preprocessing and feature engineering
- Machine‑learning models (Random Forest, XGBoost, Prophet, Decision Trees)
- Centralised SQLite/MySQL database
- Real‑time interactive dashboard built with Streamlit
- Extensible architecture for adding new modules or regions

## Project Structure
```
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ data/
│   ├─ __init__.py
│   ├─ config.py
│   ├─ collect_weather.py
│   ├─ collect_soil.py
│   ├─ collect_market.py
│   └─ database.py
├─ preprocess/
│   ├─ __init__.py
│   ├─ clean.py
│   └─ feature_engineering.py
├─ models/
│   ├─ __init__.py
│   ├─ crop_recommendation.py
│   ├─ yield_prediction.py
│   ├─ price_prediction.py
│   ├─ irrigation.py
│   ├─ fertilizer.py
│   └─ training_utils.py
├─ app/
│   ├─ __init__.py
│   ├─ dashboard.py
│   ├─ components/
│   └─ pages/
├─ utils/
│   ├─ logger.py
│   └─ metrics.py
├─ scripts/
│   ├─ run_all.sh
│   └─ train_models.py
└─ tests/
    └─ (pytest skeleton)
```
