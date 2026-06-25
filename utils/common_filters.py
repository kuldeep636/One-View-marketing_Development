import streamlit as st
import pandas as pd

from utils.reporting import (
    prepare_reporting,
    get_month_order,
    get_quarters
)

df = prepare_reporting(df)
# ==================================
# UNIVERSAL FILTERS
# ==================================

def render_common_filters(df):

    st.sidebar.markdown("## 🔍 Filters")

# ==================================
# PREPARE REPORTING COLUMNS
# ==================================

df = prepare_reporting(df)

    # ==================================
    # RESET FILTERS
    # ==================================

    if st.sidebar.button("🔄 Reset Filters"):

        filter_keys = [
            "year_filter",
            "month_filter",
            "vertical_filter",
            "activity_type_filter",
            "zone_filter",
            "brand_filter",
            "location_filter"
        ]

        for key in filter_keys:

            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    # ==================================
    # REPORTING TYPE
    # ==================================
    
    reporting_type = st.sidebar.selectbox(
        "📅 Reporting Type",
        [
            "Calendar Year",
            "Financial Year"
        ],
        key="reporting_type"
    )


# ==================================
# QUARTER
# ==================================

quarter_column = (
    "Financial Quarter"
    if reporting_type == "Financial Year"
    else "Calendar Quarter"
)

quarter = st.sidebar.selectbox(
    "Quarter",
    ["All"] + get_quarters(),
    key="quarter_filter"
)

quarter_df = year_df.copy()

if quarter != "All":

    quarter_df = quarter_df[
        quarter_df[quarter_column] == quarter
    ]   

   if filters["year"]:

    year_column = (
        "Financial Year"
        if filters["reporting_type"] == "Financial Year"
        else "Year"
    )

    filtered_df = filtered_df[
        filtered_df[year_column]
        .astype(str)
        .isin(filters["year"])
    ]
    if filters["quarter"] != "All":

    quarter_column = (
        "Financial Quarter"
        if filters["reporting_type"] == "Financial Year"
        else "Calendar Quarter"
    )

    filtered_df = filtered_df[
        filtered_df[quarter_column] == filters["quarter"]
    ]
    
    # ==================================
    # MONTH
    # ==================================

    month_list = (
        year_df["Month"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    try:

        month_list = sorted(
            month_list,
            key=lambda x: pd.to_datetime(x)
        )

    except Exception:

        month_list = sorted(month_list)

    month = st.sidebar.multiselect(
        "Month",
        month_list,
        key="month_filter"
    )

    month_df = quarter_df.copy()

    month_order = get_month_order(reporting_type)

    month_list = sorted(
        month_list,
        key=lambda x: month_order.index(x)
        if x in month_order
        else 999
    )

    # ==================================
    # VERTICAL
    # ==================================

    if "Vertical" in month_df.columns:

        vertical_list = sorted(
            month_df["Vertical"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        vertical = st.sidebar.multiselect(
            "Vertical",
            vertical_list,
            key="vertical_filter"
        )

    else:

        vertical = []

    vertical_df = month_df.copy()

    if (
        "Vertical" in vertical_df.columns
        and vertical
    ):

        vertical_df = vertical_df[
            vertical_df["Vertical"]
            .astype(str)
            .isin(vertical)
        ]

    # ==================================
    # ACTIVITY TYPE
    # ==================================

    if "Activity Type" in vertical_df.columns:

        activity_type_list = sorted(
            vertical_df["Activity Type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        activity_type = st.sidebar.multiselect(
            "Activity Type",
            activity_type_list,
            key="activity_type_filter"
        )

    else:

        activity_type = []

    activity_df = vertical_df.copy()

    if (
        "Activity Type" in activity_df.columns
        and activity_type
    ):

        activity_df = activity_df[
            activity_df["Activity Type"]
            .astype(str)
            .isin(activity_type)
        ]

    # ==================================
    # ZONE
    # ==================================

    zone_list = sorted(
        activity_df["Zone"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    zone = st.sidebar.multiselect(
        "Zone",
        zone_list,
        key="zone_filter"
    )

    zone_df = activity_df.copy()

    if zone:

        zone_df = zone_df[
            zone_df["Zone"]
            .astype(str)
            .isin(zone)
        ]

    # ==================================
    # BRAND
    # ==================================

    brand_list = sorted(
        zone_df["Brand"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    brand = st.sidebar.multiselect(
        "Brand",
        brand_list,
        key="brand_filter"
    )

    brand_df = zone_df.copy()

    if brand:

        brand_df = brand_df[
            brand_df["Brand"]
            .astype(str)
            .isin(brand)
        ]

    # ==================================
    # LOCATION
    # ==================================

    if "Location" in brand_df.columns:

        location_list = sorted(
            brand_df["Location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        location = st.sidebar.multiselect(
            "Location",
            location_list,
            key="location_filter"
        )

    else:

        location = []

    return {
        "reporting_type": reporting_type,
        "year": year,
        "quarter": quarter,
        "month": month,
        "vertical": vertical,
        "activity_type": activity_type,
        "zone": zone,
        "brand": brand,
        "location": location
    }



# ==================================
# APPLY FILTERS
# ==================================

def apply_common_filters(df, filters):

    filtered_df = df.copy()

    if filters["year"]:

        filtered_df = filtered_df[
            filtered_df["Year"]
            .astype(str)
            .isin(filters["year"])
        ]

    if filters["month"]:

        filtered_df = filtered_df[
            filtered_df["Month"]
            .astype(str)
            .isin(filters["month"])
        ]

    if (
        "Vertical" in filtered_df.columns
        and filters["vertical"]
    ):

        filtered_df = filtered_df[
            filtered_df["Vertical"]
            .astype(str)
            .isin(filters["vertical"])
        ]

    if (
        "Activity Type" in filtered_df.columns
        and filters["activity_type"]
    ):

        filtered_df = filtered_df[
            filtered_df["Activity Type"]
            .astype(str)
            .isin(filters["activity_type"])
        ]

    if filters["zone"]:

        filtered_df = filtered_df[
            filtered_df["Zone"]
            .astype(str)
            .isin(filters["zone"])
        ]

    if filters["brand"]:

        filtered_df = filtered_df[
            filtered_df["Brand"]
            .astype(str)
            .isin(filters["brand"])
        ]

    if (
        "Location" in filtered_df.columns
        and filters["location"]
    ):

        filtered_df = filtered_df[
            filtered_df["Location"]
            .astype(str)
            .isin(filters["location"])
        ]

    return filtered_df
