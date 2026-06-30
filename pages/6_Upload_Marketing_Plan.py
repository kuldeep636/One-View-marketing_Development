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

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(

    page_title="Upload Marketing Plan",

    page_icon="📤",

    layout="wide"

)

inject_css()

render_navigation()

# ==================================
# PAGE HEADER
# ==================================

st.title("📤 Marketing Plan Upload Wizard")

st.caption(
    "Upload monthly marketing plans for your assigned Zone and Brand."
)
# ==================================
# UPLOAD GUIDE
# ==================================

with st.expander(
    "📖 Upload Guide",
    expanded=True
):

    st.markdown(
        """
### Before Upload

1. Select Year
2. Select Month
3. Verify your Zone & Brand
4. Download the Sample Template
5. Fill only the sample columns
6. Upload the completed Excel

### Validation Performed

- Required Columns
- Blank Values
- Vertical Validation
- Activity Type Validation
- Activity Sub Type Validation
- Investment Validation
- Activity Start Date Validation
- Activity End Date Validation

Only valid records can be uploaded.
"""
    )

# ==================================
# DOWNLOAD SAMPLE TEMPLATE
# ==================================

sample_df = create_sample_template()

buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    sample_df.to_excel(
        writer,
        index=False
    )

st.download_button(

    label="📥 Download Sample Template",

    data=buffer.getvalue(),

    file_name="Marketing_Plan_Template.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    use_container_width=True

)

st.divider()

# ==================================
# UPLOAD DETAILS
# ==================================

st.subheader(
    "Upload Details"
)

col1, col2 = st.columns(2)

# ----------------------------------
# YEAR
# ----------------------------------

with col1:

    year = st.selectbox(

        "Select Year",

        [2025, 2026, 2027, 2028, 2029]

    )

# ----------------------------------
# MONTH
# ----------------------------------

with col2:

    month = st.selectbox(

        "Select Month",

        [

            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"

        ]

    )

# ==================================
# ROLE BASED ACCESS
# ==================================

if st.session_state["role"] in [

    "President",
    "Admin"

]:

    col1, col2 = st.columns(2)

    with col1:

        zone = st.selectbox(

            "Zone",

            [

                "East",
                "West",
                "North",
                "South",
                "Gujarat",
                "MP&Rajasthan"

            ]

        )

    with col2:

        brand = st.text_input(
            "Brand"
        )

elif st.session_state["role"] == "Zone Head":

    zone = st.session_state["zone_access"]

    st.info(
        f"Zone : {zone}"
    )

    brand = st.text_input(
        "Brand"
    )

elif st.session_state["role"] == "Brand Head":

    zone = st.session_state["zone_access"]

    brand = st.session_state["brand_access"]

    st.info(
        f"Zone : {zone}"
    )

    st.info(
        f"Brand : {brand}"
    )

st.success(
    f"Selected Upload Period : {month}-{year}"
)

st.divider()
