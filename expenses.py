
from database import DB_PATH
import sqlite3


# -----------------------------
# Add Expense
# -----------------------------

def add_expense(date, category, description, amount, payment_method):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (date, category, description, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
    """, (
        date,
        category,
        description,
        amount,
        payment_method
    ))

    connection.commit()
    connection.close()


# -----------------------------
# Get Expenses
# -----------------------------

def get_expenses():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            category,
            description,
            amount,
            payment_method
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# -----------------------------
# Delete Expense
# -----------------------------

def delete_expense(expense_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()


# -----------------------------
# Update Expense
# -----------------------------

def update_expense(
    expense_id,
    date,
    category,
    description,
    amount,
    payment_method
):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET date = ?,
            category = ?,
            description = ?,
            amount = ?,
            payment_method = ?
        WHERE id = ?
    """, (
        date,
        category,
        description,
        amount,
        payment_method,
        expense_id
    ))

    connection.commit()
    connection.close()


# -----------------------------
# Expense Summary
# -----------------------------

def get_expense_summary():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(amount), 0),
            COALESCE(AVG(amount), 0),
            COALESCE(MAX(amount), 0)
        FROM expenses
    """)

    summary = cursor.fetchone()

    connection.close()

    return summary

def get_category_summary():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    summary = cursor.fetchall()

    connection.close()

    return summary

def get_monthly_summary():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month
    """)

    summary = cursor.fetchall()

    connection.close()

    return summary

def export_expenses():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            category,
            description,
            amount,
            payment_method
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses

def search_expenses(
    search_text="",
    category="",
    payment_method=""
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            date,
            category,
            description,
            amount,
            payment_method
        FROM expenses
        WHERE 1=1
    """

    parameters = []

    # Search description or category
    if search_text:
        query += """
            AND (
                description LIKE ?
                OR category LIKE ?
            )
        """

        search_pattern = f"%{search_text}%"

        parameters.extend([
            search_pattern,
            search_pattern
        ])

    # Category filter
    if category:
        query += " AND category = ?"
        parameters.append(category)

    # Payment filter
    if payment_method:
        query += " AND payment_method = ?"
        parameters.append(payment_method)

    query += " ORDER BY date DESC, id DESC"

    cursor.execute(
        query,
        parameters
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses