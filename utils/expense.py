import pandas as pd
from datetime import datetime

from utils.reporting import prepare_reporting


# ==========================================
# PREPARE EXPENSE DATA
# ==========================================

def prepare_expense_data(
    df,
    zone,
    brand,
    year,
    month,
    uploaded_by
):

    df = df.copy()

    # -------------------------
    # Selected Filters
    # -------------------------

    df["Zone"] = zone
    df["Brand"] = brand
    df["Year"] = year
    df["Month"] = month

    # -------------------------
    # Net Expense
    # -------------------------

    df["Net Expenses"] = (
        df["Total Amt"]
        -
        df["OEM Support (W/o GST)"]
    )

    # -------------------------
    # Reporting Columns
    # -------------------------

    df = prepare_reporting(df)

    # -------------------------
    # Uploaded By
    # -------------------------

    df["Uploaded By"] = uploaded_by

    # -------------------------
    # Upload Timestamp
    # -------------------------

    df["Upload Timestamp"] = datetime.now()

    return df
