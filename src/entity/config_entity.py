from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    raw_data_path: str
    artifact_dir: str
    artifact_file: str


@dataclass
class ModelTrainerConfig:
    model_dir: str
    model_name: str


@dataclass
class TrainingConfig:
    test_size: float
    random_state: int