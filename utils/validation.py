import pandas as pd
from datetime import datetime



# ==========================================
# REQUIRED COLUMNS
# ==========================================
REQUIRED_COLUMNS = [
    "Vertical",
    "Location",
    "Activity Type",
    "Activity Sub Type",
    "Activity Description",
    "Activity Start date",
    "Activity End date",
    "Investment"
]

VALID_VERTICALS = ["Sales", "After Sales"]

VALID_ACTIVITY_TYPES = ["ATL", "BTL", "DIGITAL", "FLEXY"]

# ==========================================
# NEW MAPPINGS (as requested)
# ==========================================
VERTICAL_MAPPING = {
    "sales": "Sales",
    "after sales": "After Sales"
}




# ==========================================
# HELPER FUNCTION (as requested)
# ==========================================
def normalize_text(value):
    return " ".join(str(value).strip().split())


# ==========================================
# DATE FORMAT
# ==========================================
DATE_FORMAT = "%d-%b-%Y"


# ==========================================
# INITIALIZE
# ==========================================
def initialize_validation():
    validation_errors = []
    invalid_row_numbers = set()
    return validation_errors, invalid_row_numbers


# ==========================================
# ADD ERROR
# ==========================================
def add_error(validation_errors, invalid_row_numbers, row_no, message):
    validation_errors.append(f"Row {row_no}: {message}")
    invalid_row_numbers.add(row_no)


# ==========================================
# REQUIRED COLUMNS
# ==========================================
def validate_required_columns(df, validation_errors, invalid_row_numbers):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        validation_errors.append(
            "Missing Required Columns : " + ", ".join(missing_columns)
        )
        return False
    return True


# ==========================================
# BLANK VALUES
# ==========================================
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


# ==========================================
# UPDATED VERTICAL VALIDATION (as requested)
# ==========================================
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


# ==========================================
# ACTIVITY TYPE VALIDATION
# ==========================================
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


# ==========================================
# ACTIVITY SUB TYPE VALIDATION
# ==========================================
def validate_activity_subtype(df, activity_subtypes, validation_errors, invalid_row_numbers):
    for idx, row in df.iterrows():
        row_no = idx + 2
        activity = str(row["Activity Type"]).strip().upper()
        subtype = str(row["Activity Sub Type"]).strip()

        # FLEXY - Allow any non-blank subtype
        if activity == "FLEXY":
            if subtype == "":
                add_error(
                    validation_errors,
                    invalid_row_numbers,
                    row_no,
                    "Activity Sub Type cannot be blank"
                )
            continue

        # ATL / BTL / DIGITAL
        valid_subtypes = activity_subtypes.get(activity, [])
        if subtype not in valid_subtypes:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                f"'{subtype}' is not a valid Sub Type for {activity}"
            )


# ==========================================
# INVESTMENT VALIDATION
# ==========================================
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


# ==========================================
# DATE VALIDATION
# ==========================================
def validate_dates(
    df,
    selected_month,
    selected_year,
    validation_errors,
    invalid_row_numbers
):
    for idx, row in df.iterrows():

        row_no = idx + 2

        # -------------------------
        # Read Start Date
        # -------------------------
        try:
            start_date = pd.to_datetime(
                row["Activity Start date"],
                errors="raise"
            )
        except:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Invalid Activity Start date"
            )
            continue

        # -------------------------
        # Read End Date
        # -------------------------
        try:
            end_date = pd.to_datetime(
                row["Activity End date"],
                errors="raise"
            )
        except:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Invalid Activity End date"
            )
            continue

        # -------------------------
        # Start Date must belong to
        # selected upload month/year
        # -------------------------
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

        # -------------------------
        # End Date cannot be before
        # Start Date
        # -------------------------
        if end_date < start_date:
            add_error(
                validation_errors,
                invalid_row_numbers,
                row_no,
                "Activity End date cannot be before Activity Start date"
            )

# ==========================================
# MASTER VALIDATION
# ==========================================
def validate_upload(df_upload, selected_month, selected_year, activity_subtypes):
    validation_errors, invalid_row_numbers = initialize_validation()

    # Required Columns
    columns_ok = validate_required_columns(
        df_upload, validation_errors, invalid_row_numbers
    )
    if not columns_ok:
        return validation_errors, invalid_row_numbers

    # Blank Values
    validate_blank_values(df_upload, validation_errors, invalid_row_numbers)

    # Vertical
    validate_vertical(df_upload, validation_errors, invalid_row_numbers)

    # Activity Type
    validate_activity_type(df_upload, validation_errors, invalid_row_numbers)

    # Activity Sub Type
    validate_activity_subtype(
        df_upload, activity_subtypes, validation_errors, invalid_row_numbers
    )

    # Investment
    validate_investment(df_upload, validation_errors, invalid_row_numbers)

    # Dates
    validate_dates(
        df_upload, selected_month, selected_year, validation_errors, invalid_row_numbers
    )

    # Remove duplicate errors
    validation_errors = list(dict.fromkeys(validation_errors))
    invalid_row_numbers = sorted(list(invalid_row_numbers))

    return validation_errors, invalid_row_numbers


# ==========================================
# EXPENSE UPLOAD VALIDATION
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
    "OEM Support (W/o GST)",
    "Support Remarks"
]


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
# EXPENSE CALCULATION VALIDATION
# ==========================================

def validate_expense_calculations(df):

    validation_errors = []

    for idx, row in df.iterrows():

        row_no = idx + 2

        try:

            amount = float(row["AMT(W/o GST)"])
            gst_percent = float(row["GST%"])
            gst = float(row["GST"])
            total = float(row["Total AMT"])
            support = float(row.get("OEM Support (W/o GST)", 0) or 0)

        except Exception:
            validation_errors.append(
                f"Row {row_no}: Invalid numeric values."
            )
            continue

        expected_gst = round(amount * gst_percent / 100, 2)
        expected_total = round(amount + expected_gst, 2)
        expected_net = round(expected_total - support, 2)

        # GST Validation
        if round(gst, 2) != expected_gst:

            validation_errors.append(
                f"Row {row_no}: GST mismatch "
                f"(Expected {expected_gst}, Uploaded {gst})"
            )

        # Total Validation
        if round(total, 2) != expected_total:

            validation_errors.append(
                f"Row {row_no}: Total Amount mismatch "
                f"(Expected {expected_total}, Uploaded {total})"
            )

        # Net Expense
        row["Calculated Net Expense"] = expected_net

    return validation_errors
