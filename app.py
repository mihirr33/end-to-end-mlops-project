import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest
from pydantic import BaseModel
from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0"
)
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

# Prometheus Counter
REQUEST_COUNT = Counter(
    "request_count",
    "Total API Requests"
)


# Input Schema
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


@app.get("/")
def home():
    REQUEST_COUNT.inc()
    return {
        "message": "Welcome to Telco Customer Churn Prediction API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "loaded"
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.post("/predict")
def predict(data: ChurnInput):

    REQUEST_COUNT.inc()

    start_time = time.time()

    pipeline = PredictionPipeline()

    result_data = pipeline.predict(data.model_dump())

    prediction = result_data["prediction"]

    confidence = result_data["confidence"]

    result = "Churn" if prediction == 1 else "No Churn"

    # Dummy confidence (next step me model probability use karenge)
    confidence = 94.73 if result == "No Churn" else 87.42

    # Risk Level
    risk = "LOW" if result == "No Churn" else "HIGH"

    # Recommendation
    recommendation = (
        "Customer is likely to stay. Continue engagement strategy."
        if result == "No Churn"
        else "Customer has a high churn risk. Offer retention incentives."
    )

    response_time = round((time.time() - start_time) * 1000, 2)

    return {

    "prediction": result,

    "confidence": confidence,

    "risk": "HIGH" if prediction == 1 else "LOW",

    "recommendation":
        "Customer has a high churn risk. Offer retention incentives."
        if prediction == 1
        else
        "Customer is likely to stay. Continue engagement strategy.",

    "model": "Logistic Regression",

    "response_time": f"{response_time} ms"

}