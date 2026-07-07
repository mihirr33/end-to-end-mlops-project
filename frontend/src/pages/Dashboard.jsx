import { useState, useEffect } from "react";
import axios from "axios";

import Navbar from "../components/Navbar";
import DashboardCard from "../components/DashboardCard";
import InputField from "../components/InputField";
import PredictionHistory from "../components/PredictionHistory";
import SystemStatus from "../components/SystemStatus";
import AnalyticsChart from "../components/AnalyticsChart";

import {
    FaChartLine,
    FaServer,
    FaBrain,
    FaDocker,
} from "react-icons/fa";

function Dashboard() {

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

        MonthlyCharges: 70,
        TotalCharges: 844

    });

    const [prediction, setPrediction] = useState(null);

    const [loading, setLoading] = useState(false);

    const [history, setHistory] = useState([]);

    const [health, setHealth] = useState(false);

    // ============================
    // Handle Form Change
    // ============================

    const handleChange = (e) => {

        setFormData({

            ...formData,

            [e.target.name]: e.target.value

        });

    };

    // ============================
    // Prediction API
    // ============================

    const handlePredict = async () => {

        setLoading(true);

        try {

            const response = await axios.post(

                "http://127.0.0.1:8000/predict",

                formData

            );

            setPrediction(response.data);

            setHistory((prev) => [

                response.data,

                ...prev

            ]);

        }

        catch (error) {

            console.error(error);

            if (error.response) {

                alert(error.response.data.detail);

            }

            else {

                alert("Unable to connect API");

            }

        }

        finally {

            setLoading(false);

        }

    };

    // ============================
    // Health Check
    // ============================

    useEffect(() => {

  const checkHealth = async () => {

    try {

      await axios.get("http://127.0.0.1:8000/health");

      setHealth(true);

    } catch {

      setHealth(false);

    }

  };

  checkHealth();

  const interval = setInterval(checkHealth,10000);

  return () => clearInterval(interval);

}, []);

/* IMPORTANT */

