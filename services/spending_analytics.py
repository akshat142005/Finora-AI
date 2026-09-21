import pandas as pd


def calculate_summary(df):

    total_income = df.loc[
        df["type"] == "Income",
        "amount"
    ].sum()

    total_expense = df.loc[
        df["type"] == "Expense",
        "amount"
    ].sum()

    net_savings = total_income - total_expense

    if total_income > 0:
        savings_rate = (
            net_savings / total_income
        ) * 100
    else:
        savings_rate = 0

    transaction_count = len(df)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "transaction_count": transaction_count
    }


def category_spending(df):

    expenses = df[
        df["type"] == "Expense"
    ]

    result = (
        expenses
        .groupby("category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return result


def monthly_spending(df):

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    expenses = df[
        df["type"] == "Expense"
    ].copy()

    expenses["month"] = (
        expenses["date"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        expenses
        .groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    return result


def top_spending_category(df):

    category_data = category_spending(df)

    if category_data.empty:
        return "No Expense Data"

    return category_data.idxmax()