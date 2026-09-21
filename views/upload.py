import streamlit as st

from services.statement_parser import read_statement
from services.transaction_cleaner import clean_transactions

from database.bank_accounts import (
    get_user_accounts,
    create_bank_account
)

from database.transactions import save_transactions


def show_upload():

    st.title("📄 Upload Statement")

    st.write(
        "Upload your bank statement in CSV, XLSX, or PDF format."
    )

    # =========================================================
    # USER
    # =========================================================

    user = st.session_state.get("user")

    if not user:
        st.error("❌ User session not found.")
        return

    user_id = user.get("id")

    if not user_id:
        st.error("❌ User ID not found.")
        return

    # =========================================================
    # LOAD BANK ACCOUNTS
    # =========================================================

    try:

        accounts = get_user_accounts(user_id)

    except Exception as e:

        st.error("❌ Could not load bank accounts.")
        st.exception(e)
        return

    # =========================================================
    # SELECT BANK ACCOUNT
    # =========================================================

    st.subheader("🏦 Select Bank Account")

    if not accounts:

        st.warning(
            "No bank account found. Please create your bank account first."
        )

        create_account_form(user_id)

        return

    # ---------------------------------------------------------
    # CREATE ACCOUNT OPTIONS
    # ---------------------------------------------------------

    account_options = {}

    for account in accounts:

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

            label += f" - {account_name}"

        if last4:

            label += f" ••••{last4}"

        account_options[label] = account["id"]

    account_labels = list(
        account_options.keys()
    )

    # ---------------------------------------------------------
    # CURRENT SIDEBAR ACCOUNT
    # ---------------------------------------------------------

    current_account_id = st.session_state.get(
        "selected_account_id"
    )

    default_index = 0

    if current_account_id is not None:

        for index, account_id in enumerate(
            account_options.values()
        ):

            if account_id == current_account_id:

                default_index = index
                break

    # ---------------------------------------------------------
    # ACCOUNT SELECTBOX
    # ---------------------------------------------------------

    selected_account_label = st.selectbox(

        "Which bank account does this statement belong to?",

        account_labels,

        index=default_index,

        key="upload_account_selector"
    )

    selected_account_id = account_options[
        selected_account_label
    ]

    # ---------------------------------------------------------
    # SHOW SELECTED ACCOUNT
    # ---------------------------------------------------------

    st.success(
        f"🏦 Selected Account: {selected_account_label}"
    )

    st.caption(
        f"Account ID: {selected_account_id}"
    )

    # =========================================================
    # ADD ANOTHER BANK ACCOUNT
    # =========================================================

    st.write("")

    with st.expander(
        "➕ Add Another Bank Account"
    ):

        create_account_form(
            user_id
        )

    # =========================================================
    # UPLOAD SECTION
    # =========================================================

    st.divider()

    st.subheader("📁 Upload Statement")

    uploaded_file = st.file_uploader(

        "Choose a bank statement",

        type=[
            "csv",
            "xlsx",
            "pdf"
        ],

        key="statement_uploader"
    )

    # =========================================================
    # NO FILE
    # =========================================================

    if uploaded_file is None:

        st.info(
            "Please upload a statement to continue."
        )

        return

    # =========================================================
    # FILE SELECTED
    # =========================================================

    st.success(
        f"📄 File selected: {uploaded_file.name}"
    )

    # =========================================================
    # READ STATEMENT
    # =========================================================

    try:

        raw_df = read_statement(
            uploaded_file
        )

        if raw_df is None:

            st.error(
                "❌ Could not read the statement."
            )

            return

        if raw_df.empty:

            st.error(
                "❌ Could not extract transactions from this file."
            )

            return

        # =====================================================
        # EXTRACTED DATA
        # =====================================================

        st.subheader(
            "📋 Extracted Data"
        )

        st.dataframe(
            raw_df,
            width="stretch"
        )

        st.success(
            f"✅ {len(raw_df)} rows extracted."
        )

        # =====================================================
        # CLEAN TRANSACTIONS
        # =====================================================

        cleaned_df = clean_transactions(
            raw_df
        )

        if cleaned_df is None:

            st.error(
                "❌ Transaction cleaning failed."
            )

            return

        if cleaned_df.empty:

            st.error(
                "❌ No valid transactions were found."
            )

            return

        # =====================================================
        # CLEANED DATA
        # =====================================================

        st.subheader(
            "✅ Cleaned Transactions"
        )

        st.dataframe(
            cleaned_df,
            width="stretch"
        )

        st.success(
            f"✅ {len(cleaned_df)} valid transactions ready to save."
        )

        # =====================================================
        # SAVE SECTION
        # =====================================================

        st.divider()

        st.subheader(
            "💾 Save Transactions"
        )

        st.info(
            f"Transactions will be saved to: "
            f"**{selected_account_label}**"
        )

        st.caption(
            f"Database Account ID: {selected_account_id}"
        )

        # =====================================================
        # SAVE BUTTON
        # =====================================================

        save_clicked = st.button(

            "💾 Save Transactions",

            type="primary",

            use_container_width=True,

            key="save_transactions_button"
        )

        if save_clicked:

            st.write(
                "⏳ Saving transactions..."
            )

            try:

                success, result = save_transactions(

                    user_id=user_id,

                    transactions=cleaned_df,

                    account_id=selected_account_id
                )

                # =================================================
                # SAVE SUCCESS
                # =================================================

                if success:

                    saved_count = result.get(
                        "saved",
                        0
                    )

                    skipped_count = result.get(
                        "skipped",
                        0
                    )

                    # ---------------------------------------------
                    # SAVED
                    # ---------------------------------------------

                    if saved_count > 0:

                        st.success(
                            f"✅ {saved_count} transactions "
                            f"saved successfully!"
                        )

                    # ---------------------------------------------
                    # DUPLICATES
                    # ---------------------------------------------

                    if skipped_count > 0:

                        st.info(
                            f"ℹ️ {skipped_count} duplicate "
                            f"transactions skipped."
                        )

                    # ---------------------------------------------
                    # NOTHING SAVED
                    # ---------------------------------------------

                    if (
                        saved_count == 0
                        and skipped_count == 0
                    ):

                        st.warning(
                            "⚠️ No transactions were saved."
                        )

                    # ---------------------------------------------
                    # UPDATE SESSION
                    # ---------------------------------------------

                    st.session_state.selected_account_id = (
                        selected_account_id
                    )

                    st.session_state.transactions_loaded = False

                    # ---------------------------------------------
                    # FINAL MESSAGE
                    # ---------------------------------------------

                    st.success(
                        "🎉 Upload completed. "
                        "You can now open Dashboard or Transactions."
                    )

                # =================================================
                # SAVE FAILED
                # =================================================

                else:

                    st.error(
                        f"❌ Could not save transactions: {result}"
                    )

            except Exception as e:

                st.error(
                    "❌ Error while saving transactions."
                )

                st.exception(e)

    # =========================================================
    # FILE PROCESSING ERROR
    # =========================================================

    except Exception as e:

        st.error(
            "❌ Error while processing statement."
        )

        st.exception(e)


