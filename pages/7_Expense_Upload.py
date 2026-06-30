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
# -----------------------------
# STEP 1 : Upload Expense File
# -----------------------------

if st.session_state.expense_upload_step == 1:

    st.subheader("Step 1 • Upload Expense File")

    uploaded_file = st.file_uploader(
        "Choose Expense Excel File",
        type=["xlsx", "xls"],
        help="Upload the monthly Marketing Expense Sheet."
    )

    if uploaded_file:

        file_size = uploaded_file.size / (1024 * 1024)

        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ File Selected")

            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {file_size:.2f} MB")

        with col2:
            st.info(
                """
                **Next Step**
                
                The uploaded file will be validated for:
                
                • Required columns
                
                • Blank rows
                
                • Duplicate records
                
                • Data format
                """
            )

        st.session_state.uploaded_expense_file = uploaded_file

        if st.button(
            "Next ➜",
            type="primary",
            use_container_width=True
        ):
            st.session_state.expense_upload_step = 2
            st.rerun()
