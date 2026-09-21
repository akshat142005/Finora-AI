import pandas as pd


def answer_finance_query(df, query):

    if df is None or df.empty:
        return "📄 Please upload a bank statement first."

    if not query or not query.strip():
        return "💬 Please enter a financial question."

    query = query.lower().strip()

    # =====================================================
    # BASIC CALCULATIONS
    # =====================================================

    income = df.loc[
        df["type"] == "Income",
        "amount"
    ].sum()

    expense = df.loc[
        df["type"] == "Expense",
        "amount"
    ].sum()

    savings = income - expense

    # =====================================================
    # TOTAL INCOME
    # =====================================================

    if (
        "total income" in query
        or "my income" in query
        or "how much income" in query
    ):

        return (
            f"💰 Your total recorded income is "
            f"₹{income:,.0f}."
        )

    # =====================================================
    # TOTAL EXPENSE
    # =====================================================

    if (
        "total expense" in query
        or "total expenses" in query
        or "how much did i spend" in query
        or "how much have i spent" in query
    ):

        return (
            f"💳 Your total recorded expenses are "
            f"₹{expense:,.0f}."
        )

    # =====================================================
    # SAVINGS
    # =====================================================

    if (
        "how much did i save" in query
        or "my savings" in query
        or "net savings" in query
    ):

        return (
            f"💰 Your recorded net savings are "
            f"₹{savings:,.0f}."
        )

    # =====================================================
    # SAVINGS RATE
    # =====================================================

    if (
        "savings rate" in query
        or "saving percentage" in query
        or "how much percentage" in query
    ):

        if income > 0:

            rate = (
                savings / income
            ) * 100

        else:

            rate = 0

        return (
            f"📊 Your current recorded savings rate is "
            f"{rate:.1f}%."
        )

    # =====================================================
    # HIGHEST SPENDING CATEGORY
    # =====================================================

    if (
        "highest spending" in query
        or "most spending" in query
        or "top spending" in query
        or "biggest expense" in query
    ):

        expenses = df[
            df["type"] == "Expense"
        ]

        if expenses.empty:
            return "📄 No expense data available."

        category_totals = (
            expenses
            .groupby("category")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        category = category_totals.index[0]
        amount = category_totals.iloc[0]

        return (
            f"🔝 Your highest spending category is "
            f"{category}, with spending of "
            f"₹{amount:,.0f}."
        )

    # =====================================================
    # CATEGORY SPENDING
    # =====================================================

    categories = (
        df["category"]
        .dropna()
        .astype(str)
        .unique()
    )

    for category in categories:

        category_lower = category.lower()

        if category_lower in query:

            category_expenses = df[
                (df["type"] == "Expense")
                &
                (
                    df["category"].astype(str).str.lower()
                    == category_lower
                )
            ]

            amount = category_expenses[
                "amount"
            ].sum()

            return (
                f"💳 You spent approximately "
                f"₹{amount:,.0f} on {category}."
            )

    # =====================================================
    # MERCHANT SPENDING
    # =====================================================

    merchants = (
        df["merchant"]
        .dropna()
        .astype(str)
        .unique()
    )

    for merchant in merchants:

        merchant_lower = merchant.lower()

        if merchant_lower in query:

            merchant_expenses = df[
                (df["type"] == "Expense")
                &
                (
                    df["merchant"]
                    .astype(str)
                    .str.lower()
                    == merchant_lower
                )
            ]

            amount = merchant_expenses[
                "amount"
            ].sum()

            return (
                f"💳 You spent approximately "
                f"₹{amount:,.0f} at {merchant}."
            )

    # =====================================================
    # TRANSACTION COUNT
    # =====================================================

    if (
        "how many transactions" in query
        or "transaction count" in query
        or "number of transactions" in query
    ):

        return (
            f"📊 Your statement contains "
            f"{len(df)} transactions."
        )

    # =====================================================
    # FALLBACK
    # =====================================================

    return (
        "🤔 I couldn't understand that question yet. "
        "Try asking about your income, expenses, savings, "
        "categories, merchants, or transactions."
    )