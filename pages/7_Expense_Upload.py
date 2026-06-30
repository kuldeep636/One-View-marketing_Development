import streamlit as st
import pandas as pd

from utils.sidebar import render_navigation
from utils.access import apply_role_access
from utils.gsheet import load_users
from utils.ui import (
    inject_css,
    page_header
)
if not st.session_state.get(
    "logged_in",
    False
):
    st.warning(
        "Please login first."
    )
    st.stop()
    st.set_page_config(
        page_title="Expense Upload Wizard",
        page_icon="📤",
        layout="wide"
    )

inject_css()
render_navigation()
page_header(
    "📤 Expense Upload Wizard",
    "Upload Marketing Expense Data"
)
if "expense_upload_step" not in st.session_state:

    st.session_state.expense_upload_step = 1

with st.expander(
    "📖 Upload Guide",
    expanded=True
):

    st.markdown(
        """
### Before Upload

- Select Year
- Select Month
- Select Zone
- Select Brand
- Upload the Expense Excel

The system will automatically generate:

- Quarter
- GST
- Total Amount
- Net Expenses
- Calendar Fields
- Financial Fields
- Uploaded By
- Upload Timestamp
        """
    )
    
st.info(
    f"Step {st.session_state.expense_upload_step} of 5"
)
# ==================================
# LOAD EXPENSE DATA
# ==================================

expense_df = load_expense_data()

# Apply Role Access
expense_df = apply_role_access(expense_df)

# ==================================
# ZONE
# ==================================

zone_list = sorted(
    expense_df["Zone"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if len(zone_list) == 1:

    zone = zone_list[0]

    st.text_input(
        "Zone",
        value=zone,
        disabled=True
    )

else:

    zone = st.selectbox(
        "Select Zone",
        zone_list
    )

# ==================================
# BRAND
# ==================================

brand_df = expense_df[
    expense_df["Zone"] == zone
]

brand_list = sorted(
    brand_df["Brand"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if len(brand_list) == 1:

    brand = brand_list[0]

    st.text_input(
        "Brand",
        value=brand,
        disabled=True
    )

else:

    brand = st.selectbox(
        "Select Brand",
        brand_list
    )

# ==================================
# FILE UPLOAD
# ==================================

uploaded_file = st.file_uploader(
    "Upload Expense Excel",
    type=["xlsx"]
)

if st.button(
    "Validate File",
    type="primary",
    use_container_width=True
):

    if uploaded_file is None:
        st.error("Please upload an Excel file.")
        st.stop()

    st.session_state["upload_zone"] = zone
    st.session_state["upload_brand"] = brand
    st.session_state["uploaded_expense_file"] = uploaded_file

    st.success("File uploaded successfully. Ready for validation.")
