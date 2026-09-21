import pandas as pd
import numpy as np


def forecast_expense(df):

    if df is None or df.empty:
        return None

    data = df.copy()

    # Convert date
    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    # Only expenses
    expenses = data[
        data["type"] == "Expense"
    ].copy()

    if expenses.empty:
        return None

    # Remove invalid dates
    expenses = expenses.dropna(
        subset=["date"]
    )

    if expenses.empty:
        return None

    # Create monthly expense
    expenses["month"] = (
        expenses["date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        expenses
        .groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    monthly["amount"] = pd.to_numeric(
        monthly["amount"],
        errors="coerce"
    )

    monthly = monthly.dropna(
        subset=["amount"]
    )

    if monthly.empty:
        return None

    # Not enough historical data
    if len(monthly) == 1:

        prediction = monthly["amount"].iloc[0]

    else:

        # Simple linear trend model
        x = np.arange(
            len(monthly)
        )

        y = monthly["amount"].values

        slope, intercept = np.polyfit(
            x,
            y,
            1
        )

        next_x = len(monthly)

        prediction = (
            slope * next_x
            + intercept
        )

        # Prevent negative prediction
        prediction = max(
            0,
            prediction
        )

    return {
        "monthly_data": monthly,
        "predicted_expense": round(
            prediction,
            2
        )
    }