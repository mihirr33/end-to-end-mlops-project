from src.config.configuration import Configuration

config = Configuration()

ingestion = config.get_data_ingestion_config()

print(ingestion)
print(ingestion.raw_data_path)
print(ingestion.artifact_dir)
print(ingestion.artifact_file)