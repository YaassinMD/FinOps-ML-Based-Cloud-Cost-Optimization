import pandas as pd
import joblib

import os
from preprocess import preprocess_input
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and feature columns only once
model = joblib.load(os.path.join(BASE_DIR, "..", "models", "cloud_model.pkl"))
feature_columns = joblib.load(os.path.join(BASE_DIR, "..", "models", "model_features.pkl"))


# -------------------------------
# VM Recommendation
# -------------------------------
vm_catalog = pd.read_csv(
    os.path.join(BASE_DIR, "vm_catalog.csv")
)
def recommend_vm(predicted_vcpu, predicted_ram):

    suitable = vm_catalog[
        (vm_catalog["vcpu"] >= predicted_vcpu) &
        (vm_catalog["ram_gb"] >= predicted_ram)
    ]

    if suitable.empty:
        return None

    # Choose the cheapest suitable VM
    best = suitable.sort_values("price_per_hour").iloc[0]

    return (
        str(best["provider"]),
        str(best["vm_type"]),
        float(best["price_per_hour"])
    )
# def recommend_vm(vcpu, ram):
#     if vcpu <= 2 and ram <= 4:
#         return "AWS t3.medium", 0.0416

#     elif vcpu <= 4 and ram <= 8:
#         return "AWS t3.xlarge", 0.1664

#     elif vcpu <= 8 and ram <= 16:
#         return "AWS c5.2xlarge", 0.34

#     else:
#         return "AWS c5.4xlarge", 0.68


# -------------------------------
# Prediction Function
# -------------------------------
#  """
#     Predicts required cloud resources and recommends a VM.

#     Returns:
#         dict:
#             Predicted vCPU
#             Predicted RAM
#             Recommended VM
#             Price per Hour
#             Monthly Cost
#             Yearly Cost
#     """
def predict_resources(
    application_type,
    expected_users_per_day,
    concurrent_users,
    storage_required_gb,
    deployment_region,
    traffic_pattern
    
):
    

    # Create input dataframe
    input_df = pd.DataFrame([{
        "application_type": application_type,
        "expected_users_per_day": expected_users_per_day,
        "concurrent_users": concurrent_users,
        "storage_required_gb": storage_required_gb,
        "deployment_region": deployment_region,
        "traffic_pattern": traffic_pattern
    }])

    # One-hot encode
    

    input_df = preprocess_input(
        input_df,
        feature_columns
    )

    # Predict
    prediction = model.predict(input_df)

    predicted_vcpu = max(1, int(round(prediction[0][0])))
    predicted_ram = max(1, int(round(prediction[0][1])))

    # Recommend VM
    cloud_provider, vm_type, price_per_hour = recommend_vm(
        predicted_vcpu,
        predicted_ram
    )

    monthly_cost = float(round(price_per_hour * 24 * 30, 2))
    yearly_cost = float(round(monthly_cost * 12, 2))

    return {
        "Predicted vCPU": predicted_vcpu,
        "Predicted RAM (GB)": predicted_ram,
        "cloud_provider": cloud_provider,
        "Recommended VM": vm_type,
        "Price per Hour ($)": price_per_hour,
        "Monthly Cost ($)": monthly_cost,
        "Yearly Cost ($)": yearly_cost
    }
# comment this main before integrating wit fastapi
#used only for local testing 
if __name__ == "__main__":
    # print("Program Started")

    result = predict_resources(
        application_type="Blog",
        expected_users_per_day=1000,
        concurrent_users=30,
        storage_required_gb=20,
        deployment_region="ap-south-1",
        traffic_pattern="Low",
        
     )

    print(result)