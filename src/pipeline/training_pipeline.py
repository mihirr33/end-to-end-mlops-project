from uuid import uuid4
from datetime import datetime, timezone

from openlineage.client import OpenLineageClient
from openlineage.client.run import (
    Run,
    Job,
    InputDataset,
    OutputDataset,
    RunEvent,
    RunState,
)

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.logger import logger


class TrainingPipeline:

    def start_pipeline(self):

        logger.info("========== Training Pipeline Started ==========")

        client = OpenLineageClient(
            url="http://localhost:5000"
        )

        run = Run(
            runId=str(uuid4())
        )

        job = Job(
            namespace="customer-churn",
            name="training_pipeline"
        )

        inputs = [
            InputDataset(
                namespace="customer-churn",
                name="WA_Fn-UseC_-Telco-Customer-Churn.csv"
            )
        ]

        outputs = [
            OutputDataset(
                namespace="customer-churn",
                name="model.pkl"
            )
        ]

        # START EVENT
        client.emit(
            RunEvent(
                eventType=RunState.START,
                eventTime=datetime.now(timezone.utc).isoformat(),
                producer="https://github.com/mihirr00051/end-to-end-mlops-assignment",
                run=run,
                job=job,
                inputs=inputs,
                outputs=outputs,
            )
        )

        # Data Ingestion
        ingestion = DataIngestion()
        ingestion.initiate_data_ingestion()

        # Data Validation
        validation = DataValidation()
        validation.validate_data()

        # Data Transformation
        transformation = DataTransformation()
        transformation.initiate_data_transformation()

        # Model Training
        trainer = ModelTrainer()
        trainer.initiate_model_training()

        # COMPLETE EVENT
        client.emit(
            RunEvent(
                eventType=RunState.COMPLETE,
                eventTime=datetime.now(timezone.utc).isoformat(),
                producer="https://github.com/mihirr00051/end-to-end-mlops-assignment",
                run=run,
                job=job,
                inputs=inputs,
                outputs=outputs,
            )
        )

        logger.info("========== Training Pipeline Completed ==========")


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.start_pipeline()