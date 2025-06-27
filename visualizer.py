import matplotlib.pyplot as plt
from collections import defaultdict
from database import get_expenses, get_expenses_by_category

def show_expense_bar_chart():
    expenses = get_expenses()
    category_totals = defaultdict(float)
    for row in expenses:
        try:
            amount = float(row[1])
            category = row[2]
            category_totals[category] += amount
        except:
            continue

    categories = list(category_totals.keys())
    values = list(category_totals.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(categories, values, color='skyblue')
    ax.set_title("Spending by Category (Bar Chart)")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Spent")
    plt.tight_layout()

    def on_click(event):
        for bar, cat in zip(bars, categories):
            if bar.contains(event)[0]:
                show_category_details_pie(cat)
                break

    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()

def show_expense_pie_chart():
    expenses = get_expenses()
    category_totals = defaultdict(float)
    for row in expenses:
        try:
            amount = float(row[1])
            category = row[2]
            category_totals[category] += amount
        except:
            continue

    categories = list(category_totals.keys())
    values = list(category_totals.values())

    fig, ax = plt.subplots()
    wedges, _, autotexts = ax.pie(
        values,
        labels=categories,
        autopct='%1.1f%%',
        startangle=140
    )
    ax.set_title("Spending by Category (Pie Chart)")
    plt.tight_layout()

    def on_click(event):
        for i, wedge in enumerate(wedges):
            if wedge.contains(event)[0]:
                show_category_details_pie(categories[i])
                break

    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()

def show_category_details_pie(category):
    data = get_expenses_by_category(category)
    if not data:
        return

    item_totals = defaultdict(float)
    for row in data:
        try:
            desc = row[3]
            amount = float(row[1])
            item_totals[desc] += amount
        except:
            continue

    labels = list(item_totals.keys())
    values = list(item_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f"{category} Breakdown by Description")
    plt.tight_layout()
    plt.show()
