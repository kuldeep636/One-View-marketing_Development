import streamlit as st
import pandas as pd
from datetime import date
from utils.gsheet import load_activity_data, update_activity_execution
from utils.access import apply_role_access
from utils.sidebar import render_navigation

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Activity Execution Update",
    page_icon="✅",
    layout="wide"
)

# ==================================
# SIDEBAR
# ==================================
render_navigation()

# ==================================
# LOAD DATA
# ==================================
df = load_activity_data()
df = apply_role_access(df)

# ==================================
# HEADER
# ==================================
st.title("✅ Activity Execution Update")
st.caption("Update activity execution status and actual investment")
st.divider()

# ==================================
# FILTERS
# ==================================
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox(
        "Year",
        sorted(df["Year"].dropna().unique().tolist())
    )
with col2:
    month = st.selectbox(
        "Month",
        sorted(df["Month"].dropna().unique().tolist())
    )
with col3:
    status_filter = st.selectbox(
        "Execution Status",
        ["All", "Pending", "Executed", "Cancelled"]
    )

# Apply Filters
filtered_df = df[
    (df["Year"] == year) &
    (df["Month"] == month)
]
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Execution Status"] == status_filter]

# ==================================
# ACTIVITY SELECTOR
# ==================================
activity_options = filtered_df["Activity Description"].dropna().unique().tolist()
if not activity_options:
    st.warning("No activities found for the selected filters.")
    st.stop()

selected_activity = st.selectbox(
    "Select Activity",
    activity_options
)
st.divider()

# ==================================
# SELECTED ACTIVITY DETAILS
# ==================================
activity_df = filtered_df[filtered_df["Activity Description"] == selected_activity]
if len(activity_df) > 0:
    activity = activity_df.iloc[0]
    st.subheader("📋 Activity Details")
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Zone", value=activity.get("Zone", ""), disabled=True)
        st.text_input("Brand", value=activity.get("Brand", ""), disabled=True)
        st.text_input("Activity Type", value=activity.get("Activity Type", ""), disabled=True)
        st.text_input("Sub Type", value=activity.get("Activity Sub Type", ""), disabled=True)
    
    with c2:
        st.text_input("Location", value=activity.get("Location", ""), disabled=True)
        st.text_input("Planned Investment",
                     value=str(activity.get("Investment", "")), disabled=True)
        
        start_date = pd.to_datetime(activity.get("Activity Start date"), errors="coerce")
        end_date = pd.to_datetime(activity.get("Activity End date"), errors="coerce")
        
        st.text_input("Start Date",
                     value=start_date.strftime("%d-%b-%Y") if pd.notna(start_date) else "",
                     disabled=True)
        st.text_input("End Date",
                     value=end_date.strftime("%d-%b-%Y") if pd.notna(end_date) else "",
                     disabled=True)
    
    st.text_area("Activity Description",
                value=activity.get("Activity Description", ""),
                disabled=True, height=100)
    st.divider()
    
    # ==================================
    # EXECUTION UPDATE FORM
    # ==================================
    st.subheader("✅ Update Execution Status")
    
    # Execution Status
    current_status = str(activity.get("Execution Status", "Pending"))
    status_options = ["Pending", "Executed", "Cancelled"]
    
    execution_status = st.selectbox(
        "Execution Status",
        status_options,
        index=status_options.index(current_status) if current_status in status_options else 0
    )
    
    # Actual Investment
    actual_investment = st.number_input(
        "Actual Investment (₹)",
        min_value=0.0,
        value=float(activity.get("Actual Investment", 0) or 0),
        step=1000.0
    )
    
    # Execution Date
    existing_date = pd.to_datetime(activity.get("Execution Date", ""), errors="coerce")
    execution_date = st.date_input(
        "Execution Date",
        value=existing_date.date() if pd.notna(existing_date) else date.today()
    )
    st.caption(f"Selected Date: {execution_date.strftime('%d-%b-%Y')}")
    
    # Supporting Link
    supporting_link = st.text_input(
        "Supporting Document Link",
        value=str(activity.get("Supporting Link", "")),
        placeholder="Paste Google Drive / OneDrive / SharePoint Link"
    )
    st.caption("Optional: Add supporting document link if available.")
    
    # Remarks
    remarks = st.text_area(
        "Remarks",
        value=str(activity.get("Remarks", "")),
        height=100
    )
    
    # ==================================
    # SAVE BUTTON
    # ==================================
    if st.button("💾 Save Update", type="primary", use_container_width=True):
        try:
            # ==================================
            # VALIDATION
            # ==================================
            
            activity_start_date = pd.to_datetime(
                activity.get("Activity Start date"),
                errors="coerce"
            )
            
            if (
                execution_status == "Executed"
                and pd.notna(activity_start_date)
                and execution_date < activity_start_date.date()
            ):
            
                st.error(
                    f"❌ Activity cannot be marked Executed "
                    f"before its Start Date "
                    f"({activity_start_date.strftime('%d-%b-%Y')})"
                )
            
                st.stop()
            
            success = update_activity_execution(
                zone=activity["Zone"],
                brand=activity["Brand"],
                year=activity["Year"],
                month=activity["Month"],
                activity_description=activity["Activity Description"],
                execution_status=execution_status,
                actual_investment=actual_investment,
                execution_date=execution_date.strftime("%d-%b-%Y"),
                remarks=remarks,
                supporting_link=supporting_link
            )
            if success:
                st.success("✅ Activity Updated Successfully!")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("❌ Matching Activity Not Found")
        except Exception as e:
            st.error(f"❌ Error during update: {e}")
else:
    st.error("Could not load activity details.")

if "Actual Investment" in df.columns:
    df["Actual Investment"] = (
        pd.to_numeric(
            df["Actual Investment"],
            errors="coerce"
        )
        .fillna(0)
    )
