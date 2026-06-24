import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

allowed_roles = [
    "President",
    "Admin",
    "Senior General Manager"
]

if st.session_state.get("role") not in allowed_roles:

    st.error(
        "⛔ You are not authorized to access this page."
    )

    st.stop()

from utils.sidebar import render_navigation
from utils.gsheet import (
    add_user,
    load_users
)
from utils.gsheet import load_activity_data

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Add User",
    page_icon="👤",
    layout="wide"
)

# ==================================
# SIDEBAR
# ==================================

render_navigation()

# ==================================
# PAGE HEADER
# ==================================

st.title("👤 Add User")


# ==================================
# ACCESS MAPPING STORAGE
# ==================================

if "access_mapping_list" not in st.session_state:
    st.session_state.access_mapping_list = []

access_mapping = ";".join(
    st.session_state.access_mapping_list
)
# ==================================
# ADD USER
# ==================================

st.subheader("➕ Add User")

user_id = st.text_input(
    "User ID (Email)"
)

password = st.text_input(
    "Password",
    type="password"
)

name = st.text_input(
    "Employee Name"
)

role = st.selectbox(
    "Role",
    [
        "Director",
        "President",
        "Senior General Manager",
        "Zonal Head",
        "Brand Manager",
        "Admin"
    ]
)

activity_df = load_activity_data()

# ==================================
# ROLE ACCESS
# ==================================

zone = "All"
brand = "All"

zone_options = [
    "West",
    "MP&Rajasthan",
    "North",
    "Gujarat",
    "South",
    "East"
]

# ==================================
# ZONAL HEAD
# ==================================

if role == "Zonal Head":

    zone = st.selectbox(
        "Zone Access",
        zone_options
    )

    brand = "All"

    st.text_input(
        "Brand Access",
        value="All",
        disabled=True
    )

# ==================================
# BRAND MANAGER
# ==================================

elif role == "Brand Manager":

    brand_options = sorted(
        activity_df["Brand"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_zone = st.selectbox(
        "Zone",
        zone_options,
        key="selected_zone"
    )

    selected_brand = st.selectbox(
        "Brand",
        brand_options,
        key="selected_brand"
    )

    if st.button("➕ Add Access"):

        access_pair = (
            f"{selected_zone}|{selected_brand}"
        )

        if access_pair not in st.session_state.access_mapping_list:

            st.session_state.access_mapping_list.append(
                access_pair
            )

            st.rerun()

    st.markdown("### Current Access")

    for idx, access in enumerate(
        st.session_state.access_mapping_list
    ):

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(
                access.replace("|", " | ")
            )

        with col2:

            if st.button(
                "🗑",
                key=f"remove_{idx}"
            ):

                st.session_state.access_mapping_list.pop(
                    idx
                )

                st.rerun()

    zone = "Custom"
    brand = "Custom"

# ==================================
# FULL ACCESS ROLES
# ==================================

else:

    st.info(
        "This role will have access to All Zones and All Brands."

        
# ==================================
# ADD USER BUTTON
# ==================================

access_mapping = ";".join(
    st.session_state.access_mapping_list
)

if st.button(
    "➕ Add User",
    use_container_width=False
):

    if not user_id or not password or not name:

        st.error(
            "Please fill all required fields."
        )

    elif (
        role == "Brand Manager"
        and len(st.session_state.access_mapping_list) == 0
    ):

        st.error(
            "Please add at least one Zone-Brand Access."
        )

    else:

        success = add_user(
            user_id,
            password,
            name,
            role,
            zone,
            brand,
            access_mapping
        )

        if success:

            st.session_state.access_mapping_list = []

            st.success(
                "✅ User Added Successfully!"
            )

            st.cache_data.clear()

            st.rerun()
# ==================================
# USERS LIST
# ==================================

st.divider()

st.subheader("👥 Existing Users")

try:

    users_df = load_users()

    st.dataframe(
        users_df,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.error(
        f"Unable to load users: {e}"
    )

# ==================================
# FOOTER
# ==================================

st.divider()

st.caption(
    "Made By Kuldeep Pal"
)
