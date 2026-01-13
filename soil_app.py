# Add this at the top of your app
def hide_streamlit_branding():
    """Completely hide Streamlit branding"""
    hide_css = """
    <style>
    /* Hide all Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide deploy button */
    .stDeployButton {display: none;}
    
    /* Hide hamburger menu */
    #root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(3) > div > div {display: none;}
    
    /* Hide Streamlit decoration */
    #stDecoration {display: none;}
    
    /* Hide 'made with streamlit' */
    .viewerBadge_link__qRIco {display: none;}
    .viewerBadge_container__r5tak {display: none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {width: 10px;}
    ::-webkit-scrollbar-track {background: #f1f1f1;}
    ::-webkit-scrollbar-thumb {background: #4CAF50;}
    ::-webkit-scrollbar-thumb:hover {background: #2E7D32;}
    
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)

# Call the function
hide_streamlit_branding()
