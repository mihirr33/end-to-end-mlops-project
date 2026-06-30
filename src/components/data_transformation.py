import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logger
from src.exception import CustomException


class DataTransformation:

    def initiate_data_transformation(self, file_path):

        try:

            df = pd.read_csv(file_path)

            logger.info("Dataset Loaded Successfully")

            # TotalCharges ko numeric banao
            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

            # Missing Values Fill
            df.fillna(0, inplace=True)

            # Target Encoding
            df["Churn"] = df["Churn"].map(
                {"Yes": 1, "No": 0}
            )

            X = df.drop(
                columns=["customerID", "Churn"]
            )

            y = df["Churn"]

            X = pd.get_dummies(
                X,
                drop_first=True
            )

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

            print("Train Shape :", X_train.shape)
            print("Test Shape :", X_test.shape)

            logger.info("Data Transformation Completed")

            return (
                X_train,
                X_test,
                y_train,
                y_test
            )

        except Exception as e:
            raise CustomException(e, sys)