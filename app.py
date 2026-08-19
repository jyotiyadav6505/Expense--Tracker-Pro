import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import csv

import ttkbootstrap as tb
import matplotlib.pyplot as plt

from database import create_database
from expenses import (
    add_expense,
    get_expenses,
    delete_expense,
    update_expense,
    get_expense_summary,
    get_category_summary,
    get_monthly_summary,
    export_expenses,
    search_expenses
)


# ============================================================
# DATABASE
# ============================================================

create_database()


# ============================================================
# FUNCTIONS
# ============================================================

def refresh_dashboard():

    total_transactions, total_amount, average_amount, highest_amount = (
        get_expense_summary()
    )

    total_expenses_label.config(
        text=f"₹{total_amount:.2f}"
    )

    transactions_label.config(
        text=str(total_transactions)
    )

    average_label.config(
        text=f"₹{average_amount:.2f}"
    )

    highest_label.config(
        text=f"₹{highest_amount:.2f}"
    )


def display_expenses(expenses):

    for item in expense_table.get_children():
        expense_table.delete(item)

    for expense in expenses:

        expense_id, expense_date, category, description, amount, payment_method = expense

        expense_table.insert(
            "",
            tk.END,
            values=(
                expense_id,
                expense_date,
                category,
                description,
                f"₹{amount:.2f}",
                payment_method
            )
        )


def refresh_expenses():

    expenses = get_expenses()

    display_expenses(expenses)

    refresh_dashboard()


def clear_fields():

    date_entry.delete(0, tk.END)

    date_entry.insert(
        0,
        date.today().strftime("%Y-%m-%d")
    )

    category_entry.set("")

    description_entry.delete(0, tk.END)

    amount_entry.delete(0, tk.END)

    payment_entry.set("")


# ============================================================
# ADD EXPENSE
# ============================================================

def add_new_expense():

    expense_date = date_entry.get().strip()
    category = category_entry.get().strip()
    description = description_entry.get().strip()
    amount = amount_entry.get().strip()
    payment_method = payment_entry.get().strip()

    if not expense_date or not category or not amount or not payment_method:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all required fields."
        )

        return

    try:

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )

        return

    try:

        add_expense(
            expense_date,
            category,
            description,
            amount,
            payment_method
        )

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

        clear_fields()

        refresh_expenses()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )


# ============================================================
# DELETE EXPENSE
# ============================================================

def delete_selected_expense():

    selected = expense_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to delete."
        )

        return

    item = expense_table.item(
        selected[0]
    )

    expense_id = item["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this expense?"
    )

    if confirm:

        delete_expense(
            expense_id
        )

        refresh_expenses()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully!"
        )


# ============================================================
# EDIT EXPENSE
# ============================================================

def edit_selected_expense():

    selected = expense_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to edit."
        )

        return

    item = expense_table.item(
        selected[0]
    )

    values = item["values"]

    expense_id = values[0]

    date_entry.delete(
        0,
        tk.END
    )

    date_entry.insert(
        0,
        values[1]
    )

    category_entry.set(
        values[2]
    )

    description_entry.delete(
        0,
        tk.END
    )

    description_entry.insert(
        0,
        values[3]
    )

    amount_entry.delete(
        0,
        tk.END
    )

    amount_entry.insert(
        0,
        str(values[4]).replace("₹", "")
    )

    payment_entry.set(
        values[5]
    )

    add_button.config(
        text="✏️ Update Expense",
        command=lambda: update_selected_expense(
            expense_id
        )
    )


# ============================================================
# UPDATE EXPENSE
# ============================================================

def update_selected_expense(expense_id):

    expense_date = date_entry.get().strip()
    category = category_entry.get().strip()
    description = description_entry.get().strip()
    amount = amount_entry.get().strip()
    payment_method = payment_entry.get().strip()

    if not expense_date or not category or not amount or not payment_method:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all required fields."
        )

        return

    try:

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )

        return

    try:

        update_expense(
            expense_id,
            expense_date,
            category,
            description,
            amount,
            payment_method
        )

        messagebox.showinfo(
            "Success",
            "Expense updated successfully!"
        )

        clear_fields()

        add_button.config(
            text="➕ Add Expense",
            command=add_new_expense
        )

        refresh_expenses()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )


# ============================================================
# SEARCH & FILTER
# ============================================================

def apply_filters():

    search_text = search_entry.get().strip()

    selected_category = filter_category_entry.get().strip()

    selected_payment = filter_payment_entry.get().strip()

    expenses = search_expenses(
        search_text=search_text,
        category=selected_category,
        payment_method=selected_payment
    )

    display_expenses(
        expenses
    )


def clear_filters():

    search_entry.delete(
        0,
        tk.END
    )

    filter_category_entry.set("")

    filter_payment_entry.set("")

    refresh_expenses()


