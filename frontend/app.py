import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="FinOps AI - Cost Optimizer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling
st.markdown("""
<style>
    /* Main background and fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Gradient Title banner */
    .title-banner {
        background: linear-gradient(135deg, #1f4068, #162447, #070d19);
        color: #e4e4e4;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .title-banner h1 {
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .title-banner p {
        font-weight: 300;
        font-size: 1.1rem;
        color: #b0c4de;
    }

    /* Metric Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        border-color: #00adb5;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00adb5;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Recommendation Card styling */
    .rec-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
        border: 2px solid #00adb5;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 173, 181, 0.15);
    }

    .rec-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e4e4e4;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
    }
    
    .rec-item {
        font-size: 1.1rem;
        margin-bottom: 0.6rem;
        color: #d1d1d1;
    }
    
    .rec-item strong {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Title Banner
st.markdown("""
<div class="title-banner">
    <h1>FinOps AI Cost Optimizer</h1>
    <p>Predict cloud resource requirements and identify the most suitables virtual machines and cost estimates.</p>
</div>
""", unsafe_allow_html=True)

# Define dropdown choices aligned with the model's features
APPLICATION_TYPES = [
    "E-Commerce",
    "Blog",
    "CRM",
    "Banking",
    "ERP",
    "Healthcare",
    "News Portal",
    "Portfolio",
    "Social Media",
    "Streaming"
]

REGIONS = [
    "asia-south",
    "us-east",
    "us-west"
]

TRAFFIC_PATTERNS = [
    "High",
    "Medium",
    "Low"
]

# Set up layout
col_inputs, col_results = st.columns([1, 1.2], gap="large")

with col_inputs:
    st.subheader("Workload Specifications")
    
    with st.form("input_form"):
        # Application Characteristics
        application_type = st.selectbox(
            "Application Type",
            options=APPLICATION_TYPES,
            index=0,
            help="Select the type of application you are running."
        )
        
        # User details
        expected_users_per_day = st.number_input(
            "Expected Users per Day",
            min_value=1,
            max_value=100000000,
            value=10000,
            step=1000,
            help="Approximate number of unique users accessing the app daily."
        )
        
        concurrent_users = st.number_input(
            "Peak Concurrent Users",
            min_value=1,
            max_value=5000000,
            value=250,
            step=50,
            help="Expected peak concurrent active users."
        )
        
        # Storage required
        storage_required_gb = st.slider(
            "Storage Required (GB)",
            min_value=1,
            max_value=5000,
            value=100,
            step=10,
            help="Volume size needed in gigabytes."
        )
        
        # Region
        deployment_region = st.selectbox(
            "Deployment Region",
            options=REGIONS,
            index=0,
            help="Target deployment region."
        )
        
        # Traffic pattern
        traffic_pattern = st.selectbox(
            "Traffic Pattern",
            options=TRAFFIC_PATTERNS,
            index=1,
            help="Workload traffic intensity."
        )
        
        submit_button = st.form_submit_button(
            "Optimize Cloud Resources 🚀",
            use_container_width=True
        )

with col_results:
    st.subheader("Optimization Recommendations")
    
    if submit_button:
        # Prepare request payload
        payload = {
            "application_type": application_type,
            "expected_users_per_day": int(expected_users_per_day),
            "concurrent_users": int(concurrent_users),
            "storage_required_gb": int(storage_required_gb),
            "deployment_region": deployment_region,
            "traffic_pattern": traffic_pattern
        }
        
        try:
            # Query FastAPI backend
            backend_url = "http://127.0.0.1:8000/api/predict"
            response = requests.post(
                backend_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Show results in a clean grid
                col_cpu, col_ram = st.columns(2)
                
                with col_cpu:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{result['predicted_vcpu']}</div>
                        <div class="metric-label">Predicted vCPUs</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_ram:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{result['predicted_ram_gb']} GB</div>
                        <div class="metric-label">Predicted RAM</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Render recommendation details
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-title">Recommended Configuration</div>
                    <div class="rec-item">Cloud Provider: <strong>{result['cloud_provider']}</strong></div>
                    <div class="rec-item">VM Instance Type: <strong>{result['recommended_vm']}</strong></div>
                    <div class="rec-item">Hourly Price: <strong>${result['price_per_hour_usd']:.4f} / hr</strong></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Render cost breakdown
                st.markdown("### Estimated Cost Breakdown")
                col_hr, col_mo, col_yr = st.columns(3)
                
                with col_hr:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">${result['price_per_hour_usd']:.3f}</div>
                        <div class="metric-label">Hourly Cost</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_mo:
                    st.markdown(f"""
                    <div class="metric-card" style="border-color: #00adb5;">
                        <div class="metric-value" style="color: #00adb5;">${result['monthly_cost_usd']:.2f}</div>
                        <div class="metric-label">Monthly Cost</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_yr:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">${result['yearly_cost_usd']:.2f}</div>
                        <div class="metric-label">Yearly Cost</div>
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                st.error(f"Error {response.status_code}: Could not fetch recommendations. Please check backend logs.")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI backend. Please make sure the server is running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            
    else:
        # Placeholder before form submission
        st.info("👈 Enter your application details and click 'Optimize Cloud Resources' to see recommendations.")
        
        # Show a summary list of features supported
        st.markdown("""
        ### Features Include:
        - **Automatic Spec Estimation:** Machine learning predicts vCPU and RAM requirements based on your expected traffic levels.
        - **Cheapest VM Selection:** Evaluates AWS, GCP, and Azure pricing tables to find the most cost-effective match.
        - **Billing Projections:** See instant hourly, monthly, and yearly cost breakdowns.
        """)
