import os
import pandas as pd

from evidently.report import Report
from evidently.metric_preset import (
    DataDriftPreset,
    DataQualityPreset,
)

from src.logger import logger


class ModelMonitoring:

    def __init__(self):

        self.artifact_dir = "artifacts"
        self.report_dir = "reports"

        os.makedirs(
            self.report_dir,
            exist_ok=True
        )

    def generate_reports(self):

        logger.info("Generating Evidently Reports...")

        train_df = pd.read_csv(
            os.path.join(
                self.artifact_dir,
                "train.csv"
            )
        )

        test_df = pd.read_csv(
            os.path.join(
                self.artifact_dir,
                "test.csv"
            )
        )

        # ==========================
        # Data Drift Report
        # ==========================

        drift_report = Report(
            metrics=[
                DataDriftPreset()
            ]
        )

        drift_report.run(
            reference_data=train_df,
            current_data=test_df,
        )

        drift_report.save_html(
            os.path.join(
                self.report_dir,
                "data_drift_report.html"
            )
        )

        # ==========================
        # Data Quality Report
        # ==========================

        quality_report = Report(
            metrics=[
                DataQualityPreset()
            ]
        )

        quality_report.run(
            reference_data=train_df,
            current_data=test_df,
        )

        quality_report.save_html(
            os.path.join(
                self.report_dir,
                "data_quality_report.html"
            )
        )

        logger.info("Evidently Reports Generated Successfully.")

        print("\n====================================")
        print("EVIDENTLY REPORTS GENERATED")
        print("====================================")
        print("reports/data_drift_report.html")
        print("reports/data_quality_report.html")
        print("====================================")