import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import add_expense, get_expenses, delete_expense
from visualizer import show_expense_bar_chart, show_expense_pie_chart

root = tk.Tk()
root.title("Ekorshi's Smart Expense Tracker")
root.geometry("700x620")

amount_var = tk.StringVar()
desc_var = tk.StringVar()
category_var = tk.StringVar()

CATEGORY_LIST = [
    "Food", "Travel", "Groceries", "Entertainment", "Shopping",
    "Rent", "Utilities", "Medical", "Miscellaneous"
]

# --- Header ---
tk.Label(root, text="Smart Expense Tracker", font=("Helvetica", 18, "bold"), fg="#2c3e50").pack(pady=10)

# --- Entry Fields ---
tk.Label(root, text="Amount:", font=("Arial", 12)).pack()
tk.Entry(root, textvariable=amount_var, font=("Arial", 12)).pack()

tk.Label(root, text="Category:", font=("Arial", 12)).pack()
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=CATEGORY_LIST, font=("Arial", 12), state="readonly")
category_dropdown.pack()
category_dropdown.current(0)

tk.Label(root, text="Description:", font=("Arial", 12)).pack()
tk.Entry(root, textvariable=desc_var, font=("Arial", 12)).pack()

# --- Add Expense ---
def on_add():
    try:
        amt = float(amount_var.get())
        desc = desc_var.get().strip()
        cat = category_var.get()
        if not desc:
            raise ValueError("Description is empty")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_expense(amt, cat, desc, now)
        messagebox.showinfo("Success", "Expense Added!")
        refresh_table()
        amount_var.set('')
        desc_var.set('')
        category_dropdown.current(0)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

tk.Button(root, text="Add Expense", command=on_add, bg="#2ecc71", fg="white", font=("Arial", 12)).pack(pady=10)

# --- Table ---
tree = ttk.Treeview(root, columns=("ID", "Amount", "Category", "Description", "Date"), show='headings')
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.column("ID", width=50)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in get_expenses():
        tree.insert("", "end", values=row)

# --- Delete Expense ---
def on_delete():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an expense to delete.")
        return
    item = tree.item(selected)
    expense_id = item["values"][0]
    delete_expense(expense_id)
    messagebox.showinfo("Deleted", "Expense deleted successfully.")
    refresh_table()

tk.Button(root, text="Delete Selected Expense", command=on_delete, bg="#e74c3c", fg="white", font=("Arial", 12)).pack(pady=5)

# --- Visualization Buttons ---
tk.Button(root, text="Bar Chart", command=show_expense_bar_chart, bg="#3498db", fg="white", font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Pie Chart", command=show_expense_pie_chart, bg="#9b59b6", fg="white", font=("Arial", 12)).pack(pady=5)

refresh_table()
root.mainloop()
