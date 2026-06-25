import streamlit as st
from utils.formatters import format_value


# ==========================================
# GLOBAL CSS
# ==========================================
def inject_css():

    st.markdown("""
    <style>

    /* ==================================
       HIDE STREAMLIT DEFAULT NAVIGATION
       ================================== */

    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] ul {
        display: none !important;
    }

    nav[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ==================================
       REDUCE TOP PADDING
       ================================== */

    .block-container {
        padding-top: 1rem;
    }

    /* ==================================
       KPI CARDS
       ================================== */

    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e6e6e6;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
    }

    /* ==================================
       SIDEBAR
       ================================== */

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e6e6e6;
    }

    /* ==================================
       REMOVE EXTRA SPACING
       ================================== */

    div[data-testid="stSidebarNav"] + div {
        margin-top: 0px !important;
    }

    </style>
    """, unsafe_allow_html=True)
