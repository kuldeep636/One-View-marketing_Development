import streamlit as st


def render_navigation():

    with st.sidebar:

        # ==================================
        # USER INFO
        # ==================================

        st.markdown(
            f"**👤 {st.session_state.get('name', '')}**"
        )

        st.caption(
            f"🎯 {st.session_state.get('role', '')}"
        )

        # ==================================
        # MARKETING PLAN MENU
        # ==================================

        if "marketing_menu" not in st.session_state:
            st.session_state.marketing_menu = True

        marketing_arrow = (
            "▼"
            if st.session_state.marketing_menu
            else "▶"
        )

        if st.button(
            f"{marketing_arrow} 📋 Marketing Plan",
            use_container_width=True
        ):
            st.session_state.marketing_menu = (
                not st.session_state.marketing_menu
            )
            st.rerun()

        if st.session_state.marketing_menu:

            st.page_link(
                "pages/1_Dashboard.py",
                label="📋 Plan"
            )

            st.page_link(
                "pages/4_Activity_Execution_Update.py",
                label="✅ Activity Execution Update"
            )

            st.page_link(
                "pages/2_Budget_Target_Tracker.py",
                label="🎯 Budget & Target Tracker"
            )

        # ==================================
        # EXPENSE DASHBOARD MENU
        # ==================================

        if "expense_menu" not in st.session_state:
            st.session_state.expense_menu = False

        expense_arrow = (
            "▼"
            if st.session_state.expense_menu
            else "▶"
        )

        if st.button(
            f"{expense_arrow} 💰 Expense Dashboard",
            use_container_width=True
        ):
            st.session_state.expense_menu = (
                not st.session_state.expense_menu
            )
            st.rerun()

        if st.session_state.expense_menu:

            st.page_link(
                "pages/10_Expense_Dashboard.py",
                label="📈 Expense Dashboard"
            )

            st.page_link(
                "pages/11_Zone_Wise_Expenses.py",
                label="📍 Zone Wise Expenses"
            )

            st.page_link(
                "pages/12_Brand_Wise_Expenses.py",
                label="🚗 Brand Wise Expenses"
            )

            st.page_link(
                "pages/16_Bifurcation_Analysis.py",
                label="📑 Bifurcation Analysis"
            )

            st.page_link(
                "pages/13_Brand_Insights.py",
                label="📊 Brand Insights"
            )

            st.page_link(
                "pages/14_Treemap_Analysis.py",
                label="🌳 Treemap Analysis"
            )

        # ==================================
        # DATA MANAGEMENT
        # ==================================

        if "data_menu" not in st.session_state:
            st.session_state.data_menu = False

        data_arrow = (
            "▼"
            if st.session_state.data_menu
            else "▶"
        )

        if st.button(
            f"{data_arrow} 📤 Data Management",
            use_container_width=True
        ):
            st.session_state.data_menu = (
                not st.session_state.data_menu
            )
            st.rerun()

        if st.session_state.data_menu:

            st.page_link(
                "pages/6_Upload_Wizard.py",
                label="📤 Data Upload Wizard"
            )

        # ==================================
        # ADMINISTRATION
        # ==================================

        if st.session_state.get("role") in [
            "President",
            "Admin"
        ]:

            if "admin_menu" not in st.session_state:
                st.session_state.admin_menu = False

            admin_arrow = (
                "▼"
                if st.session_state.admin_menu
                else "▶"
            )

            if st.button(
                f"{admin_arrow} ⚙️ Administration",
                use_container_width=True
            ):
                st.session_state.admin_menu = (
                    not st.session_state.admin_menu
                )
                st.rerun()

            if st.session_state.admin_menu:

                st.page_link(
                    "pages/5_Add_User.py",
                    label="👤 Add User"
                )

        # ==================================
        # ACTION BUTTONS
        # ==================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "↻ Refresh",
                use_container_width=True
            ):
                st.cache_data.clear()
                st.rerun()

        with col2:

            if st.button(
                "⎋ Logout",
                use_container_width=True
            ):
                st.session_state.clear()
                st.switch_page("app.py")
