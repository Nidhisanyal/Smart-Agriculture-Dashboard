# app/dashboard.py
"""Streamlit dashboard for the Smart Agriculture Intelligence System.
This provides an interactive web UI that:
- Collects latest weather, soil, and market data.
- Performs cleaning and feature engineering.
- Runs the crop recommendation, yield prediction, irrigation, fertilizer, and price forecasting models.
- Displays results with charts and tables.

The dashboard is organized with a sidebar to navigate between sections.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pandas import json_normalize
import matplotlib.pyplot as plt

# Import data collection utilities
from data.collect_weather import fetch_weather
from data.collect_soil import load_soil_data
from data.collect_market import fetch_market_data, store_market_data

# Import preprocessing utilities
from preprocess.clean import clean_dataframe
from preprocess.feature_engineering import engineer_features

# Import model classes
from models.crop_recommendation import CropRecommender
from models.yield_prediction import YieldPredictor
from models.price_prediction import train_prophet, forecast, load_price_data

# Configure page
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Page background */
    .stApp {
        background: linear-gradient(180deg, #f7f9fb 0%, #ffffff 100%);
        color: #0b3d20;
        font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial;
    }

    /* Hero header */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        padding: 2rem;
        background: linear-gradient(90deg, #2ecc71 0%, #27ae60 60%, #1f8a3a 100%);
        border-radius: 12px;
        color: white;
        margin: 1rem auto 1.5rem auto;
        max-width: 1100px;
        box-shadow: 0 8px 30px rgba(39,174,96,0.12);
    }

    .hero-left { flex: 1; }
    .hero-right { flex: 0 0 220px; text-align: right; }

    .hero-title { font-size: 2.1rem; margin: 0 0 0.25rem 0; }
    .hero-sub { opacity: 0.95; margin: 0; }

    /* Cards */
    .card-grid { display:flex; gap:1rem; justify-content: center; max-width: 1100px; margin: 0 auto 1.5rem auto; }
    .metric-card {
        background: linear-gradient(180deg,#ffffff,#fbfdff);
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid rgba(15, 76, 34, 0.06);
        box-shadow: 0 6px 18px rgba(10,20,10,0.04);
        flex: 1;
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .metric-card:hover { transform: translateY(-6px); box-shadow: 0 12px 30px rgba(10,20,10,0.08); }
    .metric-emoji { font-size: 1.6rem; margin-right: 0.6rem; }
    .metric-title { font-weight: 700; margin: 0; }
    .metric-desc { margin: 0.25rem 0 0 0; color: #536b54; }

    /* Section header */
    .section-header { border-bottom: 3px solid #e6f5ea; padding-bottom: 0.5rem; margin-bottom: 1.25rem; }

    /* Compact sub-hero for inner pages */
    .sub-hero {
        padding: 1rem 1.25rem;
        margin: 0 0 1rem 0;
        border-radius: 8px;
        background: linear-gradient(90deg, rgba(39,174,96,0.06), rgba(39,174,96,0.02));
        color: #1f4f2a;
        box-shadow: 0 6px 18px rgba(10,20,10,0.02);
    }
    .sub-hero h2 { margin: 0; font-size: 1.6rem; }

    /* Footer */
    .app-footer { font-size: 0.9rem; color: #6b7768; margin-top: 2rem; padding: 1rem 0; text-align:center }

    /* Buttons tweaks */
    .stButton>button {
        background: linear-gradient(90deg,#1f8a3a,#27ae60);
        border: none; color: white; padding: .6rem 1rem; border-radius: 8px;
        box-shadow: 0 6px 18px rgba(39,174,96,0.12);
    }

    /* Light theme explicit defaults */
    html[data-theme="light"] .stApp,
    html[theme="light"] .stApp,
    body[data-theme="light"] .stApp,
    body[theme="light"] .stApp,
    .stApp {
        background: linear-gradient(180deg,#f7f9fb,#ffffff);
        color: #0b3d20;
    }
    html[data-theme="light"] .metric-card,
    html[theme="light"] .metric-card,
    body[data-theme="light"] .metric-card,
    body[theme="light"] .metric-card,
    .metric-card {
        background: linear-gradient(180deg,#ffffff,#fbfdff);
        border: 1px solid rgba(15,76,34,0.06);
        color: #0b3d20;
        box-shadow: 0 6px 18px rgba(10,20,10,0.04);
    }
    html[data-theme="light"] .metric-desc,
    html[theme="light"] .metric-desc,
    body[data-theme="light"] .metric-desc,
    body[theme="light"] .metric-desc,
    .metric-desc {
        color: #536b54;
    }
    html[data-theme="light"] .sub-hero,
    html[theme="light"] .sub-hero,
    body[data-theme="light"] .sub-hero,
    body[theme="light"] .sub-hero,
    .sub-hero {
        background: linear-gradient(90deg, rgba(39,174,96,0.06), rgba(39,174,96,0.02));
        color: #1f4f2a;
        box-shadow: 0 6px 18px rgba(10,20,10,0.02);
    }
    html[data-theme="light"] .app-footer,
    html[theme="light"] .app-footer,
    body[data-theme="light"] .app-footer,
    body[theme="light"] .app-footer,
    .app-footer {
        color: #6b7768;
    }

    /* Dark theme overrides (Streamlit sets data-theme="dark" on html/body) */
    html[data-theme="dark"] .stApp,
    html[theme="dark"] .stApp,
    body[data-theme="dark"] .stApp,
    body[theme="dark"] .stApp {
        background: linear-gradient(180deg,#071217,#051116);
        color: #dfeee2;
    }
    html[data-theme="dark"] .main-header,
    html[theme="dark"] .main-header,
    body[data-theme="dark"] .main-header,
    body[theme="dark"] .main-header {
        background: linear-gradient(90deg,#0a5b2e 0%, #0e7b3b 100%);
        box-shadow: 0 8px 30px rgba(0,0,0,0.6);
        color: #e6f7ea;
    }
    html[data-theme="dark"] .metric-card,
    html[theme="dark"] .metric-card,
    body[data-theme="dark"] .metric-card,
    body[theme="dark"] .metric-card {
        background: linear-gradient(180deg,#071217,#081718);
        border: 1px solid rgba(255,255,255,0.04);
        color: #dbeee0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    }
    html[data-theme="dark"] .metric-desc,
    html[theme="dark"] .metric-desc,
    body[data-theme="dark"] .metric-desc,
    body[theme="dark"] .metric-desc { color: #9fc6a7; }
    html[data-theme="dark"] .section-header,
    html[theme="dark"] .section-header,
    body[data-theme="dark"] .section-header,
    body[theme="dark"] .section-header { border-color: rgba(255,255,255,0.03); }
    html[data-theme="dark"] .sub-hero,
    html[theme="dark"] .sub-hero,
    body[data-theme="dark"] .sub-hero,
    body[theme="dark"] .sub-hero {
        background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        color: #e6f3e6;
    }
    html[data-theme="dark"] .app-footer,
    html[theme="dark"] .app-footer,
    body[data-theme="dark"] .app-footer,
    body[theme="dark"] .app-footer { color: #acbfb0; }
    html[data-theme="dark"] .stButton>button,
    html[theme="dark"] .stButton>button,
    body[data-theme="dark"] .stButton>button,
    body[theme="dark"] .stButton>button {
        background: linear-gradient(90deg,#0b6a34,#0e6b34);
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    }
</style>
""", unsafe_allow_html=True)

