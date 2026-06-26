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
df_exp = apply_common_filters(
    df_exp,
    filters
)
# ==================================
# MASTER BIFURCATION DATASET
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

# ==================================
# TOTALS
# ==================================

overall_total = (
    bif_master["Expense"]
    .sum()
)

activity_total = (
    bif_master.groupby(
        [
            "Zone",
            "Brand",
            "Activity type"
        ]
    )["Expense"]
    .transform("sum")
)

brand_total = (
    bif_master.groupby(
        [
            "Zone",
            "Brand"
        ]
    )["Expense"]
    .transform("sum")
)

zone_total = (
    bif_master.groupby(
        "Zone"
    )["Expense"]
    .transform("sum")
)

# ==================================
# PERCENTAGES
# ==================================

bif_master["% of Activity"] = (
    (
        bif_master["Expense"]
        /
        activity_total
    ) * 100
).round(1)

bif_master["% of Brand"] = (
    (
        bif_master["Expense"]
        /
        brand_total
    ) * 100
).round(1)

bif_master["% of Zone"] = (
    (
        bif_master["Expense"]
        /
        zone_total
    ) * 100
).round(1)

bif_master["% of Total"] = (
    (
        bif_master["Expense"]
        /
        overall_total
    ) * 100
).round(1)

# ==================================
# SORT DATA
# ==================================

bif_master = bif_master.sort_values(
    [
        "Zone",
        "Brand",
        "Activity type",
        "Expense"
    ],
    ascending=[
        True,
        True,
        True,
        False
    ]
).reset_index(drop=True)

# ==================================
# DISPLAY MASTER DATASET
# (Temporary - Remove Later)
# ==================================




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
# ACTIVITY SUMMARY
# ==================================

activity_summary = (
    df_exp.groupby(
        "Activity type",
        as_index=False
    )["AMT(W/o GST)"]
    .sum()
)

activity_summary.rename(
    columns={
        "AMT(W/o GST)": "Expense"
    },
    inplace=True
)

activity_summary["% of Total"] = (
    activity_summary["Expense"]
    /
    activity_summary["Expense"].sum()
    * 100
).round(1)

activity_summary = activity_summary.sort_values(
    "Expense",
    ascending=False
)

# ==================================
# TOP BIFURCATIONS
# ==================================

top_bif = (
    df_exp.groupby(
        "Bifurcation",
        as_index=False
    )["AMT(W/o GST)"]
    .sum()
)

top_bif.rename(
    columns={
        "AMT(W/o GST)": "Expense"
    },
    inplace=True
)

top_bif["% of Total"] = (
    top_bif["Expense"]
    /
    top_bif["Expense"].sum()
    * 100
).round(1)

top_bif = top_bif.sort_values(
    "Expense",
    ascending=False
).head(10)

# ==================================
# CHARTS
# ==================================

left, right = st.columns(2)

with left:

    st.subheader(
        "📊 Activity Type Contribution"
    )

    fig1 = px.bar(

        activity_summary,

        x="Expense",

        y="Activity type",

        orientation="h",

        text_auto=".2s"

    )

    fig1.update_layout(

        height=450,

        yaxis=dict(
            categoryorder="total ascending"
        ),

        xaxis_title="Expense",

        yaxis_title=""

    )

    st.plotly_chart(

        fig1,

        use_container_width=True

    )

with right:

    st.subheader(
        "🏆 Top 10 Bifurcations"
    )

    fig2 = px.bar(

        top_bif,

        x="Expense",

        y="Bifurcation",

        orientation="h",

        text_auto=".2s"

    )

    fig2.update_layout(

        height=450,

        yaxis=dict(
            categoryorder="total ascending"
        ),

        xaxis_title="Expense",

        yaxis_title=""

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

st.divider()

left, right = st.columns(2)

with left:

    st.subheader(
        "📋 Activity Summary"
    )

    activity_display, fmt = get_scaled_columns(

        activity_summary,

        ["Expense"]

    )

    st.dataframe(

        activity_display.style.format({

            **fmt,

            "% of Total": "{:.1f}%"

        }),

        use_container_width=True,

        hide_index=True

    )

with right:

    st.subheader(
        "📋 Top Bifurcations"
    )

    bif_display, fmt = get_scaled_columns(

        top_bif,

        ["Expense"]

    )

    st.dataframe(

        bif_display.style.format({

            **fmt,

            "% of Total": "{:.1f}%"

        }),

        use_container_width=True,

        hide_index=True

    )


# ==================================
# ZONE WISE SUMMARY
# ==================================

zone_budget = (
    df_budget.groupby(
        "Zone",
        as_index=False
    )["Budget"]
    .sum()
)

zone_expense = (
    df_exp.groupby(
        "Zone",
        as_index=False
    )
    .agg(
        {
            "AMT(W/o GST)": "sum",
            "OEM Support": "sum"
        }
    )
)

zone_summary = zone_budget.merge(

    zone_expense,

    on="Zone",

    how="left"

).fillna(0)

zone_summary.rename(

    columns={

        "AMT(W/o GST)": "Gross Expense"

    },

    inplace=True

)

zone_summary["Net Expense"] = (

    zone_summary["Gross Expense"]

    -

    zone_summary["OEM Support"]

)

zone_summary["Utilization %"] = (

    zone_summary["Net Expense"]

    /

    zone_summary["Budget"]

    *100

).round(1)

top_activity = (

    df_exp.groupby(

        ["Zone","Activity type"]

    )["AMT(W/o GST)"]

    .sum()

    .reset_index()

)

top_activity = (

    top_activity.sort_values(

        "AMT(W/o GST)",

        ascending=False

    )

    .drop_duplicates(

        "Zone"

    )

)

top_bif = (

    df_exp.groupby(

        ["Zone","Bifurcation"]

    )["AMT(W/o GST)"]

    .sum()

    .reset_index()

)

top_bif = (

    top_bif.sort_values(

        "AMT(W/o GST)",

        ascending=False

    )

    .drop_duplicates(

        "Zone"

    )

)

zone_summary = (

    zone_summary

    .merge(

        top_activity[

            ["Zone","Activity type"]

        ],

        on="Zone",

        how="left"

    )

    .merge(

        top_bif[

            ["Zone","Bifurcation"]

        ],

        on="Zone",

        how="left"

    )

)

zone_summary.rename(

    columns={

        "Activity type":"Top Activity",

        "Bifurcation":"Top Bifurcation"

    },

    inplace=True

)




st.caption(f"Values shown in : {current_unit()}")
st.caption("Made By Kuldeep Pal")
