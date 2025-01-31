"""
Configures static db access -> all the sql querys and stuff
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import datetime

from app.models.user import Admin, Treasurer, FinanceOfficer, UserType
from app.models.departement import Departement
from app.models.account import Account
from app.models.transaction import Transaction, Transfer
import sqlite3
import logging

logger = logging.getLogger("system_logger")


class DuplicateInsertException(Exception):
    """
    Is raised when a duplicate is inserted
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)


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
                return Treasurer.from_db(json_user)
            if user[3] == "FinanceOfficer":
                return FinanceOfficer.from_db(json_user)

        return None

    @staticmethod
    def get_free_treasurers():
        """
        Gets treasurers that do not have a department currently
        :return:
        """
        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, display_name, email, user_type, departement_id, password "
            "FROM USERS "
            "WHERE (departement_id = ? OR departement_id IS NULL)"
            "AND user_type = ?",
            (-1, "Treasurer"))
        users = cursor.fetchall()  # Fetches user
        conn.close()


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
        This is actually bad practice
        :return:
        """
        users = DBAccess.get_all_users()
        users.sort(key=lambda user: user.id, reverse=True)
        try:
            return users[0].id + 1
        except IndexError:
            return 0

    @staticmethod
    def get_next_departement_id():
        """
        Gets the next departement ID for user creation
        This is actually bad practice
        :return:
        """
        departements = DBAccess.get_all_departements()
        departements.sort(key=lambda departement: departement.id, reverse=True)
        try:
            return departements[0].id + 1
        except IndexError:
            return 0

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
            try:
                departement_id = user.get_departement().id
            except AttributeError:
                departement_id = DBAccess.get_next_departement_id()

        try:
            cursor.execute("""
                INSERT INTO USERS (display_name, email, password, user_type, departement_id) 
                VALUES (?, ?, ?, ?, ?)
            """, (display_name, email, password, user_type.value, departement_id))

            conn.commit()
            logger.info("User added successfully!")

        except sqlite3.IntegrityError as e:
            logger.info("Error:", e)  # Handle duplicate emails or constraints
            raise DuplicateInsertException(e)


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
        if account is None:
            # IF account doesnt exist, balance is 0
            account = Account(iD=departement.id, current_balance=0)

        DBAccess.save_account_to_db(account)  # we need to save the new account also
        try:
            cursor.execute("""INSERT INTO Departements (id, title) VALUES(?, ?)""",
                           (id, title))
            logger.info(f"created departement {title}")
        except sqlite3.IntegrityError as e:
            raise DuplicateInsertException("Duplicate Departement")
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
        DBAccess.modify_balance_by_transfer(account_id, amount)

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
        DBAccess.modify_balance_by_transfer(sender_account_id, sender_amount)
        DBAccess.modify_balance_by_transfer(receiving_account_id, receiver_amount)

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
                "date": datetime.datetime.strptime(transaction[2], "%Y-%m-%d %H:%M:%S.%f"),
                "receiving_account_id": transaction[3]
            }

            if trans_json["receiving_account_id"] == -1 or trans_json[
                "receiving_account_id"] is None:
                history.append(Transaction.from_DB(trans_json))
            else:
                history.append(Transfer.from_DB(trans_json))

        history.sort(key=lambda x: x.date, reverse=True)
        # sort newest to oldest
        return history

    @staticmethod
    def populate_db():
        """
        Populates Database with demo users, departements, etc
        :return:
        """

        planned_tables = ["USERS", "Departements", "Account", "Transactions"]

        conn = sqlite3.connect("club_finance_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        try:
            tables.remove(('sqlite_sequence',))
        except ValueError:
            pass

        received_tables = [table[0] for table in tables]
        planned_tables.sort()
        received_tables.sort()

        if planned_tables == received_tables:
            pass
        else:
            # create DB
            import app.db.database
            app.db.database.init_file()
            #
        conn.close()

        departement = Departement(id=1, title="Fußball")
        departement2 = Departement(id=2, title="Handball")
        departement3 = Departement(id=3, title="Volleyball")

        admin = Admin(id=1, display_name="Admin User", email="admin@email.de")
        treasurer = Treasurer(id=2, display_name="Treasurer User", email="treasurer@email.de",
                              departement_id=1)
        treasurer2 = Treasurer(id=3, display_name="Treasurer User2", email="treasurer2@email.de",
                               departement_id=2)
        treasurer3 = Treasurer(id=4, display_name="Treasurer User3", email="treasurer3@email.de",
                               departement_id=3)
        f_officer = FinanceOfficer(id=5, display_name="Finance Officer User",
                                   email="f.officer@email.de")

        password = "password"

        try:
            DBAccess.save_departement_to_db(departement)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.save_departement_to_db(departement2)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.save_departement_to_db(departement3)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.safe_user_to_db(admin, password, UserType.ADMIN)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.safe_user_to_db(treasurer, password, UserType.TREASURER)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.safe_user_to_db(treasurer2, password, UserType.TREASURER)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.safe_user_to_db(treasurer3, password, UserType.TREASURER)
        except DuplicateInsertException:
            pass
        try:
            DBAccess.safe_user_to_db(f_officer, password, UserType.FINANCE_OFFICER)
        except DuplicateInsertException:
            pass

        logger.info("Populated DB")
