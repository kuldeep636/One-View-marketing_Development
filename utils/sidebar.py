import streamlit as st


def render_navigation():

    with st.sidebar:

        # ==================================
        # CUSTOM STYLING
        # ==================================

        st.markdown(
            """
            <style>
            /* Sidebar base */
            section[data-testid="stSidebar"] {
                background-color: #FAFAFA;
            }

            /* User card */
            .nav-user-card {
                padding: 14px 16px;
                background: #FFFFFF;
                border: 1px solid #ECECEC;
                border-radius: 10px;
                margin-bottom: 18px;
            }
            .nav-user-name {
                font-size: 15px;
                font-weight: 600;
                color: #1A1A1A;
                margin-bottom: 2px;
            }
            .nav-user-role {
                font-size: 12.5px;
                color: #8A8A8A;
                letter-spacing: 0.2px;
            }

            /* Section labels above expanders */
            .nav-section-label {
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.6px;
                color: #A3A3A3;
                text-transform: uppercase;
                margin: 18px 0 6px 4px;
            }

            /* Expander styling -> looks like a flat menu group */
            section[data-testid="stSidebar"] .streamlit-expanderHeader,
            section[data-testid="stSidebar"] details summary {
                font-size: 14px;
                font-weight: 500;
                color: #2B2B2B;
                background-color: transparent;
                border-radius: 8px;
                padding: 6px 8px;
            }
            section[data-testid="stSidebar"] details summary:hover {
                background-color: #F0F0F0;
            }
            section[data-testid="stSidebar"] details {
                border: none;
                background: transparent;
            }
            section[data-testid="stSidebar"] [data-testid="stExpander"] {
                border: none;
                box-shadow: none;
                background: transparent;
            }

            /* Page links nested inside expanders */
            section[data-testid="stSidebar"] [data-testid="stExpander"] a {
                font-size: 13.5px !important;
                color: #444 !important;
                padding: 6px 10px !important;
                margin-left: 6px;
                border-radius: 6px;
            }
            section[data-testid="stSidebar"] [data-testid="stExpander"] a:hover {
                background-color: #F3F3F3 !important;
                color: #111 !important;
            }

            /* Divider */
            .nav-divider {
                border: none;
                border-top: 1px solid #E8E8E8;
                margin: 16px 0;
            }

            /* Action buttons */
            .nav-action-row button {
                font-size: 13px !important;
                border-radius: 8px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # ==================================
        # USER INFO
        # ==================================

        st.markdown(
            f"""
            <div class="nav-user-card">
                <div class="nav-user-name">👤 {st.session_state.get('name', '')}</div>
                <div class="nav-user-role">🎯 {st.session_state.get('role', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ==================================
        # GLOBAL SETTINGS
        # ==================================

        if "value_scale" not in st.session_state:
            st.session_state.value_scale = "Lakhs"

        st.selectbox(
            "💰 Display Values In",
            [
                "Numbers",
                "Thousands",
                "Lakhs",
                "Crores",
            ],
            key="value_scale",
        )

        st.markdown("<hr class='nav-divider'>", unsafe_allow_html=True)

        # ==================================
        # MARKETING PLAN MENU
        # ==================================

        st.markdown("<div class='nav-section-label'>Marketing</div>", unsafe_allow_html=True)

        with st.expander("📋 Marketing Plan", expanded=True):

            st.page_link(
                "pages/1_Dashboard.py",
                label="📋 Plan",
            )

            st.page_link(
                "pages/4_Activity_Execution_Update.py",
                label="✅ Activity Execution Update",
            )

            st.page_link(
                "pages/2_Budget_Target_Tracker.py",
                label="🎯 Budget & Target Tracker",
            )

        # ==================================
        # EXPENSE DASHBOARD MENU
        # ==================================

        st.markdown("<div class='nav-section-label'>Finance</div>", unsafe_allow_html=True)

        with st.expander("💰 Expense Dashboard", expanded=False):

            st.page_link(
                "pages/10_Expense_Dashboard.py",
                label="📈 Expense Dashboard",
            )

            st.page_link(
                "pages/11_Zone_Wise_Expenses.py",
                label="📍 Zone Wise Expenses",
            )

            st.page_link(
                "pages/12_Brand_Wise_Expenses.py",
                label="🚗 Brand Wise Expenses",
            )

            st.page_link(
                "pages/16_Bifurcation_Analysis.py",
                label="📑 Bifurcation Analysis",
            )

            st.page_link(
                "pages/13_Brand_Insights.py",
                label="📊 Brand Insights",
            )

            st.page_link(
                "pages/14_Treemap_Analysis.py",
                label="🌳 Treemap Analysis",
            )

        # ==================================
        # DATA MANAGEMENT
        # ==================================

        st.markdown("<div class='nav-section-label'>Data</div>", unsafe_allow_html=True)

        with st.expander("📤 Data Management", expanded=False):

            st.page_link(
                "pages/6_Upload_Wizard.py",
                label="📤 Data Upload Wizard",
            )

        # ==================================
        # ADMINISTRATION
        # ==================================

        if st.session_state.get("role") in [
            "President",
            "Admin",
        ]:

            st.markdown("<div class='nav-section-label'>Admin</div>", unsafe_allow_html=True)

            with st.expander("⚙️ Administration", expanded=False):

                st.page_link(
                    "pages/5_Add_User.py",
                    label="👤 Add User",
                )

        # ==================================
        # ACTION BUTTONS
        # ==================================

        st.markdown("<hr class='nav-divider'>", unsafe_allow_html=True)

        st.markdown("<div class='nav-action-row'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("↻ Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()

        with col2:
            if st.button("⎋ Logout", use_container_width=True):
                st.session_state.clear()
                st.switch_page("app.py")

        st.markdown("</div>", unsafe_allow_html=True)
