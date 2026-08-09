import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure the parent and ml directories are in sys.path to load modules correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, "ml"))

from ml.predict import predict_resources
from backend.schemas import PredictionRequest, PredictionResponse

app = FastAPI(
    title="FinOps AI Cost Optimizer API",
    description="API to predict cloud resource requirements and recommend cost-effective virtual machines.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the FinOps AI Cost Optimizer API. Visit /docs for documentation."
    }

@app.post("/api/predict", response_model=PredictionResponse)
def predict_cloud_resources(request: PredictionRequest):
    try:
        # Call the machine learning inference engine
        result = predict_resources(
            application_type=request.application_type,
            expected_users_per_day=request.expected_users_per_day,
            concurrent_users=request.concurrent_users,
            storage_required_gb=request.storage_required_gb,
            deployment_region=request.deployment_region,
            traffic_pattern=request.traffic_pattern
        )
        
        # Map raw prediction dictionary keys to our PredictionResponse schema
        return PredictionResponse(
            predicted_vcpu=result["Predicted vCPU"],
            predicted_ram_gb=result["Predicted RAM (GB)"],
            cloud_provider=result.get("cloud_provider"),
            recommended_vm=result.get("Recommended VM"),
            price_per_hour_usd=result.get("Price per Hour ($)"),
            monthly_cost_usd=result.get("Monthly Cost ($)"),
            yearly_cost_usd=result.get("Yearly Cost ($)")
        )
    except KeyError as ke:
        raise HTTPException(
            status_code=500,
            detail=f"Inference output missing expected key: {str(ke)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during prediction: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
