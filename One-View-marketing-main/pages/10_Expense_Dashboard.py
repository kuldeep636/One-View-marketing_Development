import streamlit as st
import pandas as pd

# ==================================
# AUTHENTICATION
# ==================================
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# ==================================
# IMPORTS
# ==================================
from utils.access import apply_role_access
from utils.gsheet import load_expense_data, load_budget_data
from utils.common_filters import render_common_filters, apply_common_filters
from utils.sidebar import render_navigation
from utils.ui import inject_css
from utils.preprocess import preprocess_expense, preprocess_budget

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Expense Dashboard",
    page_icon="💰",
    layout="wide"
)
inject_css()

# ==================================
# LOAD & PREPROCESS DATA
# ==================================
try:
    # Expense Data
    df = load_expense_data()
    df = preprocess_expense(df)
    df = apply_role_access(df)

    # Budget Data
    df_budget = load_budget_data()
    df_budget = preprocess_budget(df_budget)
    df_budget = apply_role_access(df_budget)

except Exception as e:
    st.error(f"❌ Error Loading Expense Data: {e}")
    st.stop()

# ==================================
# SIDEBAR & FILTERS
# ==================================
render_navigation()
filters = render_common_filters(df)

filtered_df = apply_common_filters(df, filters)
filtered_budget = apply_common_filters(df_budget, filters)

# ==================================
# EMPTY DATA CHECK
# ==================================
if filtered_df.empty:
    st.info("No Expense Data Available For Selected Filters.")
    st.stop()

# ==================================
# HEADER
# ==================================
st.markdown("""
<h1 style='margin-bottom:0'>
    💰 EXPENSE DASHBOARD
</h1>
<p style='font-size:16px;color:gray'>
    Landmark Cars Marketing Expense Dashboard
</p>
""", unsafe_allow_html=True)

st.divider()

# ==================================
# KPI CALCULATIONS
# ==================================
gross_expense = filtered_df.get("AMT(W/o GST)", pd.Series(0)).sum()
oem_support = filtered_df.get("OEM Support", pd.Series(0)).sum()

# Ensure Net Expenses column exists (fallback calculation)
if "Net Expenses" not in filtered_df.columns:
    filtered_df = filtered_df.copy()
    filtered_df["Net Expenses"] = (
        filtered_df.get("AMT(W/o GST)", 0) - filtered_df.get("OEM Support", 0)
    )

net_expense = filtered_df["Net Expenses"].sum()
total_budget = filtered_budget.get("Budget", pd.Series(0)).sum()

expense_pct = (net_expense / max(total_budget, 1)) * 100

# ==================================
# KPI CARDS
# ==================================
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Total Budget", f"₹ {total_budget:,.0f}")
c2.metric("💸 Gross Expense", f"₹ {gross_expense:,.0f}")
c3.metric("🤝 OEM Support", f"₹ {oem_support:,.0f}")
c4.metric("📉 Net Expense", f"₹ {net_expense:,.0f}")
c5.metric("📈 Expense % of Budget", f"{expense_pct:.1f}%", 
          delta=f"{expense_pct-100:+.1f}%" if expense_pct != 100 else None)

st.divider()

# ==================================
# CHARTS
# ==================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Zone Wise Expense")
    if "Zone" in filtered_df.columns and "Net Expenses" in filtered_df.columns:
        zone_df = (
            filtered_df.groupby("Zone", as_index=False)["Net Expenses"]
            .sum()
            .sort_values("Net Expenses", ascending=False)
        )
        st.bar_chart(zone_df.set_index("Zone"), use_container_width=True)
    else:
        st.info("Zone or Net Expenses data not available.")

with col2:
    st.subheader("🚗 Brand Wise Expense")
    if "Brand" in filtered_df.columns and "Net Expenses" in filtered_df.columns:
        brand_df = (
            filtered_df.groupby("Brand", as_index=False)["Net Expenses"]
            .sum()
            .sort_values("Net Expenses", ascending=False)
        )
        st.bar_chart(brand_df.set_index("Brand"), use_container_width=True)
    else:
        st.info("Brand or Net Expenses data not available.")

st.divider()

# Activity Type Analysis
if "Activity Type" in filtered_df.columns or "Activity type" in filtered_df.columns:
    activity_col = "Activity Type" if "Activity Type" in filtered_df.columns else "Activity type"
    
    st.subheader("📢 Activity Type Spend")
    activity_df = (
        filtered_df.groupby(activity_col, as_index=False)["Net Expenses"]
        .sum()
        .sort_values("Net Expenses", ascending=False)
    )
    st.bar_chart(activity_df.set_index(activity_col), use_container_width=True)
    st.divider()

# ==================================
# DETAILED TABLE
# ==================================
with st.expander("📋 View All Expense Details", expanded=False):
    display_df = filtered_df.copy()
    
    # Format numeric columns
    numeric_cols = ["AMT(W/o GST)", "OEM Support", "Net Expenses", "Actual Investment"]
    for col in numeric_cols:
        if col in display_df.columns:
            display_df[col] = pd.to_numeric(display_df[col], errors="coerce").fillna(0)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# ==================================
# FOOTER
# ==================================
st.divider()
st.caption("Made By Kuldeep Pal")
