"""
--> Class Transfer
-> basically helper class that gets stored with foreign keys in sender and receiver
-> sender(Account)
-> receiver(Account)
    -> amount
    -> datetime
    -> Authorizer -> User
"""

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
    def from_DB(cls, json: dict):
        iD = json.get("iD")
        current_balance = json.get("current_balance")
        return cls(iD, current_balance)

    @classmethod
    def from_user_input(cls, dep_id: int):
        return cls(dep_id, 0)

    def get_history(self):
        return db_access.get_history(self.iD)

    def get_formatted_balance(self):
        return '{:,.2f}€'.format(self.current_balance / 100)

    def withdraw(self, amount: int):
        """
        Withdraws funds from the account
        :param amount: Positive
        :return:
        """

        if amount > self.current_balance:
            raise OverdraftException("Not enough funds available")

        transaction = Transaction(accountID=self.iD,
                                  amount=-amount)  # Needs to be added as a negative amount
        transaction.add_to_db()
        self.current_balance = self.current_balance - amount

    def deposit(self, amount: int):
        """
        Deposits a specific amount to the account
        :param amount:
        :return:
        """
        transaction = Transaction(accountID=self.iD,
                                  amount=amount)  # Needs to be added as a negative amount
        transaction.add_to_db()
        self.current_balance = self.current_balance + amount

    def transfer(self, amount: int, receivingAccountID: int):
        """
        Transfers money out of the account into another account
        :param amount:
        :param receivingAccountID:
        :return:
        """

        if amount > self.current_balance:
            raise OverdraftException("Not enough funds available")

        transfer = Transfer(accountID=self.iD, amount=-amount,
                            receivingAccountID=receivingAccountID)
        transfer.add_to_db()
        self.current_balance = self.current_balance - amount
