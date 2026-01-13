# Add this in sidebar CSS
st.markdown("""
<style>
    /* Add permanent toggle icon */
    .sidebar-toggle {
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 1.5rem;
        color: #4CAF50;
        cursor: pointer;
        z-index: 1000;
    }
</style>

<div class="sidebar-toggle">☰</div>
""", unsafe_allow_html=True)
