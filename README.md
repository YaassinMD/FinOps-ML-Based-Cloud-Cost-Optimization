# FinOps AI - Cloud Cost Optimizer

FinOps AI is an AI-powered cloud cost optimization system that predicts the cloud compute resources (vCPU, RAM) required for an application based on its workload characteristics, and recommends the most suitable and cost-effective virtual machine (VM) instance across AWS, Azure, and GCP, along with estimated cloud costs.

---

## Features

- **Workload Resource Prediction:** Predicts required vCPU and RAM capacity using a trained Machine Learning model.
- **Cheapest VM Recommendation:** Evaluates and recommends the cheapest suitable VM from AWS, Azure, and GCP instance catalogs.
- **Dynamic Cost Projection:** Estimates hourly, monthly, and yearly costs, combining VM compute rates and SSD block storage costs ($0.10/GB-month).
- **FastAPI Backend Integration:** Scalable REST API with Pydantic validation and interactive auto-generated Swagger docs.
- **Streamlit Dashboard Frontend:** Modern, clean, dark-themed user interface with interactive sliders and visual metric cards.

---

## Project Structure

```text
FinOps_AI/
│
├── backend/                  # FastAPI Backend API
│   ├── main.py               # API routing, CORS middleware, and inference endpoint
│   └── schemas.py            # Pydantic validation schemas for requests/responses
│
├── frontend/                 # Streamlit UI Dashboard
│   └── app.py                # Dashboard inputs, API calls, and metric cards
│
├── datasets/                 # Training Dataset
│   └── ml_training_dataset_v3_cleaned.csv
│
├── jupyter/                  # ML Development Notebooks
│   ├── 01_EDA.ipynb          # Exploratory Data Analysis
│   ├── 02_Preprocessing.ipynb# Data preprocessing and cleaning
│   ├── 03_ModelTraining.ipynb# Model training
│   ├── 04_ModelTesting.ipynb # Model verification
│   └── 05_ModelVisualization.ipynb # Feature importances and visualization
│
├── ml/                       # ML Prediction Module
│   ├── predict.py            # Inference runner and cost estimation formula
│   ├── preprocess.py         # One-hot encoder aligning user inputs
│   └── vm_catalog.csv        # Cloud instance spec and pricing catalog
│
├── models/                   # Trained ML Models
│   ├── cloud_model.pkl       # Saved RandomForest model
│   └── model_features.pkl    # Saved model feature column mappings
│
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Technology Stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **Frontend:** Streamlit, Requests
- **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib, Matplotlib

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MilinManu/Finops_AI.git
cd Finops_AI
```

### 2. Install Dependencies
Make sure you have Python 3.11+ installed, then run:
```bash
pip install -r requirements.txt
```

---

## How to Run

To run the application, you will need to start both the backend API and the frontend dashboard in separate terminal windows.

### Step 1: Start the FastAPI Backend
From the project root directory, run:
```bash
python -m uvicorn backend.main:app --reload
```
- **API Base URL:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`
- **Alternative ReDoc Docs:** `http://127.0.0.1:8000/redoc`

### Step 2: Start the Streamlit Frontend
From the project root directory in a new terminal, run:
```bash
streamlit run frontend/app.py
```
- **Streamlit Local URL:** `http://localhost:8501`

---

## API Specifications

### `POST /api/predict`
Queries the prediction engine to evaluate required resources and recommend a VM.

**Request Body (`PredictionRequest`):**
```json
{
  "application_type": "E-Commerce",
  "expected_users_per_day": 25000,
  "concurrent_users": 600,
  "storage_required_gb": 300,
  "deployment_region": "ap-south-1",
  "traffic_pattern": "High"
}
```

**Response Body (`PredictionResponse`):**
```json
{
  "predicted_vcpu": 2,
  "predicted_ram_gb": 4,
  "cloud_provider": "GCP",
  "recommended_vm": "e2-medium",
  "price_per_hour_usd": 0.033,
  "monthly_cost_usd": 53.76,
  "yearly_cost_usd": 645.12
}
```

---

## Cost Calculation Architecture

The total monthly cost is computed by combining:
1. **VM Compute Rate:** The hourly instance rate fetched from the `vm_catalog.csv` catalog, mapped to 720 hours/month ($24 \text{ hours} \times 30 \text{ days}$).
2. **SSD Storage Volume Rate:** Evaluated at a standard SSD block storage rate of **$0.10/GB per month**.

$$\text{Total Monthly Cost} = (\text{VM Hourly Price} \times 24 \times 30) + (\text{Storage Required (GB)} \times \$0.10)$$

---

## Future Enhancements

- **Model Retraining & Fine-tuning:** Incorporate and tune feature weights (like concurrent users and region coefficients) in the RandomForest training dataset to distribute prediction weights beyond `expected_users_per_day`.
- **Real-Time Pricing APIs:** Integrate cloud provider pricing APIs (e.g., AWS Price List API) to pull live, region-specific VM pricing.
- **Kubernetes Optimization:** Add recommendation support for container pods and Kubernetes autoscaling limits.
- **Multi-Cloud Comparison:** Show side-by-side cost comparisons for the same workload on AWS vs Azure vs GCP.