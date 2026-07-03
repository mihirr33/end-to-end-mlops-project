import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load dataset
df = pd.read_csv("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Create report
report = Report(metrics=[
    DataDriftPreset()
])

# Run report
report.run(
    reference_data=df,
    current_data=df
)

# Save HTML
report.save_html("evidently_report.html")

print("✅ Evidently Report Generated Successfully!")