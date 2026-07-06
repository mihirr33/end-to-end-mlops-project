import os
import sys
import joblib
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from src.components.data_transformation import DataTransformation
from src.config.configuration import Configuration
from src.logger import logger
from src.exception import CustomException


class ModelTrainer:

    def __init__(self):

        config = Configuration()

        self.model_config = config.get_model_trainer_config()

    def initiate_model_training(self):

        try:

            transformer = DataTransformation()

            X_train, X_test, y_train, y_test = (
                transformer.initiate_data_transformation()
            )

            with mlflow.start_run():

                model = LogisticRegression(max_iter=1000)

                model.fit(X_train, y_train)

                prediction = model.predict(X_test)

                accuracy = accuracy_score(y_test, prediction)

                mlflow.log_param("model", "LogisticRegression")
                mlflow.log_param("max_iter", 1000)

                mlflow.log_metric("accuracy", accuracy)

                mlflow.sklearn.log_model(
                    sk_model=model,
                    name="model"
                )

                os.makedirs(
                    self.model_config.model_dir,
                    exist_ok=True
                )

                model_path = os.path.join(
                    self.model_config.model_dir,
                    self.model_config.model_name
                )

                joblib.dump(model, model_path)

                # Save feature names
                feature_path = os.path.join(
                self.model_config.model_dir,
                "feature_names.pkl"
                )

                joblib.dump(list(X_train.columns), feature_path)

                print(f"Feature Names Saved : {feature_path}")

                print(f"\nAccuracy : {accuracy:.4f}")

                print(f"\nModel Saved : {model_path}")

                logger.info(f"Accuracy : {accuracy}")

        except Exception as e:
            raise CustomException(e, sys)