import sqlite3
import main

conn = sqlite3.connect("../data/budget.db")
cursor = conn.cursor()


def create_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            description TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT CHECK(category IN ('Groceries', 'Electricity', 'Entertainment', 'Rent', 'Dining', 'Shopping', 
            'Transportation', 'Medical', 'Subscription', 'Other')),
            description TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
    """)


def create_test_user():  # TODO: als deze user al eens aangemaakt is hoeft deze niet meer aangemaakt te worden
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   ('testuser', 'test@example.com', 'testpassword'))
    conn.commit()

    cursor.execute("SELECT id FROM users WHERE username=?", ('testuser',))
    user_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO incomes (user_id, amount, description) VALUES (?, ?, ?)",
                   (user_id, 1000.0, 'Salary'))
    cursor.execute("INSERT INTO incomes (user_id, amount, description) VALUES (?, ?, ?)",
                   (user_id, 500.0, 'Bonus'))
    conn.commit()

    categories = ['Groceries', 'Electricity', 'Entertainment', 'Rent', 'Dining', 'Shopping',
                  'Transportation', 'Medical', 'Subscription', 'Other']

    for category in categories:
        cursor.execute("INSERT INTO expenses (user_id, amount, category, description) VALUES (?, ?, ?, ?)",
                       (user_id, 50.0, category, f'{category} expense'))
    conn.commit()

    print("Test user created with incomes and expenses.")


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
        main.logged_in_menu(user_id)
    else:
        print("Invalid username or password. Please try again.")


def get_total_income(user_id):
    cursor.execute("SELECT SUM(amount) FROM incomes WHERE user_id=?",
                   (user_id,))
    total_income = cursor.fetchone()[0]

    print("Total Income:", total_income if total_income else 0.0, "EUR")


def get_total_expense(user_id):
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?",
                   (user_id,))
    total_expense = cursor.fetchone()[0]
    print("Total Expense:", total_expense if total_expense else 0.0, "EUR")


def get_total_expense_by_category(
        user_id):  # TODO: zet dit nog in een mooie tabel, want momenteel zijn er rare inspringen
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category",
                   (user_id,))
    expense_by_category = cursor.fetchall()

    print("Expense by Category:")
    for category, amount in expense_by_category:
        print(f"\t> {category}: {amount} EUR")


def view_all_incomes(user_id):  # TODO: zet dit nog in een mooie tabel, want momenteel zijn er rare inspringen
    cursor.execute("SELECT id, amount, description FROM incomes WHERE user_id=?",
                   (user_id,))
    all_incomes = cursor.fetchall()

    if not all_incomes:
        print("No incomes found.")
        return

    print("All Incomes:")
    for income in all_incomes:
        income_id, amount, description = income
        print(f"{income_id}: {amount} EUR\t\tDescription: {description}")


def view_all_expenses(user_id):  # TODO: zet dit nog in een mooie tabel, want momenteel zijn er rare inspringen
    cursor.execute("SELECT id, amount, category, description FROM expenses WHERE user_id=?",
                   (user_id,))
    all_expenses = cursor.fetchall()

    if not all_expenses:
        print("No expenses found.")
        return

    print("All Expenses:")
    for expense in all_expenses:
        expense_id, amount, category, description = expense
        print(f"{expense_id}: {amount} EUR\t\tCategory: {category}\t\tDescription: {description}")


def view_all_expenses_by_selected_category(
        user_id):  # TODO: zet dit nog in een mooie tabel, want momenteel zijn er rare inspringen
    cursor.execute("SELECT DISTINCT category FROM expenses WHERE user_id=?", (user_id,))
    categories = [category[0] for category in cursor.fetchall()]

    if not categories:
        print("No expense categories found.")
        return

    print("Expense Categories:")
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

    print(f"Expenses for Category {selected_category}:")
    for expense_id, amount, description in expenses_for_category:
        print(f"{expense_id}: {amount} EUR\t\tDescription: {description}")


def add_income(user_id):
    amount = float(input("Enter the income amount: "))
    description = input("Enter a description for the income: ")
    cursor.execute("INSERT INTO incomes (user_id, amount, description) VALUES (?, ?, ?)",
                   (user_id, amount, description))
    conn.commit()
    print("Income added successfully!")


def add_expense(user_id):
    cursor.execute("SELECT DISTINCT category FROM expenses WHERE user_id=?", (user_id,))
    categories = [category[0] for category in cursor.fetchall()]

    amount = float(input("Enter the expense amount: "))

    print("Expense Categories:")
    for category in categories:
        print(category)

    while True:
        category = input("Enter the expense category: ").title()
        if category in categories:
            break
        else:
            print("Invalid category. Please choose a valid category.")

    description = input("Enter a description for the expense: ")
    cursor.execute("INSERT INTO expenses (user_id, amount, category, description) VALUES (?, ?, ?, ?)",
                   (user_id, amount, category, description))
    conn.commit()
    print("Expense added successfully!")


def edit_income(user_id):
    view_all_incomes(user_id)
    income_id = input("Enter the ID of the income you want to edit: ")
    amount = float(input("Enter the new income amount: "))
    description = input("Enter a new description for the income: ")
    cursor.execute("UPDATE incomes SET amount=?, description=? WHERE id=?",
                   (amount, description, income_id))
    conn.commit()
    print(f"Income with ID {income_id} edited successfully.")


def edit_expense(user_id):
    cursor.execute("SELECT DISTINCT category FROM expenses WHERE user_id=?", (user_id,))
    categories = [category[0] for category in cursor.fetchall()]

    view_all_expenses(user_id)
    expense_id = input("Enter the ID of the expense you want to edit: ")
    amount = float(input("Enter the expense amount: "))

    print("Expense Categories:")
    for category in categories:
        print(category)

    while True:
        category = input("Enter the expense category: ").title()
        if category in categories:
            break
        else:
            print("Invalid category. Please choose a valid category.")

    description = input("Enter a description for the expense: ")
    cursor.execute("UPDATE expenses SET amount=?, category=?, description=? WHERE id=?",
                   (amount, category, description, expense_id))
    conn.commit()
    print(f"Expense with ID {expense_id} edited successfully.")


def delete_income(user_id):
    view_all_incomes(user_id)
    income_id = input("Enter the ID of the income you want to delete: ")
    cursor.execute("DELETE FROM incomes WHERE id=?",
                   (income_id,))
    conn.commit()
    print(f"Income with ID {income_id} deleted successfully.")


def delete_expense(user_id):
    view_all_expenses(user_id)
    expense_id = input("Enter the ID of the expense you want to delete: ")
    cursor.execute("DELETE FROM expenses WHERE id=?",
                   (expense_id,))
    conn.commit()
    print(f"Expense with ID {expense_id} deleted successfully.")

#  TODO: Ik moet al de gegevens nog wegschrijven naar een extern bestand --> extra methode hiervoor schrijven
#  TODO: Output van methoden moet in een overzichtelijke table weergegeven worden ipv rare inspringen van "\t"
#  TODO: Clean code --> kuis de code op --> geen duplicate code meer
