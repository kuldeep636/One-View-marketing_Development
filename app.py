import streamlit as st

from utils.auth import login
from utils.login_ui import inject_login_css

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Landmark Marketing MIS",
    page_icon="🔐",
    layout="centered"
)

# ==================================
# CUSTOM CSS
# ==================================

inject_login_css()

# ==================================
# HIDE STREAMLIT NAVIGATION
# ==================================

st.markdown("""
<style>

[data-testid="stSidebarNav"] {
    display: none;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# REDIRECT IF ALREADY LOGGED IN
# ==================================

if st.session_state.get("logged_in", False):
    st.switch_page("pages/1_Dashboard.py")

# ==================================
# HEADER
# ==================================

st.markdown(
    """
    <h1 style='
        text-align:center;
        color:#002060;
        font-size:42px;
        font-weight:700;
        margin-bottom:0;
    '>
    Landmark Marketing MIS
    </h1>

    <p style='
        text-align:center;
        color:#6c757d;
        font-size:18px;
        margin-bottom:30px;
    '>
    Marketing Command Center
    </p>
    """,
    unsafe_allow_html=True
)

# ==================================
# LOGIN FORM
# ==================================

login()

# ==================================
# FOOTER
# ==================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='
        text-align:center;
        color:#9aa0a6;
        font-size:12px;
    '>

    Powered by Landmark Cars | Marketing Analytics Platform

    </div>
    """,
    unsafe_allow_html=True
)
