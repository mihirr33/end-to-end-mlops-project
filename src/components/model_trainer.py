import os
import sys
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from src.components.data_transformation import DataTransformation
from src.logger import logger
from src.exception import CustomException


class ModelTrainer:

    def initiate_model_training(self):

        try:

            transformer = DataTransformation()

            X_train, X_test, y_train, y_test = transformer.initiate_data_transformation(
                "artifacts/raw_data.csv"
            )

            model = LogisticRegression(max_iter=1000)

            model.fit(X_train, y_train)

            prediction = model.predict(X_test)

            accuracy = accuracy_score(y_test, prediction)

            print(f"\nModel Accuracy : {accuracy:.4f}")

            os.makedirs("models", exist_ok=True)

            joblib.dump(model, "models/model.pkl")

            logger.info("Model Training Completed")

            logger.info(f"Accuracy : {accuracy}")

            print("\nModel Saved Successfully")

        except Exception as e:
            raise CustomException(e, sys)