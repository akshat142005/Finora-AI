import streamlit as st
import pandas as pd
import plotly.express as px
# =========================================================
# GLOBAL UI STYLE
# =========================================================

def load_css():

    try:

        with open(
            "assets/style.css",
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        pass


load_css()

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Finora AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "transactions" not in st.session_state:
    st.session_state.transactions = None

if "transactions_loaded" not in st.session_state:
    st.session_state.transactions_loaded = False

if "selected_account_id" not in st.session_state:
    st.session_state.selected_account_id = None

if "accounts" not in st.session_state:
    st.session_state.accounts = []


# =========================================================
# LOGIN / REGISTER
# =========================================================

if not st.session_state.logged_in:

    from views.login import show_login_page

    show_login_page()

    st.stop()


# =========================================================
# CURRENT USER
# =========================================================

user = st.session_state.user


# =========================================================
# LOAD BANK ACCOUNTS
# =========================================================

from database.bank_accounts import get_user_accounts

try:

    accounts = get_user_accounts(
        user["id"]
    )

    st.session_state.accounts = accounts

except Exception as e:

    st.error(
        "❌ Unable to load bank accounts."
    )

    st.error(str(e))

    st.session_state.accounts = []


# =========================================================
# CHECK SELECTED ACCOUNT
# =========================================================

available_account_ids = [
    account["id"]
    for account in st.session_state.accounts
]


selected_account_id = (
    st.session_state.get(
        "selected_account_id"
    )
)


# If selected account no longer exists,
# automatically switch to All Accounts.

if (
    selected_account_id is not None
    and selected_account_id not in available_account_ids
):

    st.session_state.selected_account_id = None

    selected_account_id = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # BRAND
    # -----------------------------------------------------

    st.title("💰 Finora AI")

    st.caption(
        "Personal Finance Intelligence"
    )

    st.divider()


    # -----------------------------------------------------
    # ACCOUNT
    # -----------------------------------------------------

    st.subheader("👤 Account")

    current_user = st.session_state.get(
        "user"
    )

    if isinstance(current_user, dict):

        user_name = current_user.get(
            "name",
            "User"
        )

        user_email = current_user.get(
            "email",
            ""
        )

        st.markdown(
            f"**{user_name}**"
        )

        if user_email:

            st.caption(
                user_email
            )


    st.divider()


    # -----------------------------------------------------
    # BANK ACCOUNT SELECTOR
    # -----------------------------------------------------

    st.subheader(
        "🏦 Bank Account"
    )

    account_options = {
        "🌐 All Accounts": None
    }


    for account in st.session_state.accounts:

        bank_name = account.get(
            "bank_name",
            "Bank"
        )

        account_name = account.get(
            "account_name"
        )

        last4 = account.get(
            "account_number_last4"
        )

        label = bank_name


        if account_name:

            label += (
                f" - {account_name}"
            )


        if last4:

            label += (
                f" ••••{last4}"
            )


        account_options[
            label
        ] = account["id"]


    account_labels = list(
        account_options.keys()
    )


    # -----------------------------------------------------
    # FIND CURRENT ACCOUNT INDEX
    # -----------------------------------------------------

    current_account_id = (
        st.session_state.get(
            "selected_account_id"
        )
    )

    default_index = 0


    if current_account_id is not None:

        for index, account_id in enumerate(
            account_options.values()
        ):

            if account_id == current_account_id:

                default_index = index

                break


    # -----------------------------------------------------
    # ACCOUNT SELECTBOX
    # -----------------------------------------------------

    selected_account_label = st.selectbox(
        "Select account",
        account_labels,
        index=default_index,
        key="sidebar_account_selector"
    )


    new_selected_account_id = (
        account_options[
            selected_account_label
        ]
    )


    # -----------------------------------------------------
    # ACCOUNT CHANGE
    # -----------------------------------------------------

    if (
        new_selected_account_id
        != st.session_state.get(
            "selected_account_id"
        )
    ):

        st.session_state.selected_account_id = (
            new_selected_account_id
        )

        st.session_state.transactions_loaded = (
            False
        )

        st.session_state.transactions = None

        st.rerun()


    st.divider()


    # =====================================================
    # NAVIGATION
    # =====================================================

    st.subheader(
        "🧭 Navigation"
    )


    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "🏦 Bank Accounts",
            "📄 Upload Statement",
            "💳 Transactions",
            "📊 Analytics",
            "🤖 AI Insights",
            "🔄 Recurring Payments",
            "⚠️ Anomaly Detection",
            "📈 Expense Forecast",
            "❤️ Financial Health",
            "💬 Ask Finora AI",
            "📥 Reports & Export",
        ],
        label_visibility="collapsed"
    )


    st.divider()


    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user = None

        st.session_state.transactions = None

        st.session_state.transactions_loaded = False

        st.session_state.selected_account_id = None

        st.session_state.accounts = []

        st.rerun()


