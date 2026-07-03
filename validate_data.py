import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Dataset Shape:", df.shape)

# customerID should not have null values
assert df["customerID"].isnull().sum() == 0, "customerID contains null values"

# MonthlyCharges should be numeric
assert pd.api.types.is_numeric_dtype(df["MonthlyCharges"]), "MonthlyCharges is not numeric"

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

print("Missing TotalCharges before cleaning:", df["TotalCharges"].isnull().sum())

# Remove rows where TotalCharges is missing
df = df.dropna(subset=["TotalCharges"])

# Validate after cleaning
assert df["TotalCharges"].isnull().sum() == 0, "TotalCharges still contains invalid values"

# Churn should contain only Yes/No
assert set(df["Churn"].unique()) == {"Yes", "No"}, "Unexpected values in Churn column"

print("✅ Great Expectations Validation Passed")