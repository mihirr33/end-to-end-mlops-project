from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.logger import logger


class TrainingPipeline:

    def start_pipeline(self):

        logger.info("========== Training Pipeline Started ==========")

        # Step 1
        ingestion = DataIngestion()
        ingestion.initiate_data_ingestion()

        # Step 2
        validation = DataValidation()
        validation.validate_data()

        # Step 3
        transformation = DataTransformation()
        transformation.initiate_data_transformation()

        # Step 4
        trainer = ModelTrainer()
        trainer.initiate_model_training()

        logger.info("========== Training Pipeline Completed ==========")


if __name__ == "__main__":

    pipeline = TrainingPipeline()

    pipeline.start_pipeline()