# =========================================================
# LOAD USER TRANSACTIONS
# =========================================================

if not st.session_state.transactions_loaded:

    from database.transactions import (
        get_user_transactions
    )

    try:

        user = st.session_state.user

        selected_account_id = (
            st.session_state.get(
                "selected_account_id"
            )
        )


        # -------------------------------------------------
        # ALL ACCOUNTS
        # -------------------------------------------------

        if selected_account_id is None:

            saved_transactions = (
                get_user_transactions(
                    user["id"]
                )
            )


        # -------------------------------------------------
        # SPECIFIC ACCOUNT
        # -------------------------------------------------

        else:

            saved_transactions = (
                get_user_transactions(
                    user["id"],
                    selected_account_id
                )
            )


        # -------------------------------------------------
        # SAVE TO SESSION
        # -------------------------------------------------

        if saved_transactions:

            st.session_state.transactions = (
                pd.DataFrame(
                    saved_transactions
                )
            )

        else:

            st.session_state.transactions = None


        st.session_state.transactions_loaded = (
            True
        )


    except Exception as e:

        st.error(
            "❌ Unable to load saved transactions."
        )

        st.error(
            str(e)
        )

        st.session_state.transactions = None

        st.session_state.transactions_loaded = True


# =========================================================
# MAIN APPLICATION IMPORTS
# =========================================================

from services.spending_analytics import (
    calculate_summary,
    category_spending,
    top_spending_category
)


# =========================================================
# CURRENT USER
# =========================================================

user = st.session_state.user


# =========================================================
# PAGE ROUTING
# =========================================================

if page == "🏠 Dashboard":

    from views.dashboard import (
        show_dashboard
    )

    show_dashboard()

    st.stop()


elif page == "🏦 Bank Accounts":

    from views.bank_accounts import (
        show_bank_accounts
    )

    show_bank_accounts()

    st.stop()


elif page == "📄 Upload Statement":

    from views.upload import (
        show_upload
    )

    show_upload()

    st.stop()


elif page == "💳 Transactions":

    from views.transactions import (
        show_transactions
    )

    show_transactions()

    st.stop()


elif page == "📊 Analytics":

    from views.analytics import (
        show_analytics
    )

    show_analytics()

    st.stop()


elif page == "🤖 AI Insights":

    from views.ai_insights import (
        show_ai_insights
    )

    show_ai_insights()

    st.stop()


elif page == "🔄 Recurring Payments":

    from views.recurring import (
        show_recurring
    )

    show_recurring()

    st.stop()


elif page == "⚠️ Anomaly Detection":

    from views.anomalies import (
        show_anomalies
    )

    show_anomalies()

    st.stop()


elif page == "📈 Expense Forecast":

    from views.forecast import (
        show_forecast
    )

    show_forecast()

    st.stop()


elif page == "❤️ Financial Health":

    from views.financial_health import (
        show_financial_health
    )

    show_financial_health()

    st.stop()


elif page == "💬 Ask Finora AI":

    from views.finance_query import (
        show_finance_query
    )

    show_finance_query()

    st.stop()


elif page == "📥 Reports & Export":

    from views.reports import (
        show_reports
    )

    show_reports()

    st.stop()


# =========================================================
# DASHBOARD DATA
# =========================================================

transactions = (
    st.session_state.transactions
)


if (
    transactions is not None
    and not transactions.empty
):

    summary = calculate_summary(
        transactions
    )


    total_income = summary[
        "total_income"
    ]


    total_expense = summary[
        "total_expense"
    ]


    net_savings = summary[
        "net_savings"
    ]


    savings_rate = summary[
        "savings_rate"
    ]


    category_data = category_spending(
        transactions
    )


    top_category = top_spending_category(
        transactions
    )


else:

    total_income = 0

    total_expense = 0

    net_savings = 0

    savings_rate = 0

    category_data = pd.Series(
        dtype="float64"
    )

    top_category = "No Data"


# =========================================================
# DASHBOARD
# =========================================================

st.title(
    "💰 Finora AI"
)

st.subheader(
    "Personal Finance Intelligence"
)

st.write(
    f"Welcome **{user['name']}** 👋 "
    "to your financial command center. "
    "Understand your spending, savings and "
    "financial patterns from one place."
)


# =========================================================
# SELECTED ACCOUNT INFORMATION
# =========================================================

selected_account_id = (
    st.session_state.get(
        "selected_account_id"
    )
)


if selected_account_id is None:

    st.caption(
        "🏦 Showing data for all bank accounts"
    )

else:

    selected_account = None

    for account in st.session_state.accounts:

        if account["id"] == selected_account_id:

            selected_account = account

            break


    if selected_account:

        bank_name = selected_account.get(
            "bank_name",
            "Bank"
        )

        st.caption(
            f"🏦 Showing data for selected bank "
            f"account: {bank_name} "
            f"(Account ID: {selected_account_id})"
        )


