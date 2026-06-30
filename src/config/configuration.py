import yaml

from src.entity.config_entity import (
    DataIngestionConfig,
    ModelTrainerConfig,
    TrainingConfig,
)


class Configuration:

    def __init__(self, config_filepath="config/config.yaml"):

        with open(config_filepath, "r") as file:
            self.config = yaml.safe_load(file)

    def get_data_ingestion_config(self):

        config = self.config["data_ingestion"]

        return DataIngestionConfig(
            raw_data_path=config["raw_data_path"],
            artifact_dir=config["artifact_dir"],
            artifact_file=config["artifact_file"],
        )

    def get_model_trainer_config(self):

        config = self.config["model_training"]

        return ModelTrainerConfig(
            model_dir=config["model_dir"],
            model_name=config["model_name"],
        )

    def get_training_config(self):

        config = self.config["training"]

        return TrainingConfig(
            test_size=config["test_size"],
            random_state=config["random_state"],
        )