from datetime import timedelta

from feast import Entity
from feast import FeatureView
from feast import Field
from feast import FileSource

from feast.types import String, Int64, Float32
from feast.types import String
from feast.data_format import ParquetFormat



customer = Entity(
    name="customer",
    join_keys=["customerID"],
    
)


customer_source = FileSource(
    path="data/telco_raw.parquet",
    file_format=ParquetFormat(),
    event_timestamp_column="event_timestamp",
)


customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=365),

    schema=[

        Field(name="gender", dtype=String),
        Field(name="SeniorCitizen", dtype=Int64),
        Field(name="Partner", dtype=String),
        Field(name="Dependents", dtype=String),

        Field(name="tenure", dtype=Int64),

        Field(name="PhoneService", dtype=String),
        Field(name="MultipleLines", dtype=String),

        Field(name="InternetService", dtype=String),

        Field(name="OnlineSecurity", dtype=String),
        Field(name="OnlineBackup", dtype=String),
        Field(name="DeviceProtection", dtype=String),
        Field(name="TechSupport", dtype=String),

        Field(name="StreamingTV", dtype=String),
        Field(name="StreamingMovies", dtype=String),

        Field(name="Contract", dtype=String),
        Field(name="PaperlessBilling", dtype=String),
        Field(name="PaymentMethod", dtype=String),

        Field(name="MonthlyCharges", dtype=Float32),
        Field(name="TotalCharges", dtype=Float32),
    ],

    source=customer_source,
)

Field(
    name="event_timestamp",
    dtype=String,
),