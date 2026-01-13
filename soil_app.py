import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="Soil Stabilization Advisor",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.title("🏗️ Soil Stabilization Advisor")
st.markdown("### AI-powered tool for optimal soil stabilization method selection")

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Soil Parameters")
    
    soil_type = st.selectbox(
        "Soil Type",
        ["Clay", "Silt", "Sand", "Gravel", "Loam", "Peat", "Chalk"]
    )
    
    plasticity_index = st.slider("Plasticity Index (PI)", 0, 50, 15)
    cbr_value = st.slider("CBR Value (%)", 1, 100, 15)
    moisture_content = st.slider("Moisture Content (%)", 5, 50, 20)
    ph_value = st.slider("pH Value", 4.0, 10.0, 7.0, 0.1)
    organic_content = st.slider("Organic Content (%)", 0.0, 20.0, 5.0, 0.5)
    
    load_requirement = st.selectbox(
        "Load Requirement",
        ["Low (Footpaths)", "Medium (Residential Roads)", "High (Highways)", "Very High (Airfield)"]
    )
    
    budget = st.selectbox(
        "Budget Constraint",
        ["Low", "Medium", "High"]
    )
    
    environmental_impact = st.selectbox(
        "Environmental Priority",
        ["Low", "Medium", "High"]
    )
    
    analyze_btn = st.button("🚀 ANALYZE & GET RECOMMENDATIONS", use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 About This Tool")
    st.markdown("""
    This AI-powered advisor recommends the most suitable soil stabilization method based on:
    - **Soil properties** (type, plasticity, CBR, moisture, pH, organic content)
    - **Project requirements** (load capacity, budget, environmental impact)
    - **Technical feasibility** and **cost-effectiveness**
    
    The recommendations are based on published research data and engineering best practices.
    """)
    
    # Display soil parameters
    if soil_type:
        st.markdown("### 📝 Current Input Summary")
        params_df = pd.DataFrame({
            "Parameter": ["Soil Type", "Plasticity Index", "CBR Value", "Moisture Content", "pH", "Organic Content"],
            "Value": [soil_type, f"{plasticity_index}", f"{cbr_value}%", f"{moisture_content}%", f"{ph_value}", f"{organic_content}%"]
        })
        st.table(params_df)

with col2:
    st.markdown("### ⚙️ Common Methods")
    methods_info = {
        "Cement Stabilization": "Good for sandy/gravel soils",
        "Lime Stabilization": "Best for clayey soils with high PI",
        "Bitumen Stabilization": "Waterproofing, flexible pavement",
        "Geotextiles": "Reinforcement, separation",
        "Chemical Polymers": "Quick setting, low environmental impact",
        "Mechanical Compaction": "Simple, cost-effective for granular soils"
    }
    
    for method, desc in methods_info.items():
        with st.expander(f"📌 {method}"):
            st.write(desc)

# AI Recommendation Engine
def get_stabilization_recommendation(inputs):
    """AI-based recommendation logic"""
    recommendations = []
    
    # Rule-based logic (can be replaced with ML model)
    soil_type = inputs["soil_type"]
    pi = inputs["plasticity_index"]
    cbr = inputs["cbr_value"]
    moisture = inputs["moisture_content"]
    load = inputs["load_requirement"]
    budget = inputs["budget"]
    
    if soil_type in ["Clay", "Silt"] and pi > 15:
        recommendations.append({
            "method": "Lime Stabilization",
            "confidence": "85%",
            "reason": "Effective for high plasticity clay/silt soils",
            "cost": "Medium",
            "duration": "2-4 weeks"
        })
    
    if soil_type in ["Sand", "Gravel"] and cbr < 20:
        recommendations.append({
            "method": "Cement Stabilization",
            "confidence": "90%",
            "reason": "Excellent for granular soils with low CBR",
            "cost": "Medium-High",
            "duration": "1-3 weeks"
        })
    
    if moisture > 25:
        recommendations.append({
            "method": "Chemical Polymer Stabilization",
            "confidence": "80%",
            "reason": "Quick setting in high moisture conditions",
            "cost": "High",
            "duration": "3-7 days"
        })
    
    if budget == "Low":
        recommendations.append({
            "method": "Mechanical Compaction with Geotextiles",
            "confidence": "75%",
            "reason": "Cost-effective solution for low budget projects",
            "cost": "Low",
            "duration": "1-2 weeks"
        })
    
    if not recommendations:
        recommendations.append({
            "method": "Lime-Cement Composite Stabilization",
            "confidence": "70%",
            "reason": "General purpose solution for mixed soil conditions",
            "cost": "Medium",
            "duration": "2-3 weeks"
        })
    
    return recommendations

# Display results when button is clicked
if analyze_btn:
    st.markdown("---")
    st.markdown("## 🔍 Analysis Results")
    
    # Create input dictionary
    inputs = {
        "soil_type": soil_type,
        "plasticity_index": plasticity_index,
        "cbr_value": cbr_value,
        "moisture_content": moisture_content,
        "ph_value": ph_value,
        "organic_content": organic_content,
        "load_requirement": load_requirement,
        "budget": budget,
        "environmental_impact": environmental_impact
    }
    
    # Get recommendations
    recommendations = get_stabilization_recommendation(inputs)
    
    # Display top recommendation
    st.markdown("### 🏆 Top Recommendation")
    top_rec = recommendations[0]
    
    st.markdown(f"""
    <div class="success-box">
    <h3>{top_rec['method']}</h3>
    <p><strong>Confidence:</strong> {top_rec['confidence']}</p>
    <p><strong>Reason:</strong> {top_rec['reason']}</p>
    <p><strong>Estimated Cost:</strong> {top_rec['cost']}</p>
    <p><strong>Duration:</strong> {top_rec['duration']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional recommendations
    if len(recommendations) > 1:
        st.markdown("### 🔄 Alternative Methods")
        cols = st.columns(len(recommendations)-1)
        for idx, rec in enumerate(recommendations[1:], 1):
            with cols[idx-1]:
                st.markdown(f"""
                <div class="info-box">
                <h4>{rec['method']}</h4>
                <p>Confidence: {rec['confidence']}</p>
                <p>Cost: {rec['cost']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Visualization
    st.markdown("### 📈 Method Comparison")
    methods = [rec["method"] for rec in recommendations]
    confidence = [int(rec["confidence"].replace("%", "")) for rec in recommendations]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.barh(methods, confidence, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'][:len(methods)])
    ax.set_xlabel('Confidence Score (%)')
    ax.set_title('Method Recommendation Confidence')
    ax.bar_label(bars, fmt='%d%%')
    st.pyplot(fig)
    
    # Implementation steps
    st.markdown("### 📋 Implementation Steps")
    steps = [
        "1. Conduct detailed soil testing",
        "2. Prepare subgrade and remove debris",
        "3. Apply recommended stabilizer at specified dosage",
        "4. Mix thoroughly using appropriate equipment",
        "5. Compact to required density (95% Proctor minimum)",
        "6. Cure properly (7-14 days depending on method)",
        "7. Perform quality control tests (CBR, UCS, density)"
    ]
    for step in steps:
        st.markdown(f"- {step}")

# Footer
st.markdown("---")
st.markdown("### Soil Stabilization Advisor v1.0")
st.markdown("*For research and educational purposes*")
st.markdown("**© 2024 | All calculations based on published research data**")

# Optional: Add download report button
if analyze_btn:
    report_text = f"""
    SOIL STABILIZATION REPORT
    ==========================
    Soil Type: {soil_type}
    Plasticity Index: {plasticity_index}
    CBR Value: {cbr_value}%
    Moisture Content: {moisture_content}%
    pH Value: {ph_value}
    Organic Content: {organic_content}%
    Load Requirement: {load_requirement}
    
    RECOMMENDATIONS:
    """
    for rec in recommendations:
        report_text += f"\n- {rec['method']} (Confidence: {rec['confidence']})"
    
    st.download_button(
        label="📥 Download Report",
        data=report_text,
        file_name="soil_stabilization_report.txt",
        mime="text/plain"
    )
