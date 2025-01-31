"""
Defines User Classes for club system
also defines user type enum
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

from app.models.departement import Departement
from app.db import db_access
from enum import Enum
import logging

logger = logging.getLogger("system_logger")


class UserType(Enum):
    """
    User Type Enum
    """
    ADMIN = "Admin"
    TREASURER = "Treasurer"
    FINANCE_OFFICER = "FinanceOfficer"
    USER = "User"


class User:
    """
    User Parent Class
    """

    def __init__(self, id: int, display_name: str, email: str):
        """
        Initializes a Parent User
        :param id:
        :param display_name:
        :param email:
        """
        self.id = id
        self.display_name = display_name
        self.email = email
        self.is_logged_in = False

    def log_in(self):
        """
        Logs in User
        :return:
        """
        logger.info("logged in")
        self.is_logged_in = True

    def log_out(self):
        """
        Logs out user
        :return:
        """
        logger.info("logged out")
        self.is_logged_in = False

    def __str__(self):
        """
        String
        :return:
        """
        return self.display_name


class Admin(User):
    """
    Admin class
    """

    def __init__(self, id: int, display_name: str, email: str):
        """
        Initializes an Admin
        :param id:
        :param display_name:
        :param email:
        """
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
    """
    Treasurer
    """


    def __init__(self, id: int, display_name: str, email: str, departement_id: int):
        """
        Initializes a Treasurer
        :param id:
        :param display_name:
        :param email:
        :param departement_id:
        """
        super().__init__(id, display_name, email)
        self.departement = None
        self.departement_id = departement_id

    @classmethod
    def from_db(cls, json: dict):
        """
        Gets user from dict
        :param json:
        :return:
        """
        id = json.get("id")
        display_name = json.get("display_name")
        email = json.get("email")
        department_id = json.get("departement_id")
        departement = db_access.DBAccess.get_departement_by_id(department_id)

        return cls(id, display_name, email, department_id)

    @classmethod
    def from_user_input(cls, display_name: str, email: str, password: str, departement_id: int):
        """
        Creates user from user input
        :param display_name:
        :param email:
        :param password:
        :param departement_id:
        :return:
        """
        iD = db_access.DBAccess.get_next_user_id()
        treasurer = cls(iD, display_name, email, departement_id)
        treasurer.__to_db(password)
        return treasurer

    def get_departement(self):
        """
        Gets the department
        :return:
        """
        if self.departement is None:
            self.departement = db_access.DBAccess.get_departement_by_id(self.id)
        return self.departement

    def __to_db(self, password: str):
        """
        Saves Treasurer to DB
        :param password:
        :return:
        """
        db_access.DBAccess.safe_user_to_db(self, password, UserType.TREASURER)


class FinanceOfficer(User):

    """
    Finance Officer
    """

    def __init__(self, id: int, display_name: str, email: str):
        """
        Initializes a finance officer
        :param id:
        :param display_name:
        :param email:
        """
        super().__init__(id, display_name, email)
        self.departments = db_access.DBAccess.get_all_departements()

    @classmethod
    def from_db(cls, json: dict):
        """
        Gets fofficer from dit
        :param json:
        :return:
        """
        id = json.get("id")
        display_name = json.get("display_name")
        email = json.get("email")
        departements = db_access.DBAccess.get_all_departements()

        return cls(id, display_name, email)

    @classmethod
    def from_user_input(cls, display_name: str, email: str, password: str):
        """
        Gets a finance officer from user input
        :param display_name:
        :param email:
        :param password:
        :return:
        """

        iD = db_access.DBAccess.get_next_user_id()
        finance_officer = cls(iD, display_name, email)
        finance_officer.__to_db(password)
        return finance_officer

    def __to_db(self, password: str):
        """
        Saves user to db
        :param password:
        :return:
        """
        db_access.DBAccess.safe_user_to_db(self, password, UserType.FINANCE_OFFICER)
