import os
import sys
import pandas as pd

from src.logger import logger
from src.exception import CustomException
from src.config.configuration import Configuration


class DataValidation:

    def __init__(self):

        config = Configuration()

        self.ingestion_config = config.get_data_ingestion_config()

    def validate_data(self):

        try:

            file_path = os.path.join(
                self.ingestion_config.artifact_dir,
                self.ingestion_config.artifact_file
            )

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