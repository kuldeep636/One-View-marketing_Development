import pandas as pd
from datetime import datetime

# ==========================================
# REQUIRED COLUMNS
# ==========================================
REQUIRED_COLUMNS = [
    "Vertical", "Location", "Activity Type", "Activity Sub Type",
    "Activity Description", "Activity Start date", "Activity End date", "Investment"
]

VALID_VERTICALS = ["Sales", "After Sales"]
VALID_ACTIVITY_TYPES = ["ATL", "BTL", "DIGITAL", "FLEXY"]

# ==========================================
# MAPPINGS
# ==========================================
VERTICAL_MAPPING = {
    "sales": "Sales",
    "after sales": "After Sales"
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def normalize_text(value):
    return " ".join(str(value).strip().split())


def initialize_validation():
    validation_errors = []
    invalid_row_numbers = set()
    return validation_errors, invalid_row_numbers


def add_error(validation_errors, invalid_row_numbers, row_no, message):
    validation_errors.append(f"Row {row_no}: {message}")
    invalid_row_numbers.add(row_no)


# ==========================================
# VALIDATION FUNCTIONS
# ==========================================
def validate_required_columns(df, validation_errors, invalid_row_numbers):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        validation_errors.append(
            "Missing Required Columns : " + ", ".join(missing_columns)
        )
        return False
    return True


def validate_blank_values(df, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        for col in REQUIRED_COLUMNS:
            value = row[col]
            if pd.isna(value) or str(value).strip() == "":
                add_error(
                    validation_errors,
                    invalid_row_numbers,
                    row_no,
                    f"{col} cannot be blank"
                )


def validate_vertical(df, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        vertical = normalize_text(row["Vertical"])
        key = vertical.lower()
        if key in VERTICAL_MAPPING:
            df.at[idx, "Vertical"] = VERTICAL_MAPPING[key]
        else:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"Invalid Vertical '{vertical}'"
            )


def validate_activity_type(df, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        activity = str(row["Activity Type"]).strip().upper()
        if activity not in VALID_ACTIVITY_TYPES:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"Invalid Activity Type '{activity}'"
            )


def validate_activity_subtype(df, activity_subtypes, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        activity = str(row["Activity Type"]).strip().upper()
        subtype = str(row["Activity Sub Type"]).strip()

        if activity == "FLEXY":
            if subtype == "":
                add_error(
                    validation_errors,
                    invalid_row_numbers,
                    row_no,
                    "Activity Sub Type cannot be blank"
                )
            continue

        valid_subtypes = activity_subtypes.get(activity, [])
        if subtype not in valid_subtypes:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"'{subtype}' is not a valid Sub Type for {activity}"
            )


def validate_investment(df, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        value = row["Investment"]
        try:
            value = float(value)
        except:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Investment must be numeric"
            )
            continue
        if value < 0:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Investment cannot be negative"
            )


def validate_dates(df, selected_month, selected_year, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        try:
            start_date = pd.to_datetime(row["Activity Start date"], errors="raise")
        except:
            add_error(validation_errors, invalid_row_numbers, row_no, "Invalid Activity Start date")
            continue

        try:
            end_date = pd.to_datetime(row["Activity End date"], errors="raise")
        except:
            add_error(validation_errors, invalid_row_numbers, row_no, "Invalid Activity End date")
            continue

        if start_date.strftime("%b") != selected_month:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"Activity Start date must belong to {selected_month}"
            )
        if start_date.year != int(selected_year):
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"Activity Start date must belong to {selected_year}"
            )

        if end_date < start_date:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Activity End date cannot be before Activity Start date"
            )


def validate_upload(df_upload, selected_month, selected_year, activity_subtypes):
    validation_errors, invalid_row_numbers = initialize_validation()

    columns_ok = validate_required_columns(df_upload, validation_errors, invalid_row_numbers)
    if not columns_ok:
        return validation_errors, invalid_row_numbers

    validate_blank_values(df_upload, validation_errors, invalid_row_numbers)
    validate_vertical(df_upload, validation_errors, invalid_row_numbers)
    validate_activity_type(df_upload, validation_errors, invalid_row_numbers)
    validate_activity_subtype(df_upload, activity_subtypes, validation_errors, invalid_row_numbers)
    validate_investment(df_upload, validation_errors, invalid_row_numbers)
    validate_dates(df_upload, selected_month, selected_year, validation_errors, invalid_row_numbers)

    validation_errors = list(dict.fromkeys(validation_errors))
    invalid_row_numbers = sorted(list(invalid_row_numbers))
    return validation_errors, invalid_row_numbers


