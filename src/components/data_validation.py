import os
import pandas as pd
import sys

from src.logger import logger
from src.exception import CustomException


class DataValidation:

    def validate_data(self, file_path):

        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_path} not found.")

            df = pd.read_csv(file_path)

            logger.info(f"Dataset Shape: {df.shape}")

            print("Dataset Shape :", df.shape)

            print("\nColumns:\n")
            print(df.columns.tolist())

            logger.info("Data Validation Successful")

            return True

        except Exception as e:
            raise CustomException(e, sys)