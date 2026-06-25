import streamlit as st


# ==========================================
# DISPLAY UNIT
# ==========================================
def get_display_unit():
    """
    Returns the selected display unit from session state.
    Default = Lakhs
    """
    return st.session_state.get("value_scale", "Lakhs")


# ==========================================
# SCALE FACTOR
# ==========================================
def get_scale_factor():

    scale = get_display_unit()

    factors = {
        "Numbers": 1,
        "Thousands": 1_000,
        "Lakhs": 1_00_000,
        "Crores": 1_00_00_000
    }

    suffix = {
        "Numbers": "",
        "Thousands": "K",
        "Lakhs": "L",
        "Crores": "Cr"
    }

    return (
        factors[scale],
        suffix[scale]
    )


# ==========================================
# FORMAT VALUE
# ==========================================
def format_value(value):

    if value is None:
        return "-"

    factor, suffix = get_scale_factor()

    scaled = float(value) / factor

    if suffix == "":
        return f"₹ {scaled:,.0f}"

    return f"₹ {scaled:,.2f} {suffix}"


# ==========================================
# SCALE VALUE
# ==========================================
def scale_value(value):

    factor, _ = get_scale_factor()

    return value / factor


# ==========================================
# SCALE DATAFRAME
# ==========================================
def scale_dataframe(df, columns):

    factor, _ = get_scale_factor()

    df = df.copy()

    for col in columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna(0)
                .astype(float)
                / factor
            )

    return df


# ==========================================
# FORMAT PERCENT
# ==========================================
def format_percent(value):
    return f"{value:.1f}%"


# ==========================================
# CURRENT UNIT
# ==========================================
def current_unit():

    _, suffix = get_scale_factor()

    if suffix == "":
        return "₹"

    return f"₹ ({suffix})"