return (

<div className="dashboard">

    <Navbar />
    {/* ================= KPI ================= */ }

    <div className="stats">

        <DashboardCard
            title="Accuracy"
            value="82.19%"
            icon={<FaChartLine />}
        />

        <DashboardCard
            title="API"
            value={health ? "Healthy" : "Offline"}
            icon={<FaServer />}
        />

        <DashboardCard
            title="Model"
            value="Logistic Regression"
            icon={<FaBrain />}
        />

        <DashboardCard
            title="Deployment"
            value="Docker + Kubernetes"
            icon={<FaDocker />}
        />

    </div>

    {/* ================= MAIN GRID ================= */ }

    <div className="dashboard-grid">

        {/* ================= LEFT PANEL ================= */}

        <div className="left-panel">

            <h2>Customer Information</h2>

            <div className="form-grid">

                <InputField label="Gender">
                    <select
                        name="gender"
                        value={formData.gender}
                        onChange={handleChange}
                    >
                        <option>Male</option>
                        <option>Female</option>
                    </select>
                </InputField>

                <InputField label="Senior Citizen">
                    <select
                        name="SeniorCitizen"
                        value={formData.SeniorCitizen}
                        onChange={handleChange}
                    >
                        <option value={0}>No</option>
                        <option value={1}>Yes</option>
                    </select>
                </InputField>

                <InputField label="Partner">
                    <select
                        name="Partner"
                        value={formData.Partner}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </InputField>

                <InputField label="Dependents">
                    <select
                        name="Dependents"
                        value={formData.Dependents}
                        onChange={handleChange}
                    >
                        <option>No</option>
                        <option>Yes</option>
                    </select>
                </InputField>

                <InputField label="Phone Service">
                    <select
                        name="PhoneService"
                        value={formData.PhoneService}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </InputField>

                <InputField label="Multiple Lines">
                    <select
                        name="MultipleLines"
                        value={formData.MultipleLines}
                        onChange={handleChange}
                    >
                        <option>No</option>
                        <option>Yes</option>
                        <option>No phone service</option>
                    </select>
                </InputField>

                <InputField label="Internet Service">
                    <select
                        name="InternetService"
                        value={formData.InternetService}
                        onChange={handleChange}
                    >
                        <option>DSL</option>
                        <option>Fiber optic</option>
                        <option>No</option>
                    </select>
                </InputField>

                <InputField label="Online Security">
                    <select
                        name="OnlineSecurity"
                        value={formData.OnlineSecurity}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                        <option>No internet service</option>
                    </select>
                </InputField>

                <InputField label="Online Backup">
                    <select
                        name="OnlineBackup"
                        value={formData.OnlineBackup}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                        <option>No internet service</option>
                    </select>
                </InputField>

                <InputField label="Device Protection">
                    <select
                        name="DeviceProtection"
                        value={formData.DeviceProtection}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                        <option>No internet service</option>
                    </select>
                </InputField>

                <InputField label="Tech Support">
                    <select
                        name="TechSupport"
                        value={formData.TechSupport}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                        <option>No internet service</option>
                    </select>
                </InputField>

                <InputField label="Streaming TV">
                    <select
                        name="StreamingTV"
                        value={formData.StreamingTV}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                        <option>No internet service</option>
                    </select>
                </InputField>

                <InputField label="Streaming Movies">
                    <select
                        name="StreamingMovies"
                        value={formData.StreamingMovies}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                        <option>No internet service</option>
                    </select>
                </InputField>

                <InputField label="Contract">
                    <select
                        name="Contract"
                        value={formData.Contract}
                        onChange={handleChange}
                    >
                        <option>Month-to-month</option>
                        <option>One year</option>
                        <option>Two year</option>
                    </select>
                </InputField>

                <InputField label="Paperless Billing">
                    <select
                        name="PaperlessBilling"
                        value={formData.PaperlessBilling}
                        onChange={handleChange}
                    >
                        <option>Yes</option>
                        <option>No</option>
                    </select>
                </InputField>

                <InputField label="Payment Method">
                    <select
                        name="PaymentMethod"
                        value={formData.PaymentMethod}
                        onChange={handleChange}
                    >
                        <option>Electronic check</option>
                        <option>Mailed check</option>
                        <option>Bank transfer (automatic)</option>
                        <option>Credit card (automatic)</option>
                    </select>
                </InputField>

                <InputField label="Tenure">
                    <input
                        type="number"
                        name="tenure"
                        value={formData.tenure}
                        onChange={handleChange}
                    />
                </InputField>

                <InputField label="Monthly Charges">
                    <input
                        type="number"
                        name="MonthlyCharges"
                        value={formData.MonthlyCharges}
                        onChange={handleChange}
                    />
                </InputField>

                <InputField label="Total Charges">
                    <input
                        type="number"
                        name="TotalCharges"
                        value={formData.TotalCharges}
                        onChange={handleChange}
                    />
                </InputField>

            </div>

            <button
                className="predict-btn"
                onClick={handlePredict}
                disabled={loading}
            >
                {loading ? "⏳ Analyzing..." : "🚀 Analyze Customer"}
            </button>

        </div>

        {/* ================= RIGHT PANEL ================= */}

        <div className="right-panel">

            <h2>AI Prediction</h2>

            <div className="prediction-box">

                {prediction ? (

                    <>

                        <h1>
                            {prediction.prediction === "No Churn" ? "🟢" : "🔴"}
                        </h1>

                        <h2>{prediction.prediction}</h2>

                        <p><strong>Confidence</strong></p>

                        <h3>
                            {prediction.confidence ?? "N/A"}%
                        </h3>

                        <hr />

                        <p><strong>Risk Level</strong></p>

                        <h3>
                            {prediction.risk ?? "N/A"}
                        </h3>

                        <hr />

                        <p><strong>Recommendation</strong></p>

                        <p>
                            {prediction.recommendation ??
                                "No recommendation available"}
                        </p>

                        <hr />

                        <p><strong>Model</strong></p>

                        <p>
                            {prediction.model ??
                                "Logistic Regression"}
                        </p>

                        <hr />

                        <p><strong>Response Time</strong></p>

                        <p>
                            {prediction.response_time ??
                                "N/A"}
                        </p>

                    </>

                ) : (

                    <>

                        <h1>🤖</h1>

                        <h2>AI Ready</h2>

                        <p>

                            Fill customer details and click
                            <br />
                            <strong>Analyze Customer</strong>

                        </p>

                    </>

                )}

            </div>

        </div>

    </div>

    {/* ================= HISTORY ================= */ }

    <PredictionHistory
        history={history}
    />

    {/* ================= SYSTEM STATUS ================= */ }

    <SystemStatus
        health={health}
    />

    {/* ================= ANALYTICS ================= */ }

<AnalyticsChart />

</div>

);

}

export default Dashboard;