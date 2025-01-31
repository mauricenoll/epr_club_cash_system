"""
Initializes DB for club system
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import sqlite3

connection = sqlite3.connect("club_finance_system.db")
cursor = connection.cursor()


def init_file():
    """
    The function is here so git won't optimize the import
    :return:
    """
    pass


# create user table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        display_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        user_type TEXT CHECK( user_type IN ('Admin', 'Treasurer', 'FinanceOfficer', 'User') ) NOT NULL,
        departement_id INTEGER,
        FOREIGN KEY (departement_id) REFERENCES Departements(id) ON DELETE SET NULL
    )
""")

# Create Departements table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Departements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL
    )
""")

# Create Account table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account (
        id INTEGER PRIMARY KEY,
        current_balance INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (id) REFERENCES Departements(id) ON DELETE CASCADE
    )
""")

# Create Transactions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        accountID INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        receiving_account_id INTEGER,
        FOREIGN KEY (accountID) REFERENCES Account(id) ON DELETE CASCADE,
        FOREIGN KEY (receiving_account_id) REFERENCES Account(id) ON DELETE SET NULL
    )
""")


# Commit changes and close connection
connection.commit()
connection.close()
