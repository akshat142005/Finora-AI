import streamlit as st
import pandas as pd


def show_transactions():

    st.title("💳 Transactions")

    st.write(
        "View, search and filter your processed bank transactions."
    )

    # =========================================================
    # CHECK DATA
    # =========================================================

    transactions = st.session_state.get(
        "transactions",
        None
    )

    if transactions is None or transactions.empty:

        st.info(
            "📄 No transactions available. "
            "Please upload a bank statement first."
        )

        return

    df = transactions.copy()

    # =========================================================
    # FILTER SECTION
    # =========================================================

    st.subheader("🔎 Search & Filter")

    col1, col2, col3 = st.columns(3)

    # ---------------- SEARCH ----------------

    with col1:

        search = st.text_input(
            "Search Merchant",
            placeholder="e.g. Amazon, Swiggy..."
        )

    # ---------------- TYPE FILTER ----------------

    with col2:

        type_options = [
            "All",
            "Income",
            "Expense"
        ]

        selected_type = st.selectbox(
            "Transaction Type",
            type_options
        )

    # ---------------- CATEGORY FILTER ----------------

    with col3:

        categories = sorted(
            df["category"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Category",
            ["All"] + categories
        )

    # =========================================================
    # APPLY FILTERS
    # =========================================================

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df["merchant"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if selected_type != "All":

        filtered_df = filtered_df[
            filtered_df["type"] == selected_type
        ]

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    # =========================================================
    # SUMMARY
    # =========================================================

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Transactions",
            len(filtered_df)
        )

    with col2:

        income = filtered_df.loc[
            filtered_df["type"] == "Income",
            "amount"
        ].sum()

        st.metric(
            "Income",
            f"₹{income:,.0f}"
        )

    with col3:

        expense = filtered_df.loc[
            filtered_df["type"] == "Expense",
            "amount"
        ].sum()

        st.metric(
            "Expense",
            f"₹{expense:,.0f}"
        )

    # =========================================================
    # TRANSACTION TABLE
    # =========================================================

    st.write("")

    st.subheader("📋 Transaction History")

    display_df = filtered_df.copy()

    if "date" in display_df.columns:

        display_df["date"] = (
            pd.to_datetime(
                display_df["date"],
                errors="coerce"
            )
            .dt.strftime("%d-%m-%Y")
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        height=500
    )

    # =========================================================
    # EXPORT
    # =========================================================

    st.divider()

    st.header("📥 Export Transactions")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Transactions CSV",
        data=csv_data,
        file_name="finora_transactions.csv",
        mime="text/csv",
        width="stretch"
    )