import pandas as pd


def generate_insights(df):

    insights = []

    if df is None or df.empty:
        return [
            "📄 Upload a bank statement to generate financial insights."
        ]

    # -----------------------------------------
    # Basic calculations
    # -----------------------------------------

    income = df.loc[
        df["type"] == "Income",
        "amount"
    ].sum()

    expense = df.loc[
        df["type"] == "Expense",
        "amount"
    ].sum()

    savings = income - expense

    if income > 0:
        savings_rate = (savings / income) * 100
    else:
        savings_rate = 0

    # -----------------------------------------
    # Savings insight
    # -----------------------------------------

    if savings_rate >= 30:

        insights.append(
            f"💰 Your current savings rate is "
            f"{savings_rate:.1f}%, with net savings of "
            f"₹{savings:,.0f}."
        )

    elif savings_rate >= 10:

        insights.append(
            f"💰 You are currently saving "
            f"{savings_rate:.1f}% of your recorded income."
        )

    else:

        insights.append(
            f"⚠️ Your current savings rate is "
            f"{savings_rate:.1f}%. Your expenses are "
            f"taking up a large portion of your recorded income."
        )

    # -----------------------------------------
    # Category analysis
    # -----------------------------------------

    expenses = df[
        df["type"] == "Expense"
    ]

    if not expenses.empty:

        category_totals = (
            expenses
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        top_category = category_totals.index[0]
        top_amount = category_totals.iloc[0]

        percentage = (
            top_amount / expense * 100
            if expense > 0
            else 0
        )

        insights.append(
            f"🔝 Your highest spending category is "
            f"{top_category}, accounting for "
            f"₹{top_amount:,.0f} "
            f"({percentage:.1f}% of expenses)."
        )

        # -----------------------------------------
        # Food spending
        # -----------------------------------------

        if "Food" in category_totals.index:

            food_amount = category_totals["Food"]

            food_percentage = (
                food_amount / expense * 100
                if expense > 0
                else 0
            )

            if food_percentage >= 20:

                insights.append(
                    f"🍔 Food spending is relatively high at "
                    f"₹{food_amount:,.0f}, representing "
                    f"{food_percentage:.1f}% of expenses."
                )

        # -----------------------------------------
        # Shopping spending
        # -----------------------------------------

        if "Shopping" in category_totals.index:

            shopping_amount = category_totals["Shopping"]

            if expense > 0:

                shopping_percentage = (
                    shopping_amount / expense
                ) * 100

                if shopping_percentage >= 25:

                    insights.append(
                        f"🛍️ Shopping accounts for "
                        f"{shopping_percentage:.1f}% of your "
                        f"recorded expenses."
                    )

    # -----------------------------------------
    # Transaction count
    # -----------------------------------------

    transaction_count = len(df)

    insights.append(
        f"📊 Finora AI analyzed "
        f"{transaction_count} transactions from your statement."
    )

    return insights