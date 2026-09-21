import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors


def create_pdf_report(df, user_name):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15
    )

    normal_style = styles["Normal"]

    story = []

    # Title
    story.append(
        Paragraph("Finora AI - Financial Report", title_style)
    )

    story.append(
        Paragraph(
            f"User: {user_name}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"Report Date: {datetime.now().strftime('%d-%m-%Y')}",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Financial calculations
    income = df.loc[
        df["type"].astype(str).str.lower() == "income",
        "amount"
    ].sum()

    expenses = df.loc[
        df["type"].astype(str).str.lower() == "expense",
        "amount"
    ].sum()

    savings = income - expenses

    if income > 0:
        savings_rate = (savings / income) * 100
    else:
        savings_rate = 0

    transaction_count = len(df)

    # Summary
    story.append(
        Paragraph("<b>Financial Summary</b>", styles["Heading2"])
    )

    summary_data = [
        ["Metric", "Amount"],
        ["Total Income", f"Rs. {income:,.2f}"],
        ["Total Expenses", f"Rs. {expenses:,.2f}"],
        ["Net Savings", f"Rs. {savings:,.2f}"],
        ["Savings Rate", f"{savings_rate:.1f}%"],
        ["Transactions", str(transaction_count)]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[250, 200]
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(summary_table)

    story.append(Spacer(1, 20))

    # Category-wise spending
    story.append(
        Paragraph(
            "<b>Category-wise Spending</b>",
            styles["Heading2"]
        )
    )

    expense_df = df[
        df["type"].astype(str).str.lower() == "expense"
    ].copy()

    if not expense_df.empty:

        category_data = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        category_table_data = [
            ["Category", "Amount"]
        ]

        for category, amount in category_data.items():
            category_table_data.append(
                [str(category), f"Rs. {amount:,.2f}"]
            )

        category_table = Table(
            category_table_data,
            colWidths=[250, 200]
        )

        category_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6)
            ])
        )

        story.append(category_table)

    else:
        story.append(
            Paragraph(
                "No expense transactions available.",
                normal_style
            )
        )

    story.append(Spacer(1, 20))

    # Transaction details
    story.append(
        Paragraph(
            "<b>Transaction Details</b>",
            styles["Heading2"]
        )
    )

    transaction_data = [
        ["Date", "Merchant", "Type", "Amount", "Category"]
    ]

    for _, row in df.iterrows():

        date_value = row.get("date", "")

        if pd.notna(date_value):
            try:
                date_value = pd.to_datetime(date_value).strftime(
                    "%d-%m-%Y"
                )
            except Exception:
                date_value = str(date_value)

        merchant = str(row.get("merchant", ""))[:25]
        transaction_type = str(row.get("type", ""))
        amount = float(row.get("amount", 0))
        category = str(row.get("category", ""))[:20]

        transaction_data.append([
            str(date_value),
            merchant,
            transaction_type,
            f"Rs. {amount:,.2f}",
            category
        ])

    transaction_table = Table(
        transaction_data,
        colWidths=[70, 130, 70, 90, 100],
        repeatRows=1
    )

    transaction_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4)
        ])
    )

    story.append(transaction_table)

    story.append(Spacer(1, 20))

    # Disclaimer
    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated from the "
            "transactions uploaded to Finora AI. It is intended for "
            "personal financial analysis and does not constitute "
            "professional financial advice.",
            normal_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# REPORTS PAGE
# =========================================================

def show_reports():

    st.title("📥 Reports & Export")

    st.write(
        "Generate and download your Finora AI financial report."
    )

    df = st.session_state.get("transactions")

    # No transactions
    if df is None or df.empty:
        st.warning(
            "No transactions available. Please upload a bank statement first."
        )
        return

    # Required columns check
    required_columns = ["type", "amount"]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            f"Missing required columns: {', '.join(missing_columns)}"
        )
        return

    # Calculations
    income = df.loc[
        df["type"].astype(str).str.lower() == "income",
        "amount"
    ].sum()

    expenses = df.loc[
        df["type"].astype(str).str.lower() == "expense",
        "amount"
    ].sum()

    savings = income - expenses

    if income > 0:
        savings_rate = (savings / income) * 100
    else:
        savings_rate = 0

    transaction_count = len(df)

    # User name
    user = st.session_state.get("user")

    if isinstance(user, dict):
        user_name = user.get("name", "User")
    else:
        user_name = "User"

    # Summary
    st.subheader("📊 Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Income",
            f"Rs. {income:,.0f}"
        )

    with col2:
        st.metric(
            "Expenses",
            f"Rs. {expenses:,.0f}"
        )

    with col3:
        st.metric(
            "Savings",
            f"Rs. {savings:,.0f}"
        )

    with col4:
        st.metric(
            "Transactions",
            transaction_count
        )

    st.divider()

    st.write(f"**User:** {user_name}")
    st.write(f"**Transactions included:** {transaction_count}")
    st.write(
        f"**Report Date:** {datetime.now().strftime('%d-%m-%Y')}"
    )

    st.divider()

    # Generate PDF
    try:

        pdf_file = create_pdf_report(
            df,
            user_name
        )

        st.download_button(
            label="📥 Download Financial Report PDF",
            data=pdf_file,
            file_name="Finora_AI_Financial_Report.pdf",
            mime="application/pdf",
            key="finora_pdf_report_download"
        )

    except Exception as e:

        st.error(
            f"Unable to generate PDF report: {e}"
        )