import streamlit as st
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(
    page_title="Soil Stabilization Advisor",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🌱 Soil Stabilization Advisor</h1>', unsafe_allow_html=True)
st.write("Enter soil properties to get optimal stabilization method recommendation")

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Soil Properties")
    
    # Soil type
    soil_type = st.selectbox(
        "Soil Type",
        ["CL (Lean Clay)", "ML (Silt)", "SM (Silty Sand)", "SP (Poor Sand)", "CH (Fat Clay)"]
    )
    
    # Soil composition
    st.subheader("Soil Composition (%)")
    clay = st.slider("Clay", 0, 100, 58)
    silt = st.slider("Silt", 0, 100, 42)
    sand = 100 - clay - silt
    st.info(f"**Sand:** {sand}% (auto-calculated)")
    
    # Other properties
    st.subheader("Other Properties")
    moisture = st.slider("Moisture Content (%)", 0, 50, 15)
    pi = st.slider("Plasticity Index (PI)", 0, 50, 12)
    ph = st.slider("pH Level", 4.0, 10.0, 7.0, 0.1)
    
    # Project requirements
    st.subheader("Project Requirements")
    target_strength = st.number_input("Desired UCS (MPa)", 0.1, 10.0, 1.0, 0.1)
    curing_days = st.selectbox("Curing Time (days)", [7, 14, 28, 56, 90])
    budget = st.selectbox("Budget", ["Low", "Medium", "High"])

# Recommendation logic
def get_recommendation(clay, silt, sand, moisture, pi, ph, soil_type):
    """Simple rule-based recommendation engine"""
    
    results = {}
    
    # Rule 1: Soil type based recommendation
    if clay > 40 or "Clay" in soil_type:
        results['method'] = "Mycelium"
        results['myc_pct'] = 5.0
        results['micp_pct'] = 0.0
        results['strength'] = 0.6  # MPa
        results['reason'] = "Clayey soils respond best to mycelium"
        
    elif sand > 60 or "Sand" in soil_type:
        results['method'] = "MICP"
        results['myc_pct'] = 0.0
        results['micp_pct'] = 2.0
        results['strength'] = 2.0  # MPa
        results['reason'] = "Sandy soils have high permeability for MICP"
        
    else:  # Silty or mixed
        results['method'] = "Hybrid"
        results['myc_pct'] = 15.0
        results['micp_pct'] = 1.0
        results['strength'] = 1.2  # MPa
        results['reason'] = "Mixed soils benefit from combined approach"
    
    # Adjust based on moisture
    if moisture > 25:
        results['strength'] *= 0.8
        results['reason'] += " (reduced due to high moisture)"
    
    # Adjust based on pH for MICP
    if results['method'] in ["MICP", "Hybrid"]:
        if 6.5 <= ph <= 8.5:
            results['strength'] *= 1.3
            results['reason'] += " (enhanced by optimal pH)"
        else:
            results['strength'] *= 0.7
            results['reason'] += " (reduced due to non-optimal pH)"
    
    # Adjust for curing time
    curing_factor = curing_days / 28  # Normalize to 28 days
    results['strength'] *= curing_factor
    
    # Calculate improvement
    base_strength = 0.225  # Untreated soil
    results['improvement'] = ((results['strength'] - base_strength) / base_strength) * 100
    
    return results

# Cost estimation
def estimate_cost(method, myc_pct, micp_pct, budget):
    cost = 0
    if method == "Mycelium":
        cost = 50 + (myc_pct * 3)
    elif method == "MICP":
        cost = 100 + (micp_pct * 20)
    else:  # Hybrid
        cost = 150 + (myc_pct * 2) + (micp_pct * 15)
    
    # Adjust for budget
    if budget == "Low":
        cost *= 0.8
    elif budget == "High":
        cost *= 1.5
    
    return round(cost, 2)

# Main analysis button
if st.button("🔍 Analyze & Recommend", type="primary", use_container_width=True):
    
    # Get recommendations
    rec = get_recommendation(clay, silt, sand, moisture, pi, ph, soil_type)
    cost = estimate_cost(rec['method'], rec['myc_pct'], rec['micp_pct'], budget)
    
    # Display results
    st.markdown("---")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Recommended Method", rec['method'])
    
    with col2:
        st.metric("Predicted UCS", f"{rec['strength']:.3f} MPa")
    
    with col3:
        st.metric("Improvement", f"{rec['improvement']:.1f}%")
    
    with col4:
        st.metric("Estimated Cost", f"${cost}/m³")
    
    # Detailed recommendation
    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
    
    if rec['method'] == "Mycelium":
        st.success(f"""
        **✅ MYCELIUM STABILIZATION RECOMMENDED**
        
        **Optimal Percentage:** {rec['myc_pct']}%
        **Expected UCS:** {rec['strength']:.3f} MPa
        **Improvement:** {rec['improvement']:.1f}% over untreated soil
        
        **📋 Procedure:**
        1. Mix {rec['myc_pct']}% mycelium with soil
        2. Maintain moisture at 15-20%
        3. Cure for {curing_days} days
        4. Protect from direct sunlight
        
        **💡 Tip:** Use C-type fungal strain for maximum strength
        """)
    
    elif rec['method'] == "MICP":
        st.info(f"""
        **✅ MICP (MICROBIAL INDUCED CALCITE PRECIPITATION) RECOMMENDED**
        
        **Chemical Concentration:** {rec['micp_pct']}%
        **Expected UCS:** {rec['strength']:.3f} MPa
        **Improvement:** {rec['improvement']:.1f}% over untreated soil
        
        **📋 Procedure:**
        1. Apply {rec['micp_pct']}% cementation solution
        2. Use Sporosarcina pasteurii bacteria
        3. Apply in 3-5 cycles
        4. Cure for {curing_days} days
        
        **💡 Tip:** Maintain pH between 6.5-8.5 for best results
        """)
    
    else:  # Hybrid
        st.warning(f"""
        **✅ HYBRID APPROACH RECOMMENDED**
        
        **Mycelium:** {rec['myc_pct']}%
        **MICP:** {rec['micp_pct']}%
        **Expected UCS:** {rec['strength']:.3f} MPa
        **Improvement:** {rec['improvement']:.1f}% over untreated soil
        
        **📋 Procedure:**
        1. First apply {rec['myc_pct']}% mycelium, cure for 7 days
        2. Then apply {rec['micp_pct']}% MICP in 3 cycles
        3. Total curing time: {curing_days} days
        
        **💡 Benefit:** Combines organic binding with mineral strength
        """)
    
    st.markdown(f"**Reason:** {rec['reason']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if target is met
    if rec['strength'] >= target_strength:
        st.balloons()
        st.success(f"🎯 **Target achieved!** Your desired strength of {target_strength} MPa is met.")
    else:
        st.warning(f"⚠️ **Target not met.** Desired: {target_strength} MPa, Predicted: {rec['strength']:.3f} MPa")
        st.write("Consider increasing curing time or using higher percentages.")

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Select soil type** from dropdown
    2. **Adjust soil composition** sliders
    3. **Enter other soil properties**
    4. **Set project requirements**
    5. **Click 'Analyze & Recommend' button**
    6. **Review** the recommended method and procedure
    
    **Note:** These recommendations are based on published research data.
    Always conduct site-specific tests before full application.
    """)

# Footer
st.markdown("---")
st.caption("🌱 Soil Stabilization Advisor | Based on BCS, MLS & MBLS Research Data")
