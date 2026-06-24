import streamlit as st
import pandas as pd


def apply_role_access(df):

    role = st.session_state.get(
        "role",
        ""
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
    # ZONAL HEAD (OLD LOGIC)
    # ==================================

    if role == "Zonal Head":

        zone_access = str(
            st.session_state.get(
                "zone_access",
                "All"
            )
        )

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

        return df

    # ==================================
    # BRAND MANAGER (NEW LOGIC)
    # ==================================

    access_mapping = str(
        st.session_state.get(
            "access_mapping",
            ""
        )
    )

    if access_mapping.strip() == "":
        return df.iloc[0:0]

    allowed_pairs = []

    for pair in access_mapping.split(";"):

        pair = pair.strip()

        if "|" in pair:

            zone, brand = pair.split("|", 1)

            allowed_pairs.append(
                (
                    zone.strip().upper(),
                    brand.strip().upper()
                )
            )

    if len(allowed_pairs) == 0:
        return df.iloc[0:0]

    df_temp = df.copy()

    df_temp["Zone_Key"] = (
        df_temp["Zone"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df_temp["Brand_Key"] = (
        df_temp["Brand"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    mask = df_temp.apply(
        lambda row:
        (
            row["Zone_Key"],
            row["Brand_Key"]
        )
        in allowed_pairs,
        axis=1
    )

    return df_temp[mask].drop(
        columns=[
            "Zone_Key",
            "Brand_Key"
        ],
        errors="ignore"
    )