# ============================================================
# CATEGORY CHART
# ============================================================

def show_category_chart():

    category_data = get_category_summary()

    if not category_data:

        messagebox.showinfo(
            "No Data",
            "There are no expenses available to create a chart."
        )

        return

    categories = [
        item[0]
        for item in category_data
    ]

    amounts = [
        item[1]
        for item in category_data
    ]

    plt.figure(
        figsize=(8, 5)
    )

    plt.bar(
        categories,
        amounts
    )

    plt.title(
        "Expenses by Category"
    )

    plt.xlabel(
        "Category"
    )

    plt.ylabel(
        "Amount (₹)"
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MONTHLY CHART
# ============================================================

def show_monthly_chart():

    monthly_data = get_monthly_summary()

    if not monthly_data:

        messagebox.showinfo(
            "No Data",
            "There are no expenses available to create a chart."
        )

        return

    months = [
        item[0]
        for item in monthly_data
    ]

    amounts = [
        item[1]
        for item in monthly_data
    ]

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        months,
        amounts,
        marker="o"
    )

    plt.title(
        "Monthly Expenses"
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Amount (₹)"
    )

    plt.xticks(
        rotation=30
    )

    plt.grid(
        True
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# EXPORT CSV
# ============================================================

def export_to_csv():

    expenses = export_expenses()

    if not expenses:

        messagebox.showinfo(
            "No Data",
            "There are no expenses available to export."
        )

        return

    file_path = filedialog.asksaveasfilename(
        title="Save Expense Report",
        defaultextension=".csv",
        filetypes=[
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ],
        initialfile="expense_report.csv"
    )

    if not file_path:
        return

    try:

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "ID",
                "Date",
                "Category",
                "Description",
                "Amount",
                "Payment Method"
            ])

            writer.writerows(
                expenses
            )

        messagebox.showinfo(
            "Export Successful",
            "Expense report exported successfully!"
        )

    except Exception as error:

        messagebox.showerror(
            "Export Error",
            f"Could not export expenses:\n{error}"
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tb.Window(
    themename="darkly"
)

root.title(
    "Expense Tracker Pro"
)

root.geometry(
    "1200x850"
)

root.minsize(
    1000,
    700
)


# ============================================================
# HEADER
# ============================================================

header = ttk.Frame(
    root
)

header.pack(
    fill="x",
    padx=25,
    pady=(20, 10)
)


title_label = ttk.Label(
    header,
    text="💰 Expense Tracker Pro",
    font=("Arial", 28, "bold")
)

title_label.pack(
    side="left"
)


subtitle_label = ttk.Label(
    header,
    text="Smart Personal Expense Management",
    font=("Arial", 11)
)

subtitle_label.pack(
    side="right",
    pady=10
)


# ============================================================
# DASHBOARD
# ============================================================

dashboard_frame = ttk.LabelFrame(
    root,
    text="  📊 Expense Overview  ",
    padding=15
)

dashboard_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


# Total Expenses

total_card = ttk.Frame(
    dashboard_frame,
    padding=10
)

total_card.grid(
    row=0,
    column=0,
    padx=20
)

ttk.Label(
    total_card,
    text="💰 Total Expenses",
    font=("Arial", 11, "bold")
).pack()


total_expenses_label = ttk.Label(
    total_card,
    text="₹0.00",
    font=("Arial", 20, "bold")
)

total_expenses_label.pack(
    pady=5
)


# Transactions

transaction_card = ttk.Frame(
    dashboard_frame,
    padding=10
)

transaction_card.grid(
    row=0,
    column=1,
    padx=20
)

ttk.Label(
    transaction_card,
    text="🧾 Transactions",
    font=("Arial", 11, "bold")
).pack()


transactions_label = ttk.Label(
    transaction_card,
    text="0",
    font=("Arial", 20, "bold")
)

transactions_label.pack(
    pady=5
)


# Average

average_card = ttk.Frame(
    dashboard_frame,
    padding=10
)

average_card.grid(
    row=0,
    column=2,
    padx=20
)

ttk.Label(
    average_card,
    text="📈 Average Expense",
    font=("Arial", 11, "bold")
).pack()


average_label = ttk.Label(
    average_card,
    text="₹0.00",
    font=("Arial", 20, "bold")
)

average_label.pack(
    pady=5
)


# Highest

highest_card = ttk.Frame(
    dashboard_frame,
    padding=10
)

highest_card.grid(
    row=0,
    column=3,
    padx=20
)

ttk.Label(
    highest_card,
    text="🔝 Highest Expense",
    font=("Arial", 11, "bold")
).pack()


highest_label = ttk.Label(
    highest_card,
    text="₹0.00",
    font=("Arial", 20, "bold")
)

highest_label.pack(
    pady=5
)


# ============================================================
# SEARCH & FILTER
# ============================================================

filter_frame = ttk.LabelFrame(
    root,
    text="  🔎 Search & Filter  ",
    padding=15
)

filter_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


ttk.Label(
    filter_frame,
    text="Search:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


search_entry = ttk.Entry(
    filter_frame,
    width=25
)

search_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    filter_frame,
    text="Category:"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


filter_category_entry = ttk.Combobox(
    filter_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Education",
        "Health",
        "Other"
    ],
    width=17,
    state="readonly"
)

filter_category_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


ttk.Label(
    filter_frame,
    text="Payment:"
).grid(
    row=0,
    column=4,
    padx=5,
    pady=5
)


filter_payment_entry = ttk.Combobox(
    filter_frame,
    values=[
        "Cash",
        "UPI",
        "Card",
        "Net Banking",
        "Other"
    ],
    width=17,
    state="readonly"
)

filter_payment_entry.grid(
    row=0,
    column=5,
    padx=5,
    pady=5
)


# IMPORTANT:
# These are tb.Button, not ttk.Button.

tb.Button(
    filter_frame,
    text="🔎 Search",
    bootstyle="primary",
    command=apply_filters
).grid(
    row=0,
    column=6,
    padx=5
)


tb.Button(
    filter_frame,
    text="✖ Clear",
    bootstyle="secondary",
    command=clear_filters
).grid(
    row=0,
    column=7,
    padx=5
)


# ============================================================
# ADD / EDIT EXPENSE
# ============================================================

input_frame = ttk.LabelFrame(
    root,
    text="  ➕ Add / Edit Expense  ",
    padding=15
)

input_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


# Date

ttk.Label(
    input_frame,
    text="Date:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


date_entry = ttk.Entry(
    input_frame,
    width=18
)

date_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

date_entry.insert(
    0,
    date.today().strftime("%Y-%m-%d")
)


# Category

ttk.Label(
    input_frame,
    text="Category:"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


category_entry = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Education",
        "Health",
        "Other"
    ],
    width=16,
    state="readonly"
)

category_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# Description

ttk.Label(
    input_frame,
    text="Description:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


description_entry = ttk.Entry(
    input_frame,
    width=18
)

description_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# Amount

ttk.Label(
    input_frame,
    text="Amount:"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)


amount_entry = ttk.Entry(
    input_frame,
    width=18
)

amount_entry.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)


# Payment

ttk.Label(
    input_frame,
    text="Payment:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)


payment_entry = ttk.Combobox(
    input_frame,
    values=[
        "Cash",
        "UPI",
        "Card",
        "Net Banking",
        "Other"
    ],
    width=16,
    state="readonly"
)

payment_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


# Add Button

add_button = tb.Button(
    input_frame,
    text="➕ Add Expense",
    bootstyle="success",
    command=add_new_expense
)

add_button.grid(
    row=2,
    column=3,
    padx=5,
    pady=10
)


# ============================================================
# EXPENSE TABLE
# ============================================================

table_frame = ttk.LabelFrame(
    root,
    text="  📋 Expense Records  ",
    padding=10
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


columns = (
    "ID",
    "Date",
    "Category",
    "Description",
    "Amount",
    "Payment"
)


expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:

    expense_table.heading(
        column,
        text=column
    )

    expense_table.column(
        column,
        width=150,
        anchor="center"
    )


expense_table.pack(
    fill="both",
    expand=True
)


# ============================================================
# ACTION BUTTONS
# ============================================================

button_frame = ttk.Frame(
    root
)

button_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


tb.Button(
    button_frame,
    text="✏️ Edit Selected",
    bootstyle="warning",
    command=edit_selected_expense
).pack(
    side="left",
    padx=5
)


tb.Button(
    button_frame,
    text="🗑️ Delete Selected",
    bootstyle="danger",
    command=delete_selected_expense
).pack(
    side="left",
    padx=5
)


tb.Button(
    button_frame,
    text="🔄 Refresh",
    bootstyle="secondary",
    command=refresh_expenses
).pack(
    side="left",
    padx=5
)


tb.Button(
    button_frame,
    text="📊 Category Chart",
    bootstyle="info",
    command=show_category_chart
).pack(
    side="left",
    padx=5
)


tb.Button(
    button_frame,
    text="📅 Monthly Chart",
    bootstyle="info",
    command=show_monthly_chart
).pack(
    side="left",
    padx=5
)


tb.Button(
    button_frame,
    text="📤 Export CSV",
    bootstyle="success",
    command=export_to_csv
).pack(
    side="right",
    padx=5
)


# ============================================================
# LOAD DATA
# ============================================================

refresh_expenses()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()