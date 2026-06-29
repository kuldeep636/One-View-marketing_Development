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


# ==================================
# SUCCESS SCREEN
# ==================================

if st.session_state.upload_completed:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.image(
            "assets/upload_success.webp",
            width=300
        )

        st.success(
            "Marketing Plan Uploaded Successfully"
        )

        st.caption(
            "Thank you for uploading your marketing plan."
        )

        if st.button(
            "📤 Upload Another File",
            use_container_width=True
        ):

            st.session_state.upload_completed = False

            st.rerun()

    st.stop()


# ==================================
# USER INFO
# ==================================

role = st.session_state.get(
    "role",
    ""
)

name = st.session_state.get(
    "name",
    "Unknown"
)

st.sidebar.info(
    f"**Logged in as:** {name} ({role})"
)


# ==================================
# FUNCTION DEFINITIONS
# ==================================

def marketing_plan_upload():

    pass


def expense_upload():

    pass


def budget_upload():

    st.warning(
        "🚧 Budget & Target Upload is under development."
    )
