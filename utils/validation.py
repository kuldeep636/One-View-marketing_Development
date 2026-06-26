def validate_activity_subtype(
    df,
    activity_subtypes,
    validation_errors,
    invalid_row_numbers
):
    for idx, row in df.iterrows():
        row_no = idx + 2
        activity = str(
            row["Activity Type"]
        ).strip().upper()
        subtype = str(
            row["Activity Sub Type"]
        ).strip()

        # ==========================================
        # FLEXY
        # Allow any non-blank subtype
        # ==========================================
        if activity == "FLEXY":
            if subtype == "":
                add_error(
                    validation_errors,
                    invalid_row_numbers,
                    row_no,
                    "Activity Sub Type cannot be blank"
                )
            continue

        # ==========================================
        # ATL / BTL / DIGITAL
        # Validate against predefined list
        # ==========================================
        valid_subtypes = activity_subtypes.get(
            activity,
            []
        )
        if subtype not in valid_subtypes:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"'{subtype}' is not a valid Sub Type for {activity}"
            )