# ==========================================
# EXPENSE VALIDATION
# ==========================================

EXPENSE_REQUIRED_COLUMNS = [
    "Location",
    "Vertical",
    "Activity type",
    "Vendor",
    "Bifurcation",
    "Description of Work",
    "State",
    "City",
    "Activity Start date",
    "Activity End date",
    "AMT(W/o GST)",
    "GST%",
    "GST Amt",
    "Total Amt",
    "OEM Support (W/o GST)",
    "Support Remarks"
]


# ==========================================
# REQUIRED COLUMNS
# ==========================================

def validate_expense_required_columns(df):

    missing_columns = [
        col
        for col in EXPENSE_REQUIRED_COLUMNS
        if col not in df.columns
    ]

    extra_columns = [
        col
        for col in df.columns
        if col not in EXPENSE_REQUIRED_COLUMNS
    ]

    return missing_columns, extra_columns


# ==========================================
# BLANK VALUES
# ==========================================

def validate_expense_blank_values(
    df,
    validation_errors,
    invalid_row_numbers
):

    for idx, row in df.iterrows():

        row_no = idx + 2

        for col in EXPENSE_REQUIRED_COLUMNS:

            value = row[col]

            if pd.isna(value) or str(value).strip() == "":

                add_error(
                    validation_errors,
                    invalid_row_numbers,
                    row_no,
                    f"{col} cannot be blank"
                )


# ==========================================
# GST VALIDATION
# ==========================================

def validate_gst(
    df,
    validation_errors,
    invalid_row_numbers
):

    for idx, row in df.iterrows():

        row_no = idx + 2

        try:

            amount = float(row["AMT(W/o GST)"])
            gst_percent = float(row["GST%"])
            gst = float(row["GST Amt"])

        except:

            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Invalid GST values"
            )

            continue

        expected_gst = round(
            amount * gst_percent / 100,
            2
        )

        if round(gst, 2) != expected_gst:

            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"GST Amt should be {expected_gst}"
            )


# ==========================================
# TOTAL AMOUNT VALIDATION
# ==========================================

def validate_total_amount(
    df,
    validation_errors,
    invalid_row_numbers
):

    for idx, row in df.iterrows():

        row_no = idx + 2

        try:

            amount = float(row["AMT(W/o GST)"])
            gst = float(row["GST Amt"])
            total = float(row["Total Amt"])

        except:

            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Invalid Total Amount"
            )

            continue

        expected_total = round(
            amount + gst,
            2
        )

        if round(total, 2) != expected_total:

            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"Total Amt should be {expected_total}"
            )


# ==========================================
# MASTER VALIDATION
# ==========================================

def validate_expense_upload(df_upload):

    validation_errors, invalid_row_numbers = initialize_validation()

    # --------------------------
    # Required Columns
    # --------------------------

    missing_columns, extra_columns = (
        validate_expense_required_columns(df_upload)
    )

    if missing_columns:

        validation_errors.append(
            "Missing Required Columns : "
            + ", ".join(missing_columns)
        )

        return (
            validation_errors,
            invalid_row_numbers,
            extra_columns
        )

    # --------------------------
    # Blank Values
    # --------------------------

    validate_expense_blank_values(
        df_upload,
        validation_errors,
        invalid_row_numbers
    )

    # --------------------------
    # GST Validation
    # --------------------------

    validate_gst(
        df_upload,
        validation_errors,
        invalid_row_numbers
    )

    # --------------------------
    # Total Amount Validation
    # --------------------------

    validate_total_amount(
        df_upload,
        validation_errors,
        invalid_row_numbers
    )

    # --------------------------
    # Remove Duplicate Errors
    # --------------------------

    validation_errors = list(
        dict.fromkeys(validation_errors)
    )

    invalid_row_numbers = sorted(
        list(invalid_row_numbers)
    )

    return (
        validation_errors,
        invalid_row_numbers,
        extra_columns
    )