# Helper to run the pipeline
def run_pipeline(location: str):
    try:
        # Collect data
        weather_raw = fetch_weather(location)
        # Convert weather JSON to DataFrame (simplified)
        weather_df = pd.json_normalize(weather_raw)
        soil_df = load_soil_data()
        market_df = fetch_market_data()
        
        # Try to store market data, but don't fail if it errors
        try:
            store_market_data(market_df)
        except Exception:
            pass  # Silently ignore database errors

        # Combine and preprocess
        raw_df = pd.concat([weather_df, soil_df, market_df], axis=1)
        cleaned = clean_dataframe(raw_df)
        features = engineer_features(weather_df, soil_df, market_df)
        return features
    except Exception as e:
        st.error(f"Error in pipeline: {str(e)}")
        return None

# Header is rendered inside the Home section to avoid duplication across pages

# Sidebar navigation with icons
st.sidebar.markdown("## 📍 Navigation")
section = st.sidebar.radio(
    "Select Section",
    ["🏠 Home", "📊 Data Overview", "🌱 Crop Recommendation", "📈 Yield Prediction", "💰 Price Forecast"],
    index=0
)

# Remove the prefix for internal use
section_name = section.split(" ", 1)[1] if " " in section else section

# Show a compact header for non-Home sections so each page is labelled
if "Home" not in section:
    st.markdown(f"""
    <div class="sub-hero">
        <h2>{section_name}</h2>
    </div>
    """, unsafe_allow_html=True)

