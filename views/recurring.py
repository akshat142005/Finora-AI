import streamlit as st
import pandas as pd


st.title("🔄 Recurring Payments")

st.write(
    "Finora AI identifies repeated payments and "
    "estimates their recurring expense pattern."
)


# =========================================================
# LOAD TRANSACTIONS
# =========================================================

transactions = st.session_state.get(
    "transactions",
    None
)


if transactions is None or transactions.empty:

    st.info(
        "📄 Upload a bank statement first to detect "
        "recurring payments."
    )

    st.stop()


df = transactions.copy()


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "date",
    "merchant",
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
        "Missing columns:",
        missing_columns
    )

    st.stop()


# =========================================================
# CLEAN DATA
# =========================================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

df["merchant"] = (
    df["merchant"]
    .fillna("")
    .astype(str)
    .str.strip()
)


df = df.dropna(
    subset=["date", "amount"]
)


# Only expenses
expenses = df[
    df["type"] == "Expense"
].copy()


if expenses.empty:

    st.info(
        "No expense transactions are available "
        "for recurring payment detection."
    )

    st.stop()


# =========================================================
# DETECT RECURRING PAYMENTS
# =========================================================

recurring_records = []


merchant_groups = expenses.groupby(
    "merchant"
)


for merchant, group in merchant_groups:

    if not merchant or merchant.lower() == "nan":
        continue

    group = group.sort_values("date")

    transaction_count = len(group)

    # A recurring payment needs at least 2 occurrences
    if transaction_count < 2:
        continue

    dates = group["date"].tolist()

    intervals = []

    for i in range(1, len(dates)):

        difference = (
            dates[i] - dates[i - 1]
        ).days

        intervals.append(difference)


    if not intervals:
        continue


    average_interval = sum(intervals) / len(intervals)


    # Monthly: approximately 25–35 days
    if 25 <= average_interval <= 35:

        frequency = "Monthly"

    # Weekly: approximately 6–8 days
    elif 6 <= average_interval <= 8:

        frequency = "Weekly"

    # Quarterly: approximately 80–100 days
    elif 80 <= average_interval <= 100:

        frequency = "Quarterly"

    else:

        continue


    average_amount = group["amount"].mean()

    if frequency == "Weekly":

        estimated_monthly = (
            average_amount * 4.33
        )

    elif frequency == "Monthly":

        estimated_monthly = average_amount

    elif frequency == "Quarterly":

        estimated_monthly = (
            average_amount / 3
        )

    else:

        estimated_monthly = average_amount


    recurring_records.append({

        "Merchant": merchant,

        "Frequency": frequency,

        "Occurrences": transaction_count,

        "Average Amount": average_amount,

        "Estimated Monthly Cost":
            estimated_monthly,

        "Last Payment":
            group["date"].max()

    })


# =========================================================
# RESULTS
# =========================================================

st.header("🔄 Detected Recurring Payments")


if not recurring_records:

    st.success(
        "✅ No recurring payment pattern was detected "
        "in the available statement."
    )

    st.info(
        "More historical transaction data can help "
        "Finora AI identify recurring payments."
    )

    st.stop()


recurring_df = pd.DataFrame(
    recurring_records
)


# =========================================================
# SUMMARY
# =========================================================

total_recurring_monthly = (
    recurring_df[
        "Estimated Monthly Cost"
    ].sum()
)


recurring_count = len(
    recurring_df
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Recurring Payments",
        recurring_count
    )


with col2:

    st.metric(
        "Estimated Monthly Cost",
        f"₹{total_recurring_monthly:,.0f}"
    )


st.divider()


# =========================================================
# DISPLAY TABLE
# =========================================================

st.subheader("📋 Recurring Payment Details")


display_df = recurring_df.copy()


display_df[
    "Average Amount"
] = display_df[
    "Average Amount"
].map(
    lambda x: f"₹{x:,.0f}"
)


display_df[
    "Estimated Monthly Cost"
] = display_df[
    "Estimated Monthly Cost"
].map(
    lambda x: f"₹{x:,.0f}"
)


display_df[
    "Last Payment"
] = pd.to_datetime(
    display_df["Last Payment"],
    errors="coerce"
).dt.strftime(
    "%d-%m-%Y"
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# RECURRING PAYMENT CARDS
# =========================================================

st.header("💳 Recurring Payment Overview")


for _, row in recurring_df.iterrows():

    merchant = row["Merchant"]

    frequency = row["Frequency"]

    occurrences = row["Occurrences"]

    average_amount = row["Average Amount"]

    monthly_cost = row[
        "Estimated Monthly Cost"
    ]


    with st.container(border=True):

        st.subheader(
            f"🔄 {merchant}"
        )

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Frequency",
                frequency
            )


        with col2:

            st.metric(
                "Average Payment",
                f"₹{average_amount:,.0f}"
            )


        with col3:

            st.metric(
                "Monthly Estimate",
                f"₹{monthly_cost:,.0f}"
            )


        st.caption(
            f"Detected from {occurrences} transactions."
        )


# =========================================================
# INFORMATION
# =========================================================

st.divider()


with st.expander(
    "ℹ️ How does Finora AI detect recurring payments?"
):

    st.write(
        "Finora AI groups expense transactions "
        "by merchant and compares the dates "
        "between repeated payments."
    )

    st.write(
        "Payments with approximately weekly, "
        "monthly or quarterly intervals are "
        "considered potential recurring payments."
    )

    st.write(
        "This is a pattern-based detection system. "
        "A detected recurring payment should be "
        "reviewed by the user before making financial decisions."
    )


st.divider()


st.caption(
    "ℹ️ Recurring payment detection depends on "
    "the transaction history available in the uploaded statement."
)