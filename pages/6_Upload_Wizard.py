import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

from utils.validation import validate_upload
from utils.gsheet import (
    load_activity_data,
    append_dataframe_to_sheet
)
from utils.sidebar import render_navigation
from utils.ui import inject_css


# ==================================
# ACTIVITY SUB TYPES
# ==================================

ACTIVITY_SUBTYPES = {

    "ATL": [

        "Newspaper Advertisement",
        "Magazine Advertisement",
        "Radio Campaign",
        "Hoarding",
        "Cinema Advertising",
        "TV Advertising",
        "Elevator Promotions",
        "Leaflet Distribution",
        "Podcast Advertisement"

    ],

    "BTL": [

        "Mall Display",
        "Hotel Display",
        "Roadshow / Drive Event",
        "Corporate Activity",
        "RWA/Society Display",
        "CSR Activity",
        "Special Day / Experiential Activity",
        "Service Camp",
        "Service Clinic",
        "Test Drive Event",
        "Customer Meet",
        "Surveyor's Meet",
        "Product Launch",
        "Exhibition",
        "Golf Event"

    ],

    "DIGITAL": [

        "Content Creation",
        "Meta Ads",
        "Google Ads",
        "SEO",
        "Email Marketing",
        "WhatsApp Marketing",
        "Influencer Marketing",
        "Aggregator"

    ]

}


# ==================================
# SAMPLE TEMPLATE
# ==================================

@st.cache_data
def create_sample_template():

    return pd.DataFrame({

        "Vertical": ["Sales"],

        "Location": ["Ahmedabad"],

        "Activity Type": ["BTL"],

        "Activity Sub Type": ["Mall Display"],

        "Activity Description": [
            "Weekend Lead Generation Activity"
        ],

        "Activity Start date": [
            "01-Jul-2026"
        ],

        "Activity End date": [
            "03-Jul-2026"
        ],

        "Investment": [50000]

    })


# ==================================
# LOGIN CHECK
# ==================================

if not st.session_state.get(
    "logged_in",
    False
):

    st.warning(
        "Please login first."
    )

    st.stop()


if "upload_completed" not in st.session_state:

    st.session_state.upload_completed = False


# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(

    page_title="Data Upload Wizard",

    page_icon="📤",

    layout="wide"

)

inject_css()

render_navigation()


# ==================================
# PAGE HEADER
# ==================================

st.markdown(
    """
<h1 style='margin-bottom:0'>
📤 DATA UPLOAD WIZARD
</h1>

<p style='font-size:16px;color:gray'>
Marketing Data Upload Center
</p>
""",
    unsafe_allow_html=True
)

st.divider()


st.subheader("Step 1 : Upload Type")

upload_type = st.selectbox(
    "Select Upload Type",
    [
        "Marketing Plan",
        "Expense Data",
        "Budget & Target"
    ]
)

st.divider()

if upload_type == "Marketing Plan":

    st.success(
        "📋 Marketing Plan Upload"
    )

    if st.button(
        "Open Marketing Plan Upload",
        use_container_width=True
    ):
        st.switch_page(
            "pages/6_Upload_Marketing_Plan.py"
        )

elif upload_type == "Expense Data":

    st.info(
        "💰 Expense Upload"
    )

    if st.button(
        "Open Expense Upload",
        use_container_width=True
    ):
        st.switch_page(
            "pages/7_Expense_Upload.py"
        )

elif upload_type == "Budget & Target":

    st.warning(
        "🎯 Budget Upload"
    )

    if st.button(
        "Open Budget Upload",
        use_container_width=True
    ):
        st.switch_page(
            "pages/8_Budget_Upload.py"
        )