# =========================================================
# NO STATEMENT
# =========================================================

if (
    transactions is None
    or transactions.empty
):

    st.info(
        "📄 Start by uploading your bank statement "
        "to unlock Finora AI analytics."
    )


    st.divider()


    st.header(
        "✨ What Finora AI Can Do"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.subheader(
                "📊 Smart Analytics"
            )

            st.write(
                "Analyze income, expenses, categories, "
                "merchants and spending trends."
            )


    with col2:

        with st.container(border=True):

            st.subheader(
                "🤖 AI Insights"
            )

            st.write(
                "Generate automatic insights from "
                "your transaction patterns."
            )


    with col3:

        with st.container(border=True):

            st.subheader(
                "🔮 Predictive Intelligence"
            )

            st.write(
                "Detect unusual payments, recurring "
                "expenses and future spending."
            )


    st.divider()


    st.caption(
        "Upload a statement to begin."
    )

    st.stop()


# =========================================================
# FINANCIAL OVERVIEW
# =========================================================

st.header(
    "💰 Financial Overview"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Income",
        f"₹{total_income:,.0f}"
    )


with col2:

    st.metric(
        "Total Expense",
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


st.write("")


# =========================================================
# SPENDING ANALYSIS
# =========================================================

st.header(
    "📊 Spending Analysis"
)


left, right = st.columns(
    [1.4, 1]
)


# =========================================================
# CATEGORY BAR CHART
# =========================================================

with left:

    st.subheader(
        "Spending by Category"
    )


    if not category_data.empty:

        chart_df = (
            category_data
            .reset_index()
        )


        chart_df.columns = [
            "Category",
            "Amount"
        ]


        fig = px.bar(
            chart_df,
            x="Category",
            y="Amount",
            text="Amount",
            title="Category-wise Expenses"
        )


        fig.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )


        fig.update_layout(
            height=400,
            showlegend=False
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.info(
            "No expense data available."
        )


# =========================================================
# EXPENSE PIE CHART
# =========================================================

with right:

    st.subheader(
        "Expense Distribution"
    )


    if not category_data.empty:

        pie_df = (
            category_data
            .reset_index()
        )


        pie_df.columns = [
            "Category",
            "Amount"
        ]


        fig2 = px.pie(
            pie_df,
            names="Category",
            values="Amount",
            hole=0.55,
            title="Expense Distribution"
        )


        fig2.update_layout(
            height=400
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )


    else:

        st.info(
            "No expense data available."
        )


# =========================================================
# QUICK FINANCIAL INSIGHTS
# =========================================================

st.header(
    "🧠 Quick Financial Insights"
)


col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.subheader(
            "🔝 Top Spending"
        )


        st.write(
            "Highest spending category:"
        )


        st.markdown(
            f"### {top_category}"
        )


with col2:

    with st.container(border=True):

        st.subheader(
            "💰 Savings"
        )


        st.write(
            "Your recorded net savings:"
        )


        st.markdown(
            f"### ₹{net_savings:,.0f}"
        )


with col3:

    with st.container(border=True):

        st.subheader(
            "📊 Activity"
        )


        st.write(
            "Transactions analyzed:"
        )


        st.markdown(
            f"### {len(transactions)}"
        )


# =========================================================
# FINORA AI INTELLIGENCE
# =========================================================

st.header(
    "🚀 Finora AI Intelligence"
)


col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.subheader(
            "🤖 AI Insights"
        )


        st.write(
            "Automatically identify important "
            "financial spending patterns."
        )


        st.caption(
            "Use AI Insights from the sidebar."
        )


with col2:

    with st.container(border=True):

        st.subheader(
            "⚠️ Anomaly Detection"
        )


        st.write(
            "Identify unusually high or "
            "unusual transactions."
        )


        st.caption(
            "Use Anomaly Detection from the sidebar."
        )


with col3:

    with st.container(border=True):

        st.subheader(
            "📈 Expense Forecast"
        )


        st.write(
            "Estimate future expenses using "
            "historical spending patterns."
        )


        st.caption(
            "Use Expense Forecast from the sidebar."
        )


# =========================================================
# FINORA AI MODULES
# =========================================================

st.divider()


st.header(
    "🧩 Finora AI Modules"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.info(
        "📄\n\n"
        "**Statement Parser**\n\n"
        "Extract transactions from "
        "PDF, CSV and Excel."
    )


with col2:

    st.info(
        "🤖\n\n"
        "**ML Categorization**\n\n"
        "Automatically classify "
        "transactions."
    )


with col3:

    st.info(
        "🔄\n\n"
        "**Recurring Payments**\n\n"
        "Detect subscriptions and "
        "repeated payments."
    )


with col4:

    st.info(
        "❤️\n\n"
        "**Financial Health**\n\n"
        "Analyze overall financial "
        "behavior."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "Finora AI analyzes the transaction data "
    "provided in your uploaded bank statement."
)