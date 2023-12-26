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


def register_user():
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
    conn.commit()
    print("User registered successfully!\n")


def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    user = cursor.fetchone()
    if user:
        user_id = user[0]  # Wat wordt er met dit lijntje code gedaan? die nul hangt toch af van wie er ingelogd is? moet dat ni "id" zijn uit de user tabel?
        main.logged_in_menu(user_id)
    else:
        print("Invalid username or password. Please try again.")


def get_income_overview(user_id):
    cursor.execute("SELECT SUM(amount) FROM incomes WHERE user_id=?",
                   (user_id,))
    total_income = cursor.fetchone()[0]

    print("Total Income:", total_income if total_income else 0.0)


def get_expense_overview(user_id):
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?",
                   (user_id,))
    total_expense = cursor.fetchone()[0]
    print("Total Expense:", total_expense if total_expense else 0.0)


def get_expense_by_category(user_id):
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category",
                   (user_id,))
    expense_by_category = cursor.fetchall()
    return expense_by_category


def add_income(user_id, amount, description):
    cursor.execute("INSERT INTO incomes (user_id, amount, description) VALUES (?, ?, ?)",
                   (user_id, amount, description))
    conn.commit()


def add_expense(user_id, amount, category, description):
    cursor.execute("INSERT INTO expenses (user_id, amount, category, description) VALUES (?, ?, ?, ?)",
                   (user_id, amount, category, description))
    conn.commit()


def delete_income(income_id):
    cursor.execute("DELETE FROM incomes WHERE id=?",
                   (income_id,))
    conn.commit()


def delete_expense(expense_id):
    cursor.execute("DELETE FROM expenses WHERE id=?",
                   (expense_id,))
    conn.commit()


def edit_income(income_id, amount, description):
    cursor.execute("UPDATE incomes SET amount=?, description=? WHERE id=?",
                   (amount, description, income_id))
    conn.commit()


def edit_expense(expense_id, amount, category, description):
    cursor.execute("UPDATE expenses SET amount=?, category=?, description=? WHERE id=?",
                   (amount, category, description, expense_id))
    conn.commit()


def get_all_incomes(user_id):
    cursor.execute("SELECT * FROM incomes WHERE user_id=?", (user_id,))
    return cursor.fetchall()


def get_all_expenses(user_id):
    cursor.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,))
    return cursor.fetchall()


def get_all_expenses_category(user_id):
    cursor.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,))
    return cursor.fetchall()


def get_expenses_for_category(user_id, category):
    cursor.execute("SELECT * FROM expenses WHERE user_id=? AND category=?", (user_id, category))
    return cursor.fetchall()