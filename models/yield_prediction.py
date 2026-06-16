# models/yield_prediction.py
"""Yield prediction model using Random Forest Regressor.

Provides a simple training and inference interface.
"""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

class YieldPredictor:
    def __init__(self, n_estimators=200, random_state=42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.is_trained = False

    def train(self, features: pd.DataFrame, target: pd.Series):
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        self.is_trained = True
        return {"mae": mae, "r2": r2}

    def predict(self, features: pd.DataFrame):
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction.")
        return self.model.predict(features)
