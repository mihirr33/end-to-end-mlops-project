import os
import sys
import pandas as pd
import great_expectations as gx

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

            logger.info(f"Dataset Shape : {df.shape}")

            print("\n==============================")
            print("Great Expectations Validation")
            print("==============================")

            # Create GX dataframe
            gx_df = gx.from_pandas(df)

            # -----------------------------------
            # Dataset Level
            # -----------------------------------

            gx_df.expect_table_row_count_to_be_between(
                min_value=1000,
                max_value=10000
            )

            gx_df.expect_table_column_count_to_equal(
                21
            )

            # -----------------------------------
            # Required Columns
            # -----------------------------------

            expected_columns = [
                "customerID",
                "gender",
                "SeniorCitizen",
                "Partner",
                "Dependents",
                "tenure",
                "PhoneService",
                "MultipleLines",
                "InternetService",
                "OnlineSecurity",
                "OnlineBackup",
                "DeviceProtection",
                "TechSupport",
                "StreamingTV",
                "StreamingMovies",
                "Contract",
                "PaperlessBilling",
                "PaymentMethod",
                "MonthlyCharges",
                "TotalCharges",
                "Churn"
            ]

            gx_df.expect_table_columns_to_match_ordered_list(
                expected_columns
            )

            # -----------------------------------
            # Null Checks
            # -----------------------------------

            gx_df.expect_column_values_to_not_be_null(
                "customerID"
            )

            gx_df.expect_column_values_to_not_be_null(
                "gender"
            )

            gx_df.expect_column_values_to_not_be_null(
                "MonthlyCharges"
            )

            gx_df.expect_column_values_to_not_be_null(
                "Churn"
            )

            # -----------------------------------
            # Unique Customer IDs
            # -----------------------------------

            gx_df.expect_column_values_to_be_unique(
                "customerID"
            )

            # -----------------------------------
            # Tenure
            # -----------------------------------

            gx_df.expect_column_values_to_be_between(
                "tenure",
                min_value=0,
                max_value=72
            )

            # -----------------------------------
            # Monthly Charges
            # -----------------------------------

            gx_df.expect_column_values_to_be_between(
                "MonthlyCharges",
                min_value=0,
                max_value=150
            )

            # -----------------------------------
            # Churn Values
            # -----------------------------------

            gx_df.expect_column_values_to_be_in_set(
                "Churn",
                ["Yes", "No"]
            )

            # -----------------------------------
            # Validation
            # -----------------------------------

            results = gx_df.validate()

            print("\nValidation Success :", results["success"])

            if results["success"]:

                print("\nAll Great Expectations Passed")

                logger.info(
                    "Great Expectations Validation Passed"
                )

            else:

                print("\nValidation Failed")

                logger.error(
                    "Great Expectations Validation Failed"
                )

                raise Exception(
                    "Great Expectations Validation Failed"
                )

            logger.info("Data Validation Successful")

            return True

        except Exception as e:

            raise CustomException(e, sys)