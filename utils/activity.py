import streamlit as st
import pandas as pd


def render_activity_breakdown(filtered_df):

    st.subheader("📊 Activity Breakdown")

    # ==================================
    # SESSION STATES
    # ==================================

    if "selected_activity" not in st.session_state:
        st.session_state.selected_activity = None

    if "selected_subtype" not in st.session_state:
        st.session_state.selected_subtype = None

    # ==================================
    # COUNTS
    # ==================================

    atl_count = len(
        filtered_df[
            filtered_df["Activity Type"].str.upper() == "ATL"
        ]
    )

    btl_count = len(
        filtered_df[
            filtered_df["Activity Type"].str.upper() == "BTL"
        ]
    )

    digital_count = len(
        filtered_df[
            filtered_df["Activity Type"].str.upper() == "DIGITAL"
        ]
    )

    flexy_count = len(
        filtered_df[
            filtered_df["Activity Type"].str.upper() == "FLEXY"
        ]
    )

    # ==================================
    # TOP ACTIVITY BUTTONS
    # ==================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            f"📺 ATL\n\n{atl_count}",
            use_container_width=True
        ):

            if st.session_state.selected_activity == "ATL":
                st.session_state.selected_activity = None
                st.session_state.selected_subtype = None
            else:
                st.session_state.selected_activity = "ATL"
                st.session_state.selected_subtype = None

            st.rerun()

    with c2:

        if st.button(
            f"🎯 BTL\n\n{btl_count}",
            use_container_width=True
        ):

            if st.session_state.selected_activity == "BTL":
                st.session_state.selected_activity = None
                st.session_state.selected_subtype = None
            else:
                st.session_state.selected_activity = "BTL"
                st.session_state.selected_subtype = None

            st.rerun()

    with c3:

        if st.button(
            f"💻 Digital\n\n{digital_count}",
            use_container_width=True
        ):

            if st.session_state.selected_activity == "DIGITAL":
                st.session_state.selected_activity = None
                st.session_state.selected_subtype = None
            else:
                st.session_state.selected_activity = "DIGITAL"
                st.session_state.selected_subtype = None

            st.rerun()

    with c4:

        if st.button(
            f"📦 Flexy\n\n{flexy_count}",
            use_container_width=True
        ):

            if st.session_state.selected_activity == "FLEXY":
                st.session_state.selected_activity = None
                st.session_state.selected_subtype = None
            else:
                st.session_state.selected_activity = "FLEXY"
                st.session_state.selected_subtype = None

            st.rerun()

    # ==================================
    # BREAKDOWN
    # ==================================

    selected = st.session_state.selected_activity

    if selected:

        st.markdown("---")

        st.subheader(
            f"{selected} Breakdown"
        )

        # Selected Sub Type Info

        if st.session_state.selected_subtype:

            col1, col2 = st.columns([4, 1])

            with col1:

                st.info(
                    f"Selected Sub Type : "
                    f"{st.session_state.selected_subtype}"
                )

            with col2:

                if st.button(
                    "❌ Clear",
                    use_container_width=True
                ):

                    st.session_state.selected_subtype = None
                    st.rerun()

        # Breakdown Data

        breakdown_df = (
            filtered_df[
                filtered_df["Activity Type"]
                .str.upper() == selected
            ]
            .groupby("Activity Sub Type")
            .size()
            .reset_index(name="Count")
            .sort_values(
                "Count",
                ascending=False
            )
        )

        cols = st.columns(4)

        for idx, row in breakdown_df.iterrows():

            with cols[idx % 4]:

                subtype = row[
                    "Activity Sub Type"
                ]

                count = row["Count"]

                if st.button(
                    f"{subtype}\n\n{count}",
                    key=f"subtype_{subtype}",
                    use_container_width=True
                ):

                    if (
                        st.session_state.selected_subtype
                        == subtype
                    ):

                        st.session_state.selected_subtype = None

                    else:

                        st.session_state.selected_subtype = subtype

                    st.rerun()
