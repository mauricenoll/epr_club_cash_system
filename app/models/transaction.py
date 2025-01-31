"""
Defines Transaction and Transfer class
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from datetime import datetime
from app.db import db_access
import logging

logger = logging.getLogger("system_logger")

class Transaction:
    """
    This is for Withdrawal and Deposit, this is basically a helper class for history
    """

    def __init__(self, account_id: int, amount: int, date: datetime | None = datetime.now()):
        """
        Initializes a Transaction
        :param account_id:
        :param amount:
        :param date:
        """
        self.account_id = account_id
        self.amount = amount
        self.date = date  # transaction time is current time

    @classmethod
    def from_DB(cls, json: dict):
        """
        JSON -> Transaction
        :param json:
        :return:
        """
        account_id = json.get("account_id")
        amount = json.get("amount")
        date = json.get("date")
        return cls(account_id, amount, date)

    def add_to_db(self):
        """
        Adds a transaction to DB
        :return:
        """
        logger.debug("Adding transaction to DB")
        db_access.DBAccess.add_transaction_to_db(self)

    def __str__(self):
        """
        String
        :return:
        """
        if self.amount > 0:
            return f"{self.date.strftime('%d.%m.%Y %H:%M')} - Deposit  {'{:,.2f}€'.format(self.amount / 100)}"
        return f"{self.date.strftime('%d.%m.%Y %H:%M')} - Withdrawal  {'{:,.2f}€'.format(self.amount / 100)}"


class Transfer(Transaction):
    """
    Amount is negative if we send
    Amount is positive if we receive
    """

    def __init__(self, account_id: int, amount: int, receiving_account_id: int, date: None = datetime.now()):
        """
        Initializes a Transfer
        :param account_id:
        :param amount:
        :param receiving_account_id:
        :param date:
        """
        super().__init__(account_id, amount, date)
        self.receiving_account_id = receiving_account_id

    @classmethod
    def from_DB(cls, json: dict):
        """
        JSON -> Transfer
        :param json:
        :return:
        """
        account_id = json.get("account_id")
        amount = json.get("amount")
        date = json.get("date")
        receiving_account_id = json.get("receiving_account_id")
        return cls(account_id, amount, receiving_account_id, date)

    def __str__(self):
        """
        String
        :return:
        """
        if self.amount > 0:
            return f"{self.date.strftime('%d.%m.%Y %H:%M')} - Received from {self.receiving_account_id}  {'{:,.2f}€'.format(self.amount / 100)}"
        return f"{self.date.strftime('%d.%m.%Y %H:%M')} - Send to {self.receiving_account_id}  {'{:,.2f}€'.format(self.amount / 100)}"

    def add_to_db(self):
        """
        Adds a transfer to DB
        :return:
        """

        db_access.DBAccess.add_transfer_to_db(self)
