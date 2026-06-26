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

# ==========================================
# VERTICAL VALIDATION
# ==========================================

def validate_vertical(

    df,

    validation_errors,

    invalid_row_numbers

):

    for idx, row in df.iterrows():

        row_no = idx + 2

        vertical = str(
            row["Vertical"]
        ).strip()

        if vertical not in VALID_VERTICALS:

            add_error(

                validation_errors,

                invalid_row_numbers,

                row_no,

                f"Invalid Vertical '{vertical}'"

            )


# ==========================================
# ACTIVITY TYPE VALIDATION
# ==========================================

def validate_activity_type(

    df,

    validation_errors,

    invalid_row_numbers

):

    for idx, row in df.iterrows():

        row_no = idx + 2

        activity = str(
            row["Activity Type"]
        ).strip().upper()

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

        if activity == "FLEXY":

            continue

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


# ==========================================
# INVESTMENT VALIDATION
# ==========================================

def validate_investment(

    df,

    validation_errors,

    invalid_row_numbers

):

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

        for col in [

            "Activity Start date",

            "Activity End date"

        ]:

            value = row[col]

            try:

                if isinstance(

                    value,

                    datetime

                ):

                    dt = value

                else:

                    dt = datetime.strptime(

                        str(value),

                        DATE_FORMAT

                    )

            except:

                add_error(

                    validation_errors,

                    invalid_row_numbers,

                    row_no,

                    f"{col} has invalid format"

                )

                continue

            if dt.strftime("%b") != selected_month:

                add_error(

                    validation_errors,

                    invalid_row_numbers,

                    row_no,

                    f"{col} must belong to {selected_month}"

                )

            if dt.year != int(selected_year):

                add_error(

                    validation_errors,

                    invalid_row_numbers,

                    row_no,

                    f"{col} must belong to {selected_year}"

                )
