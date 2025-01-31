"""
Defines club class
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.models.user import User
from app.models.departement import Departement
from app.db import db_access


class Club:

    def __init__(self, users: list[User], departements: list[Departement]):
        self.users = users
        self.departements = departements

    @classmethod
    def from_db(cls):
        users = db_access.DBAccess.get_all_users()
        departements = db_access.DBAccess.get_all_departements()
        return cls(users, departements)

    def get_total_balance(self):
        return sum([departement.get_account().current_balance for departement in self.departements])
