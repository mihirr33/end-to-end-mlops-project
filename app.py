from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0"
)

# Prometheus Counter
REQUEST_COUNT = Counter(
    "request_count",
    "Total API Requests"
)


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
def predict():
    # Yahan tumhara existing prediction code rahega
    return {
        "prediction": "Add your prediction logic here"
    }