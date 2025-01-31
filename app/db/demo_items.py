from app.models.user import UserType
from app.models.departement import Departement
from app.models.account import Account
from app.models.transaction import Transaction, Transfer

demo_account = Account(iD=1, current_balance=112000)

demo_user_db = [
    {
        "id": 1,
        "department_id": -1,
        "email": "admin@email.de",
        "password": "password",
        "display_name": "Admin Michael",
        "user_type": UserType.ADMIN
    },
    {
        "id": 2,
        "department_id": -1,
        "email": "finance_officer@email.de",
        "password": "password",
        "display_name": "Finance Officer Michael",
        "user_type": UserType.FINANCE_OFFICER
    },
    {
        "id": 3,
        "department_id": 1,
        "email": "treasurer@email.de",
        "password": "password",
        "display_name": "Treasurer Michael",
        "user_type": UserType.TREASURER
    }
]

demo_departement_db = [
    {
        "id": 1,
        "title": "Schwimmen",
    },
    {
        "id": 2,
        "title": "Leichtathletik"
    },
    {
        "id": 3,
        "title": "Radfahren"
    }
]

demo_account_db = [
    {
        "id": 1,
        "current_balance": 0
    },
    {
        "id": 2,
        "current_balance": 0
    },
    {
        "id": 3,
        "current_balance": 0
    },
]

demo_transaction_db = [
    {

    }
]


demoDep = Departement(
    id=1,
    title="Schwimmen",
    account=demo_account
)

transactions = []


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
