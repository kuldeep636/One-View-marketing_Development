import pandas as pd


def preprocess_expense(df):

    numeric_cols = [
        "AMT(W/o GST)",
        "OEM Support",
        "Net Expenses",
        "Actual Investment"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = (
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )
                .fillna(0)
            )

    return df


def preprocess_budget(df):

    numeric_cols = [
        "Retail Target",
        "Lead Target",
        "Budget",
        "Spends"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            df[col] = (
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )
                .fillna(0)
            )

    return df
