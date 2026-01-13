import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# ========== HIDE STREAMLIT BRANDING ==========
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
#stDecoration {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .app-footer {
        text-align: center;
        margin-top: 50px;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== APP CODE ==========
# (Yeh aapka existing app code yahan paste karein)
# ...

# ========== CUSTOM FOOTER ==========
st.markdown("""
<div class="app-footer">
<hr>
<p>🌱 <b>Soil Stabilization Advisor v1.0</b></p>
<p>Developed for Civil Engineering Applications</p>
<p>© 2024 All rights reserved</p>
</div>
""", unsafe_allow_html=True)
