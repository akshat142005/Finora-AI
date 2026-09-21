import streamlit as st
import pandas as pd

from database.transactions import get_user_transactions


# =========================================================
# ASK FINORA AI
# =========================================================

def show_finance_query():

    st.title("💬 Ask Finora AI")

    st.write(
        "Ask questions about your income, expenses, "
        "savings and transactions."
    )

    # =====================================================
    # USER
    # =====================================================

    user = st.session_state.get("user")

    if not isinstance(user, dict):
        st.error("❌ User session not found.")
        return

    user_id = user.get("id")

    if not user_id:
        st.error("❌ User ID not found.")
        return

    # =====================================================
    # SELECTED ACCOUNT
    # =====================================================

    selected_account_id = (
        st.session_state.get("selected_account_id")
    )

    # =====================================================
    # LOAD TRANSACTIONS
    # =====================================================

    try:

        if selected_account_id is None:

            saved_transactions = get_user_transactions(
                user_id
            )

        else:

            saved_transactions = get_user_transactions(
                user_id,
                selected_account_id
            )

    except Exception as e:

        st.error(
            "❌ Unable to load transactions."
        )

        st.exception(e)

        return

    # =====================================================
    # NO TRANSACTIONS
    # =====================================================

    if not saved_transactions:

        st.info(
            "📄 No transaction data available "
            "for the selected bank account."
        )

        return

    df = pd.DataFrame(
        saved_transactions
    )

    if df.empty:

        st.info(
            "📄 No transaction data available."
        )

        return

    # =====================================================
    # CLEAN DATA
    # =====================================================

    if "amount" in df.columns:

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).fillna(0)

    if "type" in df.columns:

        df["type"] = (
            df["type"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    if "category" in df.columns:

        df["category"] = (
            df["category"]
            .fillna("Other")
            .astype(str)
            .str.strip()
        )

    if "merchant" in df.columns:

        df["merchant"] = (
            df["merchant"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    # =====================================================
    # ACCOUNT INFORMATION
    # =====================================================

    if selected_account_id is None:

        st.info(
            "ℹ️ Finora AI is analyzing transactions "
            "from all accounts."
        )

    else:

        st.info(
            f"ℹ️ Finora AI is analyzing transactions "
            f"for Account ID: {selected_account_id}."
        )

    # =====================================================
    # CALCULATE FINANCIAL DATA
    # =====================================================

    income_df = df[
        df["type"].str.lower() == "income"
    ]

    expense_df = df[
        df["type"].str.lower() == "expense"
    ]

    total_income = income_df[
        "amount"
    ].sum()

    total_expense = expense_df[
        "amount"
    ].sum()

    net_savings = (
        total_income -
        total_expense
    )

    if total_income > 0:

        savings_rate = (
            net_savings /
            total_income
        ) * 100

    else:

        savings_rate = 0

    # =====================================================
    # QUICK QUESTIONS
    # =====================================================

    st.subheader(
        "💡 Quick Questions"
    )

    col1, col2 = st.columns(2)

    with col1:

        q1 = st.button(
            "💰 What is my total income?",
            use_container_width=True
        )

        q2 = st.button(
            "💸 What is my total expense?",
            use_container_width=True
        )

        q3 = st.button(
            "💵 How much did I save?",
            use_container_width=True
        )

    with col2:

        q4 = st.button(
            "📊 What is my highest spending category?",
            use_container_width=True
        )

        q5 = st.button(
            "💳 What is my biggest transaction?",
            use_container_width=True
        )

        q6 = st.button(
            "🔢 How many transactions do I have?",
            use_container_width=True
        )

    q7 = st.button(
        "📋 Give me a financial summary",
        use_container_width=True
    )

    # =====================================================
    # CUSTOM QUESTION
    # =====================================================

    st.divider()

    st.subheader(
        "🧠 Ask Your Own Question"
    )

    question = st.text_input(
        "Your question",
        placeholder="Example: How much did I spend?"
    )

    ask = st.button(
        "🤖 Ask Finora AI",
        type="primary",
        use_container_width=True
    )

    # =====================================================
    # DETERMINE QUESTION
    # =====================================================

    selected_question = None

    if q1:

        selected_question = "income"

    elif q2:

        selected_question = "expense"

    elif q3:

        selected_question = "savings"

    elif q4:

        selected_question = "category"

    elif q5:

        selected_question = "biggest"

    elif q6:

        selected_question = "count"

    elif q7:

        selected_question = "summary"

    elif ask and question.strip():

        selected_question = (
            question
            .lower()
            .strip()
        )

    # =====================================================
    # NO QUESTION
    # =====================================================

    if selected_question is None:

        st.divider()

        st.subheader(
            "💡 Example Questions"
        )

        st.markdown(
            """
            - How much did I spend?
            - How much did I save?
            - What is my savings rate?
            - What is my highest spending category?
            - What is my biggest transaction?
            - How many transactions do I have?
            - Give me a financial summary.
            """
        )

        return

    # =====================================================
    # TOTAL INCOME
    # =====================================================

    if selected_question == "income" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "total income" in selected_question
            or "my income" in selected_question
            or "income" == selected_question
            or "how much did i earn" in selected_question
            or "how much i earned" in selected_question
        )
    ):

        st.success(
            f"💰 Your recorded total income is "
            f"**₹{total_income:,.0f}**."
        )

    # =====================================================
    # TOTAL EXPENSE
    # =====================================================

    elif selected_question == "expense" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "total expense" in selected_question
            or "total expenses" in selected_question
            or "how much did i spend" in selected_question
            or "how much i spent" in selected_question
            or "my expenses" in selected_question
            or "expense" == selected_question
        )
    ):

        st.success(
            f"💳 Your recorded total expenses are "
            f"**₹{total_expense:,.0f}**."
        )

    # =====================================================
    # SAVINGS
    # =====================================================

    elif selected_question == "savings" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "how much did i save" in selected_question
            or "how much i saved" in selected_question
            or "my savings" in selected_question
            or "total savings" in selected_question
            or "savings" == selected_question
        )
    ):

        st.success(
            f"💰 Your recorded net savings are "
            f"**₹{net_savings:,.0f}**."
        )

    # =====================================================
    # SAVINGS RATE
    # =====================================================

    elif (
        isinstance(
            selected_question,
            str
        )
        and (
            "saving rate" in selected_question
            or "savings rate" in selected_question
        )
    ):

        st.success(
            f"📈 Your current recorded savings rate is "
            f"**{savings_rate:.1f}%**."
        )

    # =====================================================
    # HIGHEST SPENDING CATEGORY
    # =====================================================

    elif selected_question == "category" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "highest spending category"
            in selected_question
            or "highest spending"
            in selected_question
            or "top spending category"
            in selected_question
            or "spending category"
            in selected_question
        )
    ):

        if expense_df.empty:

            st.info(
                "No expense transactions available."
            )

        else:

            category_totals = (
                expense_df
                .groupby("category")["amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            top_category = (
                category_totals.index[0]
            )

            top_amount = (
                category_totals.iloc[0]
            )

            st.success(
                f"🔝 Your highest spending category is "
                f"**{top_category}** with "
                f"**₹{top_amount:,.0f}**."
            )

    # =====================================================
    # BIGGEST TRANSACTION
    # =====================================================

    elif selected_question == "biggest" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "biggest transaction"
            in selected_question
            or "biggest expense"
            in selected_question
            or "largest transaction"
            in selected_question
            or "largest expense"
            in selected_question
        )
    ):

        if expense_df.empty:

            st.info(
                "No expense transactions available."
            )

        else:

            biggest_index = (
                expense_df["amount"]
                .idxmax()
            )

            biggest = (
                expense_df.loc[
                    biggest_index
                ]
            )

            merchant = biggest.get(
                "merchant",
                "Unknown"
            )

            amount = biggest.get(
                "amount",
                0
            )

            st.success(
                f"💳 Your biggest recorded expense is "
                f"**₹{amount:,.0f}** at "
                f"**{merchant}**."
            )

    # =====================================================
    # TRANSACTION COUNT
    # =====================================================

    elif selected_question == "count" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "how many transactions"
            in selected_question
            or "transaction count"
            in selected_question
            or "number of transactions"
            in selected_question
        )
    ):

        transaction_count = len(df)

        st.success(
            f"🔢 You have "
            f"**{transaction_count} recorded transactions**."
        )

    # =====================================================
    # FINANCIAL SUMMARY
    # =====================================================

    elif selected_question == "summary" or (
        isinstance(
            selected_question,
            str
        )
        and (
            "financial summary"
            in selected_question
            or "give me a summary"
            in selected_question
            or "give me financial summary"
            in selected_question
            or selected_question == "summary"
        )
    ):

        st.subheader(
            "📊 Financial Summary"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Income",
                f"₹{total_income:,.0f}"
            )

        with col2:

            st.metric(
                "Expenses",
                f"₹{total_expense:,.0f}"
            )

        with col3:

            st.metric(
                "Net Savings",
                f"₹{net_savings:,.0f}"
            )

        with col4:

            st.metric(
                "Savings Rate",
                f"{savings_rate:.1f}%"
            )

        st.write(
            f"🧾 Total transactions: **{len(df)}**"
        )

    # =====================================================
    # UNKNOWN QUESTION
    # =====================================================

    else:

        st.warning(
            "🤔 I couldn't understand that question yet."
        )

        st.write(
            "Try asking about your **income, expenses, "
            "savings, spending categories, biggest "
            "transaction, transaction count, or "
            "financial summary**."
        )