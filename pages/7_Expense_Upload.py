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
