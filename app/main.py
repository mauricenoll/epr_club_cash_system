"""
This is the virtual club system
Main should just start the gui / should load all the data

"""

from auth_provider import AuthProvider
from app.static.tk_app import TkinterApp
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

    db_access.DBAccess.populate_db()

    app = TkinterApp()
    app.mainloop()
