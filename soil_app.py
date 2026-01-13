import streamlit as st
import pandas as pd
import numpy as np

# ========== REMOVE STREAMLIT BRANDING ==========
def hide_streamlit_branding():
    """Hide Streamlit branding elements"""
    hide_css = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    #stDecoration {display: none;}
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Soil Stabilization Advisor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
custom_css = """
<style>
    .main-header {
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
    .custom-footer {
        text-align: center;
        margin-top: 50px;
        color: #666;
        font-size: 0.9rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    # Hide Streamlit branding
    hide_streamlit_branding()
    
    # Custom header
    st.markdown('<h1 class="main-header">🌱 Soil Stabilization Advisor</h1>', unsafe_allow_html=True)
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
        st.info(f"**Sand:** {sand}%")
        
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
    
    # Simple calculation function
    def get_recommendation(clay, silt, moisture, pi, ph, soil_type):
        """Simple rule-based recommendation"""
        if clay > 40 or "Clay" in soil_type:
            return {
                'method': "Mycelium",
                'myc_pct': 5.0,
                'micp_pct': 0.0,
                'strength': 0.6,
                'reason': "Clayey soils respond best to mycelium"
            }
        elif sand > 60:
            return {
                'method': "MICP",
                'myc_pct': 0.0,
                'micp_pct': 2.0,
                'strength': 2.0,
                'reason': "Sandy soils have high permeability for MICP"
            }
        else:
            return {
                'method': "Hybrid",
                'myc_pct': 15.0,
                'micp_pct': 1.0,
                'strength': 1.2,
                'reason': "Mixed soils benefit from combined approach"
            }
    
    # Cost estimation
    def estimate_cost(method, myc_pct, micp_pct, budget):
        cost = 0
        if method == "Mycelium":
            cost = 50 + (myc_pct * 3)
        elif method == "MICP":
            cost = 100 + (micp_pct * 20)
        else:  # Hybrid
            cost = 150 + (myc_pct * 2) + (micp_pct * 15)
        
        if budget == "Low":
            cost *= 0.8
        elif budget == "High":
            cost *= 1.5
        
        return round(cost, 2)
    
    # Main analysis button
    if st.button("🔍 Analyze & Recommend", type="primary", use_container_width=True):
        # Get recommendations
        rec = get_recommendation(clay, silt, moisture, pi, ph, soil_type)
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
            improvement = ((rec['strength'] - 0.225) / 0.225) * 100
            st.metric("Improvement", f"{improvement:.1f}%")
        with col4:
            st.metric("Estimated Cost", f"${cost}/m³")
        
        # Detailed recommendation
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        
        if rec['method'] == "Mycelium":
            st.success(f"""
            **✅ MYCELIUM STABILIZATION RECOMMENDED**
            
            **Optimal Percentage:** {rec['myc_pct']}%
            **Expected UCS:** {rec['strength']:.3f} MPa
            
            **📋 Procedure:**
            1. Mix {rec['myc_pct']}% mycelium with soil
            2. Maintain moisture at 15-20%
            3. Cure for {curing_days} days
            
            **Reason:** {rec['reason']}
            """)
        elif rec['method'] == "MICP":
            st.info(f"""
            **✅ MICP RECOMMENDED**
            
            **Chemical Concentration:** {rec['micp_pct']}%
            **Expected UCS:** {rec['strength']:.3f} MPa
            
            **📋 Procedure:**
            1. Apply {rec['micp_pct']}% cementation solution
            2. Use Sporosarcina pasteurii bacteria
            3. Apply in 3-5 cycles
            
            **Reason:** {rec['reason']}
            """)
        else:
            st.warning(f"""
            **✅ HYBRID APPROACH RECOMMENDED**
            
            **Mycelium:** {rec['myc_pct']}%
            **MICP:** {rec['micp_pct']}%
            **Expected UCS:** {rec['strength']:.3f} MPa
            
            **📋 Procedure:**
            1. Apply mycelium first, cure for 7 days
            2. Then apply MICP in 3 cycles
            3. Total curing: {curing_days} days
            
            **Reason:** {rec['reason']}
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check target
        if rec['strength'] >= target_strength:
            st.success(f"🎯 **Target achieved!** Desired: {target_strength} MPa")
        else:
            st.warning(f"⚠️ **Target not met.** Desired: {target_strength} MPa, Predicted: {rec['strength']:.3f} MPa")
    
    # Custom footer
    st.markdown("""
    <div class="custom-footer">
    <hr>
    <p>🌱 <b>Soil Stabilization Advisor v1.0</b> | Geotechnical Engineering Tool</p>
    <p>© 2024 | For research and educational purposes</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
