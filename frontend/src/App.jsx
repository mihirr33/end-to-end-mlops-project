import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    gender: "Male",
    SeniorCitizen: 0,
    Partner: "Yes",
    Dependents: "No",
    tenure: 12,
    PhoneService: "Yes",
    MultipleLines: "No",
    InternetService: "DSL",
    OnlineSecurity: "Yes",
    OnlineBackup: "No",
    DeviceProtection: "No",
    TechSupport: "Yes",
    StreamingTV: "No",
    StreamingMovies: "No",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: 70.35,
    TotalCharges: 844.2,
  });

  const [result, setResult] = useState("");

  const handlePredict = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData
      );

      setResult(response.data.prediction);
    } catch (error) {
      console.error(error);
      alert("Prediction failed");
    }
  };

  return (
    <div className="container">
      <h1>Customer Churn Prediction</h1>

      <form onSubmit={handlePredict}>
        <button type="submit">Predict</button>
      </form>

      <h2>Prediction Result</h2>

      <h3>{result}</h3>
    </div>
  );
}

export default App;