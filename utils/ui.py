import streamlit as st
from utils.formatters import format_value


# ==========================================
# GLOBAL CSS
# ==========================================
def inject_css():

    st.markdown("""
    <style>

    /* ==================================
       HIDE STREAMLIT DEFAULT NAVIGATION
       ================================== */

    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] ul {
        display: none !important;
    }

    nav[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ==================================
       REDUCE TOP PADDING
       ================================== */

    .block-container {
        padding-top: 1rem;
    }

    /* ==================================
       KPI CARDS
       ================================== */

    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e6e6e6;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
    }

    /* ==================================
       SIDEBAR
       ================================== */

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e6e6e6;
    }

    /* ==================================
       REMOVE EXTRA SPACING
       ================================== */

    div[data-testid="stSidebarNav"] + div {
        margin-top: 0px !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE HEADER
# ==========================================
def page_header(title, subtitle=""):

    st.markdown(
        f"""
        <h1 style="margin-bottom:0">
            {title}
        </h1>

        <p style="color:gray;font-size:16px;">
            {subtitle}
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()


# ==========================================
# SECTION HEADER
# ==========================================
def section_header(title):

    st.markdown(f"### {title}")


# ==========================================
# KPI CARD
# ==========================================
def metric_card(
    title,
    value,
    delta=None,
    is_percent=False
):

    if is_percent:

        display_value = (
            f"{value:.1f}%"
            if value is not None
            else "-"
        )

    else:

        display_value = format_value(value)

    st.metric(
        label=title,
        value=display_value,
        delta=delta
    )


# ==========================================
# INFO MESSAGE
# ==========================================
def info_card(message):

    st.info(message)


# ==========================================
# SUCCESS MESSAGE
# ==========================================
def success_card(message):

    st.success(message)


# ==========================================
# WARNING MESSAGE
# ==========================================
def warning_card(message):

    st.warning(message)


# ==========================================
# ERROR MESSAGE
# ==========================================
def error_card(message):

    st.error(message)


# ==========================================
# EMPTY STATE
# ==========================================
def empty_state(message="No Data Available"):

    st.info(message)


# ==========================================
# PAGE DIVIDER
# ==========================================
def page_divider():

    st.divider()
