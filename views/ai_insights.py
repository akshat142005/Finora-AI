import streamlit as st

from services.ai_insights import generate_insights


# =========================================================
# PAGE TITLE
# =========================================================

st.title("🤖 AI Financial Insights")

st.write(
    "Finora AI analyzes your transactions and "
    "generates personalized financial insights."
)


# =========================================================
# GET TRANSACTIONS
# =========================================================

transactions = st.session_state.get(
    "transactions",
    None
)


# =========================================================
# NO DATA
# =========================================================

if transactions is None or transactions.empty:

    st.info(
        "📄 Upload a bank statement first to generate "
        "financial insights."
    )

    st.stop()


# =========================================================
# GENERATE INSIGHTS
# =========================================================

with st.spinner(
    "🤖 Finora AI is analyzing your financial patterns..."
):

    try:

        insights = generate_insights(
            transactions
        )

    except Exception as e:

        st.error(
            "❌ Unable to generate financial insights."
        )

        st.error(
            str(e)
        )

        st.stop()


# =========================================================
# INSIGHTS HEADER
# =========================================================

st.header(
    "🧠 Your Financial Insights"
)


st.write(
    f"Finora AI found **{len(insights)}** "
    "important patterns in your statement."
)


# =========================================================
# DISPLAY INSIGHTS
# =========================================================

for insight in insights:

    with st.container(border=True):

        st.write(
            insight
        )


# =========================================================
# QUICK FINANCIAL SUMMARY
# =========================================================

st.divider()

st.header(
    "📊 Quick Summary"
)


income = transactions.loc[
    transactions["type"] == "Income",
    "amount"
].sum()


expense = transactions.loc[
    transactions["type"] == "Expense",
    "amount"
].sum()


savings = income - expense


if income > 0:

    savings_rate = (
        savings / income
    ) * 100

else:

    savings_rate = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Income",
        f"₹{income:,.0f}"
    )


with col2:

    st.metric(
        "Expenses",
        f"₹{expense:,.0f}"
    )


with col3:

    st.metric(
        "Savings",
        f"₹{savings:,.0f}"
    )


with col4:

    st.metric(
        "Savings Rate",
        f"{savings_rate:.1f}%"
    )


# =========================================================
# CATEGORY BREAKDOWN
# =========================================================

st.divider()

st.header(
    "🏷️ Spending Categories"
)


expenses_df = transactions[
    transactions["type"] == "Expense"
]


if not expenses_df.empty:

    category_data = (
        expenses_df
        .groupby("category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    for category, amount in category_data.items():

        percentage = (
            amount / expense * 100
            if expense > 0
            else 0
        )

        col1, col2 = st.columns(
            [3, 1]
        )

        with col1:

            st.write(
                f"**{category}**"
            )

            st.progress(
                min(
                    percentage / 100,
                    1.0
                )
            )

        with col2:

            st.write(
                f"₹{amount:,.0f}"
            )

            st.caption(
                f"{percentage:.1f}%"
            )


else:

    st.info(
        "No expense categories available."
    )


# =========================================================
# TRANSACTION ACTIVITY
# =========================================================

st.divider()

st.header(
    "📈 Transaction Activity"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Transactions Analyzed",
        len(transactions)
    )


with col2:

    st.metric(
        "Expense Transactions",
        len(expenses_df)
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "ℹ️ These insights are generated from the "
    "transaction data available in your uploaded "
    "statement and are intended for informational purposes."
)