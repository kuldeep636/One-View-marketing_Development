import streamlit as st
import pandas as pd
from utils.sidebar import render_navigation
from utils.reporting import MONTH_ORDER_CALENDAR
from utils.access import apply_role_access
from utils.validation import (
    validate_expense_required_columns,
    validate_expense_upload
)
from utils.gsheet import (
    load_users,
    load_expense_data
)
from utils.ui import (
    inject_css,
    page_header
)

# Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="Expense Upload Wizard",
    page_icon="📤",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

inject_css()
render_navigation()
page_header(
    "📤 Expense Upload Wizard",
    "Upload Marketing Expense Data"
)

if "expense_upload_step" not in st.session_state:
    st.session_state.expense_upload_step = 1

with st.expander("📖 Upload Guide", expanded=True):
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
- Calendar Quarter
- Financial Quarter
- Financial Year
- Uploaded By
- Upload Timestamp
        """
    )

st.info(f"Step {st.session_state.expense_upload_step} of 5")

# ==================================
# LOAD EXPENSE DATA
# ==================================
expense_df = load_expense_data()
expense_df = apply_role_access(expense_df)

# ==================================
# FILTERS
# ==================================
col1, col2 = st.columns(2)

# LEFT COLUMN
with col1:
    # Zone
    zone_list = sorted(
        expense_df["Zone"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    if len(zone_list) == 1:
        zone = zone_list[0]
        st.text_input("Zone", value=zone, disabled=True)
    else:
        zone = st.selectbox("Select Zone", zone_list)

    # Year
    from datetime import datetime
    current_year = datetime.now().year
    year_list = [
        str(year) for year in range(current_year - 2, current_year + 3)
    ]
    year = st.selectbox("Select Year", year_list)

# RIGHT COLUMN
with col2:
    # Brand
    brand_df = expense_df[expense_df["Zone"] == zone]
    brand_list = sorted(
        brand_df["Brand"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    if len(brand_list) == 1:
        brand = brand_list[0]
        st.text_input("Brand", value=brand, disabled=True)
    else:
        brand = st.selectbox("Select Brand", brand_list)

# MONTH
month = st.selectbox(
    "Select Month",
    MONTH_ORDER_CALENDAR
)

with st.expander("🔍 Validation Guide", expanded=False):
    st.markdown("""
### The system will validate the following before upload

#### 📄 Template Validation
- Required columns must be present.
- Extra columns will be ignored.

#### 💰 Financial Validation
- GST will be verified.
- Total Amount will be verified.

#### ⚙️ System Generated
The following fields will be generated automatically:
- Zone, Brand, Year, Month
- Net Expenses
- Calendar Quarter, Financial Quarter
- Financial Year
- Uploaded By, Upload Timestamp

#### ❌ Upload will stop if
- Required columns are missing.
- GST calculation is incorrect.
- Total Amount calculation is incorrect.
""")

# ==================================
# UPLOAD SECTION
# ==================================
st.divider()
st.subheader("📂 Upload File")
col1, col2 = st.columns([1, 2])

with col1:
    try:
        with open("assets/Expense_Upload_Template.xlsx", "rb") as file:
            st.download_button(
                label="📥 Download Sample Template",
                data=file,
                file_name="Expense_Upload_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    except FileNotFoundError:
        st.warning("Template file not found.")

with col2:
    uploaded_file = st.file_uploader(
        "Upload Expense Excel",
        type=["xlsx"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"Selected File : {uploaded_file.name}")

# ==================================
# VALIDATION BUTTON
# ==================================
if st.button("Validate File", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("Please upload an Excel file.")
        st.stop()

    # Read Excel
    df_upload = pd.read_excel(uploaded_file)

    # Full Validation
    validation_errors, invalid_rows, extra_columns = validate_expense_upload(df_upload)

    if validation_errors:
        st.error("❌ Validation Failed")
        for error in validation_errors:
            st.write(error)
        st.stop()

    if extra_columns:
        st.warning("⚠️ Extra Columns Found")
        st.write(extra_columns)

    st.success("✅ Template validated successfully.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df_upload))
    with col2:
        st.metric("Total Columns", len(df_upload.columns))
    with col3:
        st.metric(
            "Total Amount",
            f"₹ {df_upload['AMT(W/o GST)'].sum():,.0f}"
        )

    st.divider()
    st.subheader("Preview")
    st.dataframe(
        df_upload,
        use_container_width=True,
        hide_index=True
    )

    # Save to session state
    st.session_state["upload_zone"] = zone
    st.session_state["upload_brand"] = brand
    st.session_state["upload_year"] = year
    st.session_state["upload_month"] = month
    st.session_state["uploaded_expense_file"] = uploaded_file
    st.session_state["expense_df"] = df_upload
