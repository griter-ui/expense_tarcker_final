import csv
import os

FILE_NAME = "expenses.csv"

def get_next_id():
    if not os.path.exists(FILE_NAME):
        return 1
    with open(FILE_NAME, 'r') as f:
        rows = list(csv.reader(f))
        if not rows:
            return 1
        return int(rows[-1][0]) + 1

def add_expense(amount, category, description, date):
    expense_id = get_next_id()
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([expense_id, amount, category, description, date])

def get_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f:
        return list(csv.reader(f))

def delete_expense(expense_id):
    if not os.path.exists(FILE_NAME):
        return
    with open(FILE_NAME, 'r') as f:
        rows = [row for row in csv.reader(f) if row[0] != str(expense_id)]
    with open(FILE_NAME, 'w', newline='') as f:
        csv.writer(f).writerows(rows)

def get_expenses_by_category(category):
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f:
        return [row for row in csv.reader(f) if row[2] == category]
