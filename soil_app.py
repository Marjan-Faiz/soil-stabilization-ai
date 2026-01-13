import streamlit as st
import pandas as pd
import numpy as np

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Soil Stabilization Advisor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ========== CUSTOM CSS ==========
custom_css = """
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling - FIXED */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FFF8 0%, #E8F5E9 100%);
        border-right: 3px solid #4CAF50;
        min-width: 320px !important;
    }
    
    /* Sidebar headers bold and visible */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #2E7D32 !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Sidebar section headers */
    .sidebar-section-header {
        background: #4CAF50;
        color: white !important;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 15px 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Make all labels bold */
    [data-testid="stSidebar"] label {
        font-weight: bold !important;
        color: #333 !important;
        font-size: 1rem !important;
        margin-top: 10px;
        display: block;
    }
    
    /* Slider styling */
    div[data-testid="stSlider"] > label {
        font-weight: 700 !important;
        color: #2E7D32 !important;
        font-size: 1.1rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1.1rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== SIDEBAR CONTENT ==========
with st.sidebar:
    # Custom sidebar header with icon
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 2.5rem;">🧪</div>
        <h2 style="color: #2E7D32; margin: 10px 0;">Soil Properties</h2>
        <p style="color: #666; font-size: 0.9rem;">Adjust parameters below</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1: Soil Type
    st.markdown('<div class="sidebar-section-header">🌍 Soil Classification</div>', unsafe_allow_html=True)
    soil_type = st.selectbox(
        "**Select Soil Type**",
        ["CL (Lean Clay)", "ML (Silt)", "SM (Silty Sand)", "SP (Poorly Graded Sand)", "CH (Fat Clay)"],
        index=0
    )
    
    # Section 2: Soil Composition
    st.markdown('<div class="sidebar-section-header">📊 Soil Composition (%)</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        clay = st.slider("**Clay**", 0, 100, 58, key="clay_slider")
    with col2:
        silt = st.slider("**Silt**", 0, 100, 42, key="silt_slider")
    with col3:
        sand = 100 - clay - silt
        st.metric("**Sand**", f"{sand}%")
    
    # Section 3: Soil Properties
    st.markdown('<div class="sidebar-section-header">🔬 Soil Properties</div>', unsafe_allow_html=True)
    
    moisture = st.slider("**Moisture Content (%)**", 0, 50, 15, 
                        help="Optimal range: 10-25%")
    pi = st.slider("**Plasticity Index (PI)**", 0, 50, 12,
                  help="PI = Liquid Limit - Plastic Limit")
    ph = st.slider("**pH Level**", 4.0, 10.0, 7.0, 0.1,
                  help="Optimal for MICP: 6.5-8.5")
    
    # Section 4: Project Requirements
    st.markdown('<div class="sidebar-section-header">🏗️ Project Requirements</div>', unsafe_allow_html=True)
    
    target_strength = st.number_input("**Desired UCS (MPa)**", 0.1, 10.0, 1.0, 0.1,
                                     help="Target Unconfined Compressive Strength")
    curing_days = st.selectbox("**Curing Time (days)**", [7, 14, 28, 56, 90],
                              help="Longer curing = Higher strength")
    budget = st.selectbox("**Budget Category**", ["Low", "Medium", "High", "No Limit"],
                         help="Cost consideration")
    
    # Divider
    st.markdown("---")
    
    # Quick tips
    with st.expander("💡 Quick Tips"):
        st.write("""
        - **Clay > 40%:** Mycelium works best
        - **Sand > 60%:** MICP recommended
        - **Moisture 10-25%:** Optimal range
        - **pH 6.5-8.5:** Best for MICP
        - **Curing > 28 days:** Maximum strength gain
        """)

# ========== MAIN CONTENT ==========
# Custom header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #2E7D32; font-size: 2.8rem; margin-bottom: 0.5rem;">🌱 Soil Stabilization Advisor</h1>
    <p style="color: #666; font-size: 1.1rem;">AI-powered tool for optimal soil stabilization method selection</p>
</div>
""", unsafe_allow_html=True)

# Add analyze button at top
col1, col2, col3 = st.columns([1,2,1])
with col2:
    analyze_clicked = st.button("🚀 **ANALYZE & GET RECOMMENDATIONS**", 
                               type="primary", 
                               use_container_width=True,
                               help="Click to analyze soil properties")

# Simple calculation function
def get_recommendation(clay, silt, sand, moisture, pi, ph, soil_type):
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

if analyze_clicked:
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
        improvement = ((rec['strength'] - 0.225) / 0.225) * 100
        st.metric("Improvement", f"{improvement:.1f}%")
    with col4:
        st.metric("Estimated Cost", f"${cost}/m³")
    
    # Detailed recommendation box
    recommendation_box = f"""
    <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin: 20px 0;">
        <h3 style="color: #2E7D32; margin-top: 0;">✅ {rec['method']} STABILIZATION RECOMMENDED</h3>
    """
    
    if rec['method'] == "Mycelium":
        recommendation_box += f"""
        <p><b>Optimal Mycelium Percentage:</b> {rec['myc_pct']}%</p>
        <p><b>Expected UCS:</b> {rec['strength']:.3f} MPa</p>
        <p><b>Procedure:</b> Mix {rec['myc_pct']}% mycelium with soil, maintain moisture 15-20%, cure for {curing_days} days</p>
        """
    elif rec['method'] == "MICP":
        recommendation_box += f"""
        <p><b>Chemical Concentration:</b> {rec['micp_pct']}%</p>
        <p><b>Expected UCS:</b> {rec['strength']:.3f} MPa</p>
        <p><b>Procedure:</b> Apply {rec['micp_pct']}% cementation solution in 3-5 cycles, cure for {curing_days} days</p>
        """
    else:
        recommendation_box += f"""
        <p><b>Mycelium:</b> {rec['myc_pct']}% | <b>MICP:</b> {rec['micp_pct']}%</p>
        <p><b>Expected UCS:</b> {rec['strength']:.3f} MPa</p>
        <p><b>Procedure:</b> Apply mycelium first (7 days), then MICP in 3 cycles, total {curing_days} days curing</p>
        """
    
    recommendation_box += f"""
        <p><b>Reason:</b> {rec['reason']}</p>
    </div>
    """
    
    st.markdown(recommendation_box, unsafe_allow_html=True)
    
    # Check target
    if rec['strength'] >= target_strength:
        st.success(f"🎯 **Target achieved!** Desired strength: {target_strength} MPa")
    else:
        st.warning(f"⚠️ **Target not met.** Desired: {target_strength} MPa | Predicted: {rec['strength']:.3f} MPa")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; background: #F8FFF8; border-radius: 10px;">
    <p style="color: #666; margin: 0;">🌱 <b>Soil Stabilization Advisor v1.0</b></p>
    <p style="color: #888; font-size: 0.9rem; margin: 5px 0;">For research and educational purposes</p>
    <p style="color: #888; font-size: 0.8rem; margin: 0;">© 2024 | All calculations based on published research data</p>
</div>
""", unsafe_allow_html=True)
