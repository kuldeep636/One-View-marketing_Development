# ==========================================
# MONTHS
# ==========================================

MONTH_ORDER_CALENDAR = [
    "Jan", "Feb", "Mar",
    "Apr", "May", "Jun",
    "Jul", "Aug", "Sep",
    "Oct", "Nov", "Dec"
]

MONTH_ORDER_FINANCIAL = [
    "Apr", "May", "Jun",
    "Jul", "Aug", "Sep",
    "Oct", "Nov", "Dec",
    "Jan", "Feb", "Mar"
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


# ==========================================
# STANDARDIZE MONTH
# ==========================================

def standardize_month(month):

    if month is None:
        return None

    month = str(month).strip()[:3].upper()

    return MONTH_MAP.get(month, month.title())


# ==========================================
# FINANCIAL YEAR
# ==========================================

def get_financial_year(year, month):

    month = standardize_month(month)

    year = int(year)

    if month in [
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
    ]:
        return f"{year}-{str(year+1)[-2:]}"

    return f"{year-1}-{str(year)[-2:]}"


# ==========================================
# QUARTER
# ==========================================

def get_quarter(month, reporting_type):

    month = standardize_month(month)

    if reporting_type == "Financial Year":

        mapping = {
            "Apr":"Q1","May":"Q1","Jun":"Q1",
            "Jul":"Q2","Aug":"Q2","Sep":"Q2",
            "Oct":"Q3","Nov":"Q3","Dec":"Q3",
            "Jan":"Q4","Feb":"Q4","Mar":"Q4"
        }

    else:

        mapping = {
            "Jan":"Q1","Feb":"Q1","Mar":"Q1",
            "Apr":"Q2","May":"Q2","Jun":"Q2",
            "Jul":"Q3","Aug":"Q3","Sep":"Q3",
            "Oct":"Q4","Nov":"Q4","Dec":"Q4"
        }

    return mapping.get(month)


# ==========================================
# ADD REPORTING COLUMNS
# ==========================================

def prepare_reporting(df):

    df = df.copy()

    df["Month"] = (
        df["Month"]
        .apply(standardize_month)
    )

    df["Financial Year"] = df.apply(
        lambda x: get_financial_year(
            x["Year"],
            x["Month"]
        ),
        axis=1
    )

    df["Calendar Quarter"] = df["Month"].apply(
        lambda x: get_quarter(
            x,
            "Calendar Year"
        )
    )

    df["Financial Quarter"] = df["Month"].apply(
        lambda x: get_quarter(
            x,
            "Financial Year"
        )
    )

    return df


# ==========================================
# MONTH ORDER
# ==========================================

def get_month_order(reporting_type):

    if reporting_type == "Financial Year":
        return MONTH_ORDER_FINANCIAL

    return MONTH_ORDER_CALENDAR


# ==========================================
# QUARTERS
# ==========================================

def get_quarters():

    return [
        "Q1",
        "Q2",
        "Q3",
        "Q4"
    ]
