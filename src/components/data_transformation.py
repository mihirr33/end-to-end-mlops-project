from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import joblib


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

            file_path = os.path.join(
                self.ingestion_config.artifact_dir,
                self.ingestion_config.artifact_file
            )

            df = pd.read_csv(file_path)

            logger.info("Dataset Loaded Successfully")

            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

            df.fillna(0, inplace=True)

            df["Churn"] = df["Churn"].map(
                {"Yes": 1, "No": 0}
            )

            X = df.drop(columns=["customerID", "Churn"])
            y = df["Churn"]
            # Separate numerical and categorical columns
            numerical_columns = X.select_dtypes(exclude="object").columns

            categorical_columns = X.select_dtypes(include="object").columns

            

            X = pd.get_dummies(X, drop_first=True)

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=self.training_config.test_size,
                random_state=self.training_config.random_state
            )

            print("Train Shape :", X_train.shape)
            print("Test Shape :", X_test.shape)

            logger.info("Data Transformation Completed")

            return X_train, X_test, y_train, y_test

        except Exception as e:
            raise CustomException(e, sys)