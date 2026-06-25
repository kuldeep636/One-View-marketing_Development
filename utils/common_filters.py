import streamlit as st
import pandas as pd
from utils.reporting import (
    prepare_reporting,
    get_month_order,
    get_quarters
)


# ==================================
# UNIVERSAL FILTERS
# ==================================
def render_common_filters(df):
    # ----------------------------------
    # Prepare Reporting Columns
    # ----------------------------------
    df = prepare_reporting(df)
    st.sidebar.markdown("## 🔍 Filters")

    # ==================================
    # RESET FILTERS
    # ==================================
    if st.sidebar.button("🔄 Reset Filters"):
        filter_keys = [
            "reporting_type",
            "year_filter",
            "quarter_filter",
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
        ["Calendar Year", "Financial Year"],
        key="reporting_type"
    )

    # ==================================
    # YEAR COLUMN
    # ==================================
    if reporting_type == "Financial Year":
        year_column = "Financial Year"
    else:
        year_column = "Year"

    # ==================================
    # YEAR FILTER
    # ==================================
    year_list = sorted(
        df[year_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    year = st.sidebar.multiselect(
        year_column,
        year_list,
        key="year_filter"
    )

    year_df = df.copy()
    if year:
        year_df = year_df[
            year_df[year_column]
            .astype(str)
            .isin(year)
        ]

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

    # ==================================
    # MONTH
    # ==================================
    month_list = (
        quarter_df["Month"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    month_order = get_month_order(reporting_type)

    month_list = sorted(
        month_list,
        key=lambda x: month_order.index(x) if x in month_order else 999
    )

    month = st.sidebar.multiselect(
        "Month",
        month_list,
        key="month_filter"
    )

    month_df = quarter_df.copy()
    if month:
        month_df = month_df[
            month_df["Month"]
            .astype(str)
            .isin(month)
        ]

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
    if "Vertical" in vertical_df.columns and vertical:
        vertical_df = vertical_df[
            vertical_df["Vertical"]
            .astype(str)
            .isin(vertical)
        ]

    # ==================================
    # ACTIVITY TYPE
    # ==================================
    activity_column = None
    if "Activity Type" in vertical_df.columns:
        activity_column = "Activity Type"
    elif "Activity type" in vertical_df.columns:
        activity_column = "Activity type"

    if activity_column:
        activity_type_list = sorted(
            vertical_df[activity_column]
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
    if activity_column and activity_type:
        activity_df = activity_df[
            activity_df[activity_column]
            .astype(str)
            .isin(activity_type)
        ]

    # ==================================
    # ZONE
    # ==================================
    if "Zone" in activity_df.columns:
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
    else:
        zone = []

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
    if "Brand" in zone_df.columns:
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
    else:
        brand = []

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
    filtered_df = prepare_reporting(df)

    # ==================================
    # YEAR
    # ==================================
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

    # ==================================
    # QUARTER
    # ==================================
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
    if filters["month"]:
        filtered_df = filtered_df[
            filtered_df["Month"]
            .astype(str)
            .isin(filters["month"])
        ]

    # ==================================
    # VERTICAL
    # ==================================
    if "Vertical" in filtered_df.columns and filters["vertical"]:
        filtered_df = filtered_df[
            filtered_df["Vertical"]
            .astype(str)
            .isin(filters["vertical"])
        ]

    # ==================================
    # ACTIVITY TYPE
    # ==================================
    activity_column = None
    if "Activity Type" in filtered_df.columns:
        activity_column = "Activity Type"
    elif "Activity type" in filtered_df.columns:
        activity_column = "Activity type"

    if activity_column and filters["activity_type"]:
        filtered_df = filtered_df[
            filtered_df[activity_column]
            .astype(str)
            .isin(filters["activity_type"])
        ]

    # ==================================
    # ZONE
    # ==================================
    if filters["zone"]:
        filtered_df = filtered_df[
            filtered_df["Zone"]
            .astype(str)
            .isin(filters["zone"])
        ]

    # ==================================
    # BRAND
    # ==================================
    if filters["brand"]:
        filtered_df = filtered_df[
            filtered_df["Brand"]
            .astype(str)
            .isin(filters["brand"])
        ]

    # ==================================
    # LOCATION
    # ==================================
    if "Location" in filtered_df.columns and filters["location"]:
        filtered_df = filtered_df[
            filtered_df["Location"]
            .astype(str)
            .isin(filters["location"])
        ]

    return filtered_df
