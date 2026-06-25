
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
    page_title="📗 BRAND WISE MIS SUMMARY",
    page_icon="📗",
    layout="wide"
)

inject_css()

# ==================================
# LOAD DATA
# ==================================

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

    # Standardize keys

    df_exp["Zone"] = (
        df_exp["Zone"]
        .astype(str)
        .str.strip()
    )

    df_exp["Brand"] = (
        df_exp["Brand"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df_budget["Zone"] = (
        df_budget["Zone"]
        .astype(str)
        .str.strip()
    )

    df_budget["Brand"] = (
        df_budget["Brand"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

except Exception as e:

    st.error(f"Error Loading Data: {e}")
    st.stop()

# ==================================
# SIDEBAR
# ==================================

render_navigation()

filters = render_common_filters(df_budget)

df_budget = apply_common_filters(
    df_budget,
    filters
)

df_exp = apply_common_filters(
    df_exp,
    filters
)

if df_budget.empty:

    st.info(
        "No data available for selected filters."
    )

    st.stop()
# ==================================
# HEADER
# ==================================

page_header(
    "🚗 Brand Wise MIS Summary",
    "Brand → Zone | Budget vs Expenses"
)

# ==================================
# KPI SNAPSHOT
# ==================================

gross_expense = df_exp["AMT(W/o GST)"].sum()

oem_support = df_exp["OEM Support"].sum()

net_expense = gross_expense - oem_support

total_budget = df_budget["Budget"].sum()

expense_pct = (
    net_expense /
    max(total_budget, 1)
) * 100

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
        "📈 Expense %",
        expense_pct,
        is_percent=True
    )
# ==================================
# ACTIVITY SPLIT
# ==================================

activity_df = (
    df_exp.pivot_table(
        index=["Brand", "Zone"],
        columns="Activity type",
        values="AMT(W/o GST)",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

for col in [
    "ATL",
    "BTL",
    "DIGITAL",
    "FLEXY"
]:

    if col not in activity_df.columns:
        activity_df[col] = 0

# ==================================
# AGGREGATIONS
# ==================================

exp_sum = (
    df_exp.groupby(
        ["Brand", "Zone"],
        as_index=False
    )
    .agg({
        "AMT(W/o GST)": "sum",
        "OEM Support": "sum"
    })
    .rename(
        columns={
            "AMT(W/o GST)": "Gross Expense"
        }
    )
)

bud_sum = (
    df_budget.groupby(
        ["Brand", "Zone"],
        as_index=False
    )["Budget"]
    .sum()
)

df_summary = (
    bud_sum
    .merge(
        exp_sum,
        on=["Brand", "Zone"],
        how="left"
    )
    .merge(
        activity_df,
        on=["Brand", "Zone"],
        how="left"
    )
    .fillna(0)
)

# ==================================
# CALCULATIONS
# ==================================

df_summary["Net Expense"] = (
    df_summary["Gross Expense"]
    -
    df_summary["OEM Support"]
)

df_summary["Utilization %"] = (
    df_summary["Net Expense"]
    /
    df_summary["Budget"]
).replace(
    [float("inf"), -float("inf")],
    0
) * 100

df_summary["Utilization %"] = (
    df_summary["Utilization %"]
    .round(1)
)

# ==================================
# FINAL TABLE
# ==================================

final_rows = []

for brand, bdf in sorted(
    df_summary.groupby("Brand")
):

    bdf = bdf.sort_values("Zone")

    first = True

    for _, row in bdf.iterrows():

        r = row.to_dict()

        r["Brand"] = (
            brand
            if first
            else ""
        )

        final_rows.append(r)

        first = False

    final_rows.append({

        "Brand": f"{brand} TOTAL",

        "Zone": "",

        "Budget":
            bdf["Budget"].sum(),

        "OEM Support":
            bdf["OEM Support"].sum(),

        "ATL":
            bdf["ATL"].sum(),

        "BTL":
            bdf["BTL"].sum(),

        "DIGITAL":
            bdf["DIGITAL"].sum(),

        "FLEXY":
            bdf["FLEXY"].sum(),

        "Gross Expense":
            bdf["Gross Expense"].sum(),

        "Net Expense":
            bdf["Net Expense"].sum(),

        "Utilization %":
            round(
                (
                    bdf["Net Expense"].sum()
                    /
                    max(
                        bdf["Budget"].sum(),
                        1
                    )
                ) * 100,
                1
            )
    })
    
final_df = pd.DataFrame(
    final_rows
)

final_df = final_df[
    [
        "Brand",
        "Zone",
        "Budget",
        "OEM Support",
        "ATL",
        "BTL",
        "DIGITAL",
        "FLEXY",
        "Gross Expense",
        "Net Expense",
        "Utilization %"
    ]
]

# ==================================
# STYLING
# ==================================

def util_color(val):

    if val > 120:

        return (
            "background-color:#ff4d4d;"
            "color:white;"
            "font-weight:bold"
        )

    elif val >= 100:

        return (
            "background-color:#ffcc66;"
            "font-weight:bold"
        )

    return (
        "background-color:#90ee90;"
        "font-weight:bold"
    )


def brand_total_style(row):

    if "TOTAL" in str(row["Brand"]):

        return [
            "background-color:#002060;"
            "color:white;"
            "font-weight:bold"
        ] * len(row)

    return [""] * len(row)
    
styled = (
    final_df.style
    .map(
        util_color,
        subset=["Utilization %"]
    )
    .apply(
        brand_total_style,
        axis=1
    )
    .format({
        "Budget": "{:,.0f}",
        "OEM Support": "{:,.0f}",
        "ATL": "{:,.0f}",
        "BTL": "{:,.0f}",
        "DIGITAL": "{:,.0f}",
        "FLEXY": "{:,.0f}",
        "Gross Expense": "{:,.0f}",
        "Net Expense": "{:,.0f}",
        "Utilization %": "{:.1f}%"
    })
)
st.dataframe(
    styled,
    use_container_width=True,
    height=1100
)

st.caption(
    "🟢 <100% | 🟠 100–120% | 🔴 >120%"
)

st.divider()

st.caption(
    "Made By Kuldeep Pal"
)
