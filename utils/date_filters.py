MONTH_ORDER_CALENDAR = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]

MONTH_ORDER_FINANCIAL = [
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar"
]


MONTH_MAP = {
    "JAN": "Jan",
    "FEB": "Feb",
    "MAR": "Mar",
    "APR": "Apr",
    "MAY": "May",
    "JUN": "Jun",
    "JUL": "Jul",
    "AUG": "Aug",
    "SEP": "Sep",
    "OCT": "Oct",
    "NOV": "Nov",
    "DEC": "Dec"
}


def standardize_month(month):
    """
    Converts month names to standard format.
    Example:
    january -> Jan
    JAN -> Jan
    """
    if month is None:
        return None

    month = str(month).strip()[:3].upper()

    return MONTH_MAP.get(month, month.title())


def get_financial_year(year, month):
    """
    Returns Financial Year.

    Example:

    Apr 2025 -> 2025-26

    Jan 2025 -> 2024-25
    """

    month = standardize_month(month)

    year = int(year)

    if month in [
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]:

        return f"{year}-{str(year + 1)[-2:]}"

    return f"{year - 1}-{str(year)[-2:]}"


def add_financial_year(df):
    """
    Adds Financial Year column if missing.
    """

    if "Financial Year" in df.columns:
        return df

    df = df.copy()

    df["Month"] = (
        df["Month"]
        .apply(standardize_month)
    )

    df["Financial Year"] = df.apply(
        lambda row: get_financial_year(
            row["Year"],
            row["Month"]
        ),
        axis=1
    )

    return df


def get_month_order(period_type):
    """
    Returns correct month sequence.
    """

    if period_type == "Financial Year":
        return MONTH_ORDER_FINANCIAL

    return MONTH_ORDER_CALENDAR
