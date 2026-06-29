import streamlit as st
import pandas as pd

# ==================================
# LOGIN CHECK
# ==================================
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Upload Marketing Plan",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Marketing Plan Upload Wizard")

# ==================================
# USER INFO
# ==================================
role = st.session_state.get("role", "")
zone_access = st.session_state.get("zone_access", "")
brand_access = st.session_state.get("brand_access", "")

# ==================================
# STEP 1 : ROLE DETECTION
# ==================================
st.subheader("Step 1 : Upload Details")

if role in ["President", "Admin"]:
    st.success("Admin Upload Mode")
    zone = st.selectbox(
        "Select Zone",
        ["East", "West", "North", "South", "Gujarat", "MP&Rajasthan"]
    )
    brand = st.text_input("Brand")

elif role == "Zone Head":
    zone = zone_access
    st.info(f"Zone : {zone}")
    brand = st.text_input("Brand")

elif role == "Brand Head":
    zone = zone_access
    brand = brand_access
    st.info(f"Zone : {zone}")
    st.info(f"Brand : {brand}")

else:
    st.error("Role not configured.")
    st.stop()

# ==================================
# STEP 2 : YEAR
# ==================================
year = st.selectbox(
    "Select Year",
    [2025, 2026, 2027, 2028, 2029]
)

# ==================================
# STEP 3 : MONTH
# ==================================
month = st.selectbox(
    "Select Month",
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)

selected_period = f"{month}-{year}"
st.info(f"Selected Period : {selected_period}")

# ==================================
# STEP 4 : FILE UPLOAD
# ==================================
uploaded_file = st.file_uploader(
    "Upload Marketing Plan",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"{len(df)} records loaded.")

    # ==================================
    # REQUIRED COLUMNS
    # ==================================
    REQUIRED_COLUMNS = [
        "Vertical",
        "Location",
        "Activity Type",
        "Activity Sub Type",
        "Activity Description",
        "Activity Start date",
        "Activity End date",
        "Investment"
    ]

    errors = []

    # ==================================
    # COLUMN VALIDATION
    # ==================================
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append({
                "Row": "-",
                "Column": col,
                "Error": "Column Missing"
            })

    # ==================================
    # BLANK VALUE CHECK
    # ==================================
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            invalid_rows = df[df[col].isna()].index.tolist()
            for row in invalid_rows:
                errors.append({
                    "Row": row + 2,
                    "Column": col,
                    "Error": "Blank Value"
                })

    # ==================================
    # SHOW RESULTS
    # ==================================
    st.subheader("Validation Summary")

    if len(errors) == 0:
        st.success("✅ Validation Passed")
        st.dataframe(df.head(20), use_container_width=True)
        
        if st.button("Upload Data", use_container_width=True):
            st.success("Ready for Google Sheet Upload")
    else:
        st.error(f"{len(errors)} validation errors found.")
        error_df = pd.DataFrame(errors)
        st.dataframe(error_df, use_container_width=True)
