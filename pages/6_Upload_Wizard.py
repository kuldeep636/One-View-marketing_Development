import streamlit as st
import pandas as pd
from datetime import datetime
from utils.validation import validate_upload
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
        st.image("assets/upload_success.webp", width=300)
        st.success("Marketing Plan Uploaded Successfully")
        st.caption("Thank you for uploading your marketing plan.")
        if st.button("📤 Upload Another File", use_container_width=True):
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
# STEP 1: UPLOAD TYPE
# ==================================
st.subheader("Step 1 : Upload Type")
upload_type = st.selectbox(
    "Select Upload Type",
    ["Marketing Plan", "Budget & Target", "Expense Data"]
)

if upload_type == "Marketing Plan":
    st.success("📋 Marketing Plan Upload")
elif upload_type == "Budget & Target":
    st.warning("🚧 Budget & Target Upload is under development.")
    st.stop()
elif upload_type == "Expense Data":
    st.markdown("---")
    st.subheader("💰 Expense Upload")
    st.caption("Upload monthly marketing expense data.")
    st.markdown("### Step 2 : Upload Information")
    c1, c2 = st.columns(2)
    with c1:
        year = st.selectbox(
            "Year",
            ["2025", "2026", "2027"],
            key="expense_year"
        )
    with c2:
        month = st.selectbox(
            "Month",
            ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"],
            key="expense_month"
        )
    st.markdown("---")
    st.markdown("### Step 3 : Upload Scope")
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Zone", ["Loading..."], key="expense_zone")
    with c2:
        st.selectbox("Brand", ["Loading..."], key="expense_brand")
    st.markdown("---")
    with st.expander("📖 Upload Guide", expanded=True):
        st.markdown("""
- Select Year
- Select Month
- Select Zone
- Select Brand
- Upload the Expense Excel file

The system will automatically generate:
- GST
- Total Amount
- Net Expense
- Calendar Fields
- Financial Fields
- Uploaded By
- Upload Timestamp
        """)
    st.download_button(
        "📥 Download Expense Template",
        data=b"",
        file_name="Expense_Template.xlsx",
        use_container_width=True
    )
    expense_file = st.file_uploader(
        "📤 Upload Expense File",
        type=["xlsx"],
        key="expense_upload"
    )
    st.button("Next ➜", use_container_width=True, disabled=True)

# ==================================
# STEP 2: SELECT PERIOD (for Marketing Plan)
# ==================================
st.subheader("Step 2 : Select Period")
col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("Year", [2025, 2026, 2027], key="upload_year")
with col2:
    month = st.selectbox(
        "Month",
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        key="upload_month"
    )

st.info(f"**Selected Period**: {month} {year}")
st.divider()

