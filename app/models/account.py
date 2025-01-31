"""
Defines Account class for Club System
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.models.transaction import Transaction, Transfer
from app.db import db_access


class OverdraftException(Exception):
    """
    Is thrown when account would go into negative
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class Account:
    """
    We calculate the balance as cents since with floats sometimes float errors can occur.
    We don't do history as a property, so we don't have to carry around as many bulky objects

    """

    def __init__(self, iD: int, current_balance: int):
        self.iD = iD
        self.current_balance = current_balance

    @classmethod
    def from_db_json(cls, json: dict):
        """
        JSON -> Account
        :param json:
        :return:
        """
        iD = json.get("iD")
        current_balance = json.get("current_balance")
        return cls(iD, current_balance)

    @classmethod
    def from_db_tuple(cls, db_tuple: tuple):
        """
        id=0
        current_balance=1
        :param db_tuple:
        :return:
        """
        return cls(db_tuple[0], db_tuple[1])

    @classmethod
    def from_user_input(cls, dep_id: int):
        """
        Creates an account from User input
        :param dep_id:
        :return:
        """
        return cls(dep_id, 0)

    def get_history(self):
        """
        Gets the account history from DB
        :return:
        """
        return db_access.DBAccess.get_account_history(self.iD)

    def get_formatted_balance(self):
        """
        Formats Int to readable currency
        :return:
        """
        return '{:,.2f}€'.format(self.current_balance / 100)

    def withdraw(self, amount: int):
        """
        Withdraws funds from the account
        :param amount: Positive
        :return:
        """

        if amount > self.current_balance:
            raise OverdraftException("Not enough funds available")

        transaction = Transaction(account_id=self.iD,
                                  amount=-amount)  # Needs to be added as a negative amount
        transaction.add_to_db()
        self.current_balance = self.current_balance - amount

    def deposit(self, amount: int):
        """
        Deposits a specific amount to the account
        :param amount:
        :return:
        """
        transaction = Transaction(account_id=self.iD,
                                  amount=amount)  # Needs to be added as a negative amount
        transaction.add_to_db()
        self.current_balance = self.current_balance + amount

    def transfer(self, amount: int, receiving_account_id: int):
        """
        Transfers money out of the account into another account
        :param amount:
        :param receiving_account_id:
        :return:
        """

        if amount > self.current_balance:
            raise OverdraftException("Not enough funds available")

        transfer = Transfer(account_id=self.iD, amount=-amount,
                            receiving_account_id=receiving_account_id)
        transfer.add_to_db()
        self.current_balance = self.current_balance - amount
