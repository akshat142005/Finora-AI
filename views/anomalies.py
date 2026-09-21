import streamlit as st
import pandas as pd
import numpy as np


# =========================================================
# PAGE TITLE
# =========================================================

st.title("⚠️ Anomaly Detection")

st.write(
    "Finora AI identifies unusually high transactions "
    "that differ from your normal spending pattern."
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
        "📄 Upload a bank statement first to detect "
        "unusual transactions."
    )

    st.stop()


# =========================================================
# COPY DATA
# =========================================================

df = transactions.copy()


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "amount",
    "type"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error(
        "❌ Required transaction columns are missing."
    )

    st.write(
        "Missing:",
        missing_columns
    )

    st.stop()


# =========================================================
# EXPENSE DATA
# =========================================================

expenses = df[
    df["type"] == "Expense"
].copy()


# =========================================================
# NO EXPENSES
# =========================================================

if expenses.empty:

    st.info(
        "No expense transactions are available "
        "for anomaly detection."
    )

    st.stop()


# =========================================================
# PREPARE AMOUNTS
# =========================================================

expenses["amount"] = pd.to_numeric(
    expenses["amount"],
    errors="coerce"
)


expenses = expenses.dropna(
    subset=["amount"]
)


# =========================================================
# ANOMALY DETECTION
# =========================================================
#
# Method:
# Mean + Standard Deviation
#
# A transaction is considered unusual when:
#
# amount > mean + 2 * standard deviation
#
# This is a simple statistical anomaly detector.
# =========================================================

mean_amount = expenses[
    "amount"
].mean()


std_amount = expenses[
    "amount"
].std()


# If only one transaction exists
if pd.isna(std_amount):

    std_amount = 0


threshold = (
    mean_amount +
    (2 * std_amount)
)


# =========================================================
# CALCULATE ANOMALY SCORE
# =========================================================

if std_amount > 0:

    expenses["anomaly_score"] = (
        expenses["amount"] - mean_amount
    ) / std_amount

else:

    expenses["anomaly_score"] = 0


# =========================================================
# DETECT ANOMALIES
# =========================================================

anomalies = expenses[
    expenses["amount"] > threshold
].copy()


# =========================================================
# HEADER
# =========================================================

st.header(
    "🔍 Unusual Transactions"
)


# =========================================================
# SUMMARY
# =========================================================

if anomalies.empty:

    st.success(
        "✅ No unusually high transactions were detected."
    )

    st.write(
        "Your recorded expense transactions are "
        "within the normal range of this analysis."
    )

else:

    st.warning(
        f"⚠️ {len(anomalies)} unusual "
        "transaction(s) detected."
    )


# =========================================================
# ANOMALY TABLE
# =========================================================

if not anomalies.empty:

    st.subheader(
        "📋 Detected Transactions"
    )

    display_columns = []

    for column in [
        "date",
        "merchant",
        "description",
        "category",
        "amount",
        "anomaly_score"
    ]:

        if column in anomalies.columns:

            display_columns.append(
                column
            )


    anomaly_table = anomalies[
        display_columns
    ].copy()


    # Rename columns
    rename_map = {

        "date": "Date",

        "merchant": "Merchant",

        "description": "Description",

        "category": "Category",

        "amount": "Amount",

        "anomaly_score": "Anomaly Score"

    }


    anomaly_table = anomaly_table.rename(
        columns=rename_map
    )


    # Format amount
    if "Amount" in anomaly_table.columns:

        anomaly_table["Amount"] = (
            anomaly_table["Amount"]
            .map(
                lambda x: f"₹{x:,.0f}"
            )
        )


    # Format score
    if "Anomaly Score" in anomaly_table.columns:

        anomaly_table["Anomaly Score"] = (
            anomaly_table["Anomaly Score"]
            .map(
                lambda x: f"{x:.2f}"
            )
        )


    st.dataframe(
        anomaly_table,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# AI ALERTS
# =========================================================

st.header(
    "🚨 AI Alerts"
)


if anomalies.empty:

    with st.container(border=True):

        st.subheader(
            "✅ No Critical Alerts"
        )

        st.write(
            "Finora AI did not detect any unusually "
            "high expense transactions in the "
            "available statement data."
        )

else:

    # -----------------------------------------------------
    # CREATE ALERT FOR EACH ANOMALY
    # -----------------------------------------------------

    for _, row in anomalies.iterrows():

        amount = row["amount"]

        category = row.get(
            "category",
            "Unknown"
        )

        merchant = row.get(
            "merchant",
            "Unknown Merchant"
        )

        score = row["anomaly_score"]


        with st.container(border=True):

            st.subheader(
                "🚨 Unusual Payment"
            )

            st.write(
                f"**Merchant:** {merchant}"
            )

            st.write(
                f"**Amount:** ₹{amount:,.0f}"
            )

            st.write(
                f"**Category:** {category}"
            )

            st.write(
                f"**Anomaly Score:** {score:.2f}"
            )

            st.warning(
                "This transaction is significantly "
                "higher than the typical expense amount "
                "in the uploaded statement."
            )


# =========================================================
# DETECTION DETAILS
# =========================================================

st.divider()

st.header(
    "🧠 Detection Details"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Expense",
        f"₹{mean_amount:,.0f}"
    )


with col2:

    st.metric(
        "Detection Threshold",
        f"₹{threshold:,.0f}"
    )


with col3:

    st.metric(
        "Unusual Transactions",
        len(anomalies)
    )


# =========================================================
# EXPLANATION
# =========================================================

with st.expander(
    "ℹ️ How does Finora AI detect anomalies?"
):

    st.write(
        "Finora AI compares each expense against "
        "the average expense and its standard deviation."
    )

    st.write(
        "A transaction above the calculated statistical "
        "threshold is flagged as an unusual transaction."
    )

    st.write(
        "This is a statistical indicator and does not "
        "automatically mean that a transaction is fraudulent."
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "ℹ️ Anomaly detection is based on the transaction "
    "data available in the uploaded statement. "
    "An unusual transaction is not necessarily fraudulent."
)