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
# ==============================
# STEP 1 : Upload File
# ==============================

users_df = load_users()

# Zone List
zone_list = sorted(
    users_df["Zone"]
    .dropna()
    .unique()
    .tolist()
)

zone = st.selectbox(
    "Select Zone",
    zone_list,
    index=None,
    placeholder="Choose Zone"
)

brand = None

if zone:

    brand_list = sorted(
        users_df[
            users_df["Zone"] == zone
        ]["Brand"]
        .dropna()
        .unique()
        .tolist()
    )

    brand = st.selectbox(
        "Select Brand",
        brand_list,
        index=None,
        placeholder="Choose Brand"
    )

uploaded_file = st.file_uploader(
    "Upload Expense Excel",
    type=["xlsx"],
    accept_multiple_files=False
)

if st.button(
    "Validate File",
    type="primary",
    use_container_width=True
):

    if not zone:
        st.error("Please select Zone.")
        st.stop()

    if not brand:
        st.error("Please select Brand.")
        st.stop()

    if uploaded_file is None:
        st.error("Please upload an Excel file.")
        st.stop()

    st.session_state.zone = zone
    st.session_state.brand = brand
    st.session_state.uploaded_expense_file = uploaded_file

    st.success("Step 1 completed successfully.")
