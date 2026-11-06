
"""
SQLite database layer.

Responsible for database initialization,
connection management, and financial data persistence.

Monetary amounts are stored as integer cents.
"""

import sqlite3

from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal

from config.settings import DATABASE_PATH, DATA_DIR


# --------------------------------------------------
# Connection management
# --------------------------------------------------

@contextmanager
def get_connection():
    """
    Provide a managed SQLite connection.

    Automatically commits successful transactions
    and rolls back failed transactions.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# --------------------------------------------------
# Database initialization
# --------------------------------------------------

def initialize_database():
    """
    Create database tables if they do not exist.
    """

    with get_connection() as connection:

        connection.executescript("""

            CREATE TABLE IF NOT EXISTS households (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                amount_cents INTEGER NOT NULL
                    CHECK(amount_cents >= 0),
                frequency TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (household_id)
                    REFERENCES households(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount_cents INTEGER NOT NULL
                    CHECK(amount_cents >= 0),
                frequency TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (household_id)
                    REFERENCES households(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                amount_cents INTEGER NOT NULL
                    CHECK(amount_cents >= 0),
                frequency TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (household_id)
                    REFERENCES households(id)
                    ON DELETE CASCADE
            );

        """)


# --------------------------------------------------
# Monetary conversion
# --------------------------------------------------

def to_cents(amount) -> int:
    """
    Convert decimal currency into integer cents.
    """

    value = Decimal(str(amount))

    if not value.is_finite() or value < 0:
        raise ValueError("Amount must be finite and non-negative.")

    return int(
        (value * 100).quantize(Decimal("1"))
    )


def from_cents(amount_cents: int) -> Decimal:
    """
    Convert integer cents into decimal currency.
    """

    return Decimal(amount_cents) / Decimal("100")


# --------------------------------------------------
# Household management
# --------------------------------------------------

def create_household(name: str) -> int:
    """
    Create a household and return its database ID.
    """

    if not name.strip():
        raise ValueError("Household name cannot be empty.")

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO households (name, created_at)
            VALUES (?, ?)
            """,
            (
                name.strip(),
                datetime.now(timezone.utc).isoformat()
            )
        )

        return cursor.lastrowid


def get_households() -> list:
    """
    Retrieve all registered households.
    """

    with get_connection() as connection:

        rows = connection.execute(
            "SELECT * FROM households ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]


# --------------------------------------------------
# Generic financial record insertion
# --------------------------------------------------

def _insert_record(
    table: str,
    household_id: int,
    description: str,
    amount,
    frequency: str,
    category: str = None
) -> int:
    """
    Insert a financial record.

    Table names are restricted internally to prevent
    SQL injection through dynamic identifiers.
    """

    allowed_tables = {
        "income",
        "expenses",
        "savings"
    }

    if table not in allowed_tables:
        raise ValueError("Invalid financial table.")

    if not description.strip():
        raise ValueError("Description cannot be empty.")

    if not frequency.strip():
        raise ValueError("Frequency cannot be empty.")

    amount_cents = to_cents(amount)

    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:

        if table == "expenses":

            cursor = connection.execute(
                """
                INSERT INTO expenses (
                    household_id,
                    description,
                    category,
                    amount_cents,
                    frequency,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    household_id,
                    description.strip(),
                    category,
                    amount_cents,
                    frequency,
                    created_at
                )
            )

        else:

            cursor = connection.execute(
                f"""
                INSERT INTO {table} (
                    household_id,
                    description,
                    amount_cents,
                    frequency,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    household_id,
                    description.strip(),
                    amount_cents,
                    frequency,
                    created_at
                )
            )

        return cursor.lastrowid


# --------------------------------------------------
# Public financial record methods
# --------------------------------------------------

def add_income(
    household_id: int,
    description: str,
    amount,
    frequency: str
) -> int:

    return _insert_record(
        "income",
        household_id,
        description,
        amount,
        frequency
    )


def add_expense(
    household_id: int,
    description: str,
    category: str,
    amount,
    frequency: str
) -> int:

    if not category.strip():
        raise ValueError("Category cannot be empty.")

    return _insert_record(
        "expenses",
        household_id,
        description,
        amount,
        frequency,
        category
    )


def add_savings(
    household_id: int,
    description: str,
    amount,
    frequency: str
) -> int:

    return _insert_record(
        "savings",
        household_id,
        description,
        amount,
        frequency
    )


# --------------------------------------------------
# Financial record retrieval
# --------------------------------------------------

def get_financial_records(
    household_id: int,
    table: str
) -> list:
    """
    Retrieve financial records for a household.

    Returns monetary values as Decimal.
    """

    allowed_tables = {
        "income",
        "expenses",
        "savings"
    }

    if table not in allowed_tables:
        raise ValueError("Invalid financial table.")

    with get_connection() as connection:

        rows = connection.execute(
            f"""
            SELECT *
            FROM {table}
            WHERE household_id = ?
            ORDER BY id
            """,
            (household_id,)
        ).fetchall()

        records = []

        for row in rows:

            record = dict(row)

            record["amount"] = from_cents(
                record.pop("amount_cents")
            )

            records.append(record)

        return records


def get_household(household_id: int):
    """Retrieve one household by ID."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM households WHERE id = ?",
            (household_id,)
        ).fetchone()

        return dict(row) if row else None


def update_financial_record(
    record_id,
    table,
    description=None,
    amount=None,
    frequency=None,
    category=None,
):
    """Update an existing financial record."""

    allowed_tables = {"income", "expenses", "savings"}

    if table not in allowed_tables:
        raise ValueError("Invalid financial table.")

    updates = []
    values = []

    if description is not None:
        if not description.strip():
            raise ValueError("Description cannot be empty.")
        updates.append("description = ?")
        values.append(description.strip())

    if amount is not None:
        updates.append("amount_cents = ?")
        values.append(to_cents(amount))

    if frequency is not None:
        if not frequency.strip():
            raise ValueError("Frequency cannot be empty.")
        updates.append("frequency = ?")
        values.append(frequency.strip())

    if table == "expenses" and category is not None:
        if not category.strip():
            raise ValueError("Category cannot be empty.")
        updates.append("category = ?")
        values.append(category.strip())

    if not updates:
        raise ValueError("No fields provided to update.")

    values.append(record_id)

    with get_connection() as connection:
        cursor = connection.execute(
            f"UPDATE {table} SET {', '.join(updates)} WHERE id = ?",
            values,
        )

        return cursor.rowcount > 0


def delete_financial_record(record_id, table):
    """Delete one financial record."""

    allowed_tables = {"income", "expenses", "savings"}

    if table not in allowed_tables:
        raise ValueError("Invalid financial table.")

    with get_connection() as connection:
        cursor = connection.execute(
            f"DELETE FROM {table} WHERE id = ?",
            (record_id,),
        )

        return cursor.rowcount > 0


def delete_household(household_id):
    """Delete a household and all associated financial records."""

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM households WHERE id = ?",
            (household_id,),
        )

        return cursor.rowcount > 0
