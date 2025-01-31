"""
This is the virtual club system
Main should just start the gui / should load all the data

"""
import sqlite3

from auth_provider import AuthProvider
from app.static.tk_app import TkinterApp
from app.db import database
from app.models.departement import Departement
from app.models.account import Account
from app.models.user import Treasurer, UserType
from app.db import db_access
import logger_setup

logger = logger_setup.setup_logger("system_logger")
auth_provider = AuthProvider()

if __name__ == '__main__':
    """
    Admin login:
    admin@email.de
    password
    """

    db_access.DBAccess.save_departement_to_db(
        Departement(id=1, title="Schwimmen", account=Account(iD=1, current_balance=0)))
    db_access.DBAccess.save_departement_to_db(
        Departement(id=2, title="Fußball", account=Account(iD=2, current_balance=0)))
    db_access.DBAccess.save_departement_to_db(
        Departement(id=3, title="Handball", account=Account(iD=3, current_balance=0)))

    db_access.DBAccess.safe_user_to_db(
        Treasurer(id=1, display_name="Treasurer 1", email="treasurer1@mail.de", departement=Departement(id=1, title="Schwimmen", account=Account(iD=1, current_balance=0))),
        password="password",
        user_type=UserType.TREASURER
    )

    conn = sqlite3.connect("club_finance_system.db")
    cursor = conn.cursor()

    app = TkinterApp()
    app.mainloop()
