import streamlit as st

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

import plotly.express as px
from utils.access import apply_role_access
from utils.gsheet import (
    load_expense_data,
    load_budget_data
)
from utils.preprocess import (
    preprocess_expense,
    preprocess_budget
)
from utils.sidebar import render_navigation
from utils.common_filters import (
    render_common_filters,
    apply_common_filters
)
from utils.ui import (
    inject_css,
    page_header,
    metric_card
)
from utils.formatters import (
    get_scaled_columns,
    current_unit
)

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Bifurcation Analysis",
    page_icon="📑",
    layout="wide"
)

inject_css()

# Small extra styling, layered on top of inject_css() so it doesn't
# fight with the shared theme used by the other pages.
st.markdown(
    """
    <style>
    div[data-testid="stExpander"] {
        border: 1px solid rgba(49, 51, 63, 0.15);
        border-radius: 10px;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600;
    }
    h3 {
        margin-top: 0.25rem;
    }
    .section-caption {
        color: rgba(49, 51, 63, 0.6);
        font-size: 0.85rem;
        margin-top: -0.6rem;
        margin-bottom: 0.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================
# LOAD DATA
# ==================================
try:
    df_exp = load_expense_data()
    df_budget = load_budget_data()
    df_exp = preprocess_expense(df_exp)
    df_budget = preprocess_budget(df_budget)
    df_exp = apply_role_access(df_exp)
    df_budget = apply_role_access(df_budget)
except Exception as e:
    st.error(f"Error Loading Data : {e}")
    st.stop()

# ==================================
# SIDEBAR
# ==================================
render_navigation()

filters = render_common_filters(df_budget)

df_budget = apply_common_filters(df_budget, filters)

if df_exp.empty:
    st.info("No data available for selected filters.")
    st.stop()

# ==================================
# PAGE HEADER
# ==================================
page_header(
    "📑 Bifurcation Analysis",
    "Marketing Expense Analysis by Activity Type & Bifurcation"
)

# ==================================
# KPI CALCULATIONS
# ==================================
gross_expense = df_exp["AMT(W/o GST)"].sum()
oem_support = df_exp["OEM Support"].sum()
net_expense = gross_expense - oem_support
total_budget = df_budget["Budget"].sum()
expense_pct = (net_expense / max(total_budget, 1)) * 100

# ==================================
# KPI CARDS
# ==================================
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    metric_card("💰 Total Budget", total_budget)
with c2:
    metric_card("💸 Gross Expense", gross_expense)
with c3:
    metric_card("🤝 OEM Support", oem_support)
with c4:
    metric_card("📉 Net Expense", net_expense)
with c5:
    metric_card("📈 Utilization", expense_pct, is_percent=True)

st.divider()

# ==================================
# MASTER BIFURCATION DATASET
# (Interactive drill-down table)
# ==================================

bif_master = (
    df_exp.groupby(
        [
            "Zone",
            "Brand",
            "Activity type",
            "Bifurcation"
        ],
        as_index=False
    )["AMT(W/o GST)"]
    .sum()
)

bif_master.rename(
    columns={
        "AMT(W/o GST)": "Expense"
    },
    inplace=True
)

overall_total = bif_master["Expense"].sum()

activity_total = bif_master.groupby(
    ["Zone", "Brand", "Activity type"]
)["Expense"].transform("sum")

brand_total = bif_master.groupby(
    ["Zone", "Brand"]
)["Expense"].transform("sum")

zone_total = bif_master.groupby("Zone")["Expense"].transform("sum")

bif_master["% of Activity"] = ((bif_master["Expense"] / activity_total) * 100).round(1)
bif_master["% of Brand"] = ((bif_master["Expense"] / brand_total) * 100).round(1)
bif_master["% of Zone"] = ((bif_master["Expense"] / zone_total) * 100).round(1)
bif_master["% of Total"] = ((bif_master["Expense"] / overall_total) * 100).round(1)

bif_master = bif_master.sort_values(
    ["Zone", "Brand", "Activity type", "Expense"],
    ascending=[True, True, True, False]
).reset_index(drop=True)

st.subheader("🔎 Bifurcation Drill-Down")
st.markdown(
    '<p class="section-caption">Filter by Zone / Brand / Activity type to drill into the bifurcation mix. '
    'Click a column header to sort.</p>',
    unsafe_allow_html=True
)

f1, f2, f3, f4 = st.columns(4)

with f1:
    zone_pick = st.multiselect(
        "Zone",
        options=sorted(bif_master["Zone"].unique()),
        default=[],
        key="bif_drill_zone"
    )
with f2:
    brand_pick = st.multiselect(
        "Brand",
        options=sorted(bif_master["Brand"].unique()),
        default=[],
        key="bif_drill_brand"
    )
with f3:
    activity_pick = st.multiselect(
        "Activity type",
        options=sorted(bif_master["Activity type"].unique()),
        default=[],
        key="bif_drill_activity"
    )
with f4:
    search_term = st.text_input(
        "Search Bifurcation",
        placeholder="e.g. Hoarding, Radio...",
        key="bif_drill_search"
    )

drill_df = bif_master.copy()

if zone_pick:
    drill_df = drill_df[drill_df["Zone"].isin(zone_pick)]
if brand_pick:
    drill_df = drill_df[drill_df["Brand"].isin(brand_pick)]
if activity_pick:
    drill_df = drill_df[drill_df["Activity type"].isin(activity_pick)]
if search_term:
    drill_df = drill_df[
        drill_df["Bifurcation"].str.contains(search_term, case=False, na=False)
    ]

if drill_df.empty:
    st.warning("No rows match the selected filters.")
else:
    drill_display, fmt = get_scaled_columns(drill_df.copy(), ["Expense"])
    pct_fmt = {
        "% of Activity": "{:.1f}%",
        "% of Brand": "{:.1f}%",
        "% of Zone": "{:.1f}%",
        "% of Total": "{:.1f}%",
    }
    fmt.update(pct_fmt)

    st.dataframe(
        drill_display.style.format(fmt).background_gradient(
            subset=["% of Total"], cmap="Blues"
        ),
        use_container_width=True,
        hide_index=True,
        height=380
    )

    filtered_total = drill_df["Expense"].sum()
    st.caption(
        f"Showing {len(drill_df):,} row(s) · "
        f"{filtered_total:,.0f} of overall {overall_total:,.0f} "
        f"({(filtered_total / overall_total * 100):.1f}% of total) · "
        f"Values shown in : {current_unit()}"
    )

st.divider()

# ==================================
# ACTIVITY TYPE CONTRIBUTION
# ==================================
activity_df = (
    df_exp.groupby("Activity type", as_index=False)["AMT(W/o GST)"]
    .sum()
    .sort_values("AMT(W/o GST)", ascending=False)
)

activity_df["Share %"] = (
    activity_df["AMT(W/o GST)"] / activity_df["AMT(W/o GST)"].sum() * 100
).round(1)

# ==================================
# BIFURCATION BREAKDOWN
# ==================================
bif_df = (
    df_exp.groupby("Bifurcation", as_index=False)["AMT(W/o GST)"]
    .sum()
    .sort_values("AMT(W/o GST)", ascending=False)
)

bif_df["Share %"] = (
    bif_df["AMT(W/o GST)"] / bif_df["AMT(W/o GST)"].sum() * 100
).round(1)

st.caption(f"Values shown in : {current_unit()}")

# ==================================
# CHARTS
# ==================================
left, right = st.columns(2)

# ----------------------------------
# ACTIVITY TYPE
# ----------------------------------
with left:
    st.subheader("📊 Activity Type Distribution")
    fig1 = px.bar(
        activity_df,
        x="AMT(W/o GST)",
        y="Activity type",
        orientation="h",
        text_auto=".2s",
        color="Activity type",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig1.update_layout(
        height=500,
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Expense",
        yaxis_title=""
    )
    st.plotly_chart(fig1, use_container_width=True)

    display_activity = activity_df.rename(
        columns={"AMT(W/o GST)": "Expense"}
    )
    display_activity, fmt = get_scaled_columns(display_activity, ["Expense"])

    with st.expander("📋 View Activity Details", expanded=False):
        st.dataframe(
            display_activity.style.format(fmt),
            use_container_width=True,
            hide_index=True
        )

# ----------------------------------
# BIFURCATION
# ----------------------------------
with right:
    st.subheader("📑 Bifurcation Distribution")
    fig2 = px.pie(
        bif_df,
        names="Bifurcation",
        values="AMT(W/o GST)",
        hole=0.60,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig2.update_traces(textinfo="percent+label")
    fig2.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)

    display_bif = bif_df.rename(columns={"AMT(W/o GST)": "Expense"})
    display_bif, fmt = get_scaled_columns(display_bif, ["Expense"])

    with st.expander("📋 View Bifurcation Details", expanded=False):
        st.dataframe(
            display_bif.style.format(fmt),
            use_container_width=True,
            hide_index=True
        )

st.divider()

# ==================================
# TOP 10 BIFURCATIONS
# ==================================
st.subheader("🏆 Top 10 Bifurcations by Spend")

top_bif = (
    df_exp.groupby("Bifurcation", as_index=False)["AMT(W/o GST)"]
    .sum()
    .sort_values("AMT(W/o GST)", ascending=False)
    .head(10)
)

fig3 = px.bar(
    top_bif,
    x="AMT(W/o GST)",
    y="Bifurcation",
    orientation="h",
    text_auto=".2s",
    color="AMT(W/o GST)",
    color_continuous_scale="Blues"
)

fig3.update_layout(
    height=550,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Expense",
    yaxis_title="",
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=10, b=10)
)

st.plotly_chart(fig3, use_container_width=True)

# ==================================
# TOP 10 TABLE
# ==================================
top_display = top_bif.rename(columns={"AMT(W/o GST)": "Expense"})
top_display, fmt = get_scaled_columns(top_display, ["Expense"])

with st.expander("📋 View Top 10 Details", expanded=False):
    st.dataframe(
        top_display.style.format(fmt),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==================================
# ZONE & BRAND ANALYSIS
# ==================================
zone_df = (
    df_exp.groupby("Zone", as_index=False)["AMT(W/o GST)"]
    .sum()
    .sort_values("AMT(W/o GST)", ascending=False)
)

brand_df = (
    df_exp.groupby("Brand", as_index=False)["AMT(W/o GST)"]
    .sum()
    .sort_values("AMT(W/o GST)", ascending=False)
)

st.subheader("📍 Zone & Brand Wise Expense")

left, right = st.columns(2)

with left:
    fig_zone = px.bar(
        zone_df,
        x="AMT(W/o GST)",
        y="Zone",
        orientation="h",
        text_auto=".2s",
        color="AMT(W/o GST)",
        color_continuous_scale="Teal"
    )
    fig_zone.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Expense",
        yaxis_title=""
    )
    st.plotly_chart(fig_zone, use_container_width=True)

    zone_display = zone_df.rename(columns={"AMT(W/o GST)": "Expense"})
    zone_display, fmt = get_scaled_columns(zone_display, ["Expense"])

    with st.expander("📋 View Zone Details", expanded=False):
        st.dataframe(
            zone_display.style.format(fmt),
            use_container_width=True,
            hide_index=True
        )

with right:
    fig_brand = px.bar(
        brand_df,
        x="AMT(W/o GST)",
        y="Brand",
        orientation="h",
        text_auto=".2s",
        color="AMT(W/o GST)",
        color_continuous_scale="Purp"
    )
    fig_brand.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Expense",
        yaxis_title=""
    )
    st.plotly_chart(fig_brand, use_container_width=True)

    brand_display = brand_df.rename(columns={"AMT(W/o GST)": "Expense"})
    brand_display, fmt = get_scaled_columns(brand_display, ["Expense"])

    with st.expander("📋 View Brand Details", expanded=False):
        st.dataframe(
            brand_display.style.format(fmt),
            use_container_width=True,
            hide_index=True
        )

st.caption(f"Values shown in : {current_unit()}")
st.caption("Made By Kuldeep Pal")
