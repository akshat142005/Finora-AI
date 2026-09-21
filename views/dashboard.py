import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database.transactions import get_user_transactions


def show_dashboard():

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

    user_name = user.get("name", "User")

    # =====================================================
    # SELECTED BANK ACCOUNT
    # =====================================================

    selected_account_id = st.session_state.get(
        "selected_account_id"
    )

    # =====================================================
    # LOAD TRANSACTIONS
    # =====================================================

    try:

        if selected_account_id is None:

            # All accounts
            saved_transactions = get_user_transactions(
                user_id
            )

        else:

            # Selected account only
            saved_transactions = get_user_transactions(
                user_id,
                selected_account_id
            )

    except Exception as e:

        st.error("❌ Unable to load transactions.")
        st.exception(e)
        return

    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    if not saved_transactions:

        st.title("💰 Finora AI")
        st.caption("Personal Finance Intelligence")

        st.info(
            "No transaction data available for the selected "
            "bank account."
        )

        return

    df = pd.DataFrame(saved_transactions)

    if df.empty:

        st.title("💰 Finora AI")
        st.caption("Personal Finance Intelligence")

        st.info(
            "No transaction data available."
        )

        return

    # =====================================================
    # CLEAN DATA
    # =====================================================

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

    if "amount" in df.columns:

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).fillna(0)

    if "type" not in df.columns:
        df["type"] = "Other"

    if "category" not in df.columns:
        df["category"] = "Other"

    if "merchant" not in df.columns:
        df["merchant"] = "Unknown"

    df["type"] = df["type"].fillna("Other")
    df["category"] = df["category"].fillna("Other")
    df["merchant"] = df["merchant"].fillna("Unknown")

    # =====================================================
    # CALCULATIONS
    # =====================================================

    income = df.loc[
        df["type"] == "Income",
        "amount"
    ].sum()

    expenses = df.loc[
        df["type"] == "Expense",
        "amount"
    ].sum()

    savings = income - expenses

    savings_rate = (
        savings / income * 100
        if income > 0
        else 0
    )

    total_transactions = len(df)

    expense_transactions = len(
        df[df["type"] == "Expense"]
    )

    income_transactions = len(
        df[df["type"] == "Income"]
    )

    # =====================================================
    # HEADER
    # =====================================================

    header_left, header_right = st.columns(
        [3.5, 1.2]
    )

    with header_left:

        st.title("💰 Finora AI")

        st.caption(
            "Personal Finance Intelligence"
        )

    with header_right:

        st.write("")

        st.info(
            f"👋 Welcome, **{user_name}**"
        )

    st.divider()

    # =====================================================
    # SELECTED ACCOUNT INFO
    # =====================================================

    if selected_account_id is None:

        st.caption(
            "🌐 Showing data from all bank accounts"
        )

    else:

        st.caption(
            f"🏦 Showing data for selected bank account "
            f"(Account ID: {selected_account_id})"
        )

    # =====================================================
    # MAIN BALANCE CARD
    # =====================================================

    with st.container(border=True):

        balance_left, balance_middle, balance_right = st.columns(
            [2.5, 1.5, 1.5]
        )

        with balance_left:

            st.caption("NET SAVINGS")

            st.header(
                f"₹{savings:,.0f}"
            )

            if savings >= 0:

                st.success(
                    f"↑ {savings_rate:.1f}% of income saved"
                )

            else:

                st.error(
                    "Expenses are higher than income"
                )

        with balance_middle:

            st.metric(
                "Income",
                f"₹{income:,.0f}"
            )

        with balance_right:

            st.metric(
                "Expenses",
                f"₹{expenses:,.0f}"
            )

    # =====================================================
    # KPI ROW
    # =====================================================

    st.write("")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        with st.container(border=True):

            st.metric(
                "💰 Total Income",
                f"₹{income:,.0f}"
            )

            st.caption(
                f"{income_transactions} income transactions"
            )

    with k2:

        with st.container(border=True):

            st.metric(
                "💸 Total Expenses",
                f"₹{expenses:,.0f}"
            )

            st.caption(
                f"{expense_transactions} expense transactions"
            )

    with k3:

        with st.container(border=True):

            st.metric(
                "🏦 Net Savings",
                f"₹{savings:,.0f}"
            )

            st.caption(
                f"{savings_rate:.1f}% savings rate"
            )

    with k4:

        with st.container(border=True):

            st.metric(
                "🧾 Transactions",
                total_transactions
            )

            st.caption(
                "Recorded transactions"
            )

    # =====================================================
    # NAVIGATION TABS
    # =====================================================

    st.write("")

    overview_tab, spending_tab, transactions_tab = st.tabs(
        [
            "📊 Overview",
            "💳 Spending",
            "🧾 Transactions"
        ]
    )

    # =====================================================
    # OVERVIEW TAB
    # =====================================================

    with overview_tab:

        st.write("")

        chart_left, chart_right = st.columns(2)

        # -------------------------------------------------
        # CATEGORY CHART
        # -------------------------------------------------

        with chart_left:

            with st.container(border=True):

                st.subheader(
                    "Spending Breakdown"
                )

                expense_df = df[
                    df["type"] == "Expense"
                ]

                category_df = (
                    expense_df
                    .groupby(
                        "category",
                        as_index=False
                    )["amount"]
                    .sum()
                    .sort_values(
                        "amount",
                        ascending=False
                    )
                )

                if not category_df.empty:

                    fig = px.pie(
                        category_df,
                        names="category",
                        values="amount",
                        hole=0.62
                    )

                    fig.update_layout(
                        height=380,
                        margin=dict(
                            l=10,
                            r=10,
                            t=20,
                            b=10
                        ),
                        showlegend=True
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No expense data available."
                    )

        # -------------------------------------------------
        # CASH FLOW
        # -------------------------------------------------

        with chart_right:

            with st.container(border=True):

                st.subheader(
                    "Cash Flow"
                )

                monthly = df.copy()

                if "date" in monthly.columns:

                    monthly["month"] = (
                        monthly["date"]
                        .dt.to_period("M")
                        .astype(str)
                    )

                else:

                    monthly["month"] = "Unknown"

                monthly_income = (
                    monthly[
                        monthly["type"] == "Income"
                    ]
                    .groupby("month")["amount"]
                    .sum()
                )

                monthly_expense = (
                    monthly[
                        monthly["type"] == "Expense"
                    ]
                    .groupby("month")["amount"]
                    .sum()
                )

                months = sorted(
                    set(monthly_income.index)
                    |
                    set(monthly_expense.index)
                )

                cashflow = pd.DataFrame({
                    "Month": months,
                    "Income": [
                        monthly_income.get(
                            m,
                            0
                        )
                        for m in months
                    ],
                    "Expenses": [
                        monthly_expense.get(
                            m,
                            0
                        )
                        for m in months
                    ]
                })

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=cashflow["Month"],
                        y=cashflow["Income"],
                        name="Income"
                    )
                )

                fig.add_trace(
                    go.Bar(
                        x=cashflow["Month"],
                        y=cashflow["Expenses"],
                        name="Expenses"
                    )
                )

                fig.update_layout(
                    barmode="group",
                    height=380,
                    margin=dict(
                        l=10,
                        r=10,
                        t=20,
                        b=10
                    ),
                    yaxis_title="₹"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # -------------------------------------------------
        # FINORA AI INSIGHTS
        # -------------------------------------------------

        st.write("")

        with st.container(border=True):

            st.subheader(
                "🤖 Finora AI Insights"
            )

            expense_df = df[
                df["type"] == "Expense"
            ]

            if not expense_df.empty:

                category_summary = (
                    expense_df
                    .groupby("category")["amount"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                top_category = (
                    category_summary.index[0]
                )

                top_amount = (
                    category_summary.iloc[0]
                )

                percentage = (
                    top_amount /
                    expenses *
                    100
                    if expenses > 0
                    else 0
                )

                insight1, insight2 = st.columns(2)

                with insight1:

                    st.info(
                        f"🛍️ **Highest spending**\n\n"
                        f"{top_category}: "
                        f"₹{top_amount:,.0f} "
                        f"({percentage:.1f}%)"
                    )

                with insight2:

                    if savings_rate >= 30:

                        st.success(
                            f"🏦 **Savings snapshot**\n\n"
                            f"You saved "
                            f"{savings_rate:.1f}% "
                            f"of recorded income."
                        )

                    elif savings_rate >= 0:

                        st.warning(
                            f"🏦 **Savings snapshot**\n\n"
                            f"Current savings rate: "
                            f"{savings_rate:.1f}%."
                        )

                    else:

                        st.error(
                            "⚠️ Expenses exceed recorded income."
                        )

            else:

                st.info(
                    "No expense data available."
                )

    # =====================================================
    # SPENDING TAB
    # =====================================================

    with spending_tab:

        st.write("")

        expense_df = df[
            df["type"] == "Expense"
        ].copy()

        category_df = (
            expense_df
            .groupby(
                "category",
                as_index=False
            )["amount"]
            .sum()
            .sort_values(
                "amount",
                ascending=False
            )
        )

        st.subheader(
            "💳 Spending Analysis"
        )

        if not category_df.empty:

            for _, row in category_df.head(8).iterrows():

                percentage = (
                    row["amount"]
                    / expenses
                    * 100
                    if expenses > 0
                    else 0
                )

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.write(
                        f"**{row['category']}**"
                    )

                    st.progress(
                        min(
                            percentage / 100,
                            1.0
                        )
                    )

                with col2:

                    st.write(
                        f"₹{row['amount']:,.0f}"
                    )

                    st.caption(
                        f"{percentage:.1f}%"
                    )

        else:

            st.info(
                "No spending data available."
            )

    # =====================================================
    # TRANSACTIONS TAB
    # =====================================================

    with transactions_tab:

        st.write("")

        st.subheader(
            "🧾 Recent Transactions"
        )

        display_df = df.copy()

        if "date" in display_df.columns:

            display_df = display_df.sort_values(
                "date",
                ascending=False
            )

        columns = [
            "date",
            "merchant",
            "amount",
            "type",
            "category"
        ]

        available_columns = [
            col
            for col in columns
            if col in display_df.columns
        ]

        st.dataframe(
            display_df[
                available_columns
            ].head(10),
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # FOOTER
    # =====================================================

    st.write("")

    st.caption(
        "Finora AI • Personal Finance Intelligence"
    )