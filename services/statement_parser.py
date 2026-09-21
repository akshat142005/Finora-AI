import pandas as pd
import pdfplumber
import re


# ============================================================
# CSV
# ============================================================

def read_csv(file):
    return pd.read_csv(file)


# ============================================================
# EXCEL
# ============================================================

def read_excel(file):
    """
    Read Excel bank statements.

    Supports:
    1. Normal structured Excel statements
    2. PhonePe multi-sheet statements
    """

    try:
        excel = pd.ExcelFile(file)
        all_transactions = []

        for sheet_name in excel.sheet_names:

            # -------------------------------------------------
            # Read sheet without assuming a header
            # -------------------------------------------------
            raw_df = pd.read_excel(
                excel,
                sheet_name=sheet_name,
                header=None
            )

            if raw_df.empty:
                continue

            # -------------------------------------------------
            # Detect PhonePe transaction rows
            #
            # PhonePe format:
            # Date | Transaction Details | Type | Amount
            # -------------------------------------------------
            for _, row in raw_df.iterrows():

                if len(row) < 4:
                    continue

                date_value = row.iloc[0]
                description_value = row.iloc[1]
                type_value = row.iloc[2]
                amount_value = row.iloc[3]

                # Skip incomplete rows
                if (
                    pd.isna(date_value)
                    or pd.isna(description_value)
                    or pd.isna(type_value)
                    or pd.isna(amount_value)
                ):
                    continue

                transaction_type = (
                    str(type_value)
                    .strip()
                    .upper()
                )

                # Only actual transaction rows
                if transaction_type not in [
                    "DEBIT",
                    "CREDIT"
                ]:
                    continue

                # -------------------------------------------------
                # Clean PhonePe date
                # Example:
                # "Sep 1 5, 2026"
                # becomes
                # "Sep 15, 2026"
                # -------------------------------------------------
                date_text = str(
                    date_value
                ).strip()

                date_text = re.sub(
                    r"(?<=\d)\s+(?=\d)",
                    "",
                    date_text
                )

                date_text = re.sub(
                    r"\s*,\s*",
                    ", ",
                    date_text
                )

                transaction_date = pd.to_datetime(
                    date_text,
                    errors="coerce"
                )

                if pd.isna(transaction_date):
                    continue

                # -------------------------------------------------
                # Clean amount
                # -------------------------------------------------
                amount = clean_amount(
                    amount_value
                )

                if amount <= 0:
                    continue

                description = (
                    str(description_value)
                    .strip()
                )

                # -------------------------------------------------
                # Convert DEBIT / CREDIT
                # -------------------------------------------------
                debit = 0.0
                credit = 0.0

                if transaction_type == "DEBIT":
                    debit = amount

                elif transaction_type == "CREDIT":
                    credit = amount

                all_transactions.append({
                    "date": transaction_date,
                    "description": description,
                    "debit": debit,
                    "credit": credit,
                    "balance": 0.0
                })

        # -----------------------------------------------------
        # Return all transactions
        # -----------------------------------------------------
        if not all_transactions:
            return pd.DataFrame(
                columns=[
                    "date",
                    "description",
                    "debit",
                    "credit",
                    "balance"
                ]
            )

        return pd.DataFrame(
            all_transactions
        )

    except Exception as e:

        print(
            f"Excel extraction error: {e}"
        )

        return pd.DataFrame()


# ============================================================
# HELPER: CLEAN COLUMN NAME
# ============================================================

def clean_column_name(column):
    column = str(column)

    column = (
        column
        .strip()
        .lower()
        .replace("\n", " ")
        .replace("\r", " ")
    )

    column = re.sub(r"\s+", " ", column)

    return column


# ============================================================
# HELPER: FIND COLUMN
# ============================================================

def find_column(columns, possible_names):

    for column in columns:

        clean_name = clean_column_name(column)

        for name in possible_names:

            if name in clean_name:
                return column

    return None


# ============================================================
# NORMALIZE BANK TABLE
# ============================================================

