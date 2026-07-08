import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest
from pydantic import BaseModel

from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(
    title="Customer Churn Prediction API",
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
# Prometheus Counter
# -----------------------------
REQUEST_COUNT = Counter(
    "request_count",
    "Total API Requests"
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
        "message": "Welcome to Telco Customer Churn Prediction API"
    }


# -----------------------------
# Health
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "loaded"
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


# -----------------------------
# Prediction
# -----------------------------
@app.post("/predict")
def predict(data: ChurnInput):

    try:

        REQUEST_COUNT.inc()

        start_time = time.time()

        pipeline = PredictionPipeline()

        result = pipeline.predict(data.model_dump())

        # Convert numeric prediction to text
        result["prediction"] = (
            "Churn"
            if result["prediction"] == 1
            else "No Churn"
        )

        # Extra information
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

        result["response_time"] = (
            f"{round((time.time() - start_time) * 1000, 2)} ms"
        )

        return result

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {
            "error": str(e)
        }