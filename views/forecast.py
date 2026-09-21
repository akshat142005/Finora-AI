import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# PAGE TITLE
# =========================================================

st.title("📈 Expense Forecast")

st.write(
    "Finora AI uses your historical spending pattern "
    "to estimate future expenses."
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
        "an expense forecast."
    )

    st.stop()


# =========================================================
# PREPARE DATA
# =========================================================

df = transactions.copy()


if "date" not in df.columns:

    st.error(
        "❌ Date information is required for forecasting."
    )

    st.stop()


if "amount" not in df.columns:

    st.error(
        "❌ Transaction amount information is required."
    )

    st.stop()


# Convert date

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# Convert amount

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)


# Remove invalid rows

df = df.dropna(
    subset=["date", "amount"]
)


# =========================================================
# EXPENSE DATA
# =========================================================

if "type" in df.columns:

    expenses = df[
        df["type"] == "Expense"
    ].copy()

else:

    expenses = df.copy()


# =========================================================
# NO EXPENSE DATA
# =========================================================

if expenses.empty:

    st.warning(
        "⚠️ No expense transactions are available "
        "for forecasting."
    )

    st.stop()


# =========================================================
# MONTHLY EXPENSE CALCULATION
# =========================================================

expenses["month"] = (
    expenses["date"]
    .dt.to_period("M")
)


monthly_data = (
    expenses
    .groupby("month")["amount"]
    .sum()
    .reset_index()
)


monthly_data["month"] = (
    monthly_data["month"]
    .astype(str)
)


monthly_data = monthly_data.sort_values(
    "month"
).reset_index(
    drop=True
)


# =========================================================
# FORECAST CALCULATION
# =========================================================

monthly_values = (
    monthly_data["amount"]
    .astype(float)
    .values
)


number_of_months = len(
    monthly_values
)


# ---------------------------------------------------------
# NO MONTHLY DATA
# ---------------------------------------------------------

if number_of_months == 0:

    predicted_expense = 0

    forecast_method = (
        "Insufficient historical data"
    )


# ---------------------------------------------------------
# ONE MONTH
# ---------------------------------------------------------

elif number_of_months == 1:

    # With only one month available,
    # use that month as the baseline.

    predicted_expense = monthly_values[0]

    forecast_method = (
        "Single-month baseline"
    )


# ---------------------------------------------------------
# TWO OR MORE MONTHS
# ---------------------------------------------------------

else:

    x = np.arange(
        number_of_months
    )

    y = monthly_values


    # Linear trend

    coefficients = np.polyfit(
        x,
        y,
        1
    )


    slope = coefficients[0]

    intercept = coefficients[1]


    next_x = number_of_months


    predicted_expense = (
        slope * next_x
        + intercept
    )


    # Avoid negative forecast

    predicted_expense = max(
        predicted_expense,
        0
    )


    forecast_method = (
        "Historical trend analysis"
    )


# =========================================================
# ROUND FORECAST
# =========================================================

predicted_expense = round(
    float(predicted_expense),
    2
)


# =========================================================
# NEXT MONTH PREDICTION
# =========================================================

st.header(
    "🔮 Next Month Prediction"
)


with st.container(border=True):

    st.subheader(
        "💰 Predicted Next Month Expense"
    )

    st.metric(
        "Estimated Expense",
        f"₹{predicted_expense:,.0f}"
    )

    st.caption(
        f"Forecast method: {forecast_method}"
    )


# =========================================================
# HISTORICAL MONTHLY SPENDING
# =========================================================

st.header(
    "📊 Historical Monthly Spending"
)


if not monthly_data.empty:

    chart_df = monthly_data.copy()

    chart_df.columns = [
        "Month",
        "Expense"
    ]


    fig = px.line(
        chart_df,
        x="Month",
        y="Expense",
        markers=True,
        title="Monthly Expense Trend"
    )


    fig.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Expense (₹)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.info(
        "No historical monthly spending data available."
    )


# =========================================================
# MONTHLY SPENDING TABLE
# =========================================================

st.subheader(
    "📋 Monthly Spending Data"
)


display_monthly = monthly_data.copy()


display_monthly.columns = [
    "Month",
    "Expense"
]


display_monthly["Expense"] = (
    display_monthly["Expense"]
    .map(
        lambda x: f"₹{x:,.0f}"
    )
)


st.dataframe(
    display_monthly,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FORECAST INFORMATION
# =========================================================

st.header(
    "🧠 Forecast Information"
)


with st.container(border=True):

    st.subheader(
        "🔮 AI Prediction"
    )

    if number_of_months == 1:

        st.write(
            f"Based on the available historical spending "
            f"data, Finora AI estimates your next month's "
            f"expense at approximately "
            f"**₹{predicted_expense:,.0f}**."
        )

        st.info(
            "Only one month of spending data is currently "
            "available. The prediction therefore uses the "
            "available month as a baseline rather than "
            "assuming a long-term trend."
        )


    elif number_of_months >= 2:

        st.write(
            f"Based on your historical monthly spending "
            f"pattern, Finora AI estimates your next month's "
            f"expense at approximately "
            f"**₹{predicted_expense:,.0f}**."
        )

        st.info(
            f"The forecast uses {number_of_months} months "
            "of historical expense data and a linear "
            "trend model."
        )


    else:

        st.write(
            "There is not enough historical data to "
            "generate a reliable expense forecast."
        )


# =========================================================
# FORECAST METRICS
# =========================================================

st.divider()

st.subheader(
    "📌 Forecast Metrics"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Months Analyzed",
        number_of_months
    )


with col2:

    average_expense = (
        monthly_values.mean()
        if number_of_months > 0
        else 0
    )

    st.metric(
        "Average Monthly Expense",
        f"₹{average_expense:,.0f}"
    )


with col3:

    st.metric(
        "Next Month Estimate",
        f"₹{predicted_expense:,.0f}"
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "ℹ️ Expense forecasting is an estimate based on "
    "the transaction history available in the uploaded "
    "statement. More historical months can improve "
    "trend-based predictions."
)