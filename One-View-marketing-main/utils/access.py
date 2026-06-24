import streamlit as st


def apply_role_access(df):

    role = st.session_state.get(
        "role",
        ""
    )

    zone_access = str(
        st.session_state.get(
            "zone_access",
            "All"
        )
    )

    brand_access = str(
        st.session_state.get(
            "brand_access",
            "All"
        )
    )

    # ==================================
    # FULL ACCESS ROLES
    # ==================================

    if role in [
        "Director",
        "President",
        "Senior General Manager",
        "Admin"
    ]:
        return df

    # ==================================
    # ZONE FILTER
    # ==================================

    if (
        "Zone" in df.columns
        and zone_access.upper() != "ALL"
    ):

        allowed_zones = [
            z.strip().upper()
            for z in zone_access.split(",")
        ]

        df = df[
            df["Zone"]
            .astype(str)
            .str.strip()
            .str.upper()
            .isin(allowed_zones)
        ]

    # ==================================
    # BRAND FILTER
    # ==================================

    if (
        "Brand" in df.columns
        and brand_access.upper() != "ALL"
    ):

        allowed_brands = [
            b.strip().upper()
            for b in brand_access.split(",")
        ]

        df = df[
            df["Brand"]
            .astype(str)
            .str.strip()
            .str.upper()
            .isin(allowed_brands)
        ]

    return df
