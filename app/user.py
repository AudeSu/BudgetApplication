import sqlite3

from app import menu
from decouple import config
from database import cursor, conn, hash_password

DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY")


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def register(self):
        try:
            hashed_password = hash_password(self.password)
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (self.username, self.email, hashed_password))
            conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username or email already in use. Please choose a different username and/or email.")

    def login(self):
        try:
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                           (self.username, self.password))
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                menu.logged_in_menu(user_id)
            else:
                print("Invalid username or password. Please try again.")
        except sqlite3.IntegrityError as e:
            print(f"Database error: {e}")
