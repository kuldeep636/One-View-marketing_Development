# ==================================
# 1. IMPORTS
# ==================================
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.ui import inject_css
from utils.sidebar import render_navigation
from utils.common_filters import render_common_filters, apply_common_filters
from utils.access import apply_role_access
from utils.gsheet import load_activity_data
from utils.activity import render_activity_breakdown

# ==================================
# 2. PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Marketing Plan",
    page_icon="🚗",
    layout="wide"
)
inject_css()

# ==================================
# 3. LOAD DATA
# ==================================
try:
    df = load_activity_data()
    df = apply_role_access(df)
except Exception as e:
    st.error(f"❌ Google Sheet Connection Error: {e}")
    st.stop()

# ==================================
# 4. SIDEBAR & FILTERS
# ==================================
render_navigation()
filters = render_common_filters(df)

# ==================================
# 5. HEADER
# ==================================
st.markdown("""
<h1 style='margin-bottom:0'>
    📋 ONE VIEW MARKETING PLAN
</h1>
<p style='font-size:16px;color:gray'>
    Landmark Cars Marketing Plan Tracker
</p>
""", unsafe_allow_html=True)

st.caption(f"Last Refreshed: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
st.divider()

# ==================================
# 6. APPLY FILTERS
# ==================================
view_df = apply_common_filters(df, filters)

# Additional session state filters
if st.session_state.get("selected_activity"):
    view_df = view_df[
        view_df["Activity Type"].str.upper() == st.session_state.selected_activity.upper()
    ]
if st.session_state.get("selected_subtype"):
    view_df = view_df[view_df["Activity Sub Type"] == st.session_state.selected_subtype]

# ==================================
# 7. ACTIVE FILTER INDICATORS
# ==================================
if st.session_state.get("selected_activity"):
    st.info(f"🎯 Activity Filter: **{st.session_state.selected_activity}**")
if st.session_state.get("selected_subtype"):
    st.success(f"🔍 Sub Type Filter: **{st.session_state.selected_subtype}**")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("❌ Clear All Filters", use_container_width=True):
        for key in ["selected_activity", "selected_subtype"]:
            if key in st.session_state:
                st.session_state[key] = None
        st.rerun()

st.divider()

# ==================================
# 8. DATA NORMALIZATION (Once)
# ==================================
view_df = view_df.copy()
view_df["Activity Type"] = view_df["Activity Type"].astype(str).str.strip().str.upper()

# ==================================
# 9. KPI CALCULATIONS
# ==================================
planned = len(view_df)
executed = len(view_df[view_df["Execution Status"] == "Executed"])
pending = len(view_df[view_df["Execution Status"] == "Pending"])
cancelled = len(view_df[view_df["Execution Status"] == "Cancelled"])

execution_pct = round((executed / planned) * 100, 1) if planned > 0 else 0

atl_count = len(view_df[view_df["Activity Type"] == "ATL"])
btl_count = len(view_df[view_df["Activity Type"] == "BTL"])
digital_count = len(view_df[view_df["Activity Type"] == "DIGITAL"])
flexy_count = len(view_df[view_df["Activity Type"] == "FLEXY"])

# ==================================
# KPI CARDS
# ==================================
st.markdown("## 📊 Plan Overview")

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1:
    st.metric("📍 Zones", view_df["Zone"].nunique())

with c2:
    st.metric("🚗 Brands", view_df["Brand"].nunique())

with c3:
    st.metric("📋 Planned", f"{planned:,}")

with c4:
    st.metric("✅ Executed", f"{executed:,}")

with c5:
    st.metric("⏳ Pending", f"{pending:,}")

with c6:
    st.metric("❌ Cancelled", f"{cancelled:,}")

with c7:
    st.metric("🎯 Execution %", f"{execution_pct}%")

st.markdown("")


st.divider()

# ==================================
# ACTIVITY BREAKDOWN
# ==================================

render_activity_breakdown(view_df)

st.divider()

# ==================================
# 10. ZONE & BRAND VIEW
# ==================================
left, right = st.columns(2)

# ------------------- ZONE VIEW -------------------
with left:
    st.subheader("📍 Zone View")
    for zone_name in sorted(view_df["Zone"].dropna().unique()):
        zone_df = view_df[view_df["Zone"] == zone_name]
        
        atl = len(zone_df[zone_df["Activity Type"] == "ATL"])
        btl = len(zone_df[zone_df["Activity Type"] == "BTL"])
        digital = len(zone_df[zone_df["Activity Type"] == "DIGITAL"])
        
        with st.expander(f"{zone_name} | ATL: {atl} | BTL: {btl} | Digital: {digital}"):
            for brand_name in sorted(zone_df["Brand"].dropna().unique()):
                brand_df = zone_df[zone_df["Brand"] == brand_name]
                
                b_atl = len(brand_df[brand_df["Activity Type"] == "ATL"])
                b_btl = len(brand_df[brand_df["Activity Type"] == "BTL"])
                b_digital = len(brand_df[brand_df["Activity Type"] == "DIGITAL"])
                
                st.markdown(
                    f"🚗 **{brand_name}** — "
                    f"ATL: **{b_atl}** | BTL: **{b_btl}** | Digital: **{b_digital}**"
                )

# ------------------- BRAND VIEW -------------------
with right:
    st.subheader("🚗 Brand View")
    for brand_name in sorted(view_df["Brand"].dropna().unique()):
        brand_df = view_df[view_df["Brand"] == brand_name]
        
        atl = len(brand_df[brand_df["Activity Type"] == "ATL"])
        btl = len(brand_df[brand_df["Activity Type"] == "BTL"])
        digital = len(brand_df[brand_df["Activity Type"] == "DIGITAL"])
        
        with st.expander(f"{brand_name} | ATL: {atl} | BTL: {btl} | Digital: {digital}"):
            for zone_name in sorted(brand_df["Zone"].dropna().unique()):
                zone_brand_df = brand_df[brand_df["Zone"] == zone_name]
                
                z_atl = len(zone_brand_df[zone_brand_df["Activity Type"] == "ATL"])
                z_btl = len(zone_brand_df[zone_brand_df["Activity Type"] == "BTL"])
                z_digital = len(zone_brand_df[zone_brand_df["Activity Type"] == "DIGITAL"])
                
                st.markdown(
                    f"📍 **{zone_name}** — "
                    f"ATL: **{z_atl}** | BTL: **{z_btl}** | Digital: **{z_digital}**"
                )

st.divider()

# ==================================
# 11. ACTIVITY DETAILS
# ==================================
with st.expander("📋 View All Planned Activities", expanded=False):
    if not view_df.empty:
        st.dataframe(
            view_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No data available for the selected filters.")

# ==================================
# 12. FOOTER
# ==================================
st.caption("Made By Kuldeep Pal")