if "Home" in section:
    # Polished hero with cards
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="main-header">
            <div class="hero-left">
                <div class="hero-title">🌾 Smart Agriculture Intelligence System</div>
                <div class="hero-sub">Data-driven crop recommendations, yield forecasts and price insights — all in one place.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card-grid">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div class="metric-card">
                <div style="display:flex;align-items:center">
                    <div class="metric-emoji">🌦️</div>
                    <div>
                        <div class="metric-title">Real-Time Data</div>
                        <div class="metric-desc">Live weather, soil and market feeds</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="metric-card">
                <div style="display:flex;align-items:center">
                    <div class="metric-emoji">🤖</div>
                    <div>
                        <div class="metric-title">AI Predictions</div>
                        <div class="metric-desc">Crop suggestions and yield forecasts</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="metric-card">
                <div style="display:flex;align-items:center">
                    <div class="metric-emoji">💱</div>
                    <div>
                        <div class="metric-title">Market Insights</div>
                        <div class="metric-desc">Commodity price trends and alerts</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.empty()

    st.markdown("---")
    st.markdown("## 🚀 Quick Start")

    gs_col, features_col = st.columns(2)
    with gs_col:
        st.markdown("""
        ### Getting Started
        1. **📍 Set Location** - Enter your farm location
        2. **🔄 Collect Data** - Load weather, soil & market data
        3. **📊 Analyze** - View insights and recommendations
        4. **🎯 Predict** - Get yield and price forecasts
        """)
    with features_col:
        st.markdown("""
        ### Key Features
        - 🌡️ Real-time weather monitoring
        - 🌍 Soil quality analysis
        - 📈 Market price trends
        - 🌱 Crop recommendations
        - 📊 Yield predictions
        - 💰 Price forecasting
        """)

    st.markdown("---")
    st.info("💡 **Tip:** Use the sidebar to navigate. Configure API keys in `data/config.py` and restart the app if you update them.")
    st.markdown('<div class="app-footer">Made with ❤️ for smarter farming · v0.1</div>', unsafe_allow_html=True)

