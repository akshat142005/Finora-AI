import streamlit as st
import pandas as pd
import plotly.express as px


def show_analytics():

    st.title("📊 Advanced Analytics")

    df = st.session_state.get("transactions")

    if df is None or df.empty:
        st.warning(
            "No transaction data available. Please upload a statement first."
        )
        return

    df = df.copy()

    # --------------------------------------------------
    # DATA PREPARATION
    # --------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0)

    df["type"] = (
        df["type"]
        .fillna("Other")
        .astype(str)
    )

    df["category"] = (
        df["category"]
        .fillna("Other")
        .astype(str)
    )

    df["merchant"] = (
        df["merchant"]
        .fillna("Unknown Merchant")
        .astype(str)
    )

    # Remove invalid dates
    df = df[df["date"].notna()].copy()

    if df.empty:
        st.warning("No valid transaction dates found.")
        return

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    st.subheader("🔎 Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        transaction_types = [
            "All",
            "Income",
            "Expense"
        ]

        selected_type = st.selectbox(
            "Transaction Type",
            transaction_types
        )

    with col2:

        categories = sorted(
            df["category"].unique().tolist()
        )

        selected_category = st.selectbox(
            "Category",
            ["All"] + categories
        )

    with col3:

        merchants = sorted(
            df["merchant"].unique().tolist()
        )

        selected_merchant = st.selectbox(
            "Merchant",
            ["All"] + merchants
        )

    # Apply filters

    filtered_df = df.copy()

    if selected_type != "All":

        filtered_df = filtered_df[
            filtered_df["type"].str.lower()
            == selected_type.lower()
        ]

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["category"]
            == selected_category
        ]

    if selected_merchant != "All":

        filtered_df = filtered_df[
            filtered_df["merchant"]
            == selected_merchant
        ]

    if filtered_df.empty:

        st.warning(
            "No transactions match the selected filters."
        )
        return

    st.divider()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    income = filtered_df.loc[
        filtered_df["type"].str.lower() == "income",
        "amount"
    ].sum()

    expenses = filtered_df.loc[
        filtered_df["type"].str.lower() == "expense",
        "amount"
    ].sum()

    savings = income - expenses

    if income > 0:
        savings_rate = (
            savings / income
        ) * 100
    else:
        savings_rate = 0

    transaction_count = len(filtered_df)

    st.subheader("💰 Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

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

    with col4:
        st.metric(
            "Savings Rate",
            f"{savings_rate:.1f}%"
        )

    st.divider()

    # --------------------------------------------------
    # MONTHLY INCOME VS EXPENSE
    # --------------------------------------------------

    st.subheader("📈 Monthly Income vs Expenses")

    monthly_df = filtered_df.copy()

    monthly_df["month"] = (
        monthly_df["date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_income = (
        monthly_df[
            monthly_df["type"].str.lower() == "income"
        ]
        .groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    monthly_income["Type"] = "Income"

    monthly_income.rename(
        columns={"amount": "Amount"},
        inplace=True
    )

    monthly_expense = (
        monthly_df[
            monthly_df["type"].str.lower() == "expense"
        ]
        .groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    monthly_expense["Type"] = "Expense"

    monthly_expense.rename(
        columns={"amount": "Amount"},
        inplace=True
    )

    monthly_chart_df = pd.concat(
        [
            monthly_income,
            monthly_expense
        ],
        ignore_index=True
    )

    if not monthly_chart_df.empty:

        fig_monthly = px.bar(
            monthly_chart_df,
            x="month",
            y="Amount",
            color="Type",
            barmode="group",
            title="Monthly Income vs Expenses"
        )

        fig_monthly.update_layout(
            xaxis_title="Month",
            yaxis_title="Amount",
            legend_title="Transaction Type"
        )

        st.plotly_chart(
            fig_monthly,
            width="stretch"
        )

    # --------------------------------------------------
    # CATEGORY SPENDING
    # --------------------------------------------------

    st.subheader("🍩 Category-wise Spending")

    expense_df = filtered_df[
        filtered_df["type"].str.lower() == "expense"
    ].copy()

    if not expense_df.empty:

        category_df = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .reset_index()
            .sort_values(
                "amount",
                ascending=False
            )
        )

        category_df.rename(
            columns={"amount": "Amount"},
            inplace=True
        )

        fig_category = px.pie(
            category_df,
            names="category",
            values="Amount",
            hole=0.45,
            title="Expense Distribution by Category"
        )

        st.plotly_chart(
            fig_category,
            width="stretch"
        )

    else:

        st.info(
            "No expense transactions available."
        )

    # --------------------------------------------------
    # TOP MERCHANTS
    # --------------------------------------------------

    st.subheader("🏆 Top Merchants")

    if not expense_df.empty:

        merchant_df = (
            expense_df
            .groupby("merchant")["amount"]
            .sum()
            .reset_index()
            .sort_values(
                "amount",
                ascending=False
            )
            .head(10)
        )

        merchant_df.rename(
            columns={"amount": "Amount"},
            inplace=True
        )

        fig_merchant = px.bar(
            merchant_df,
            x="Amount",
            y="merchant",
            orientation="h",
            title="Top 10 Merchants by Spending"
        )

        fig_merchant.update_layout(
            yaxis_title="Merchant",
            xaxis_title="Amount"
        )

        st.plotly_chart(
            fig_merchant,
            width="stretch"
        )

    # --------------------------------------------------
    # SAVINGS TREND
    # --------------------------------------------------

    st.subheader("💰 Monthly Savings Trend")

    savings_df = monthly_df.copy()

    income_by_month = (
        savings_df[
            savings_df["type"].str.lower() == "income"
        ]
        .groupby("month")["amount"]
        .sum()
    )

    expense_by_month = (
        savings_df[
            savings_df["type"].str.lower() == "expense"
        ]
        .groupby("month")["amount"]
        .sum()
    )

    savings_monthly = pd.DataFrame({
        "Income": income_by_month,
        "Expenses": expense_by_month
    }).fillna(0)

    savings_monthly["Savings"] = (
        savings_monthly["Income"]
        - savings_monthly["Expenses"]
    )

    savings_monthly = (
        savings_monthly
        .reset_index()
    )

    if not savings_monthly.empty:

        fig_savings = px.line(
            savings_monthly,
            x="month",
            y="Savings",
            markers=True,
            title="Monthly Savings"
        )

        fig_savings.update_layout(
            xaxis_title="Month",
            yaxis_title="Savings"
        )

        st.plotly_chart(
            fig_savings,
            width="stretch"
        )

    # --------------------------------------------------
    # SPENDING TREND
    # --------------------------------------------------

    st.subheader("📊 Daily Spending Trend")

    daily_expense = (
        expense_df
        .groupby("date")["amount"]
        .sum()
        .reset_index()
    )

    if not daily_expense.empty:

        fig_daily = px.line(
            daily_expense,
            x="date",
            y="amount",
            markers=True,
            title="Daily Expense Trend"
        )

        fig_daily.update_layout(
            xaxis_title="Date",
            yaxis_title="Expense"
        )

        st.plotly_chart(
            fig_daily,
            width="stretch"
        )

    # --------------------------------------------------
    # AUTOMATIC INSIGHTS
    # --------------------------------------------------

    st.subheader("💡 Analytics Insights")

    if not expense_df.empty:

        top_category_row = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not top_category_row.empty:

            top_category = (
                top_category_row.index[0]
            )

            top_category_amount = (
                top_category_row.iloc[0]
            )

            st.info(
                f"Your highest spending category is "
                f"**{top_category}** with "
                f"₹{top_category_amount:,.0f}."
            )

        top_merchant_row = (
            expense_df
            .groupby("merchant")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not top_merchant_row.empty:

            top_merchant = (
                top_merchant_row.index[0]
            )

            top_merchant_amount = (
                top_merchant_row.iloc[0]
            )

            st.info(
                f"Your highest-spending merchant is "
                f"**{top_merchant}** with "
                f"₹{top_merchant_amount:,.0f}."
            )

    if savings_rate >= 30:

        st.success(
            f"Your current savings rate is "
            f"**{savings_rate:.1f}%**."
        )

    elif savings_rate > 0:

        st.warning(
            f"Your current savings rate is "
            f"**{savings_rate:.1f}%**."
        )

    else:

        st.warning(
            "Your recorded expenses are equal to or "
            "higher than your recorded income."
        )

    # --------------------------------------------------
    # TRANSACTION TABLE
    # --------------------------------------------------

    st.subheader("📋 Filtered Transactions")

    st.dataframe(
        filtered_df.sort_values(
            "date",
            ascending=False
        ),
        width="stretch"
    )

    st.caption(
        f"Showing {len(filtered_df)} of {len(df)} transactions."
    )