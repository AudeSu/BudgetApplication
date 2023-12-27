import sqlite3
import menu
import csv
from database import cursor, conn


def register_user():
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username or email already in use. Please choose different username and/or email.")


def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        menu.logged_in_menu(user_id)
    else:
        print("Invalid username or password. Please try again.")


def get_total_income(user_id):
    try:
        cursor.execute("SELECT SUM(amount) FROM incomes WHERE user_id=?",
                       (user_id,))
        total_income = cursor.fetchone()[0]
        print(f"Total Income: {total_income if total_income else 0.0} EUR")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def get_total_expense(user_id):
    try:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?",
                       (user_id,))
        total_expense = cursor.fetchone()[0]
        print(f"Total Expense: {total_expense if total_expense else 0.0} EUR")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def get_total_expense_by_category(user_id):
    try:
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category",
                       (user_id,))
        expense_by_category = cursor.fetchall()

        print("Expense by Category:")
        print("{:<20} {:<15}".format("Category", "Amount (EUR)"))
        print("-" * 35)
        for category, amount in expense_by_category:
            print("{:<20} {:<15}".format(category, amount))
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def view_all_incomes(user_id):
    try:
        cursor.execute("SELECT id, amount, description FROM incomes WHERE user_id=?", (user_id,))
        all_incomes = cursor.fetchall()

        if not all_incomes:
            print("No incomes found.")
            return

        print("All Incomes:")
        print("{:<5} {:<15} {:<20}".format("ID", "Amount (EUR)", "Description"))
        print("-" * 70)
        for income_id, amount, description in all_incomes:
            print("{:<5} {:<15} {:<20}".format(income_id, amount, description))
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def view_all_expenses(user_id):
    try:
        cursor.execute("SELECT id, amount, category, description FROM expenses WHERE user_id=?", (user_id,))
        all_expenses = cursor.fetchall()

        if not all_expenses:
            print("No expenses found.")
            return

        print("All Expenses:")
        print("{:<5} {:<15} {:<20} {:<20}".format("ID", "Amount (EUR)", "Category", "Description"))
        print("-" * 70)
        for expense_id, amount, category, description in all_expenses:
            print("{:<5} {:<15} {:<20} {:<20}".format(expense_id, amount, category, description))
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def view_all_expenses_by_selected_category(user_id):
    try:
        cursor.execute("SELECT DISTINCT category FROM expenses WHERE user_id=?", (user_id,))
        categories = [category[0] for category in cursor.fetchall()]

        if not categories:
            print("No expense categories found.")
            return

        print("\nExpense Categories:")
        for category in categories:
            print(category)

        while True:
            selected_category = input("Enter the category to view expenses: ").title()
            if selected_category in categories:
                break
            else:
                print("Invalid category. Please choose a valid category.")

        cursor.execute("SELECT id, amount, description FROM expenses WHERE user_id=? AND category=?",
                       (user_id, selected_category))
        expenses_for_category = cursor.fetchall()

        if not expenses_for_category:
            print(f"No expenses found for category: {selected_category}")
            return

        print(f"\nExpenses for Category {selected_category}:")
        print("{:<5} {:<15} {:<20}".format("ID", "Amount (EUR)", "Description"))
        print("-" * 40)
        for expense_id, amount, description in expenses_for_category:
            print("{:<5} {:<15} {:<20}".format(expense_id, amount, description))
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def add_income(user_id):
    try:
        amount = float(input("Enter the income amount: "))
        description = input("Enter a description for the income: ")
        cursor.execute("INSERT INTO incomes (user_id, amount, description) VALUES (?, ?, ?)",
                       (user_id, amount, description))
        conn.commit()
        print("Income added successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def add_expense(user_id):
    try:
        amount = float(input("Enter the expense amount: "))

        valid_categories = ['Groceries', 'Electricity', 'Entertainment', 'Rent', 'Dining', 'Shopping',
                            'Transportation', 'Medical', 'Subscription', 'Other']

        print("Valid Categories:", ", ".join(valid_categories))

        while True:
            category = input("Enter the expense category: ").title()
            if category in valid_categories:
                break
            else:
                print("Invalid category. Please choose a valid category.")

        description = input("Enter a description for the expense: ")
        cursor.execute("INSERT INTO expenses (user_id, amount, category, description) VALUES (?, ?, ?, ?)",
                       (user_id, amount, category, description))
        conn.commit()
        print("Expense added successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def edit_income(user_id):
    try:
        view_all_incomes(user_id)
        income_id = input("Enter the ID of the income you want to edit: ")
        amount = float(input("Enter the new income amount: "))
        description = input("Enter a new description for the income: ")
        cursor.execute("UPDATE incomes SET amount=?, description=? WHERE id=?",
                       (amount, description, income_id))
        conn.commit()
        print(f"Income with ID {income_id} edited successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def edit_expense(user_id):
    try:
        view_all_expenses(user_id)
        expense_id = input("Enter the ID of the expense you want to edit: ")
        amount = float(input("Enter the expense amount: "))

        valid_categories = ['Groceries', 'Electricity', 'Entertainment', 'Rent', 'Dining', 'Shopping',
                            'Transportation', 'Medical', 'Subscription', 'Other']

        print("Valid Categories:", ", ".join(valid_categories))

        while True:
            category = input("Enter the expense category: ").title()
            if category in valid_categories:
                break
            else:
                print("Invalid category. Please choose a valid category.")

        description = input("Enter a description for the expense: ")
        cursor.execute("UPDATE expenses SET amount=?, category=?, description=? WHERE id=?",
                       (amount, category, description, expense_id))
        conn.commit()
        print(f"Expense with ID {expense_id} edited successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def delete_income(user_id):
    try:
        view_all_incomes(user_id)
        income_id = input("Enter the ID of the income you want to delete: ")
        cursor.execute("DELETE FROM incomes WHERE id=?",
                       (income_id,))
        conn.commit()
        print(f"Income with ID {income_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def delete_expense(user_id):
    try:
        view_all_expenses(user_id)
        expense_id = input("Enter the ID of the expense you want to delete: ")
        cursor.execute("DELETE FROM expenses WHERE id=?",
                       (expense_id,))
        conn.commit()
        print(f"Expense with ID {expense_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def export_data_to_csv(user_id):
    try:
        cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
        username = cursor.fetchone()[0]

        cursor.execute("SELECT id, amount, description FROM incomes WHERE user_id=?", (user_id,))
        incomes = cursor.fetchall()

        cursor.execute("SELECT id, amount, category, description FROM expenses WHERE user_id=?", (user_id,))
        expenses = cursor.fetchall()

        filename = f"{username}_budget_data.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)

            writer.writerow(["Income_ID", "Amount", "Description"])
            for income in incomes:
                writer.writerow(income)

            writer.writerow([])

            writer.writerow(["Expense_ID", "Amount", "Category", "Description"])
            for expense in expenses:
                writer.writerow(expense)

        print(f"Data is succesvol geëxporteerd naar {filename}.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
