"""
Defines club class
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.models.user import User
from app.models.departement import Departement
from app.db import db_access


class Club:

    def __init__(self, users: list[User], departements: list[Departement]):
        """
        Initializes a club
        :param users:
        :param departements:
        """
        self.users = users
        self.departements = departements

    @classmethod
    def from_db(cls):
        """
        Gets club from DB
        :return:
        """
        users = db_access.DBAccess.get_all_users()
        departements = db_access.DBAccess.get_all_departements()
        return cls(users, departements)

    def get_total_balance(self):
        """
        Gets the total balance in the club
        :return:
        """
        return sum([departement.get_account().current_balance for departement in self.departements])
