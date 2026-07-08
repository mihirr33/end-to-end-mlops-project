import os
import joblib
import pandas as pd

from src.config.configuration import Configuration


class PredictionPipeline:

    def __init__(self):

        config = Configuration()

        self.model_config = config.get_model_trainer_config()

        model_path = os.path.join(
            self.model_config.model_dir,
            self.model_config.model_name
        )

        feature_path = os.path.join(
            self.model_config.model_dir,
            "feature_names.pkl"
        )

        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)

    # -----------------------------
    # Prediction
    # -----------------------------
    def predict(self, data: dict):

        df = pd.DataFrame([data])

        # One Hot Encoding
        df = pd.get_dummies(df)

        # Missing columns
        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0

        # Correct order
        df = df[self.feature_names]

        prediction = self.model.predict(df)[0]

        confidence = None

        if hasattr(self.model, "predict_proba"):

            probability = self.model.predict_proba(df)[0]

            confidence = round(max(probability) * 100, 2)

        return {
            "prediction": int(prediction),
            "confidence": confidence
        }