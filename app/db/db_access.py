from app.models.user import User, Admin, Treasurer, FinanceOfficer
from app.db import demo_items


def get_user_from_db(email: str, password: str):
    return FinanceOfficer(id=1, display_name="Michael Müller", email=email, departements=demo_items.generate_demo_departements(5))


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