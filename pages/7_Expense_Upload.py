import streamlit as st
import pandas as pd
from datetime import datetime

from utils.sidebar import render_navigation
from utils.reporting import MONTH_ORDER_CALENDAR
from utils.access import apply_role_access
from utils.validation import validate_expense_upload
from utils.expense import prepare_expense_data
from utils.gsheet import (
    load_expense_data,
    append_dataframe_to_sheet
)
from utils.ui import (
    inject_css,
    page_header
)

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Expense Upload Wizard",
    page_icon="📤",
    layout="wide"
)

# ==================================
# LOGIN CHECK
# ==================================
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# ==================================
# SESSION VARIABLES
# ==================================
if "validated" not in st.session_state:
    st.session_state["validated"] = False

if "expense_df" not in st.session_state:
    st.session_state["expense_df"] = None

if "expense_upload_step" not in st.session_state:
    st.session_state["expense_upload_step"] = 1

# ==================================
# USER INFO
# ==================================
role = st.session_state.get("role", "")
name = st.session_state.get("name", "Unknown")

# ==================================
# UI
# ==================================
inject_css()
render_navigation()

page_header(
    "📤 Expense Upload Wizard",
    "Upload Marketing Expense Data"
)

st.info(
    f"Step {st.session_state.expense_upload_step} of 5"
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

- Select Zone
- Select Brand
- Select Year
- Select Month
- Upload Expense Excel

### System Generated

The following fields will be generated automatically

- Net Expenses
- Calendar Quarter
- Financial Quarter
- Financial Year
- Uploaded By
- Upload Timestamp
"""
    )

# ==================================
# LOAD DATA
# ==================================
expense_df = load_expense_data()
expense_df = apply_role_access(expense_df)

# ==================================
# FILTERS
# ==================================
col1, col2 = st.columns(2)

# -----------------------------
# LEFT
# -----------------------------
with col1:

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

    current_year = datetime.now().year

    year_list = [
        str(year)
        for year in range(
            current_year - 2,
            current_year + 3
        )
    ]

    year = st.selectbox(
        "Select Year",
        year_list
    )

# -----------------------------
# RIGHT
# -----------------------------
with col2:

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

    month = st.selectbox(
        "Select Month",
        MONTH_ORDER_CALENDAR
    )

# ==================================
# VALIDATION GUIDE
# ==================================
with st.expander(
    "🔍 Validation Guide",
    expanded=False
):
    st.markdown(
        """
### Template Validation

- Required columns must be present.
- Extra columns are allowed.

### Financial Validation

- GST Amount will be verified.
- Total Amount will be verified.

### System Generated

- Zone
- Brand
- Year
- Month
- Net Expenses
- Calendar Quarter
- Financial Quarter
- Financial Year
- Uploaded By
- Upload Timestamp

### Upload will stop if

- Required columns are missing.
- GST Amount is incorrect.
- Total Amount is incorrect.
"""
    )

# ==================================
# FILE UPLOAD
# ==================================
st.divider()

st.subheader("📂 Upload File")

col1, col2 = st.columns([1, 2])

with col1:

    try:

        with open(
            "assets/Expense_Upload_Template.xlsx",
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Sample Template",
                data=file,
                file_name="Expense_Upload_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    except FileNotFoundError:

        st.warning(
            "Template file not found."
        )

with col2:

    uploaded_file = st.file_uploader(
        "Upload Expense Excel",
        type=["xlsx"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        st.success(
            f"Selected File : {uploaded_file.name}"
        )


# ==================================
# VALIDATE FILE
# ==================================

if st.button(
    "✅ Validate File",
    type="primary",
    use_container_width=True
):

    if uploaded_file is None:
        st.error("Please upload an Excel file.")
        st.stop()

    # Read Excel
    df_upload = (
        pd.read_excel(uploaded_file)
        .dropna(how="all")
        .reset_index(drop=True)
    )

    # -----------------------------
    # VALIDATION
    # -----------------------------
    validation_errors, invalid_rows, extra_columns = (
        validate_expense_upload(df_upload)
    )

    if validation_errors:

        st.error("❌ Validation Failed")

        for error in validation_errors:
            st.write(error)

        st.stop()

    if extra_columns:

        st.warning("⚠️ Extra Columns Found")

        st.write(extra_columns)

    # -----------------------------
    # PREPARE DATA
    # -----------------------------
    df_upload = prepare_expense_data(
        df=df_upload,
        zone=zone,
        brand=brand,
        year=year,
        month=month,
        uploaded_by=name
    )

    # -----------------------------
    # SAVE SESSION
    # -----------------------------
    st.session_state["validated"] = True
    st.session_state["expense_df"] = df_upload

    st.session_state["upload_zone"] = zone
    st.session_state["upload_brand"] = brand
    st.session_state["upload_year"] = year
    st.session_state["upload_month"] = month
    st.session_state["uploaded_expense_file"] = uploaded_file

    st.success("✅ Validation completed successfully.")

# ==================================
# SHOW PREVIEW
# ==================================

if st.session_state["validated"]:

    df_upload = st.session_state["expense_df"]

    st.divider()

    st.subheader("📊 Upload Summary")

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric(
            "Total Rows",
            len(df_upload)
        )

    with kpi2:
        st.metric(
            "Gross Expense",
            f"₹ {df_upload['AMT(W/o GST)'].sum():,.0f}"
        )

    with kpi3:
        st.metric(
            "Net Expense",
            f"₹ {df_upload['Net Expenses'].sum():,.0f}"
        )

    st.divider()

    st.subheader("📋 Upload Preview")

    st.caption(
        "The following data will be uploaded to Google Sheets."
    )

    st.dataframe(
        df_upload,
        use_container_width=True,
        hide_index=True
    )

    st.divider()


# ==================================
# UPLOAD TO GOOGLE SHEET
# ==================================

if st.session_state["validated"]:

    df_upload = st.session_state["expense_df"]

    upload = st.button(
        "🚀 Upload Data",
        type="primary",
        use_container_width=True
    )

    if upload:

        with st.spinner("Uploading data to Google Sheet..."):

            success = append_dataframe_to_sheet(
                "Expenes",
                df_upload
            )

        if success:

            st.balloons()

            st.success(
                f"""
### ✅ Expense Data Uploaded Successfully

**Records Uploaded :** {len(df_upload)}

**Zone :** {st.session_state['upload_zone']}

**Brand :** {st.session_state['upload_brand']}

**Month :** {st.session_state['upload_month']}

**Year :** {st.session_state['upload_year']}
"""
            )

            # ==================================
            # CLEAR CACHE
            # ==================================

            st.cache_data.clear()

            # ==================================
            # RESET SESSION
            # ==================================

            st.session_state["validated"] = False
            st.session_state["expense_df"] = None
            st.session_state["uploaded_expense_file"] = None

            # ==================================
            # REFRESH PAGE
            # ==================================

            st.rerun()

        else:

            st.error(
                "❌ Upload failed. Please try again."
            )
