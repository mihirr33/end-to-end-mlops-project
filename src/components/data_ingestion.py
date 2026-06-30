import os
import shutil
import sys

from src.config.configuration import Configuration
from src.logger import logger
from src.exception import CustomException


class DataIngestion:

    def __init__(self):

        config = Configuration()

        self.ingestion_config = config.get_data_ingestion_config()

        os.makedirs(
            self.ingestion_config.artifact_dir,
            exist_ok=True
        )

    def initiate_data_ingestion(self):

        try:

            source_file = self.ingestion_config.raw_data_path

            destination_file = os.path.join(
                self.ingestion_config.artifact_dir,
                self.ingestion_config.artifact_file
            )

            shutil.copy(source_file, destination_file)

            logger.info("Data Ingestion Completed Successfully")

            print("Data Ingestion Completed Successfully")

            return destination_file

        except Exception as e:

            raise CustomException(e, sys)