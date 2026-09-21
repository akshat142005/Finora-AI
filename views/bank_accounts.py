import streamlit as st

from database.bank_accounts import (
    get_user_accounts,
    create_bank_account,
    delete_bank_account
)


def show_bank_accounts():

    st.title("🏦 Bank Accounts")

    st.caption(
        "Manage all your bank accounts connected to Finora AI."
    )

    # =========================================================
    # USER
    # =========================================================

    user = st.session_state.get("user")

    if not user:
        st.error("User session not found.")
        return

    user_id = user.get("id")

    # =========================================================
    # LOAD ACCOUNTS
    # =========================================================

    try:
        accounts = get_user_accounts(user_id)

    except Exception as e:
        st.error("❌ Could not load bank accounts.")
        st.exception(e)
        return

    # =========================================================
    # ADD NEW ACCOUNT
    # =========================================================

    st.subheader("➕ Add New Bank Account")

    with st.form("add_bank_account_form"):

        # -----------------------------------------------------
        # BANK LIST
        # -----------------------------------------------------

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
            bank_options
        )

        # -----------------------------------------------------
        # OTHER BANK
        # -----------------------------------------------------

        if selected_bank == "Other":

            custom_bank_name = st.text_input(
                "Enter Bank Name",
                placeholder="Example: ABC Cooperative Bank"
            )

            bank_name = custom_bank_name

        else:

            bank_name = selected_bank

        # -----------------------------------------------------
        # ACCOUNT DETAILS
        # -----------------------------------------------------

        account_name = st.text_input(
            "Account Name",
            placeholder="Example: Personal Savings"
        )

        last4 = st.text_input(
            "Last 4 digits of account number",
            max_chars=4,
            placeholder="1234"
        )

        account_type = st.selectbox(
            "Account Type",
            [
                "Savings",
                "Current",
                "Salary",
                "Other"
            ]
        )

        submitted = st.form_submit_button(
            "➕ Add Account",
            use_container_width=True
        )

    # =========================================================
    # SAVE ACCOUNT
    # =========================================================

    if submitted:

        # -----------------------------------------------------
        # BANK VALIDATION
        # -----------------------------------------------------

        if not bank_name.strip():

            st.error(
                "Please enter the bank name."
            )

            return

        # -----------------------------------------------------
        # LAST 4 VALIDATION
        # -----------------------------------------------------

        if last4:

            if (
                not last4.isdigit()
                or len(last4) != 4
            ):

                st.error(
                    "Last 4 digits must contain exactly 4 numbers."
                )

                return

        # -----------------------------------------------------
        # CREATE ACCOUNT
        # -----------------------------------------------------

        success, result = create_bank_account(

            user_id=user_id,

            bank_name=bank_name.strip(),

            account_name=(
                account_name.strip()
                or None
            ),

            account_number_last4=(
                last4
                or None
            ),

            account_type=account_type
        )

        if success:

            st.success(
                "✅ Bank account added successfully!"
            )

            # Refresh account list
            st.session_state.accounts = (
                get_user_accounts(user_id)
            )

            # Select newly created account
            st.session_state.selected_account_id = result

            st.rerun()

        else:

            st.error(
                f"❌ Could not add account: {result}"
            )

    # =========================================================
    # EXISTING ACCOUNTS
    # =========================================================

    st.divider()

    st.subheader("💳 Your Bank Accounts")

    if not accounts:

        st.info(
            "No bank accounts added yet."
        )

        return

    # =========================================================
    # DISPLAY ACCOUNTS
    # =========================================================

    for account in accounts:

        account_id = account["id"]

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

        account_type = account.get(
            "account_type",
            "Savings"
        )

        with st.container(border=True):

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.subheader(
                    f"🏦 {bank_name}"
                )

                if account_name:

                    st.write(
                        f"**Account:** {account_name}"
                    )

                if last4:

                    st.write(
                        f"**Account Number:** ••••{last4}"
                    )

                st.write(
                    f"**Account Type:** {account_type}"
                )

            with col2:

                st.write("")

                delete_clicked = st.button(
                    "🗑️ Delete",
                    key=f"delete_account_{account_id}",
                    use_container_width=True
                )

                if delete_clicked:

                    st.session_state[
                        f"confirm_delete_{account_id}"
                    ] = True

            # =================================================
            # DELETE CONFIRMATION
            # =================================================

            if st.session_state.get(
                f"confirm_delete_{account_id}",
                False
            ):

                st.warning(
                    "⚠️ Deleting this account will also "
                    "delete its transactions."
                )

                confirm_col1, confirm_col2 = st.columns(2)

                with confirm_col1:

                    confirm_delete = st.button(
                        "Yes, Delete",
                        key=f"confirm_yes_{account_id}",
                        type="primary",
                        use_container_width=True
                    )

                with confirm_col2:

                    cancel_delete = st.button(
                        "Cancel",
                        key=f"confirm_no_{account_id}",
                        use_container_width=True
                    )

                if confirm_delete:

                    success = delete_bank_account(
                        account_id,
                        user_id
                    )

                    if success:

                        if (
                            st.session_state.get(
                                "selected_account_id"
                            )
                            == account_id
                        ):

                            st.session_state.selected_account_id = None

                        st.session_state.accounts = (
                            get_user_accounts(user_id)
                        )

                        st.session_state.transactions_loaded = False

                        st.success(
                            "✅ Bank account deleted successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "❌ Could not delete bank account."
                        )

                if cancel_delete:

                    st.session_state[
                        f"confirm_delete_{account_id}"
                    ] = False

                    st.rerun()

    # =========================================================
    # FOOTER
    # =========================================================

    st.divider()

    st.caption(
        "🔐 Your bank account number is stored only as the last 4 digits."
    )