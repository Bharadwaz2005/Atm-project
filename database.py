import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("atm_database.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                transaction_date TEXT NOT NULL,
                FOREIGN KEY(account_number) REFERENCES accounts(account_number)
            )
        """)
        self.connection.commit()

    def create_account(self, account_number, name, pin, balance):
        try:
            self.cursor.execute(
                "INSERT INTO accounts (account_number, name, pin, balance) VALUES (?, ?, ?, ?)",
                (account_number, name, pin, balance)
            )
            self.connection.commit()
            if balance > 0:
                self.add_transaction(account_number, "Initial Deposit", balance)
            return True
        except sqlite3.IntegrityError:
            return False

    def get_account(self, account_number):
        self.cursor.execute(
            "SELECT account_number, name, pin, balance FROM accounts WHERE account_number = ?",
            (account_number,)
        )
        return self.cursor.fetchone()

    def update_balance(self, account_number, balance):
        self.cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (balance, account_number)
        )
        self.connection.commit()

    def update_pin(self, account_number, new_pin):
        self.cursor.execute(
            "UPDATE accounts SET pin = ? WHERE account_number = ?",
            (new_pin, account_number)
        )
        self.connection.commit()

    def add_transaction(self, account_number, transaction_type, amount):
        transaction_date = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        self.cursor.execute(
            """INSERT INTO transactions
            (account_number, transaction_type, amount, transaction_date)
            VALUES (?, ?, ?, ?)""",
            (account_number, transaction_type, amount, transaction_date)
        )
        self.connection.commit()

    def get_transactions(self, account_number):
        self.cursor.execute(
            """SELECT transaction_type, amount, transaction_date
            FROM transactions
            WHERE account_number = ?
            ORDER BY id DESC LIMIT 5""",
            (account_number,)
        )
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
