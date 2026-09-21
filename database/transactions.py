import hashlib

from database.connection import get_connection


def create_transaction_hash(user_id, account_id, row):

    raw_data = (
        f"{user_id}|"
        f"{account_id}|"
        f"{row.get('date', '')}|"
        f"{row.get('merchant', '')}|"
        f"{row.get('description', '')}|"
        f"{row.get('type', '')}|"
        f"{row.get('amount', 0)}|"
        f"{row.get('category', '')}|"
        f"{row.get('balance', 0)}"
    )

    return hashlib.sha256(
        raw_data.encode("utf-8")
    ).hexdigest()


def save_transactions(user_id, transactions, account_id):

    connection = get_connection()
    cursor = connection.cursor()

    saved_count = 0
    skipped_count = 0

    try:

        check_query = """
        SELECT id
        FROM transactions
        WHERE user_id = %s
        AND account_id = %s
        AND transaction_hash = %s
        """

        insert_query = """
        INSERT INTO transactions (
            user_id,
            account_id,
            transaction_date,
            merchant,
            description,
            transaction_type,
            amount,
            category,
            balance,
            transaction_hash
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        """

        for _, row in transactions.iterrows():

            transaction_hash = create_transaction_hash(
                user_id,
                account_id,
                row
            )

            cursor.execute(
                check_query,
                (
                    user_id,
                    account_id,
                    transaction_hash
                )
            )

            existing = cursor.fetchone()

            if existing:
                skipped_count += 1
                continue

            transaction_date = row.get(
                "date",
                None
            )

            merchant = row.get(
                "merchant",
                ""
            )

            description = row.get(
                "description",
                ""
            )

            transaction_type = row.get(
                "type",
                "Expense"
            )

            amount = row.get(
                "amount",
                0
            )

            category = row.get(
                "category",
                "Other"
            )

            balance = row.get(
                "balance",
                0
            )

            if hasattr(transaction_date, "date"):
                transaction_date = transaction_date.date()

            cursor.execute(
                insert_query,
                (
                    user_id,
                    account_id,
                    transaction_date,
                    merchant,
                    description,
                    transaction_type,
                    float(amount),
                    category,
                    float(balance),
                    transaction_hash
                )
            )

            saved_count += 1

        connection.commit()

        return True, {
            "saved": saved_count,
            "skipped": skipped_count
        }

    except Exception as e:

        connection.rollback()

        return False, str(e)

    finally:

        cursor.close()
        connection.close()


def get_user_transactions(user_id, account_id=None):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        if account_id is None:

            query = """
            SELECT
                id,
                account_id,
                transaction_date AS date,
                merchant,
                description,
                transaction_type AS type,
                amount,
                category,
                balance
            FROM transactions
            WHERE user_id = %s
            ORDER BY transaction_date DESC, id DESC
            """

            cursor.execute(
                query,
                (user_id,)
            )

        else:

            query = """
            SELECT
                id,
                account_id,
                transaction_date AS date,
                merchant,
                description,
                transaction_type AS type,
                amount,
                category,
                balance
            FROM transactions
            WHERE user_id = %s
            AND account_id = %s
            ORDER BY transaction_date DESC, id DESC
            """

            cursor.execute(
                query,
                (
                    user_id,
                    account_id
                )
            )

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


def delete_user_transactions(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
        DELETE FROM transactions
        WHERE user_id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()