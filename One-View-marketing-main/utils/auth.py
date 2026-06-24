import streamlit as st
from utils.gsheet import load_users


def login():
    """
    Render the login form and authenticate against the USERS sheet.
    Returns True if the current session is already logged in.

    NOTE: Passwords are compared as plain text because that is how
    they are stored in the USERS sheet today. This is a known
    security gap, not something this refactor silently changes -
    see the "Security" section of the project README for the
    recommended fix (hash passwords, e.g. with bcrypt, before
    storing/comparing them).
    """

    if st.session_state.get("logged_in", False):
        return True

    # ==================================
    # CENTERED LOGIN FORM
    # ==================================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email = st.text_input(
            "📧 User ID",
            key="login_email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Sign In",
            use_container_width=True,
            key="login_btn"
        ):

            users = load_users()

            user = users[
                (users["User_ID"] == email)
                &
                (users["Password"] == password)
            ]

            if len(user) > 0:

                user = user.iloc[0]

                st.session_state.logged_in = True
                st.session_state.user_id = user["User_ID"]
                st.session_state.name = user["Name"]
                st.session_state.role = user["Role"]
                st.session_state.zone_access = str(user["Zone"])
                st.session_state.brand_access = str(user["Brand"])

                st.rerun()

            else:

                st.error("❌ Invalid User ID or Password")

    return False