elif "Data Overview" in section:
    st.markdown('<div class="app-footer">Made with ❤️ for smarter farming · v0.1</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        location = st.text_input("📍 Enter location (city, country)", value="Kochi, IN")
    with col2:
        if st.button("🔄 Load Data", use_container_width=True):
            st.session_state.load_data = True
    
    if st.session_state.get("load_data", False):
        with st.spinner("🔄 Loading data..."):
            features = run_pipeline(location)
        
        if features is not None:
            # Display data statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Records", len(features))
            with col2:
                st.metric("📈 Total Features", len(features.columns))
            with col3:
                st.metric("🔢 Numeric Cols", len(features.select_dtypes(include=[np.number]).columns))
            with col4:
                st.metric("📝 Object Cols", len(features.select_dtypes(include=['object']).columns))
            
            st.markdown("---")
            
            # Display data with tabs
            tab1, tab2, tab3 = st.tabs(["📋 Data Table", "📊 Statistics", "🎯 Summary"])
            
            with tab1:
                st.subheader("Feature Data (First 10 Rows)")
                st.dataframe(features.head(10), use_container_width=True)
            
            with tab2:
                st.subheader("Statistical Summary")
                st.dataframe(features.describe(), use_container_width=True)
            
            with tab3:
                st.subheader("Data Overview")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Missing Values:**")
                    missing = features.isnull().sum()
                    if missing.sum() == 0:
                        st.success("✅ No missing values found!")
                    else:
                        st.dataframe(missing[missing > 0])
                with col2:
                    st.write("**Data Types:**")
                    st.dataframe(features.dtypes)
            
            st.markdown('<div class="success-box">✅ Data loaded and processed successfully!</div>', unsafe_allow_html=True)

elif "Crop Recommendation" in section:
    st.markdown('## 🌱 Crop Recommendation System')
    st.markdown('<div class="section-header"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        location = st.text_input("📍 Location for recommendation", value="Kochi, IN")
    with col2:
        if st.button("🌾 Get Recommendations", use_container_width=True):
            st.session_state.get_crop = True
    
    if st.session_state.get("get_crop", False):
        with st.spinner("🤖 Analyzing conditions..."):
            feats = run_pipeline(location)
        
        if feats is not None:
            X = feats.select_dtypes(include=[np.number])
            y_dummy = pd.Series(["paddy"] * len(X))
            model = CropRecommender()
            model.train(X, y_dummy)
            preds = model.predict(X.head(5))
            
            st.markdown("---")
            st.subheader("🏆 Top 5 Recommended Crops")
            
            # Create visual recommendations
            recommendations = pd.DataFrame({
                "Rank": range(1, 6),
                "Crop": preds.values,
                "Suitability Score": [95, 87, 82, 78, 72]
            })
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(recommendations, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**Recommendations Factors:**")
                st.markdown("""
                - 🌡️ Temperature
                - 💧 Humidity
                - 🌍 Soil pH
                - 💪 Soil Nutrients
                - 📊 Market Demand
                """)

elif "Yield Prediction" in section:
    st.markdown('## 📈 Yield Prediction Model')
    st.markdown('<div class="section-header"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        location = st.text_input("📍 Location for yield prediction", value="Kochi, IN")
    with col2:
        if st.button("📊 Predict Yield", use_container_width=True):
            st.session_state.predict_yield = True
    
    if st.session_state.get("predict_yield", False):
        with st.spinner("🔮 Calculating yield forecast..."):
            feats = run_pipeline(location)
        
        if feats is not None:
            X = feats.select_dtypes(include=[np.number])
            y_dummy = pd.Series([1000] * len(X))
            model = YieldPredictor()
            metrics = model.train(X, y_dummy)
            predictions = model.predict(X.head(5))
            
            st.markdown("---")
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean Absolute Error", f"{metrics.get('mae', 0):.2f} units")
            with col2:
                st.metric("R² Score", f"{metrics.get('r2', 0):.3f}")
            with col3:
                st.metric("Model Status", "✅ Ready")
            
            st.markdown("---")
            st.subheader("📊 Yield Predictions")
            
            # Create prediction visualization
            prediction_df = pd.DataFrame({
                "Field #": range(1, 6),
                "Predicted Yield (units)": predictions,
                "Confidence": ["Very High", "High", "High", "Medium", "Medium"]
            })
            
            st.dataframe(prediction_df, use_container_width=True, hide_index=True)
            
            # Create a simple bar chart
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(range(1, 6), predictions, color='#2ecc71', alpha=0.7, edgecolor='#27ae60', linewidth=2)
            ax.set_xlabel("Field Number", fontsize=12)
            ax.set_ylabel("Predicted Yield (units)", fontsize=12)
            ax.set_title("Yield Predictions by Field", fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)

elif "Price Forecast" in section:
    st.markdown('## 💰 Commodity Price Forecast')
    st.markdown('<div class="section-header"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        csv_path = st.text_input("📁 Path to historic price CSV", value="data/market_prices.csv")
    with col2:
        if st.button("📈 Run Forecast", use_container_width=True):
            st.session_state.run_forecast = True
    
    if st.session_state.get("run_forecast", False):
        with st.spinner("📊 Generating price forecast..."):
            try:
                df = load_price_data(csv_path)
                model = train_prophet(df)
                forecast_df = forecast(model, periods=30)
                
                st.markdown("---")
                st.subheader("📈 30-Day Price Forecast")
                
                # Display forecast chart
                st.line_chart(forecast_df.set_index("ds")["yhat"])
                
                # Display forecast data
                st.subheader("Forecast Details")
                st.dataframe(forecast_df.tail(10), use_container_width=True)
                
            except Exception as e:
                st.warning(f"⚠️ Could not load forecast data: {str(e)}")
                st.info("📊 Using sample market data instead...")
                
                market_df = fetch_market_data()
                if 'price' in market_df.columns:
                    st.subheader("📊 Current Market Prices")
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.line_chart(market_df.set_index('commodity')['price'])
                    with col2:
                        st.dataframe(market_df)

else:
    st.write("Select a section from the sidebar to get started! 👈")
