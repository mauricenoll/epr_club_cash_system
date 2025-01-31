from datetime import datetime


class Transaction:
    """
    This is for Withdrawal and Deposit, this is basically a helper class for history
    """

    def __init__(self, accountID: int, amount: int, date: datetime | None = datetime.now()):
        self.accountID = accountID
        self.amount = amount
        self.date = date  # transaction time is current time

    def add_to_db(self):
        # TODO
        pass

    def __str__(self):
        if self.amount > 0:
            return f"{self.date.strftime('%d.%m.%Y')} - Deposit  {'{:,.2f}€'.format(self.amount / 100)}"
        return f"{self.date.strftime('%d.%m.%Y')} - Withdrawal  {'{:,.2f}€'.format(self.amount / 100)}"


class Transfer(Transaction):

    def __init__(self, accountID: int, amount: int, receivingAccountID: int):
        super().__init__(accountID, amount)
        self.receivingAccountID = receivingAccountID

    def __str__(self):
        if self.amount > 0:
            return f"{self.date.strftime('%d.%m.%Y')} - Received from {self.receivingAccountID}  {'{:,.2f}€'.format(self.amount / 100)}"
        return f"{self.date.strftime('%d.%m.%Y')} - Send to {self.receivingAccountID}  {'{:,.2f}€'.format(self.amount / 100)}"


    def add_to_db(self):
        # TODO -> needs to override transaction
        # TODO needs to update current balance on other account as well, since balance is not depending on history
        # TODO: maybe add this once as + for receiver and once as - for sender
        pass
