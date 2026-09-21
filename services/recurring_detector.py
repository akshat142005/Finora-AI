import pandas as pd


def detect_recurring_payments(df):

    if df is None or df.empty:
        return pd.DataFrame()

    data = df.copy()

    # Only expenses
    expenses = data[
        data["type"] == "Expense"
    ].copy()

    if expenses.empty:
        return pd.DataFrame()

    # Make sure date is datetime
    expenses["date"] = pd.to_datetime(
        expenses["date"],
        errors="coerce"
    )

    recurring = []

    # Check each merchant
    for merchant, group in expenses.groupby("merchant"):

        group = group.sort_values("date")

        # Need at least 2 transactions
        if len(group) < 2:
            continue

        amounts = group["amount"].astype(float)

        average_amount = amounts.mean()

        # Amount variation
        if average_amount > 0:

            amount_variation = (
                (amounts.max() - amounts.min())
                / average_amount
            ) * 100

        else:
            amount_variation = 100

        # Check date intervals
        dates = group["date"].dropna()

        if len(dates) >= 2:

            intervals = (
                dates.diff()
                .dt.days
                .dropna()
            )

            average_interval = intervals.mean()

        else:
            average_interval = 0

        # Recurring conditions
        is_recurring = (
            len(group) >= 2
            and amount_variation <= 20
            and (
                20 <= average_interval <= 40
                or 5 <= average_interval <= 10
            )
        )

        if is_recurring:

            if 20 <= average_interval <= 40:
                frequency = "Monthly"

            elif 5 <= average_interval <= 10:
                frequency = "Weekly"

            else:
                frequency = "Recurring"

            recurring.append({
                "Merchant": merchant,
                "Frequency": frequency,
                "Average Amount": round(
                    average_amount,
                    2
                ),
                "Occurrences": len(group),
                "Average Interval (Days)": round(
                    average_interval,
                    1
                )
            })

    return pd.DataFrame(recurring)