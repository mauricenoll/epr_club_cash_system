from app.models.account import Account
from app.db import db_access


class Departement:

    def __init__(self, id: int, title: str, account: Account):
        self.id = id
        self.title = title
        self.account = account

    @classmethod
    def from_user_input(cls, title: str):
        """
        Creates a departement from User input
        :param title:
        :return:
        """
        iD = db_access.get_next_departement_id()
        departement = cls(iD, title, Account.from_user_input(iD))
        departement.__to_database()
        return departement

    def __to_database(self):
        db_access.save_departement_to_db(self)

    def get_balance_overview(self):
        return self.account.get_formatted_balance()

    def __str__(self):
        return self.title
