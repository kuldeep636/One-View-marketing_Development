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
    page_title="Brand Treemap Analysis",
    page_icon="🟩",
    layout="wide"
)

inject_css()

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

st.markdown("""
<h1 style='margin-bottom:0'>
🟩 BRAND TREEMAP ANALYSIS
</h1>

<p style='font-size:16px;color:gray'>
Activity → Top 5 Vendors | Gross Expense
</p>
""", unsafe_allow_html=True)

st.divider()

# ==================================
# BRAND ORDER
# ==================================

brands = (
    df.groupby("Brand")["AMT(W/o GST)"]
    .sum()
    .sort_values(ascending=False)
    .index
    .tolist()
)

# ==================================
# TREEMAPS
# ==================================

for i in range(0, len(brands), 2):

    row_brands = brands[i:i + 2]

    cols = st.columns(2)

    for col, brand in zip(cols, row_brands):

        brand_df = df[
            df["Brand"] == brand
        ]

        vendor_df = (
            brand_df
            .groupby(
                ["Activity type", "Vendor"],
                as_index=False
            )["AMT(W/o GST)"]
            .sum()
        )

        vendor_df["Rank"] = (
            vendor_df
            .groupby("Activity type")
            ["AMT(W/o GST)"]
            .rank(
                method="first",
                ascending=False
            )
        )

        vendor_df = vendor_df[
            vendor_df["Rank"] <= 5
        ]

        if vendor_df.empty:
            continue

        vendor_df["Brand"] = brand

        fig = px.treemap(
            vendor_df,
            path=[
                "Brand",
                "Activity type",
                "Vendor"
            ],
            values="AMT(W/o GST)",
            color="Activity type",
            color_discrete_map={
                "ATL": "#2563eb",
                "BTL": "#16a34a",
                "DIGITAL": "#f59e0b",
                "FLEXY": "#dc2626"
            }
        )

        fig.update_traces(
            texttemplate=
            "<b>%{label}</b><br>"
            "₹%{value:,.0f}",
            textposition="middle center",
            hovertemplate=
            "<b>%{label}</b><br>"
            "Amount: ₹%{value:,.0f}<br>"
            "Share: %{percentParent:.1%}"
            "<extra></extra>"
        )

        fig.update_layout(
            height=450,
            margin=dict(
                t=10,
                b=10,
                l=5,
                r=5
            ),
            uniformtext=dict(
                minsize=10,
                mode="hide"
            )
        )

        with col:

            with st.container(border=True):

                gross_expense = (
                    brand_df["AMT(W/o GST)"]
                    .sum()
                )

                st.markdown(
                    f"""
                    <h3 style='text-align:center'>
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

st.divider()

st.caption(
    "Made By Kuldeep Pal"
)
