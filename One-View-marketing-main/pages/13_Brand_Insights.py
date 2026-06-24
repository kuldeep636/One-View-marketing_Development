import streamlit as st
from utils.access import apply_role_access
if not st.session_state.get(
    "logged_in",
    False
):

    st.warning(
        "Please login first."
    )

    st.stop()
import pandas as pd
import plotly.express as px

from utils.gsheet import load_expense_data
from utils.preprocess import preprocess_expense
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
page_title="Brand Insight",
page_icon="📊",
layout="wide"
)

inject_css()
st.markdown("""
<style>
[data-testid="stVerticalBlockBorderWrapper"]{
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ==================================

# LOAD DATA

# ==================================

try:

    df = load_expense_data()

    df = preprocess_expense(df)

    df = apply_role_access(df)

except Exception as e:

    st.error(f"Error Loading Data: {e}")

    st.stop()

# ==================================

# SIDEBAR

# ==================================

render_navigation()

filters = render_common_filters(df)

df = apply_common_filters(
    df,
    filters
)

if df.empty:

    st.info(
        "No data available for selected filters."
    )

    st.stop()
    
# ==================================

# HEADER

# ==================================

st.markdown(
""" <h1 style='margin-bottom:0'>
📊 BRAND INSIGHT </h1>


<p style='font-size:16px;color:gray'>
Activity-wise Gross Expense Distribution
</p>
""",
unsafe_allow_html=True


)

st.divider()

# ==================================

# BRAND ORDER

# ==================================

brands = (
df.groupby("Brand")["AMT(W/o GST)"]
.sum()
.sort_values(ascending=False)
.index
)

# ==================================

# COLORS

# ==================================

COLOR_MAP = {
"ATL": "#FFB3B3",
"BTL": "#FF3B3B",
"DIGITAL": "#0A66C2",
"FLEXY": "#8FD0FF"
}

# ==================================

# DONUT CHARTS

# ==================================

cols = st.columns(3)

col_index = 0

for brand in brands:

    brand_df = df[
        df["Brand"] == brand
    ]

    gross_expense = (
        brand_df["AMT(W/o GST)"]
        .sum()
    )

    activity_df = (
        brand_df.groupby(
            "Activity type",
            as_index=False
        )
        .agg({
            "AMT(W/o GST)": "sum"
        })
    )

    activity_df = activity_df[
        activity_df["AMT(W/o GST)"] > 0
    ]

    if activity_df.empty:
        continue

    fig = px.pie(
        activity_df,
        names="Activity type",
        values="AMT(W/o GST)",
        hole=0.65,
        color="Activity type",
        color_discrete_map=COLOR_MAP
    )

    fig.update_traces(
        textinfo="percent",
        textfont_size=12
    )

    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.20,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(
            t=10,
            b=20,
            l=10,
            r=10
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    with cols[col_index]:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    min-height:60px;
                    padding:10px;
                ">
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <h3 style="
                    text-align:center;
                    margin-bottom:5px;
                ">
                    {brand}
                </h3>
                """,
                unsafe_allow_html=True
            )

            st.metric(
                "Gross Expense",
                f"₹ {gross_expense:,.0f}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            activity_df["Share %"] = (
                activity_df["AMT(W/o GST)"]
                /
                gross_expense
                * 100
            ).round(1)

            display_df = activity_df.rename(
                columns={
                    "Activity type": "Activity",
                    "AMT(W/o GST)": "Expense"
                }
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=180
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    col_index = (col_index + 1) % 3
st.divider()

st.caption(
"Made By Kuldeep Pal"
)
