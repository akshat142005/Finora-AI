import pandas as pd


def calculate_financial_health(df):

    if df is None or df.empty:
        return None

    data = df.copy()

    # Income
    income = data.loc[
        data["type"] == "Income",
        "amount"
    ].sum()

    # Expense
    expense = data.loc[
        data["type"] == "Expense",
        "amount"
    ].sum()

    # Savings
    savings = income - expense

    # Savings rate
    if income > 0:
        savings_rate = (
            savings / income
        ) * 100
    else:
        savings_rate = 0

    # -------------------------------------------------
    # SAVINGS SCORE
    # -------------------------------------------------

    if savings_rate >= 40:
        savings_score = 40
    elif savings_rate >= 30:
        savings_score = 35
    elif savings_rate >= 20:
        savings_score = 30
    elif savings_rate >= 10:
        savings_score = 20
    elif savings_rate > 0:
        savings_score = 10
    else:
        savings_score = 0

    # -------------------------------------------------
    # EXPENSE SCORE
    # -------------------------------------------------

    if income > 0:

        expense_ratio = (
            expense / income
        ) * 100

    else:

        expense_ratio = 100

    if expense_ratio <= 50:
        expense_score = 30
    elif expense_ratio <= 60:
        expense_score = 25
    elif expense_ratio <= 70:
        expense_score = 20
    elif expense_ratio <= 80:
        expense_score = 10
    else:
        expense_score = 0

    # -------------------------------------------------
    # TRANSACTION PATTERN SCORE
    # -------------------------------------------------

    transaction_count = len(data)

    if transaction_count >= 20:
        pattern_score = 20
    elif transaction_count >= 10:
        pattern_score = 15
    elif transaction_count >= 5:
        pattern_score = 10
    else:
        pattern_score = 5

    # -------------------------------------------------
    # FINAL SCORE
    # -------------------------------------------------

    score = (
        savings_score
        + expense_score
        + pattern_score
    )

    # Keep score between 0 and 100
    score = min(
        100,
        max(0, score)
    )

    # -------------------------------------------------
    # HEALTH LABEL
    # -------------------------------------------------

    if score >= 80:
        label = "Excellent"

    elif score >= 65:
        label = "Good"

    elif score >= 50:
        label = "Moderate"

    else:
        label = "Needs Attention"

    return {
        "score": score,
        "label": label,
        "income": income,
        "expense": expense,
        "savings": savings,
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "transaction_count": transaction_count
    }