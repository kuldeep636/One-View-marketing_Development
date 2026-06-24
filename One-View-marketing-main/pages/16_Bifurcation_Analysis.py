import streamlit as st

if not st.session_state.get(
    "logged_in",
    False
):
    st.warning(
        "Please login first."
    )
    st.stop()

from utils.access import apply_role_access

import plotly.express as px

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

from utils.ui import inject_css

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
        f"Error Loading Data: {e}"
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
# HEADER
# ==================================

st.markdown("""
<h1 style='margin-bottom:0'>
📑 BIFURCATION ANALYSIS
</h1>

<p style='font-size:16px;color:gray'>
Brand → Activity type → Bifurcation
</p>
""", unsafe_allow_html=True)

st.divider()

# ==================================
# KPI CARDS
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

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "💰 Total Budget",
    f"₹ {total_budget:,.0f}"
)

c2.metric(
    "💸 Gross Expense",
    f"₹ {gross_expense:,.0f}"
)

c3.metric(
    "🤝 OEM Support",
    f"₹ {oem_support:,.0f}"
)

c4.metric(
    "📉 Net Expense",
    f"₹ {net_expense:,.0f}"
)

c5.metric(
    "📈 Expense %",
    f"{expense_pct:.1f}%"
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
)

activity_df["Share %"] = (
    activity_df["AMT(W/o GST)"]
    /
    activity_df["AMT(W/o GST)"].sum()
    * 100
).round(1)

# ==================================
# ACTIVITY SELECTOR
# ==================================

selected_activity = st.radio(
    "🎯 Activity Type",
    activity_df["Activity type"].tolist(),
    horizontal=True
)

# ==================================
# BIFURCATION BREAKDOWN
# ==================================

bif_df = (
    df_exp[
        df_exp["Activity type"]
        == selected_activity
    ]
    .groupby(
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

# ==================================
# DONUT CHARTS
# ==================================

fig1 = px.pie(
    activity_df,
    names="Activity type",
    values="AMT(W/o GST)",
    hole=0.65
)

fig1.update_traces(
    textinfo="percent+label"
)

fig1.update_layout(
    height=500,
    showlegend=True
)

fig2 = px.pie(
    bif_df,
    names="Bifurcation",
    values="AMT(W/o GST)",
    hole=0.65
)

fig2.update_traces(
    textinfo="percent+label"
)

fig2.update_layout(
    height=500,
    showlegend=True
)

# ==================================
# DISPLAY CHARTS
# ==================================

left, right = st.columns(2)

with left:

    st.subheader(
        "📊 Activity Type Contribution"
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

    st.dataframe(
        display_activity,
        use_container_width=True,
        hide_index=True
    )

with right:

    st.subheader(
        f"📑 {selected_activity} Breakdown"
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

    st.dataframe(
        display_bif,
        use_container_width=True,
        hide_index=True
    )

# ==================================
# TOP 10 BIFURCATIONS
# ==================================

st.divider()

st.subheader(
    "🏆 Top 10 Bifurcations by Spend"
)

top_bif = (
    df_exp.groupby(
        "Bifurcation"
    )["AMT(W/o GST)"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_bif,
    x="AMT(W/o GST)",
    y="Bifurcation",
    orientation="h",
    text_auto=".2s"
)

fig3.update_layout(
    height=500,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

st.caption(
    "Made By Kuldeep Pal"
)
