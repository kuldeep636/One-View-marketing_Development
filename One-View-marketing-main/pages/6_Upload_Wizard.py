import streamlit as st
import pandas as pd
from datetime import datetime
from utils.gsheet import load_activity_data, append_dataframe_to_sheet
from utils.sidebar import render_navigation
from utils.ui import inject_css

ACTIVITY_SUBTYPES = {
    "ATL": [
        "Newspaper Advertisement",
        "Magazine Advertisement",
        "Radio Campaign",
        "Hoarding",
        "Cinema Advertising",
        "TV Advertising",
        "Elevator Promotions",
        "Leaflet Distribution"
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
        "Influencer Marketing"
    ]
}

@st.cache_data
def create_sample_template():
    return pd.DataFrame({
        "Vertical": ["Sales"],
        "Location": ["Ahmedabad"],
        "Activity Type": ["BTL"],
        "Activity Sub Type": ["Mall Display"],
        "Activity Description": ["Weekend Lead Generation Activity"],
        "Activity Start date": ["01-Jul-2026"],
        "Activity End date": ["03-Jul-2026"],
        "Investment": [50000],
    })

# ==================================
# LOGIN CHECK
# ==================================
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
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
# HEADER
# ==================================
st.markdown("""
<h1 style='margin-bottom:0'>
    📤 DATA UPLOAD WIZARD
</h1>
<p style='font-size:16px;color:gray'>
    Marketing Data Upload Center
</p>
""", unsafe_allow_html=True)
st.divider()

if st.session_state.upload_completed:
    col1, col2, col3 = st.columns([1,2,1])
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
role = st.session_state.get("role", "")
name = st.session_state.get("name", "Unknown")
st.sidebar.info(f"**Logged in as:** {name} ({role})")

# ==================================
# STEP 1-3: BASIC SELECTIONS
# ==================================
st.subheader("Step 1 : Upload Type")
upload_type = st.selectbox(
    "Select Upload Type",
    [
        "Marketing Plan",
        "Budget & Target",
        "Expense Data"
    ]
)

if upload_type == "Marketing Plan":
    st.success(
        "📋 Marketing Plan Upload"
    )
elif upload_type == "Budget & Target":
    st.warning(
        "🚧 Budget & Target Upload is under development."
    )
    st.stop()
elif upload_type == "Expense Data":
    st.warning(
        "🚧 Expense Data Upload is under development."
    )
    st.stop()

st.subheader("Step 2 : Select Period")
col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("Year", [2025, 2026, 2027], key="upload_year")
with col2:
    month = st.selectbox(
        "Month",
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        key="upload_month"
    )

st.info(f"**Selected Period**: {month} {year}")
st.divider()

# ==================================
# UPLOAD GUIDELINES
# ==================================
with st.expander(
    "📋 Allowed Values & Upload Guidelines",
    expanded=False
):
    st.markdown("""
    ### Vertical
    - Sales
    - After Sales
    ### Activity Type
    - ATL
    - BTL
    - DIGITAL
    - FLEXY
    ### Date Format
    - DD-MMM-YYYY
    - Example: 01-Jul-2026
    ### Investment
    - Numeric values only
    - Example: 50000
    ### Important Validation Rules
    - Activity Start Date must belong to the selected Month & Year
    - Activity End Date must belong to the selected Month & Year
    - Blank values are not allowed
    - Invalid Activity Types are not allowed
    - Invalid Vertical values are not allowed
    """)

with st.expander("📋 Activity Type & Sub Type Guidelines"):
    st.markdown("""
### ATL
- Newspaper Advertisement
- Magazine Advertisement
- Radio Campaign
- Hoarding
- Cinema Advertising
- TV Advertising
- Leaflet Distribution
- Elevator Promotions
### BTL
- Mall Display
- Hotel Display
- Roadshow / Drive Event
- Corporate Activity
- RWA/Society Display
- CSR Activity
- Special Day / Experiential Activity
- Service Camp
- Service Clinic
- Test Drive Event
- Customer Meet
- Surveyor's Meet
- Product Launch
- Exhibition
- Golf Event
### DIGITAL
- Content Creation
- Meta Ads
- Google Ads
- SEO
- Email Marketing
- WhatsApp Marketing
- Influencer Marketing
""")

# ==================================
# SAMPLE TEMPLATE
# ==================================
st.subheader("📥 Download Sample Template")
from io import BytesIO
sample_df = create_sample_template()
output = BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    sample_df.to_excel(
        writer,
        index=False,
        sheet_name="Marketing Plan"
    )