def normalize_bank_table(df):

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # --------------------------------------------------------
    # Remove completely empty rows/columns
    # --------------------------------------------------------

    df = df.dropna(
        how="all"
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    if df.empty:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    df.columns = [
        clean_column_name(column)
        for column in df.columns
    ]

    columns = list(df.columns)

    # --------------------------------------------------------
    # Find common bank statement columns
    # --------------------------------------------------------

    date_column = find_column(
        columns,
        [
            "date",
            "transaction date",
            "txn date",
            "value date",
            "posting date"
        ]
    )

    description_column = find_column(
        columns,
        [
            "description",
            "narration",
            "particulars",
            "transaction details",
            "details",
            "remarks"
        ]
    )

    debit_column = find_column(
        columns,
        [
            "debit",
            "withdrawal",
            "withdrawals",
            "debit amount",
            "withdrawal amount"
        ]
    )

    credit_column = find_column(
        columns,
        [
            "credit",
            "deposit",
            "deposits",
            "credit amount",
            "deposit amount"
        ]
    )

    balance_column = find_column(
        columns,
        [
            "balance",
            "closing balance",
            "available balance"
        ]
    )

    # --------------------------------------------------------
    # Create normalized dataframe
    # --------------------------------------------------------

    result = pd.DataFrame()

    # Date
    if date_column is not None:
        result["date"] = df[date_column]

    else:
        result["date"] = None

    # Description
    if description_column is not None:
        result["description"] = df[
            description_column
        ]

    else:

        # If description column is not found,
        # try combining text columns.
        text_columns = []

        for column in columns:

            if column in [
                date_column,
                debit_column,
                credit_column,
                balance_column
            ]:
                continue

            if df[column].dtype == "object":
                text_columns.append(column)

        if text_columns:

            result["description"] = (
                df[text_columns]
                .fillna("")
                .astype(str)
                .agg(" ".join, axis=1)
            )

        else:
            result["description"] = ""

    # Debit
    if debit_column is not None:
        result["debit"] = df[
            debit_column
        ]

    else:
        result["debit"] = 0

    # Credit
    if credit_column is not None:
        result["credit"] = df[
            credit_column
        ]

    else:
        result["credit"] = 0

    # Balance
    if balance_column is not None:
        result["balance"] = df[
            balance_column
        ]

    else:
        result["balance"] = 0

    return result


# ============================================================
# CLEAN AMOUNT
# ============================================================

def clean_amount(value):

    if pd.isna(value):
        return 0.0

    value = str(value).strip()

    if value == "":
        return 0.0

    # Remove currency symbols
    value = value.replace("₹", "")
    value = value.replace("Rs.", "")
    value = value.replace("Rs", "")
    value = value.replace(",", "")

    # Remove spaces
    value = value.replace(" ", "")

    # Handle parentheses: (500) = -500
    if value.startswith("(") and value.endswith(")"):
        value = "-" + value[1:-1]

    # Keep numbers, decimal and minus
    value = re.sub(
        r"[^0-9.\-]",
        "",
        value
    )

    try:
        return float(value)

    except Exception:
        return 0.0


# ============================================================
# READ PDF
# ============================================================

def read_pdf(file):

    all_tables = []

    try:

        with pdfplumber.open(file) as pdf:

            for page_number, page in enumerate(
                pdf.pages,
                start=1
            ):

                # ------------------------------------------------
                # Try normal table extraction
                # ------------------------------------------------

                tables = page.extract_tables()

                for table in tables:

                    if not table:
                        continue

                    if len(table) < 2:
                        continue

                    table_df = pd.DataFrame(
                        table
                    )

                    # First row as header
                    header = table_df.iloc[0]

                    data = table_df.iloc[1:].copy()

                    data.columns = [
                        str(x)
                        if x is not None
                        else f"column_{i}"
                        for i, x in enumerate(header)
                    ]

                    data = data.reset_index(
                        drop=True
                    )

                    if not data.empty:
                        all_tables.append(data)

    except Exception as e:

        print(
            f"PDF extraction error: {e}"
        )

        return pd.DataFrame()

    # ------------------------------------------------------------
    # No tables found
    # ------------------------------------------------------------

    if not all_tables:
        return pd.DataFrame()

    # ------------------------------------------------------------
    # Combine all tables
    # ------------------------------------------------------------

    try:

        combined = pd.concat(
            all_tables,
            ignore_index=True,
            sort=False
        )

    except Exception:

        return pd.DataFrame()

    # ------------------------------------------------------------
    # Normalize
    # ------------------------------------------------------------

    normalized = normalize_bank_table(
        combined
    )

    # ------------------------------------------------------------
    # Clean values
    # ------------------------------------------------------------

    if "date" in normalized.columns:

        normalized["date"] = pd.to_datetime(
            normalized["date"],
            dayfirst=True,
            errors="coerce"
        )

    if "description" in normalized.columns:

        normalized["description"] = (
            normalized["description"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    if "debit" in normalized.columns:

        normalized["debit"] = (
            normalized["debit"]
            .apply(clean_amount)
        )

    if "credit" in normalized.columns:

        normalized["credit"] = (
            normalized["credit"]
            .apply(clean_amount)
        )

    if "balance" in normalized.columns:

        normalized["balance"] = (
            normalized["balance"]
            .apply(clean_amount)
        )

    # ------------------------------------------------------------
    # Remove rows without useful data
    # ------------------------------------------------------------

    normalized = normalized[
        (
            normalized["date"].notna()
        )
        |
        (
            normalized["description"]
            .str.len() > 0
        )
    ]

    normalized = normalized.reset_index(
        drop=True
    )

    return normalized


# ============================================================
# MAIN STATEMENT READER
# ============================================================

def read_statement(file):

    file_name = file.name.lower()

    if file_name.endswith(".csv"):

        return read_csv(file)

    elif file_name.endswith(".xlsx"):

        return read_excel(file)

    elif file_name.endswith(".pdf"):

        return read_pdf(file)

    else:

        return pd.DataFrame()