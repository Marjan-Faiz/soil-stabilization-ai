import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Soil Stabilization Advisor",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for better look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #388E3C;
        font-size: 1.5rem;
        margin-top: 1.5rem;
    }
    .recommendation-box {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .metric-box {
        background-color: #F1F8E9;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌱 Soil Stabilization Advisor</h1>', unsafe_allow_html=True)
st.markdown("Enter soil properties to get stabilization recommendations based on research data")

# Sidebar for inputs
with st.sidebar:
    st.markdown("### 🧪 Soil Properties")
    
    # Soil type
    soil_type = st.selectbox(
        "Select Soil Type",
        ["CL (Lean Clay)", "ML (Silt)", "SM (Silty Sand)", "SP (Poorly Graded Sand)", "CH (Fat Clay)"],
        index=0
    )
    
    # Soil composition
    st.markdown("#### Soil Composition (%)")
    col1, col2, col3 = st.columns(3)
    with col1:
        clay = st.number_input("Clay %", 0, 100, 58, key="clay")
    with col2:
        silt = st.number_input("Silt %", 0, 100, 42, key="silt")
    with col3:
        sand = 100 - clay - silt
        st.metric("Sand %", sand)
    
    # Other properties
    st.markdown("#### Other Properties")
    moisture = st.slider("Moisture Content (%)", 0, 50, 13)
    pi = st.slider("Plasticity Index (PI)", 0, 50, 12)
    ph = st.slider("pH Level", 4.0, 10.0, 7.0, 0.1)
    
    # Project requirements
    st.markdown("#### Project Requirements")
    target_strength = st.number_input("Desired UCS (MPa)", 0.1, 10.0, 1.0, 0.1)
    curing_days = st.selectbox("Curing Time (days)", [3, 7, 14, 28, 56, 90], index=3)
    budget = st.selectbox("Budget", ["Low", "Medium", "High", "No Limit"], index=1)

# Rule-based recommendation engine (NO ML REQUIRED)
def calculate_recommendations(clay, silt, sand, moisture, pi, ph, soil_type, curing_days):
    """
    Simple rule-based system based on research data
    """
    
    # Base strength for untreated soil
    base_strength = 0.225  # MPa
    
    # RULE 1: Determine best method based on soil type
    if "Clay" in soil_type or clay > 40:
        primary_method = "Mycelium"
        myc_percentage = 5.0  # Optimal for clay
        micp_percentage = 0.5  # Less effective on clay
    elif "Sand" in soil_type or sand > 60:
        primary_method = "MICP"
        myc_percentage = 25.0  # Higher needed for sand
        micp_percentage = 2.0  # More effective on sand
    else:  # Silt or mixed
        primary_method = "Hybrid"
        myc_percentage = 15.0
        micp_percentage = 1.0
    
    # RULE 2: Adjust based on moisture
    if moisture > 25:
        myc_percentage *= 0.8  # Reduce mycelium for high moisture
    elif moisture < 10:
        micp_percentage *= 1.2  # Increase MICP for low moisture
    
    # RULE 3: Adjust based on pH
    if 6.5 <= ph <= 8.5:
        micp_percentage *= 1.3  # MICP works best in neutral pH
    
    # RULE 4: Adjust based on curing time
    curing_factor = curing_days / 28  # Normalize to 28 days
    myc_percentage *= curing_factor
    micp_percentage *= curing_factor
    
    # Calculate predicted strengths using empirical formulas
    # Based on research data trends
    
    # Mycelium strength formula
    myc_strength = base_strength * (1 + (myc_percentage * 0.04))
    
    # MICP strength formula
    micp_strength = base_strength * (1 + (micp_percentage * 0.8))
    
    # Hybrid strength (synergy effect)
    hybrid_strength = base_strength * (1 + (myc_percentage * 0.02) + (micp_percentage * 0.6)) * 1.2
    
    # Determine if hybrid is needed
    max_strength = max(myc_strength, micp_strength, hybrid_strength)
    
    if max_strength == hybrid_strength and (myc_strength > 0.3 or micp_strength > 0.3):
        final_method = "Hybrid"
        final_strength = hybrid_strength
        final_myc = myc_percentage
        final_micp = micp_percentage
    elif myc_strength > micp_strength:
        final_method = "Mycelium"
        final_strength = myc_strength
        final_myc = myc_percentage
        final_micp = 0
    else:
        final_method = "MICP"
        final_strength = micp_strength
        final_myc = 0
        final_micp = micp_percentage
    
    # Improvement percentage
    improvement = ((final_strength - base_strength) / base_strength) * 100
    
    return {
        'primary_method': primary_method,
        'final_method': final_method,
        'final_strength': final_strength,
        'myc_percentage': final_myc,
        'micp_percentage': final_micp,
        'improvement': improvement,
        'base_strength': base_strength,
        'myc_strength': myc_strength,
        'micp_strength': micp_strength,
        'hybrid_strength': hybrid_strength
    }

# Cost estimation
def estimate_cost(method, myc_pct, micp_pct, budget_level):
    """Estimate cost based on method and percentages"""
    
    base_cost = {
        'Low': 50,
        'Medium': 100,
        'High': 200,
        'No Limit': 300
    }
    
    cost = base_cost.get(budget_level, 100)
    
    if method == "Mycelium":
        cost += myc_pct * 2
    elif method == "MICP":
        cost += micp_pct * 10
    elif method == "Hybrid":
        cost += (myc_pct * 1.5) + (micp_pct * 8)
    
    return cost

# Main analysis
if st.button("🔍 Analyze & Get Recommendations", type="primary", use_container_width=True):
    
    # Calculate recommendations
    results = calculate_recommendations(clay, silt, sand, moisture, pi, ph, soil_type, curing_days)
    
    # Calculate cost
    estimated_cost = estimate_cost(results['final_method'], 
                                  results['myc_percentage'], 
                                  results['micp_percentage'], 
                                  budget)
    
    # Display results in columns
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Recommended Method", results['final_method'])
    
    with col2:
        st.metric("Predicted UCS", f"{results['final_strength']:.3f} MPa")
    
    with col3:
        st.metric("Improvement", f"{results['improvement']:.1f}%")
    
    with col4:
        st.metric("Estimated Cost", f"${estimated_cost:.0f}/m³")
    
    # Detailed recommendations
    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
    st.markdown("### 📋 Detailed Recommendations")
    
    if results['final_method'] == "Mycelium":
        st.success(f"""
        **✅ PRIMARY RECOMMENDATION: MYCELIUM STABILIZATION**
        
        - **Optimal Mycelium Percentage:** {results['myc_percentage']:.1f}%
        - **Expected UCS:** {results['final_strength']:.3f} MPa
        - **Improvement over untreated:** {results['improvement']:.1f}%
        - **Curing Time:** {curing_days} days (optimal: 14-28 days)
        - **Fungal Strain:** C-type recommended (highest strength)
        - **Application Method:** Mix thoroughly with soil, compact lightly
        
        **💡 Additional Notes:**
        • Mycelium works best on clayey soils with moderate moisture
        • Keep moisture around 15-20% during curing
        • Avoid direct sunlight during initial growth phase
        """)
        
    elif results['final_method'] == "MICP":
        st.info(f"""
        **✅ PRIMARY RECOMMENDATION: MICROBIAL INDUCED CALCITE PRECIPITATION**
        
        - **Chemical Concentration:** {results['micp_percentage']:.2f}%
        - **Expected UCS:** {results['final_strength']:.3f} MPa
        - **Improvement over untreated:** {results['improvement']:.1f}%
        - **Curing Time:** {curing_days} days (optimal: 7-14 days)
        - **Recommended Bacteria:** Sporosarcina pasteurii
        - **pH Range:** 6.5-8.5 (current: {ph})
        
        **💡 Additional Notes:**
        • Apply in 3-5 treatment cycles
        • Maintain temperature between 20-30°C
        • Flush with water between cycles
        """)
    
    else:  # Hybrid
        st.warning(f"""
        **✅ PRIMARY RECOMMENDATION: HYBRID APPROACH**
        
        - **Mycelium Percentage:** {results['myc_percentage']:.1f}%
        - **MICP Percentage:** {results['micp_percentage']:.2f}%
        - **Ratio:** {results['myc_percentage']:.0f}:{results['micp_percentage']:.0f}
        - **Expected UCS:** {results['final_strength']:.3f} MPa
        - **Improvement over untreated:** {results['improvement']:.1f}%
        
        **⚡ Application Procedure:**
        1. First, apply mycelium and allow to grow for 5-7 days
        2. Then, apply MICP treatment in 3 cycles
        3. Cure for total {curing_days} days
        
        **💡 Benefits:**
        • Combines organic binding of mycelium
        • Adds mineral strength from calcite
        • Better durability and water resistance
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparison chart
    st.markdown("### 📊 Method Comparison")
    
    # Create comparison data
    comparison_data = pd.DataFrame({
        'Method': ['Untreated', 'Mycelium', 'MICP', 'Hybrid'],
        'Strength (MPa)': [
            results['base_strength'],
            results['myc_strength'],
            results['micp_strength'],
            results['hybrid_strength']
        ],
        'Color': ['#FF6B6B', '#4CAF50', '#2196F3', '#FF9800']
    })
    
    # Create bar chart
    fig = px.bar(
        comparison_data,
        x='Method',
        y='Strength (MPa)',
        color='Method',
        color_discrete_map={
            'Untreated': '#FF6B6B',
            'Mycelium': '#4CAF50',
            'MICP': '#2196F3',
            'Hybrid': '#FF9800'
        },
        text='Strength (MPa)',
        height=400
    )
    
    fig.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside',
        marker_line_color='black',
        marker_line_width=1
    )
    
    fig.update_layout(
        showlegend=False,
        yaxis_title="Compressive Strength (MPa)",
        xaxis_title="",
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Technical details expander
    with st.expander("🔬 Technical Details & Research Basis"):
        st.markdown("""
        **Research Data Basis:**
        
        **Mycelium Stabilization (BCS Data):**
        - Clayey soil (58% clay, 42% silt)
        - 5% mycelium → 0.59 MPa (162% improvement)
        - 15% mycelium → 0.48-0.75 MPa
        - Optimal: 5-10% mycelium with 14+ days curing
        
        **MICP Stabilization:**
        - Sandy soils respond best
        - 1.0-2.0% chemical concentration typical
        - UCS range: 1.2-3.8 MPa
        - pH range: 6.5-8.5 optimal
        
        **Hybrid Approach:**
        - Synergy effect observed
        - 70% Mycelium + 30% MICP often optimal
        - Better durability than single methods
        """)
        
        # Show current soil classification
        st.markdown(f"""
        **Current Soil Analysis:**
        - **USCS Classification:** {soil_type}
        - **Composition:** Clay={clay}%, Silt={silt}%, Sand={sand}%
        - **Moisture:** {moisture}% ({'High' if moisture > 25 else 'Optimal' if 10 <= moisture <= 25 else 'Low'})
        - **Plasticity Index:** {pi} ({'High' if pi > 17 else 'Medium' if 7 <= pi <= 17 else 'Low'})
        - **pH:** {ph} ({'Acidic' if ph < 6.5 else 'Neutral' if 6.5 <= ph <= 8.5 else 'Alkaline'})
        """)

# Quick guide
with st.expander("📖 How to Use This Tool"):
    st.markdown("""
    1. **Select your soil type** from the dropdown
    2. **Adjust soil composition** using sliders or number inputs
    3. **Enter other soil properties** (moisture, PI, pH)
    4. **Set project requirements** (desired strength, curing time, budget)
    5. **Click "Analyze & Get Recommendations"**
    6. **Review** the recommended method, percentages, and technical details
    
    **💡 Tips:**
    - For accurate results, perform laboratory tests on your soil
    - The recommendations are based on published research data
    - Always conduct pilot tests before full-scale application
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌱 <b>Soil Stabilization Advisor</b> | Based on BCS, MLS, and MBLS Research Data</p>
    <p>Note: These are recommendations. Always validate with site-specific testing.</p>
</div>
""", unsafe_allow_html=True)
