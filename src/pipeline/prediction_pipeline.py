import os
import joblib

from src.config.configuration import Configuration


class PredictionPipeline:

    def __init__(self):

        config = Configuration()

        self.model_config = config.get_model_trainer_config()

        model_path = os.path.join(
            self.model_config.model_dir,
            self.model_config.model_name
        )

        self.model = joblib.load(model_path)

    def predict(self, data):

        prediction = self.model.predict(data)

        return prediction