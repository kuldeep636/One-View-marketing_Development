def format_value(value):

    if value >= 10000000:
        return f"₹{value/10000000:.2f} Cr"

    if value >= 100000:
        return f"₹{value/100000:.2f} L"

    return f"₹{value:,.0f}"


def format_percent(value):
    return f"{value:.1f}%"


def scale_value(value):

    if value >= 10000000:
        return value / 10000000

    return value / 100000
