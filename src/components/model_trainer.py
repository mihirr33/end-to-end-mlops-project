import os
import sys
import joblib
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

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

            mlflow.set_tracking_uri("sqlite:///mlflow.db")
            mlflow.set_experiment("Customer Churn Prediction")
            with mlflow.start_run(run_name="LogisticRegression"):

                model = LogisticRegression(
                    max_iter=1000,
                    random_state=42
                )

                model.fit(X_train, y_train)

                prediction = model.predict(X_test)

                probability = model.predict_proba(X_test)[:, 1]

                # =============================
                # Metrics
                # =============================

                accuracy = accuracy_score(y_test, prediction)

                precision = precision_score(y_test, prediction)

                recall = recall_score(y_test, prediction)

                f1 = f1_score(y_test, prediction)

                roc = roc_auc_score(y_test, probability)

                # =============================
                # Parameters
                # =============================

                mlflow.log_param("Algorithm", "Logistic Regression")
                mlflow.log_param("max_iter", 1000)
                mlflow.log_param("random_state", 42)

                # =============================
                # Metrics
                # =============================

                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision)
                mlflow.log_metric("Recall", recall)
                mlflow.log_metric("F1 Score", f1)
                mlflow.log_metric("ROC AUC", roc)

                # =============================
                # Model
                # =============================

                mlflow.sklearn.log_model(
                    sk_model=model,
                    name="model"
                )

                # =============================
                # Save Model
                # =============================

                os.makedirs(
                    self.model_config.model_dir,
                    exist_ok=True
                )

                model_path = os.path.join(
                    self.model_config.model_dir,
                    self.model_config.model_name
                )

                joblib.dump(model, model_path)

                feature_path = os.path.join(
                    self.model_config.model_dir,
                    "feature_names.pkl"
                )

                joblib.dump(
                    list(X_train.columns),
                    feature_path
                )

                # =============================
                # Confusion Matrix
                # =============================

                cm = confusion_matrix(
                    y_test,
                    prediction
                )

                with open("confusion_matrix.txt", "w") as f:
                    f.write(str(cm))

                mlflow.log_artifact(
                    "confusion_matrix.txt"
                )

                print("\n==============================")
                print("Training Completed")
                print("==============================")
                print(f"Accuracy  : {accuracy:.4f}")
                print(f"Precision : {precision:.4f}")
                print(f"Recall    : {recall:.4f}")
                print(f"F1 Score  : {f1:.4f}")
                print(f"ROC AUC   : {roc:.4f}")
                print("==============================")

                logger.info(f"Accuracy : {accuracy}")
                logger.info(f"Precision : {precision}")
                logger.info(f"Recall : {recall}")
                logger.info(f"F1 : {f1}")

        except Exception as e:

            raise CustomException(e, sys)