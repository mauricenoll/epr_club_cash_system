from app.models.user import User, Admin, Treasurer, FinanceOfficer
from app.models.departement import Departement
from app.models.account import Account
from app.models.transaction import Transaction, Transfer

demo_account = Account(iD=1, current_balance=112000)


demoDep = Departement(
    id=1,
    title="Schwimmen",
    account=demo_account
)


transactions = [
    Transaction(accountID=1, amount=5000),
    Transaction(accountID=1, amount=125000),
    Transfer(accountID=1, receivingAccountID=2, amount=-12000),
    Transaction(accountID=1, amount=-6000)
]


def generate_demo_departements(amount: int):

    deps = []

    for i in range(amount):
        account = Account(
            iD=i,
            current_balance=0
        )
        deps.append(Departement(
            id=i,
            title=f"Departement {i}",
            account=account
        ))
    return deps
