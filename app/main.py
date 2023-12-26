import sqlite3

conn = sqlite3.connect("../data/budget.db")
cursor = conn.cursor()

#create 3 tabellen: users, incomes, expenses
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
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
        category TEXT CHECK(category IN ('Groceries', 'Electricity', 'Entertainment', 'Rent', 'Dining', 'Shopping', 'Transportation', 'Medical', 'Subscription', 'Other')),
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(id)
    )
""")

conn.close()
