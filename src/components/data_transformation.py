import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logger
from src.exception import CustomException
from src.config.configuration import Configuration


class DataTransformation:

    def __init__(self):

        config = Configuration()

        self.ingestion_config = config.get_data_ingestion_config()
        self.training_config = config.get_training_config()

    def initiate_data_transformation(self):

        try:

            # ==============================
            # Load Dataset
            # ==============================

            file_path = os.path.join(
                self.ingestion_config.artifact_dir,
                self.ingestion_config.artifact_file
            )

            df = pd.read_csv(file_path)

            logger.info("Dataset Loaded Successfully")

            # ==============================
            # Data Cleaning
            # ==============================

            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

            df.fillna(0, inplace=True)

            df["Churn"] = df["Churn"].map(
                {
                    "Yes": 1,
                    "No": 0
                }
            )

            # ==============================
            # Features / Target
            # ==============================

            X = df.drop(
                columns=[
                    "customerID",
                    "Churn"
                ]
            )

            y = df["Churn"]

            # ==============================
            # One Hot Encoding
            # ==============================

            X = pd.get_dummies(
                X,
                drop_first=True
            )

            # ==============================
            # Train Test Split
            # ==============================

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=self.training_config.test_size,
                random_state=self.training_config.random_state
            )

            # ==============================
            # Save Artifacts
            # ==============================

            artifact_dir = self.ingestion_config.artifact_dir

            os.makedirs(
                artifact_dir,
                exist_ok=True
            )

            train_df = X_train.copy()
            train_df["Churn"] = y_train.values

            test_df = X_test.copy()
            test_df["Churn"] = y_test.values

            train_df.to_csv(
                os.path.join(artifact_dir, "train.csv"),
                index=False
            )

            test_df.to_csv(
                os.path.join(artifact_dir, "test.csv"),
                index=False
            )

            X_train.to_csv(
                os.path.join(artifact_dir, "X_train.csv"),
                index=False
            )

            X_test.to_csv(
                os.path.join(artifact_dir, "X_test.csv"),
                index=False
            )

            y_train.to_frame().to_csv(
                os.path.join(artifact_dir, "y_train.csv"),
                index=False
            )

            y_test.to_frame().to_csv(
                os.path.join(artifact_dir, "y_test.csv"),
                index=False
            )

            logger.info("Artifacts Saved Successfully")

            print("\n==============================")
            print("Data Transformation Completed")
            print("==============================")
            print(f"Train Shape : {X_train.shape}")
            print(f"Test Shape  : {X_test.shape}")
            print("==============================")

            return X_train, X_test, y_train, y_test

        except Exception as e:
            raise CustomException(e, sys)