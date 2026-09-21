import bcrypt

from database.connection import get_connection


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):

    try:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    except Exception:

        return False


# =========================================================
# REGISTER USER
# =========================================================

def register_user(name, email, password):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        # Hash password before storing it
        hashed_password = hash_password(
            password
        )

        query = """
        INSERT INTO users (
            name,
            email,
            password
        )
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                name,
                email,
                hashed_password
            )
        )

        connection.commit()

        return True, "Registration successful!"

    except Exception as e:

        if "Duplicate entry" in str(e):

            return False, "Email already registered."

        return False, str(e)

    finally:

        cursor.close()
        connection.close()


# =========================================================
# LOGIN USER
# =========================================================

def login_user(email, password):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        query = """
        SELECT
            id,
            name,
            email,
            password
        FROM users
        WHERE email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            return False, "Invalid email or password."

        stored_password = user["password"]

        # -------------------------------------------------
        # NEW BCRYPT PASSWORD
        # -------------------------------------------------

        if stored_password.startswith("$2"):

            if verify_password(
                password,
                stored_password
            ):

                return True, {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }

            return False, "Invalid email or password."

        # -------------------------------------------------
        # OLD PLAINTEXT PASSWORD
        # -------------------------------------------------
        # This allows existing users to login once.
        # After successful login, their password is
        # automatically converted to bcrypt.
        # -------------------------------------------------

        if password == stored_password:

            new_hash = hash_password(
                password
            )

            update_query = """
            UPDATE users
            SET password = %s
            WHERE id = %s
            """

            cursor.execute(
                update_query,
                (
                    new_hash,
                    user["id"]
                )
            )

            connection.commit()

            return True, {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }

        return False, "Invalid email or password."

    except Exception as e:

        return False, str(e)

    finally:

        cursor.close()
        connection.close()