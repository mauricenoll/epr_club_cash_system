"""
Authentication Provider for easy user auth handling
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.db.db_access import DBAccess
from app.models.user import User


class AuthProvider:
    """
    We initialize one Auth Provider per Session -> current User data is saved here
    """

    def __init__(self):
        """
        Initializer
        """

        self.logged_in_user: User | None = None

    def check_auth(self, email: str, password: str):
        """
        Checks authentication as a boolean
        Also logs in the User
        :param email:
        :param password:
        :return:
        """
        user = DBAccess.authenticate_user_from_db(email, password)
        if user is not None:
            self.logged_in_user = user
            user.log_in()
            return True

        return False

    def log_out(self):
        """
        Logs out
        :return:
        """
        self.logged_in_user.log_out()
        self.logged_in_user = None


auth_provider = AuthProvider()