# ==================================
# UPLOAD GUIDELINES
# ==================================
with st.expander("📋 Allowed Values & Upload Guidelines", expanded=False):
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
- Podcast Advertisement

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
- Aggregator
    """)

# ==================================
# SAMPLE TEMPLATE
# ==================================
st.subheader("📥 Download Sample Template")
from io import BytesIO

sample_df = create_sample_template()
output = BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    sample_df.to_excel(writer, index=False, sheet_name="Marketing Plan")
excel_data = output.getvalue()

st.download_button(
    label="📥 Download Sample Marketing Plan Template",
    data=excel_data,
    file_name="Marketing_Plan_Template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

# Brand List
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

if role in ["President", "Admin"]:
    zone = st.selectbox("Select Zone", all_zones)
    zone_brands = sorted(
        activity_df[activity_df["Zone"].astype(str).str.strip() == zone]["Brand"]
        .dropna().astype(str).str.strip().unique().tolist()
    )
    if len(zone_brands) == 1:
        brand = zone_brands[0]
        st.text_input("Brand", value=brand, disabled=True)
    else:
        brand = st.selectbox("Select Brand", zone_brands)

elif role == "Zonal Head":
    zone = st.session_state.get("zone_access", "")
    st.text_input("Zone", value=zone, disabled=True)
    zone_brands = sorted(
        activity_df[activity_df["Zone"].astype(str).str.strip() == zone]["Brand"]
        .dropna().astype(str).str.strip().unique().tolist()
    )
    brand = st.selectbox("Select Brand", zone_brands)

elif role == "Brand Manager":
    access_mapping = str(st.session_state.get("access_mapping", ""))
    mappings = []
    for item in access_mapping.split(";"):
        item = item.strip()
        if "|" in item:
            zone_name, brand_name = item.split("|", 1)
            mappings.append({"zone": zone_name.strip(), "brand": brand_name.strip()})
  
    if not mappings:
        st.error("No access mapping configured.")
        st.stop()
  
    allowed_zones = sorted({m["zone"] for m in mappings})
    zone = st.selectbox("Select Zone", allowed_zones)
    allowed_brands = sorted([m["brand"] for m in mappings if m["zone"] == zone])
  
    if len(allowed_brands) == 1:
        brand = allowed_brands[0]
        st.text_input("Brand", value=brand, disabled=True)
    else:
        brand = st.selectbox("Select Brand", allowed_brands)
else:
    st.error(f"Role not configured: {role}")
    st.stop()

st.divider()

# ==================================
# STEP 5: FILE UPLOAD
# ==================================
st.subheader("Step 5 : Upload Excel File")
uploaded_file = st.file_uploader("Choose Excel File (.xlsx)", type=["xlsx"], key="excel_uploader")

df_upload = None
if uploaded_file:
    try:
        df_upload = pd.read_excel(uploaded_file)
        st.success(f"✅ File loaded: {uploaded_file.name}")
        c1, c2 = st.columns(2)
        with c1: 
            st.metric("Rows", len(df_upload))
        with c2: 
            st.metric("Columns", len(df_upload.columns))
        st.subheader("Preview (First 20 Rows)")
        st.dataframe(df_upload.head(20), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        df_upload = None

# ==================================
# VALIDATION
# ==================================
validation_passed = False
if uploaded_file and df_upload is not None:
    st.divider()
    st.subheader("Step 6 : Data Validation")
    
    validation_errors, invalid_row_numbers = validate_upload(
        df_upload=df_upload,
        selected_month=month,
        selected_year=year,
        activity_subtypes=ACTIVITY_SUBTYPES
    )
    
    total_rows = len(df_upload)
    invalid_count = len(invalid_row_numbers)
    valid_count = total_rows - invalid_count
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows", total_rows)
    c2.metric("✅ Valid Rows", valid_count)
    c3.metric("❌ Invalid Rows", invalid_count)
    
    if validation_errors:
        st.error(f"Found {len(validation_errors)} validation issues")
        with st.expander("📋 View Validation Errors", expanded=False):
            for error in validation_errors:
                st.write(error)
    else:
        st.success("🎉 All validations passed!")
        validation_passed = True

# ==================================
# DUPLICATE CHECK
# ==================================
allow_reupload = False
duplicate_found = False

if validation_passed and df_upload is not None:
    existing_df = load_activity_data()
    duplicate_check = existing_df[
        (existing_df["Year"].astype(str) == str(year)) &
        (existing_df["Month"].astype(str).str.strip() == str(month)) &
        (existing_df["Zone"].astype(str).str.strip() == str(zone)) &
        (existing_df["Brand"].astype(str).str.strip() == str(brand))
    ]
    
    if not duplicate_check.empty:
        duplicate_found = True
        uploaded_by = "Unknown"
        if ("Uploaded By" in duplicate_check.columns and 
            not duplicate_check["Uploaded By"].dropna().empty):
            uploaded_by = duplicate_check["Uploaded By"].dropna().astype(str).iloc[0]
        
        upload_time = "Unknown"
        if ("Upload Timestamp" in duplicate_check.columns and 
            not duplicate_check["Upload Timestamp"].dropna().empty):
            upload_time = duplicate_check["Upload Timestamp"].dropna().astype(str).iloc[0]
        
        st.error(f"""
⚠ Marketing Plan Already Exists

Year : {year}
Month : {month}
Zone : {zone}
Brand : {brand}

Uploaded By : {uploaded_by}
Upload Time : {upload_time}
        """)
        
        total_activities = len(duplicate_check)
        total_investment = 0
        if "Investment" in duplicate_check.columns:
            total_investment = pd.to_numeric(
                duplicate_check["Investment"], errors="coerce"
            ).fillna(0).sum()
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Existing Activities", total_activities)
        with c2:
            st.metric("Total Investment", f"₹ {total_investment:,.0f}")
        
        preview_cols = [
            "Activity Type", "Activity Sub Type", "Activity Description",
            "Activity Start date", "Activity End date", "Investment"
        ]
        available_cols = [col for col in preview_cols if col in duplicate_check.columns]
        
        with st.expander("📋 View Existing Marketing Plan", expanded=False):
            st.dataframe(duplicate_check[available_cols], use_container_width=True, hide_index=True)
        
        allow_reupload = st.checkbox("I confirm this upload is intentional")

# ==================================
# UPLOAD SECTION
# ==================================
if (validation_passed and 
    df_upload is not None and 
    (not duplicate_found or allow_reupload)):
    
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
                    append_dataframe_to_sheet(sheet_name, final_df)
                
                st.cache_data.clear()
                st.session_state.upload_completed = True
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
