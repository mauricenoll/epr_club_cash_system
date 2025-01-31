"""
Defines User Classes for club system
also defines user type enum
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.models.departement import Departement
from app.db import db_access
from enum import Enum


class UserType(Enum):
    ADMIN = "Admin"
    TREASURER = "Treasurer"
    FINANCE_OFFICER = "FinanceOfficer"
    USER = "User"


class User:

    def __init__(self, id: int, display_name: str, email: str):
        self.id = id
        self.display_name = display_name
        self.email = email
        self.is_logged_in = False

    def log_in(self):
        self.is_logged_in = True

    def log_out(self):
        self.is_logged_in = False

    def __str__(self):
        return self.display_name


class Admin(User):

    def __init__(self, id: int, display_name: str, email: str):
        super().__init__(id, display_name, email)

    @classmethod
    def from_db_json(cls, json: dict):
        """
        Creat
        :param json:
        :return:
        """
        id = json.get("id")
        display_name = json.get("display_name")
        email = json.get("email")

        return cls(id, display_name, email)


class Treasurer(User):

    def __init__(self, id: int, display_name: str, email: str, departement_id: int):
        super().__init__(id, display_name, email)
        self.departement = None
        self.departement_id = departement_id

    @classmethod
    def from_db(cls, json: dict):
        id = json.get("id")
        display_name = json.get("display_name")
        email = json.get("email")
        department_id = json.get("departement_id")
        departement = db_access.DBAccess.get_departement_by_id(department_id)

        return cls(id, display_name, email, department_id)

    @classmethod
    def from_user_input(cls, display_name: str, email: str, password: str, departement_id: int):
        iD = db_access.DBAccess.get_next_user_id()
        treasurer = cls(iD, display_name, email, departement_id)
        treasurer.__to_db(password)
        return treasurer

    def get_departement(self):
        if self.departement is None:
            self.departement = db_access.DBAccess.get_departement_by_id(self.id)
        return self.departement

    def __to_db(self, password: str):
        db_access.DBAccess.safe_user_to_db(self, password, UserType.TREASURER)


class FinanceOfficer(User):

    def __init__(self, id: int, display_name: str, email: str):
        super().__init__(id, display_name, email)
        self.departments = db_access.DBAccess.get_all_departements()

    @classmethod
    def from_db(cls, json: dict):
        id = json.get("id")
        display_name = json.get("display_name")
        email = json.get("email")
        departements = db_access.DBAccess.get_all_departements()

        return cls(id, display_name, email)

    @classmethod
    def from_user_input(cls, display_name: str, email: str, password: str):
        iD = db_access.DBAccess.get_next_user_id()
        finance_officer = cls(iD, display_name, email)
        finance_officer.__to_db(password)
        return finance_officer

    def __to_db(self, password: str):
        db_access.DBAccess.safe_user_to_db(self, password, UserType.FINANCE_OFFICER)
