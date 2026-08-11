import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        result = predict_resources(
            application_type=request.application_type,
            expected_users_per_day=request.expected_users_per_day,
            concurrent_users=request.concurrent_users,
            storage_required_gb=request.storage_required_gb,
            deployment_region=request.deployment_region,
            traffic_pattern=request.traffic_pattern
        )

        return PredictionResponse(
            predicted_vcpu=result["Predicted vCPU"],
            predicted_ram_gb=result["Predicted RAM (GB)"],
            cloud_provider=result.get("cloud_provider"),
            recommended_vm=result.get("Recommended VM"),
            price_per_hour_usd=result.get("Price per Hour ($)"),
            monthly_cost_usd=result.get("Total Monthly Cost ($)"),
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
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)