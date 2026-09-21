from database.connection import get_connection


def create_bank_account(
    user_id,
    bank_name,
    account_name=None,
    account_number_last4=None,
    account_type="Savings"
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO bank_accounts
        (
            user_id,
            bank_name,
            account_name,
            account_number_last4,
            account_type
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                bank_name,
                account_name,
                account_number_last4,
                account_type
            )
        )

        connection.commit()

        return True, cursor.lastrowid

    except Exception as e:
        connection.rollback()
        return False, str(e)

    finally:
        cursor.close()
        connection.close()


def get_user_accounts(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT
            id,
            bank_name,
            account_name,
            account_number_last4,
            account_type,
            created_at
        FROM bank_accounts
        WHERE user_id = %s
        ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_account(account_id, user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT
            id,
            bank_name,
            account_name,
            account_number_last4,
            account_type
        FROM bank_accounts
        WHERE id = %s
        AND user_id = %s
        """

        cursor.execute(query, (account_id, user_id))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def delete_bank_account(account_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        DELETE FROM bank_accounts
        WHERE id = %s
        AND user_id = %s
        """

        cursor.execute(query, (account_id, user_id))
        connection.commit()

        return True

    except Exception:
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()