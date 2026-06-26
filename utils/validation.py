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

VALID_VERTICALS = [

    "Sales",
    "After Sales"

]

VALID_ACTIVITY_TYPES = [

    "ATL",
    "BTL",
    "DIGITAL",
    "FLEXY"

]

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

    return (
        validation_errors,
        invalid_row_numbers
    )


# ==========================================
# ADD ERROR
# ==========================================

def add_error(

    validation_errors,
    invalid_row_numbers,

    row_no,

    message

):

    validation_errors.append(

        f"Row {row_no}: {message}"

    )

    invalid_row_numbers.add(

        row_no

    )


# ==========================================
# REQUIRED COLUMNS
# ==========================================

def validate_required_columns(

    df,

    validation_errors,

    invalid_row_numbers

):

    missing_columns = [

        col

        for col in REQUIRED_COLUMNS

        if col not in df.columns

    ]

    if missing_columns:

        validation_errors.append(

            "Missing Required Columns : "

            + ", ".join(missing_columns)

        )

        return False

    return True


# ==========================================
# BLANK VALUES
# ==========================================

def validate_blank_values(

    df,

    validation_errors,

    invalid_row_numbers

):

    for idx, row in df.iterrows():

        row_no = idx + 2

        for col in REQUIRED_COLUMNS:

            value = row[col]

            if pd.isna(value):

                add_error(

                    validation_errors,

                    invalid_row_numbers,

                    row_no,

                    f"{col} cannot be blank"

                )

                continue

            if str(value).strip() == "":

                add_error(

                    validation_errors,

                    invalid_row_numbers,

                    row_no,

                    f"{col} cannot be blank"

                )