# =============================================================
# CREATE BANK ACCOUNT FORM
# =============================================================

def create_account_form(user_id):

    st.write(
        "Create a new bank account before uploading its statement."
    )

    with st.form(
        "create_bank_account_form",
        clear_on_submit=True
    ):

        # =====================================================
        # BANK LIST
        # =====================================================

        bank_options = [

            "State Bank of India (SBI)",

            "HDFC Bank",

            "ICICI Bank",

            "Axis Bank",

            "Kotak Mahindra Bank",

            "Punjab National Bank (PNB)",

            "Bank of Baroda",

            "Canara Bank",

            "Union Bank of India",

            "Indian Bank",

            "Bank of India",

            "IndusInd Bank",

            "IDFC FIRST Bank",

            "Yes Bank",

            "Federal Bank",

            "AU Small Finance Bank",

            "Bandhan Bank",

            "Central Bank of India",

            "UCO Bank",

            "Indian Overseas Bank",

            "Punjab & Sind Bank",

            "Bank of Maharashtra",

            "Other"
        ]

        selected_bank = st.selectbox(

            "Bank Name",

            bank_options,

            key="upload_bank_name"
        )

        # =====================================================
        # OTHER BANK
        # =====================================================

        if selected_bank == "Other":

            custom_bank_name = st.text_input(

                "Enter Bank Name",

                placeholder="Example: ABC Cooperative Bank",

                key="upload_custom_bank_name"
            )

            bank_name = custom_bank_name

        else:

            bank_name = selected_bank

        # =====================================================
        # ACCOUNT NAME
        # =====================================================

        account_name = st.text_input(

            "Account Name",

            placeholder="Example: Personal Savings",

            key="upload_account_name"
        )

        # =====================================================
        # LAST 4 DIGITS
        # =====================================================

        account_number_last4 = st.text_input(

            "Last 4 digits of account number",

            max_chars=4,

            placeholder="1234",

            key="upload_last4"
        )

        # =====================================================
        # ACCOUNT TYPE
        # =====================================================

        account_type = st.selectbox(

            "Account Type",

            [
                "Savings",
                "Current",
                "Salary",
                "Other"
            ],

            key="upload_account_type"
        )

        # =====================================================
        # SUBMIT
        # =====================================================

        create_account = st.form_submit_button(

            "➕ Create Bank Account",

            use_container_width=True
        )

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    if create_account:

        # -----------------------------------------------------
        # BANK NAME VALIDATION
        # -----------------------------------------------------

        if not bank_name.strip():

            st.error(
                "❌ Please enter the bank name."
            )

            return

        # -----------------------------------------------------
        # LAST 4 VALIDATION
        # -----------------------------------------------------

        if account_number_last4:

            if (
                not account_number_last4.isdigit()
                or len(account_number_last4) != 4
            ):

                st.error(
                    "❌ Last 4 digits must contain exactly 4 numbers."
                )

                return

        # =====================================================
        # CREATE DATABASE ACCOUNT
        # =====================================================

        success, result = create_bank_account(

            user_id=user_id,

            bank_name=bank_name.strip(),

            account_name=(
                account_name.strip()
                or None
            ),

            account_number_last4=(
                account_number_last4
                or None
            ),

            account_type=account_type
        )

        # =====================================================
        # SUCCESS
        # =====================================================

        if success:

            new_account_id = result

            st.success(
                "✅ Bank account created successfully!"
            )

            # Update selected account
            st.session_state.selected_account_id = (
                new_account_id
            )

            # Reload accounts
            st.session_state.accounts = (
                get_user_accounts(user_id)
            )

            st.rerun()

        # =====================================================
        # FAILURE
        # =====================================================

        else:

            st.error(
                f"❌ Could not create bank account: {result}"
            )