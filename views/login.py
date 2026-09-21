import streamlit as st

from database.users import register_user, login_user


def show_login_page():

    st.title("💰 Finora AI")

    st.subheader(
        "Personal Finance Intelligence"
    )

    st.write(
        "Login or create an account to continue."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # =========================
    # LOGIN
    # =========================

    with login_tab:

        st.header("🔐 Login")

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            type="primary",
            use_container_width=True,
            key="login_button"
        ):

            if not email or not password:

                st.warning(
                    "⚠️ Please enter email and password."
                )

            else:

                try:

                    success, result = login_user(
                        email,
                        password
                    )

                    if success:

                        st.session_state.logged_in = True
                        st.session_state.user = result

                        st.success(
                            f"✅ Welcome, {result['name']}!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"❌ {result}"
                        )

                except Exception as e:

                    st.error(
                        "❌ Login error"
                    )

                    st.code(
                        str(e)
                    )

    # =========================
    # REGISTER
    # =========================

    with register_tab:

        st.header("📝 Create Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 6 characters",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Enter password again",
            key="register_confirm_password"
        )

        if st.button(
            "📝 Create Account",
            type="primary",
            use_container_width=True,
            key="register_button"
        ):

            if not name or not email or not password:

                st.warning(
                    "⚠️ Please fill all fields."
                )

            elif len(password) < 6:

                st.warning(
                    "⚠️ Password must contain at least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                try:

                    success, message = register_user(
                        name,
                        email,
                        password
                    )

                    if success:

                        st.success(
                            "🎉 Account created successfully!"
                        )

                        st.info(
                            "Now open the Login tab and login."
                        )

                    else:

                        st.error(
                            f"❌ {message}"
                        )

                except Exception as e:

                    st.error(
                        "❌ Registration error"
                    )

                    st.code(
                        str(e)
                    )