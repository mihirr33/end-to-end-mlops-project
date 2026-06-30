import os

# Project Root Directory
ROOT_DIR = os.getcwd()

# Data Directories
DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Artifact Directory
ARTIFACT_DIR = os.path.join(ROOT_DIR, "artifacts")

# Model Directory
MODEL_DIR = os.path.join(ROOT_DIR, "models")

# Config Directory
CONFIG_DIR = os.path.join(ROOT_DIR, "config")