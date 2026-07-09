import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Info,
    generate_latest,
)

from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(
    title="Ryvonexa AI API",
    version="1.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------
# Input Schema
# -----------------------------
class ChurnInput(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    REQUEST_COUNT.inc()

    return {
        "application": "Ryvonexa AI",
        "platform": "Enterprise Customer Intelligence Platform",
        "version": "1.0",
        "status": "Running"
    }

# -----------------------------
# Health
# -----------------------------
@app.get("/health")
def health():

    return {
        "status": "healthy",
        "application": "Ryvonexa AI",
        "model": "Logistic Regression",
        "version": "1.0"
    }

# -----------------------------
# Metrics
# -----------------------------
@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )

# Model Information
MODEL_INFO = Info(
    "model_version",
    "Model Information"
)

MODEL_INFO.info(
    {
        "model": "Logistic Regression",
        "version": "1.0",
        "company": "Ryvonexa AI"
    }
)


# ==========================================================
# Prometheus Metrics
# ==========================================================

# API Requests
REQUEST_COUNT = Counter(
    "request_count_total",
    "Total API Requests"
)

# Total Predictions
PREDICTION_COUNT = Counter(
    "prediction_total",
    "Total Predictions"
)

# Successful Predictions
PREDICTION_SUCCESS = Counter(
    "prediction_success_total",
    "Successful Predictions"
)

# Failed Predictions
PREDICTION_FAILED = Counter(
    "prediction_failed_total",
    "Failed Predictions"
)

# Active Requests
ACTIVE_REQUESTS = Gauge(
    "active_requests",
    "Currently Active Requests"
)

# API Response Time
API_RESPONSE_TIME = Histogram(
    "api_response_time_seconds",
    "API Response Time"
)

# Prediction Latency
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction Latency"
)

# -----------------------------
# Prediction
# -----------------------------
@app.post("/predict")
def predict(data: ChurnInput):

    ACTIVE_REQUESTS.inc()
    REQUEST_COUNT.inc()

    start_time = time.time()

    try:

        pipeline = PredictionPipeline()

        result = pipeline.predict(data.model_dump())

        # Prometheus Metrics
        PREDICTION_COUNT.inc()
        PREDICTION_SUCCESS.inc()

        response_time = time.time() - start_time

        API_RESPONSE_TIME.observe(response_time)
        PREDICTION_LATENCY.observe(response_time)

        # Convert numeric prediction
        result["prediction"] = (
            "Churn"
            if result["prediction"] == 1
            else "No Churn"
        )

        # Business fields
        result["risk"] = (
            "High"
            if result["prediction"] == "Churn"
            else "Low"
        )

        result["recommendation"] = (
            "Offer retention plan immediately."
            if result["prediction"] == "Churn"
            else "Customer likely to stay."
        )

        result["model"] = "Logistic Regression"

        result["response_time"] = f"{round(response_time * 1000,2)} ms"

        return result

    except Exception as e:

        PREDICTION_FAILED.inc()

        return {
            "error": str(e)
        }

    finally:

        ACTIVE_REQUESTS.dec()