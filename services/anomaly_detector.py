import pandas as pd
import numpy as np


def detect_anomalies(df):

    if df is None or df.empty:
        return pd.DataFrame()

    data = df.copy()

    # Only expense transactions
    expenses = data[
        data["type"] == "Expense"
    ].copy()

    if expenses.empty:
        return pd.DataFrame()

    # Convert amount to numeric
    expenses["amount"] = pd.to_numeric(
        expenses["amount"],
        errors="coerce"
    )

    expenses = expenses.dropna(
        subset=["amount"]
    )

    if len(expenses) < 3:
        return pd.DataFrame()

    # Calculate statistical threshold
    mean_amount = expenses["amount"].mean()
    std_amount = expenses["amount"].std()

    if std_amount == 0 or pd.isna(std_amount):
        return pd.DataFrame()

    threshold = mean_amount + (2 * std_amount)

    # Detect unusually high transactions
    anomalies = expenses[
        expenses["amount"] > threshold
    ].copy()

    if anomalies.empty:
        return pd.DataFrame()

    # Anomaly score
    anomalies["Anomaly Score"] = (
        (anomalies["amount"] - mean_amount)
        / std_amount
    ).round(2)

    # Reason
    anomalies["Reason"] = (
        "Transaction amount is significantly "
        "higher than the normal spending level."
    )

    # Select useful columns
    columns = [
        "date",
        "merchant",
        "description",
        "amount",
        "category",
        "Anomaly Score",
        "Reason"
    ]

    available_columns = [
        col
        for col in columns
        if col in anomalies.columns
    ]

    return anomalies[
        available_columns
    ].sort_values(
        "amount",
        ascending=False
    )