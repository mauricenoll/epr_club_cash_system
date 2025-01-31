from app.models.departement import Departement
from app.db import db_access


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


class Treasurer(User):

    def __init__(self, id: int, display_name: str, email: str, departement: Departement):
        super().__init__(id, display_name, email)
        self.departement = departement

    @classmethod
    def from_user_input(cls, display_name: str, email: str, password: str,
                        departement: Departement):
        iD = db_access.get_next_user_id()
        treasurer = cls(iD, display_name, email, departement)
        treasurer.__to_db(password)
        return treasurer

    def __to_db(self, password: str):
        db_access.save_user_to_db(self, password)


class FinanceOfficer(User):

    def __init__(self, id: int, display_name: str, email: str, departements: list[Departement]):
        super().__init__(id, display_name, email)
        self.departments = departements

    @classmethod
    def from_user_input(cls, display_name: str, email: str, password: str,
                        departement: Departement):
        iD = db_access.get_next_user_id()
        finance_officer = cls(iD, display_name, email, [departement])
        finance_officer.__to_db(password)
        return finance_officer

    def __to_db(self, password: str):
        db_access.save_user_to_db(self, password)