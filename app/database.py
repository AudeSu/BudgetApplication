import sqlite3

with sqlite3.connect("../data/budget.db") as conn:
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


def create_test_user():
    try:
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

    except sqlite3.IntegrityError:
        print("Test user already exists.")


def close_database():
    conn.close()
