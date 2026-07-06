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

    def predict(self, data: dict):

        df = pd.DataFrame([data])

        # One-hot encoding
        df = pd.get_dummies(df)

        # Add missing columns
        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0

        # Correct column order
        df = df[self.feature_names]

        prediction = self.model.predict(df)

        return int(prediction[0])