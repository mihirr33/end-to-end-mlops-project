from fastapi import FastAPI
import pandas as pd

from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to Telco Customer Churn Prediction API"
    }


@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    pipeline = PredictionPipeline()

    prediction = pipeline.predict(df)

    result = "Churn" if prediction[0] == 1 else "No Churn"

    return {
        "prediction": result
    }