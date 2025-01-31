"""
Configures static db access -> all the sql querys and stuff
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import datetime

from app.models.user import Admin, Treasurer, FinanceOfficer, UserType
from app.models.departement import Departement
from app.models.account import Account
from app.models.transaction import Transaction, Transfer
from app.db import demo_items
import sqlite3
import logging

logger = logging.getLogger("system_logger")


class DBAccess:
    """
    Provides static DB access
    """

    def __init__(self):
        """
        Provides static DB access
        """
        pass

    @staticmethod
    def authenticate_user_from_db(email: str, password: str):
        """
        Gets a user from DB if email and password match
        :param email:
        :param password:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, display_name, email, user_type, departement_id, password FROM USERS WHERE email = ?",
            (email,))
        user = cursor.fetchone()  # Fetches user
        conn.close()

        if user and user[5] == password:

            json_user = {
                "id": user[0],
                "display_name": user[1],
                "email": user[2],
                "user_type": user[3],
                "departement_id": user[4] if user[4] is not None else -1,
            }

            if user[3] == "Admin":
                return Admin.from_db_json(json_user)
            if user[3] == "Treasurer":
                print(user[4])
                print("making treasurer")
                return Treasurer.from_db(json_user)
            if user[3] == "FinanceOfficer":
                return FinanceOfficer.from_db(json_user)

        return None

    @staticmethod
    def get_account_by_departement_id(departement_id: int):

        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, current_balance FROM Account WHERE id = ?", (departement_id,))
        account = cursor.fetchone()  # Fetches user
        conn.close()

        if account:
            return Account.from_db_tuple(account)
        return None

    @staticmethod
    def get_departement_by_id(departement_id: int):

        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM Departements WHERE id = ?",
                       (departement_id,))
        departement = cursor.fetchone()  # Fetches user

        conn.close()

        if departement:
            return Departement.from_db_tuple(departement)
        return None

    @staticmethod
    def get_all_users():
        """
        Gets all users from DB
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, display_name, email, user_type, departement_id FROM USERS", )
        users_db = cursor.fetchall()  # Fetches user
        conn.close()

        users = []
        for user in users_db:
            json_user = {
                "id": user[0],
                "display_name": user[1],
                "email": user[2],
                "user_type": user[3],
                "departement_id": user[4] if user[4] is not None else -1
            }
            if json_user["user_type"] == UserType.ADMIN.value:
                users.append(Admin.from_db_json(json_user))
            if json_user["user_type"] == UserType.FINANCE_OFFICER.value:
                users.append(FinanceOfficer.from_db(json_user))
            if json_user["user_type"] == UserType.TREASURER.value:
                users.append(Treasurer.from_db(json_user))
        return users

    @staticmethod
    def get_all_departements():
        """
        Gets all departements from DB
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM Departements")
        departement_db = cursor.fetchall()  # Fetches user
        conn.close()

        departements = []
        for departement in departement_db:
            departements.append(Departement.from_db_tuple(departement))

        return departements

    @staticmethod
    def get_next_user_id():
        """
        Gets the next user ID for user creation
        :return:
        """
        users = DBAccess.get_all_users()
        users.sort(key=lambda user: user.id, reverse=True)
        return users[0].id + 1

    @staticmethod
    def get_next_departement_id():
        departements = DBAccess.get_all_departements()
        departements.sort(key=lambda departement: departement.id, reverse=True)
        return departements[0].id + 1

    @staticmethod
    def safe_user_to_db(user, password: str, user_type: UserType):
        """
        Safes a user to db
        :param user:
        :param password:
        :param user_type:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()

        display_name = user.display_name
        email = user.email

        departement_id = None

        if user_type == UserType.TREASURER:
            departement_id = user.departement.id

        try:
            cursor.execute("""
                INSERT INTO USERS (display_name, email, password, user_type, departement_id) 
                VALUES (?, ?, ?, ?, ?)
            """, (display_name, email, password, user_type.value, departement_id))

            conn.commit()
            logger.info("User added successfully!")

        except sqlite3.IntegrityError as e:
            logger.error("Error:", e)  # Handle duplicate emails or constraints

        finally:
            conn.commit()
            conn.close()

    @staticmethod
    def save_account_to_db(account: Account):
        """
        Saves account to DB
        :param account:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()

        iD = account.iD
        current_balance = account.current_balance

        try:
            cursor.execute("""INSERT INTO Account (id, current_balance) VALUES(?, ?)""",
                           (iD, current_balance))
        except sqlite3.IntegrityError as e:
            logger.error(e)
        finally:
            conn.commit()
            conn.close()

    @staticmethod
    def save_departement_to_db(departement: Departement):
        """
        Saves a departement to DB
        :param departement:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()

        id = departement.id
        title = departement.title
        account = departement.account

        DBAccess.save_account_to_db(account)  # we need to save the new account also
        try:
            cursor.execute("""INSERT INTO Departements (id, title) VALUES(?, ?)""",
                           (id, title))
            logger.info(f"created departement {title}")
        except sqlite3.IntegrityError as e:
            logger.error(e)
        finally:
            conn.commit()
            conn.close()

    @staticmethod
    def export_current_status():
        """
        This is the structure of the export DICT:
         [
            {
                "filename": "departement_title.txt",
                "data": {
                    "current_balance": float(balance),
                    "transactions": [
                        transaction1,
                        transaction2,
                        ...
                    ]
                }
            }
        ]
        :return:
        """
        status = []
        for departement in DBAccess.get_all_departements():
            status.append(departement.export_current_status())
        return status

    @staticmethod
    def add_transaction_to_db(transaction):
        """
        Adds a transaction to the DB
        :param transaction:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()

        account_id = transaction.account_id
        amount = transaction.amount
        date = transaction.date
        receiving_account_id = None

        try:
            cursor.execute(
                """INSERT INTO Transactions (accountID, amount, date, receiving_account_id) VALUES(?, ?, ?, ?)""",
                (account_id, amount, date, receiving_account_id))
        except sqlite3.IntegrityError as e:
            logger.error(e)
        finally:
            conn.commit()
            conn.close()

    @staticmethod
    def modify_balance_by_transfer(account_id: int, amount: int):
        """
        When a transfer is done, the receiving account current balance needs to be updated
        Amount is + - the transfer amount
        :param account_id:
        :param amount:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()

        current_balance = DBAccess.get_account_by_departement_id(account_id).current_balance

        new_balance = current_balance + amount

        try:
            cursor.execute("""
                UPDATE Account 
                SET current_balance = ? 
                WHERE id = ?
            """, (new_balance, account_id))

            if cursor.rowcount == 0:
                logger.warning("Account not found!")
                raise KeyError("No Account with this ID found")
            else:
                logger.info("Balance updated successfully!")

            conn.commit()

        except sqlite3.Error as e:
            logger.error("Error updating balance:", e)

        finally:
            conn.close()

    @staticmethod
    def add_transfer_to_db(transfer):
        """
        Adds transfer to DB, once positive once negative to balance accounts
        This is so we only have to filter for account ID for history
        :param transfer:
        :return:
        """

        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()

        sender_account_id = transfer.account_id
        sender_amount = transfer.amount
        receiver_amount = - transfer.amount
        receiving_account_id = transfer.receiving_account_id

        try:
            cursor.execute(
                """INSERT INTO Transactions (accountID, amount, date, receiving_account_id) VALUES(?, ?, ?, ?)""",
                (sender_account_id, sender_amount, datetime.datetime.now(), receiving_account_id))
            cursor.execute(
                """INSERT INTO Transactions (accountID, amount, date, receiving_account_id) VALUES(?, ?, ?, ?)""",
                (
                    receiving_account_id, receiver_amount, datetime.datetime.now(),
                    sender_account_id))
        except sqlite3.IntegrityError as e:
            logger.error(e)
        finally:
            conn.commit()
            conn.close()

    @staticmethod
    def get_account_history(account_id: int):
        """
        Gets the history of an account
        :param account_id:
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT accountID, amount, date, receiving_account_id"
                       " FROM Transactions "
                       "WHERE accountID = ?", (account_id,))
        transactions = cursor.fetchall()  # Fetches user
        conn.close()

        history = []

        for transaction in transactions:

            trans_json = {
                "account_id": transaction[0],
                "amount": transaction[1],
                "date": datetime.datetime.strptime(transaction[2], "%Y-%m-%d %H:%M:%S"),
                "receiving_account_id": transaction[3]
            }

            if trans_json["receiving_account_id"] == -1 or trans_json[
                "receiving_account_id"] is None:
                history.append(Transaction.from_DB(trans_json))
            else:
                history.append(Transfer.from_DB(trans_json))

        return history


def get_history(accountID):
    return demo_items.transactions


def get_departements():
    return demo_items.generate_demo_departements(25)


def export_current_status() -> list[dict]:
    return [{}]


def get_next_departement_id():
    """
    Gets next dep ID for account creation and stuff
    :return:
    """
    return 5


def save_departement_to_db(departement):
    pass


def get_next_user_id():
    return 7


def save_user_to_db(user, password: str):
    pass


def get_all_finance_officers():
    officers = []
    for i in range(5):
        officers.append(FinanceOfficer(
            id=i,
            display_name=f"Officer {i}",
            email="email@email",
            departements=[]

        ))
    return officers


def get_all_users():
    return []


def get_all_departements():
    return demo_items.generate_demo_departements(20)
