"""
Defines departement class
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.models.account import Account
from app.db import db_access


class Departement:
    """
    Departement class
    """

    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title
        self.account = None

    def __str__(self):
        return self.title

    @classmethod
    def from_db_json(cls, json: dict):
        """
        Gets departement from JSON
        :param json:
        :return:
        """
        id = json.get("id")
        title = json.get("title")
        account = db_access.DBAccess.get_account_by_departement_id(id)
        cls.account = account
        return cls(id, title)

    @classmethod
    def from_db_tuple(cls, db_tuple: tuple):
        """
        Gets Departement from DB Tuple
        :param db_tuple:
        :return:
        """
        id = db_tuple[0]
        title = db_tuple[1]
        account = db_access.DBAccess.get_account_by_departement_id(id)
        cls.account = account
        return cls(id, title)

    @classmethod
    def from_user_input(cls, title: str):
        """
        Creates a departement from User input
        :param title:
        :return:
        """
        iD = db_access.DBAccess.get_next_departement_id()
        Account.from_user_input(iD)
        departement = cls(iD, title, )
        departement.__to_database()
        return departement

    def get_account(self):
        """
        Gets account from account ID
        :return:
        """
        if self.account is None:
            self.account = db_access.DBAccess.get_account_by_departement_id(self.id)
        return self.account

    def __to_database(self):
        """
        Saves Departement to DB
        :return:
        """
        db_access.DBAccess.save_departement_to_db(self)

    def export_current_status(self):
        """
        Exports current departement Status.
        For formatting see DBAccess.export_current_status()
        :return:
        """
        filename = f"{self.title}.txt"
        current_balance = self.get_account().current_balance
        transactions = self.get_account().get_history()
        transactions.sort(key=lambda transaction: transaction.date, reverse=True)

        return {
            "filename": filename,
            "data": {
                "current_balance": round(current_balance / 100, 2),
                "transactions": transactions
            }
        }

    def get_balance_overview(self):
        return self.get_account().get_formatted_balance()
