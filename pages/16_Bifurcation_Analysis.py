import streamlit as st

if not st.session_state.get(
    "logged_in",
    False
):
    st.warning(
        "Please login first."
    )
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

    st.error(
        f"Error Loading Data : {e}"
    )

    st.stop()

# ==================================
# SIDEBAR
# ==================================

render_navigation()

filters = render_common_filters(
    df_budget
)

df_budget = apply_common_filters(
    df_budget,
    filters
)

df_exp = apply_common_filters(
    df_exp,
    filters
)

if df_exp.empty:

    st.info(
        "No data available for selected filters."
    )

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

gross_expense = (
    df_exp["AMT(W/o GST)"]
    .sum()
)

oem_support = (
    df_exp["OEM Support"]
    .sum()
)

net_expense = (
    gross_expense
    -
    oem_support
)

total_budget = (
    df_budget["Budget"]
    .sum()
)

expense_pct = (
    net_expense
    /
    max(total_budget, 1)
) * 100

# ==================================
# KPI CARDS
# ==================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    metric_card(
        "💰 Total Budget",
        total_budget
    )

with c2:

    metric_card(
        "💸 Gross Expense",
        gross_expense
    )

with c3:

    metric_card(
        "🤝 OEM Support",
        oem_support
    )

with c4:

    metric_card(
        "📉 Net Expense",
        net_expense
    )

with c5:

    metric_card(
        "📈 Utilization",
        expense_pct,
        is_percent=True
    )

st.divider()

# ==================================
# ACTIVITY TYPE CONTRIBUTION
# ==================================

activity_df = (
    df_exp.groupby(
        "Activity type",
        as_index=False
    )["AMT(W/o GST)"]
    .sum()
    .sort_values(
        "AMT(W/o GST)",
        ascending=False
    )
)

activity_df["Share %"] = (
    activity_df["AMT(W/o GST)"]
    /
    activity_df["AMT(W/o GST)"].sum()
    * 100
).round(1)



# ==================================
# BIFURCATION BREAKDOWN
# ==================================

bif_df = (
    df_exp.groupby(
        "Bifurcation",
        as_index=False
    )["AMT(W/o GST)"]
    .sum()
    .sort_values(
        "AMT(W/o GST)",
        ascending=False
    )
)

bif_df["Share %"] = (
    bif_df["AMT(W/o GST)"]
    /
    bif_df["AMT(W/o GST)"].sum()
    * 100
).round(1)

st.caption(
    f"Values shown in : {current_unit()}"
)

# ==================================
# CHARTS
# ==================================

left, right = st.columns(2)

# ----------------------------------
# ACTIVITY TYPE
# ----------------------------------

with left:

    st.subheader(
        "📑 Bifurcation Distribution"
)

    fig1 = px.bar(
        activity_df,
        x="AMT(W/o GST)",
        y="Activity type",
        orientation="h",
        text_auto=".2s"
    )

    fig1.update_layout(
        height=500,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    display_activity = activity_df.rename(
        columns={
            "AMT(W/o GST)": "Expense"
        }
    )

    display_activity, fmt = get_scaled_columns(
        display_activity,
        ["Expense"]
    )

    st.dataframe(
        display_activity.style.format(fmt),
        use_container_width=True,
        hide_index=True
    )

# ----------------------------------
# BIFURCATION
# ----------------------------------

with right:

    st.subheader(
        f"📑 {selected_activity} Breakdown"
    )

    fig2 = px.pie(
        bif_df,
        names="Bifurcation",
        values="AMT(W/o GST)",
        hole=.60
    )

    fig2.update_traces(
        textinfo="percent+label"
    )

    fig2.update_layout(
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    display_bif = bif_df.rename(
        columns={
            "AMT(W/o GST)": "Expense"
        }
    )

    display_bif, fmt = get_scaled_columns(
        display_bif,
        ["Expense"]
    )

    st.dataframe(
        display_bif.style.format(fmt),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==================================
# TOP 10 BIFURCATIONS
# ==================================

st.subheader(
    "🏆 Top 10 Bifurcations by Spend"
)

top_bif = (
    df_exp.groupby(
        "Bifurcation",
        as_index=False
    )["AMT(W/o GST)"]
    .sum()
    .sort_values(
        "AMT(W/o GST)",
        ascending=False
    )
    .head(10)
)

fig3 = px.bar(
    top_bif,
    x="AMT(W/o GST)",
    y="Bifurcation",
    orientation="h",
    text_auto=".2s"
)

fig3.update_layout(
    height=550,
    yaxis=dict(
        categoryorder="total ascending"
    ),
    xaxis_title="Expense",
    yaxis_title=""
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==================================
# TOP 10 TABLE
# ==================================

top_display = top_bif.rename(
    columns={
        "AMT(W/o GST)": "Expense"
    }
)

top_display, fmt = get_scaled_columns(
    top_display,
    ["Expense"]
)

st.dataframe(
    top_display.style.format(fmt),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    f"Values shown in : {current_unit()}"
)

st.caption(
    "Made By Kuldeep Pal"
)
