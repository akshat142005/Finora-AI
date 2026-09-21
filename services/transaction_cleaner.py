import pandas as pd

from services.category_model import predict_category
from services.merchant_normalizer import normalize_merchant


# =========================================================
# CLEAN TRANSACTION DATA
# =========================================================

def clean_transactions(df):

    # -----------------------------------------------------
    # 1. Check input
    # -----------------------------------------------------

    if df is None or df.empty:
        return pd.DataFrame(
            columns=[
                "date",
                "merchant",
                "description",
                "type",
                "amount",
                "category",
                "balance"
            ]
        )

    # Make a copy so original dataframe is not modified
    df = df.copy()

    # -----------------------------------------------------
    # 2. Clean column names
    # -----------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # -----------------------------------------------------
    # 3. Make sure required columns exist
    # -----------------------------------------------------

    required_columns = [
        "date",
        "description",
        "debit",
        "credit",
        "balance"
    ]

    for column in required_columns:

        if column not in df.columns:

            if column == "description":
                df[column] = ""

            else:
                df[column] = 0

    # -----------------------------------------------------
    # 4. Remove completely empty rows
    # -----------------------------------------------------

    df = df.dropna(how="all")

    # -----------------------------------------------------
    # 5. Clean description
    # -----------------------------------------------------

    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # 6. Clean dates
    # -----------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    # -----------------------------------------------------
    # 7. Clean monetary columns
    # -----------------------------------------------------

    def clean_amount(value):

        if pd.isna(value):
            return 0.0

        value = str(value).strip()

        if value == "":
            return 0.0

        # Remove currency symbols and commas
        value = (
            value
            .replace("₹", "")
            .replace("Rs.", "")
            .replace("Rs", "")
            .replace(",", "")
            .strip()
        )

        # Handle brackets
        # Example: (500) -> -500
        if value.startswith("(") and value.endswith(")"):

            value = "-" + value[1:-1]

        # Convert to number
        try:
            return float(value)

        except Exception:
            return 0.0

    df["debit"] = df["debit"].apply(clean_amount)
    df["credit"] = df["credit"].apply(clean_amount)
    df["balance"] = df["balance"].apply(clean_amount)

    # -----------------------------------------------------
    # 8. Remove rows with no useful transaction data
    # -----------------------------------------------------

    df = df[
        (df["description"].str.len() > 0)
        |
        (df["debit"] != 0)
        |
        (df["credit"] != 0)
    ]

    # -----------------------------------------------------
    # 9. Determine transaction type
    # -----------------------------------------------------

    def get_transaction_type(row):

        credit = row["credit"]
        debit = row["debit"]

        if credit > 0:
            return "Income"

        elif debit > 0:
            return "Expense"

        else:
            return "Other"

    df["type"] = df.apply(
        get_transaction_type,
        axis=1
    )

    # -----------------------------------------------------
    # 10. Determine transaction amount
    # -----------------------------------------------------

    def get_amount(row):

        credit = row["credit"]
        debit = row["debit"]

        if credit > 0:
            return abs(credit)

        elif debit > 0:
            return abs(debit)

        return 0.0

    df["amount"] = df.apply(
        get_amount,
        axis=1
    )

    # -----------------------------------------------------
    # 11. Merchant
    # -----------------------------------------------------

    df["merchant"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )
    df["merchant"]=df["merchant"].apply(
        normalize_merchant
    )

    # -----------------------------------------------------
    # 12. Category
    # -----------------------------------------------------

    def get_category(row):

        description = str(
            row["description"]
        ).upper()

        transaction_type = row["type"]

        # ---------------------------------------------
        # Income categories
        # ---------------------------------------------

        if transaction_type == "Income":

            if "SALARY" in description:
                return "Salary"

            elif "PAYROLL" in description:
                return "Salary"

            elif "REFUND" in description:
                return "Refund"

            elif "CASHBACK" in description:
                return "Refund"

            elif "REVERSAL" in description:
                return "Refund"

            else:
                return "Other Income"

        # ---------------------------------------------
        # Expense categories
        # ---------------------------------------------

        elif transaction_type == "Expense":

            return predict_category(
                description
            )

        # ---------------------------------------------
        # Other
        # ---------------------------------------------

        return "Other"

    df["category"] = df.apply(
        get_category,
        axis=1
    )

    # -----------------------------------------------------
    # 13. Select final columns
    # -----------------------------------------------------

    final_columns = [
        "date",
        "merchant",
        "description",
        "type",
        "amount",
        "category",
        "balance"
    ]

    df = df[final_columns]

    # -----------------------------------------------------
    # 14. Clean final values
    # -----------------------------------------------------

    df["merchant"] = (
        df["merchant"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["type"] = (
        df["type"]
        .fillna("Other")
        .astype(str)
        .str.strip()
    )

    df["category"] = (
        df["category"]
        .fillna("Other")
        .astype(str)
        .str.strip()
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0.0)

    df["balance"] = pd.to_numeric(
        df["balance"],
        errors="coerce"
    ).fillna(0.0)

    # -----------------------------------------------------
    # 15. Remove invalid zero-value transactions
    # -----------------------------------------------------

    df = df[
        df["amount"] > 0
    ]

    # -----------------------------------------------------
    # 16. Sort by date
    # -----------------------------------------------------

    df = df.sort_values(
        by="date",
        ascending=True,
        na_position="last"
    )

    # -----------------------------------------------------
    # 17. Reset index
    # -----------------------------------------------------

    df = df.reset_index(
        drop=True
    )

    return df