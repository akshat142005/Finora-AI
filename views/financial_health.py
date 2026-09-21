import streamlit as st
import pandas as pd


def show_financial_health():

    # =========================================================
    # PAGE TITLE
    # =========================================================

    st.title("❤️ Financial Health")

    st.write(
        "Finora AI evaluates your recorded financial patterns "
        "using savings, expenses and transaction activity."
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
            "📄 Upload a bank statement first to calculate "
            "your financial health."
        )

        return

    # =========================================================
    # CHECK REQUIRED COLUMNS
    # =========================================================

    required_columns = [
        "type",
        "amount"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in transactions.columns
    ]

    if missing_columns:

        st.error(
            "❌ Required transaction columns are missing."
        )

        st.write(
            "Missing:",
            missing_columns
        )

        return

    # =========================================================
    # PREPARE DATA
    # =========================================================

    df = transactions.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["amount"]
    )

    if df.empty:

        st.warning(
            "⚠️ No valid transaction amounts are available."
        )

        return

    # =========================================================
    # CALCULATE FINANCIAL METRICS
    # =========================================================

    income = df.loc[
        df["type"] == "Income",
        "amount"
    ].sum()

    expenses = df.loc[
        df["type"] == "Expense",
        "amount"
    ].sum()

    savings = income - expenses

    if income > 0:

        savings_rate = (
            savings / income
        ) * 100

        expense_ratio = (
            expenses / income
        ) * 100

    else:

        savings_rate = 0
        expense_ratio = 0

    transaction_count = len(df)

    # =========================================================
    # FINANCIAL HEALTH SCORE
    # =========================================================

    score = 0

    # Savings rate component

    if savings_rate >= 40:

        score += 50

    elif savings_rate >= 30:

        score += 45

    elif savings_rate >= 20:

        score += 35

    elif savings_rate >= 10:

        score += 25

    elif savings_rate > 0:

        score += 15

    # Expense ratio component

    if expense_ratio <= 50:

        score += 30

    elif expense_ratio <= 60:

        score += 25

    elif expense_ratio <= 70:

        score += 15

    elif expense_ratio <= 80:

        score += 10

    # Transaction activity component

    if transaction_count >= 5:

        score += 20

    elif transaction_count >= 3:

        score += 15

    elif transaction_count >= 1:

        score += 10

    # Keep score between 0 and 100

    score = min(
        max(score, 0),
        100
    )

    # =========================================================
    # HEALTH STATUS
    # =========================================================

    if score >= 80:

        status = "Excellent"
        status_icon = "🟢"

    elif score >= 65:

        status = "Good"
        status_icon = "🟢"

    elif score >= 50:

        status = "Fair"
        status_icon = "🟡"

    elif score >= 35:

        status = "Needs Attention"
        status_icon = "🟠"

    else:

        status = "At Risk"
        status_icon = "🔴"

    # =========================================================
    # FINANCIAL HEALTH SCORE
    # =========================================================

    st.header(
        "💯 Financial Health Score"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Health Score",
            f"{score}/100"
        )

    with col2:

        st.metric(
            "Status",
            f"{status_icon} {status}"
        )

    st.progress(
        score / 100
    )

    # =========================================================
    # FINANCIAL OVERVIEW
    # =========================================================

    st.header(
        "📊 Financial Overview"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Income",
            f"₹{income:,.0f}"
        )

    with col2:

        st.metric(
            "Expenses",
            f"₹{expenses:,.0f}"
        )

    with col3:

        st.metric(
            "Savings",
            f"₹{savings:,.0f}"
        )

    # =========================================================
    # KEY INDICATORS
    # =========================================================

    st.header(
        "📈 Key Indicators"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Savings Rate",
            f"{savings_rate:.1f}%"
        )

    with col2:

        st.metric(
            "Expense Ratio",
            f"{expense_ratio:.1f}%"
        )

    with col3:

        st.metric(
            "Transactions",
            transaction_count
        )

    # =========================================================
    # SCORE BREAKDOWN
    # =========================================================

    st.header(
        "🧮 Score Breakdown"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            f"💰 Savings Component\n\n"
            f"Savings rate: **{savings_rate:.1f}%**"
        )

    with col2:

        st.info(
            f"💳 Expense Component\n\n"
            f"Expense ratio: **{expense_ratio:.1f}%**"
        )

    with col3:

        st.info(
            f"📊 Activity Component\n\n"
            f"Transactions analyzed: **{transaction_count}**"
        )

    # =========================================================
    # AI ASSESSMENT
    # =========================================================

    st.header(
        "🤖 AI Assessment"
    )

    # ---------------------------------------------------------
    # SAVINGS ANALYSIS
    # ---------------------------------------------------------

    with st.container(border=True):

        st.subheader(
            "💰 Savings Analysis"
        )

        if savings_rate >= 40:

            st.write(
                f"Your recorded savings rate is "
                f"**{savings_rate:.1f}%**, which indicates "
                "a strong savings pattern."
            )

        elif savings_rate >= 20:

            st.write(
                f"Your recorded savings rate is "
                f"**{savings_rate:.1f}%**. "
                "You are maintaining a positive savings pattern."
            )

        elif savings_rate > 0:

            st.write(
                f"Your recorded savings rate is "
                f"**{savings_rate:.1f}%**. "
                "There may be room to increase savings."
            )

        else:

            st.write(
                "Your recorded expenses are equal to or "
                "greater than your recorded income."
            )

    # ---------------------------------------------------------
    # EXPENSE ANALYSIS
    # ---------------------------------------------------------

    with st.container(border=True):

        st.subheader(
            "💳 Expense Analysis"
        )

        if expense_ratio < 50:

            st.write(
                f"Your expense ratio is **{expense_ratio:.1f}%** "
                "of recorded income."
            )

        elif expense_ratio <= 60:

            st.write(
                f"Your expense ratio is **{expense_ratio:.1f}%**. "
                "Expenses are within the range used by this indicator."
            )

        else:

            st.write(
                f"Your expense ratio is **{expense_ratio:.1f}%**. "
                "A relatively high portion of recorded income "
                "is being used for expenses."
            )

    # ---------------------------------------------------------
    # OVERALL ASSESSMENT
    # ---------------------------------------------------------

    with st.container(border=True):

        st.subheader(
            "🧠 Overall Indicator"
        )

        st.write(
            f"Your Finora AI financial health indicator is "
            f"**{score}/100 ({status})**."
        )

        st.write(
            "This score is calculated only from the transaction "
            "data available in the uploaded statement."
        )

    # =========================================================
    # IMPORTANT NOTE
    # =========================================================

    st.divider()

    st.caption(
        "ℹ️ Financial Health is an analytical indicator, "
        "not financial advice. Results depend on the "
        "transactions available in the uploaded statement."
    )