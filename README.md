# FinOps AI

## Overview

FinOps AI is an AI-powered cloud cost optimization system that predicts the cloud resources required for an application and recommends the most suitable virtual machine (VM) along with estimated cloud costs.

The project helps organizations optimize cloud infrastructure by predicting the required vCPU and RAM based on workload characteristics.

---

# Features

- Predict required vCPU and RAM using Machine Learning
- Recommend the best VM configuration
- Support for AWS, Azure and GCP
- Estimate hourly, monthly and yearly cloud cost
- FastAPI backend integration
- Frontend for user interaction

---

# Project Structure

```
FinOps_AI/
│
├── backend/          # FastAPI Backend
├── frontend/         # Frontend Application
├── datasets/         # Dataset
├── jupyter/          # ML Development Notebooks
├── ml/               # ML Prediction Module
├── models/           # Trained ML Models
├── requirements.txt
└── README.md
```

---

# Machine Learning Module

The ML module predicts the cloud resources required by an application.

### Files

```
ml/
│
├── predict.py
├── preprocess.py
├── vm_catalog.csv
```

---

# Trained Models

```
models/

cloud_model.pkl
model_features.pkl
```

---

# Main Function

```python
from ml.predict import predict_resources
```

---

# Function Parameters

```python
predict_resources(
    application_type,
    expected_users_per_day,
    concurrent_users,
    storage_required_gb,
    deployment_region,
    traffic_pattern,
    cloud_provider
)
```

---

# Example

```python
from ml.predict import predict_resources

result = predict_resources(
    application_type="E-Commerce",
    expected_users_per_day=25000,
    concurrent_users=600,
    storage_required_gb=300,
    deployment_region="ap-south-1",
    traffic_pattern="High",
    cloud_provider="AWS"
)

print(result)
```

---

# Output

```python
{
    "predicted_vcpu": 2,
    "predicted_ram_gb": 4,
    "recommended_vm": "t3.medium",
    "price_per_hour_usd": 0.0416,
    "monthly_cost_usd": 29.95,
    "yearly_cost_usd": 359.40
}
```

---

# Machine Learning Workflow

1. Data Collection
2. Data Preprocessing
3. Feature Engineering
4. Model Training
5. Resource Prediction
6. VM Recommendation
7. Cost Estimation

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- FastAPI
- Streamlit
- Git
- GitHub

---

# Installation

Clone the repository

```bash
git clone https://github.com/MilinManu/Finops_AI.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the prediction module

```bash
python ml/predict.py
```

---

# Team Members

- Backend Developer
- Frontend Developer
- ML Engineer
- Database/Cloud Engineer

---

# Future Enhancements

- Real-time cloud pricing APIs
- Region-wise VM pricing
- Kubernetes resource recommendations
- Auto-scaling recommendations
- Multi-cloud cost comparison
- FinOps dashboard and analytics