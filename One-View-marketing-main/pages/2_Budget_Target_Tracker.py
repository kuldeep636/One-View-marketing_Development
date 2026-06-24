import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

from utils.sidebar import render_navigation
from utils.gsheet import load_budget_data
from utils.gsheet import load_expense_data

from utils.access import apply_role_access
from utils.preprocess import preprocess_budget
from utils.ui import inject_css

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Budget & Target Tracker",
    page_icon="🎯",
    layout="wide"
)

inject_css()

# ==================================
# LOAD DATA
# ==================================

try:

    df = load_budget_data()
    df = apply_role_access(df)
    df = preprocess_budget(df)

except Exception as e:

    st.error(f"Error Loading Data: {e}")

    st.stop()

# ==================================
# SIDEBAR
# ==================================

render_navigation()

# ==================================
# HEADER
# ==================================

st.markdown("""
<h1 style='margin-bottom:0'>
🎯 BUDGET & TARGET TRACKER
</h1>

<p style='font-size:16px;color:gray'>
Budget, Retail Target & Lead Target Overview
</p>
""", unsafe_allow_html=True)

st.divider()

# ==================================
# DATA PREVIEW
# ==================================

st.subheader("📋 Budget Data")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Total Records : {len(df)}"
)

st.divider()

st.caption(
    "Made By Kuldeep Pal"
)