excel_data = output.getvalue()
st.download_button(
    label="📥 Download Sample Marketing Plan Template",
    data=excel_data,
    file_name="Marketing_Plan_Template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

# Load Brand List (cached)
@st.cache_data(ttl=3600)
def get_brand_list():
    try:
        return sorted(
            load_activity_data()["Brand"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )
    except:
        return []

brands = get_brand_list()

# ==================================
# STEP 4: ROLE-BASED SCOPE
# ==================================
st.subheader("Step 4 : Upload Scope")
activity_df = load_activity_data()
all_zones = sorted(
    activity_df["Zone"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)
zone = ""
brand = ""

# PRESIDENT / ADMIN
if role in ["President", "Admin"]:
    zone = st.selectbox(
        "Select Zone",
        all_zones
    )
    zone_brands = sorted(
        activity_df[
            activity_df["Zone"].astype(str).str.strip() == zone
        ]["Brand"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )
    allowed_brands = zone_brands
    if len(allowed_brands) == 1:
        brand = allowed_brands[0]
        st.text_input(
            "Brand",
            value=brand,
            disabled=True
        )
    else:
        brand = st.selectbox(
            "Select Brand",
            allowed_brands
        )

# ZONAL HEAD
elif role == "Zonal Head":
    zone = st.session_state.get(
        "zone_access",
        ""
    )
    st.text_input(
        "Zone",
        value=zone,
        disabled=True
    )
    zone_brands = sorted(
        activity_df[
            activity_df["Zone"].astype(str).str.strip() == zone
        ]["Brand"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )
    brand = st.selectbox(
        "Select Brand",
        zone_brands
    )

# BRAND MANAGER
elif role == "Brand Manager":
    zone = st.session_state.get(
        "zone_access",
        ""
    )
    brand_access = st.session_state.get(
        "brand_access",
        ""
    )
    st.text_input(
        "Zone",
        value=zone,
        disabled=True
    )
    allowed_brands = [
        b.strip()
        for b in str(brand_access).split(",")
        if b.strip()
    ]
    if len(allowed_brands) == 1:
        brand = allowed_brands[0]
        st.text_input(
            "Brand",
            value=brand,
            disabled=True
        )
    else:
        brand = st.selectbox(
            "Select Brand",
            allowed_brands
        )

# INVALID ROLE
else:
    st.error(
        f"Role not configured: {role}"
    )
    st.stop()

st.divider()

# ==================================
# STEP 5: FILE UPLOAD
# ==================================
st.subheader("Step 5 : Upload Excel File")
uploaded_file = st.file_uploader(
    "Choose Excel File (.xlsx)",
    type=["xlsx"],
    key="excel_uploader"
)

df_upload = None
if uploaded_file:
    try:
        df_upload = pd.read_excel(
            uploaded_file
        )
        st.success(
            f"✅ File loaded: {uploaded_file.name}"
        )
        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                "Rows",
                len(df_upload)
            )
        with c2:
            st.metric(
                "Columns",
                len(df_upload.columns)
            )
        st.subheader(
            "Preview (First 20 Rows)"
        )
        st.dataframe(
            df_upload.head(20),
            use_container_width=True,
            hide_index=True
        )
    except Exception as e:
        st.error(
            f"❌ Error reading file: {e}"
        )
        df_upload = None

if df_upload is not None:
    # ==================================
    # STANDARDIZE VERTICAL
    # ==================================
    if "Vertical" in df_upload.columns:
        df_upload["Vertical"] = (
            df_upload["Vertical"]
            .astype(str)
            .str.strip()
            .str.title()
        )
        df_upload["Vertical"] = df_upload["Vertical"].replace({
            "After Sales": "After Sales",
            "Sales": "Sales"
        })

    # ==================================
    # STANDARDIZE ACTIVITY TYPE
    # ==================================
    if "Activity Type" in df_upload.columns:
        df_upload["Activity Type"] = (
            df_upload["Activity Type"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

# ==================================
# VALIDATION
# ==================================
validation_passed = False
if uploaded_file and df_upload is not None:
    st.divider()
    st.subheader("Step 6 : Data Validation")
    required_cols = [
        "Vertical", "Location", "Activity Type", "Activity Sub Type",
        "Activity Description", "Activity Start date", "Activity End date",
        "Investment",
    ]
   
    valid_verticals = ["SALES", "AFTER SALES"]
    valid_activity_types = ["ATL", "BTL", "DIGITAL", "FLEXY"]
    validation_errors = []
    invalid_row_numbers = set()

    # Activity Sub Type Validation
    if (
        "Activity Type" in df_upload.columns
        and
        "Activity Sub Type" in df_upload.columns
    ):
        for idx, row in df_upload.iterrows():
            activity_type = (
                str(row["Activity Type"])
                .strip()
                .upper()
            )
            activity_subtype = (
                str(row["Activity Sub Type"])
                .strip()
            )
            allowed_subtypes = ACTIVITY_SUBTYPES.get(
                activity_type,
                []
            )
            if activity_subtype not in allowed_subtypes:
                validation_errors.append(
                    f"Row {idx + 2}: "
                    f"'{activity_subtype}' is not valid for "
                    f"Activity Type '{activity_type}'"
                )
                invalid_row_numbers.add(idx)

    # 1. Missing Columns
    missing_cols = [col for col in required_cols if col not in df_upload.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    else:
        st.success("✅ All required columns present")

    # 2. Blank Values + Other Validations
    for col in required_cols:
        if col in df_upload.columns:
            blank_mask = df_upload[col].isna() | df_upload[col].astype(str).str.strip().eq('')
            for idx in df_upload[blank_mask].index:
                validation_errors.append(f"Row {idx + 2}: {col} is blank")
                invalid_row_numbers.add(idx)

    # Vertical & Activity Type Validation
    if "Vertical" in df_upload.columns:
        invalid = ~df_upload["Vertical"].astype(str).str.upper().isin(valid_verticals)
        for idx in df_upload[invalid].index:
            validation_errors.append(f"Row {idx + 2}: Invalid Vertical")
            invalid_row_numbers.add(idx)

    if "Activity Type" in df_upload.columns:
        invalid = ~df_upload["Activity Type"].astype(str).str.upper().isin(valid_activity_types)
        for idx in df_upload[invalid].index:
            validation_errors.append(f"Row {idx + 2}: Invalid Activity Type")
            invalid_row_numbers.add(idx)

    # Investment & Date Validation
    if "Investment" in df_upload.columns:
        invalid = pd.to_numeric(df_upload["Investment"], errors="coerce").isna()
        for idx in df_upload[invalid].index:
            validation_errors.append(f"Row {idx + 2}: Invalid Investment")
            invalid_row_numbers.add(idx)

    for date_col in ["Activity Start date", "Activity End date"]:
        if date_col in df_upload.columns:
            invalid = pd.to_datetime(df_upload[date_col], errors="coerce").isna()
            for idx in df_upload[invalid].index:
                validation_errors.append(f"Row {idx + 2}: Invalid date in {date_col}")
                invalid_row_numbers.add(idx)

    # ==================================
    # START DATE MONTH VALIDATION
    # ==================================
    selected_month = month[:3].upper()
    selected_year = int(year)
    for idx, row in df_upload.iterrows():
        start_date = pd.to_datetime(
            row.get("Activity Start date"),
            errors="coerce"
        )
        end_date = pd.to_datetime(
            row.get("Activity End date"),
            errors="coerce"
        )
        # Start Date Must Match Selected Month-Year
        if pd.notna(start_date):
            if (
                start_date.strftime("%b").upper() != selected_month
                or
                start_date.year != selected_year
            ):
                validation_errors.append(
                    f"Row {idx+2}: Activity Start Date must belong to {month}-{year}"
                )
                invalid_row_numbers.add(idx)
        # End Date Cannot Be Earlier Than Start Date
        if (
            pd.notna(start_date)
            and
            pd.notna(end_date)
        ):
            if end_date < start_date:
                validation_errors.append(
                    f"Row {idx+2}: Activity End Date cannot be earlier than Activity Start Date"
                )
                invalid_row_numbers.add(idx)

    # Summary
    total_rows = len(df_upload)
    invalid_count = len(invalid_row_numbers)
    valid_count = total_rows - invalid_count
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows", total_rows)
    c2.metric("✅ Valid Rows", valid_count)
    c3.metric("❌ Invalid Rows", invalid_count)

    if validation_errors:
        st.error(f"Found {len(validation_errors)} validation issues")
        with st.expander("📋 View Validation Errors"):
            for error in validation_errors[:50]:
                st.write(error)
            if len(validation_errors) > 50:
                st.write(f"... and {len(validation_errors)-50} more")
    else:
        st.success("🎉 All validations passed!")
        validation_passed = True

# ==================================
# UPLOAD SECTION
# ==================================
if validation_passed and df_upload is not None:
    if st.button("🚀 Upload to Google Sheets", type="primary", use_container_width=True):
        try:
            final_df = df_upload.copy()
       
            # Auto-populate system fields
            final_df["Zone"] = zone
            final_df["Brand"] = brand
            final_df["Year"] = year
            final_df["Month"] = month
            final_df["Status"] = "Planned"
            final_df["Execution Status"] = "Pending"
            final_df["Actual Investment"] = 0
            final_df["Execution Date"] = ""
            final_df["Remarks"] = ""
            final_df["Uploaded By"] = name
            final_df["Upload Timestamp"] = datetime.now()
       
            sheet_name_map = {
                "Marketing Plan": "Marketing Plan",
                "Expense Data": "Expenes",
                "Budget Data": "Budget and Target Overview"
            }
       
            sheet_name = sheet_name_map.get(upload_type)
            if not sheet_name:
                st.error("Invalid upload type")
            else:
                with st.spinner("Uploading Marketing Plan..."):
                    append_dataframe_to_sheet(
                        sheet_name,
                        final_df
                    )
                           
                st.cache_data.clear()
           
                st.session_state.upload_completed = True
                st.rerun()
            
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
