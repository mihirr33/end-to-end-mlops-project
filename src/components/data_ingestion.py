import os
import shutil
import sys

from src.constants import RAW_DATA_DIR, ARTIFACT_DIR
from src.logger import logger
from src.exception import CustomException


class DataIngestion:

    def __init__(self):
        os.makedirs(ARTIFACT_DIR, exist_ok=True)

    def initiate_data_ingestion(self):
        try:
            source_file = os.path.join(
                RAW_DATA_DIR,
                "WA_Fn-UseC_-Telco-Customer-Churn.csv"
            )

            destination_file = os.path.join(
                ARTIFACT_DIR,
                "raw_data.csv"
            )

            shutil.copy(source_file, destination_file)

            logger.info("Data Ingestion Completed Successfully")

            return destination_file

        except Exception as e:
            raise CustomException(e, sys)