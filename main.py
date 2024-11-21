import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Global variables
transactions = []  # To store transaction data

# File for storing data
data_file = "finance_data.csv"

# Load existing data from CSV
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        transactions = list(reader)


# Save data to CSV
def save_data():
    with open(data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount"])
        writer.writerows(transactions)


# Add a transaction
def add_transaction():
    date = date_entry.get()
    category = category_var.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if not (date and category and description and amount):
        messagebox.showerror("Error", "All fields must be filled!")
        return

    try:
        amount = float(amount)
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date or amount format!")
        return

    transactions.append([date, category, description, amount])
    save_data()
    refresh_transactions()
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


# Refresh transaction list
def refresh_transactions():
    transaction_list.delete(0, tk.END)
    for transaction in transactions:
        date, category, description, amount = transaction
        transaction_list.insert(tk.END, f"{date} | {category} | {description} | ${amount}")


# Display spending chart
def display_chart():
    categories = {}
    for transaction in transactions:
        _, category, _, amount = transaction
        amount = float(amount)
        categories[category] = categories.get(category, 0) + amount

    if not categories:
        messagebox.showerror("Error", "No data to display!")
        return

    labels = categories.keys()
    values = categories.values()

    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Spending by Category")
    plt.show()


# GUI setup
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("700x500")

# Input fields
tk.Label(root, text="Date (yyyy-mm-dd):").grid(row=0, column=0, padx=10, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
category_var = tk.StringVar(value="Food")
categories = ["Food", "Rent", "Entertainment", "Utilities", "Other"]
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Add Transaction", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=10)

# Transaction list
tk.Label(root, text="Transactions:").grid(row=5, column=0, columnspan=2, pady=5)
transaction_list = tk.Listbox(root, width=70, height=10)
transaction_list.grid(row=6, column=1, columnspan=2, pady=4)

# Display chart button
tk.Button(root, text="Show Spending Chart", command=display_chart).grid(row=7, column=0, columnspan=2, pady=10)

# Populate transaction list
refresh_transactions()

# Start the GUI
root.mainloop()
