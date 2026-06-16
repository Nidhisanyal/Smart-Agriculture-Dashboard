# models/crop_recommendation.py
"""Crop recommendation model.
Uses RandomForestClassifier or XGBoost to predict suitable crops based on features.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# Optional: import xgboost as xgb

class CropRecommender:
    def __init__(self, model_type="random_forest", n_estimators=100, random_state=42):
        if model_type == "random_forest":
            self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        # elif model_type == "xgboost":
        #     self.model = xgb.XGBClassifier(n_estimators=n_estimators, random_state=random_state)
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")
        self.model_type = model_type

    def train(self, X: pd.DataFrame, y: pd.Series):
        """Fit the model.
        X: feature dataframe
        y: target series with crop labels
        """
        self.model.fit(X, y)
        return self

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Predict suitable crop(s) for given feature rows.
        Returns a Series of predicted crop names.
        """
        return pd.Series(self.model.predict(X), index=X.index)

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """Return class probabilities.
        Useful for confidence scores.
        """
        probs = self.model.predict_proba(X)
        return pd.DataFrame(probs, index=X.index, columns=self.model.classes_)
