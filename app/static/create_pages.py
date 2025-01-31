import os.path
import tkinter as tk
from tkinter import ttk, messagebox

from app.db.db_access import get_departements, get_all_finance_officers
from app.models.departement import Departement
from app.models.user import Treasurer

MEDFONT = ("Verdana", 18)


class CreatePage(tk.Frame):
    def __init__(self, parent, controller, auth_provider):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.auth_provider = auth_provider


class CreateDepartementPage(CreatePage):

    def __init__(self, parent, controller, auth_provider):
        CreatePage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        departement_frame = tk.Frame(container)
        departement_frame.pack(side="top", fill="both", pady=10)
        self.dep_frame = departement_frame

        ttk.Label(departement_frame, text="Create new Departement", font=("Arial", 18)).pack(
            pady=5)

        row_frame = tk.Frame(departement_frame)
        row_frame.pack(pady=5)

        ttk.Label(row_frame, text="Departement Name:").pack(side="left", padx=5)
        self.dep_name_entry = ttk.Entry(row_frame, width=30)
        self.dep_name_entry.pack(side="left")

        row_frame2 = tk.Frame(departement_frame)
        row_frame2.pack(pady=5)

        ttk.Label(row_frame2, text="Treasurer Name:").pack(side="left", padx=5)
        self.treasurer_name_entry = ttk.Entry(row_frame2, width=25)
        self.treasurer_name_entry.pack(side="left")

        ttk.Label(row_frame2, text="Treasurer Email:").pack(side="left", padx=5)
        self.treasurer_email_entry = ttk.Entry(row_frame2, width=25)
        self.treasurer_email_entry.pack(side="left")

        ttk.Label(row_frame2, text="Treasurer Password:").pack(side="left", padx=5)
        self.treasurer_password_entry = ttk.Entry(row_frame2, width=25, show="*")
        self.treasurer_password_entry.pack(side="left")

        ttk.Button(departement_frame, text="Save new departement",
                   command=self.save_departement).pack(pady=10, side="bottom")

    def save_departement(self):
        # TODO: error handling, no input handling
        dep_name = self.dep_name_entry.get()

        treasurer_name = self.treasurer_name_entry.get()
        treasurer_email = self.treasurer_email_entry.get()
        treasurer_password = self.treasurer_password_entry.get()

        departement = Departement.from_user_input(dep_name)
        treasurer = Treasurer.from_user_input(treasurer_name, treasurer_email, treasurer_password,
                                              departement)

        messagebox.showinfo("Created Departement", "Departement created successfully")
        self.controller.show_frame("AdminDashboard")


class CreateFinanceOfficerPage(CreatePage):

    def __init__(self, parent, controller, auth_provider):
        CreatePage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        finance_officer_frame = tk.Frame(container)
        finance_officer_frame.pack(side="top", fill="both", pady=10)
        self.dep_frame = finance_officer_frame

        ttk.Label(finance_officer_frame, text="Create new Finance Officer",
                  font=("Arial", 18)).pack(
            pady=5)

        ttk.Label(finance_officer_frame, text="Select a departement", font=("Arial", 14)).pack(
            pady=5)

        self.options = get_departements()
        self.selected_option = tk.StringVar()

        self.dep_dropdown = ttk.Combobox(finance_officer_frame, textvariable=self.selected_option,
                                         values=self.options, state="readonly")
        self.dep_dropdown.pack(padx=5)
        self.dep_dropdown.current(0)  # Set default selection

        ttk.Label(finance_officer_frame, text="Select an existing Officer or create a new one",
                  font=("Arial", 14)).pack(pady=5)
        ttk.Label(finance_officer_frame,
                  text="If a new officer is filled out it is prioritized").pack(pady=5)

        self.options = get_all_finance_officers()
        self.selected_option = tk.StringVar()

        self.officer_dropdown = ttk.Combobox(finance_officer_frame,
                                             textvariable=self.selected_option,
                                             values=self.options, state="readonly")
        self.officer_dropdown.pack(padx=5)
        self.officer_dropdown.current(0)  # Set default selection

        row_frame2 = tk.Frame(finance_officer_frame)
        row_frame2.pack(pady=15)

        ttk.Label(row_frame2, text="Finance Officer Name:").pack(side="left", padx=5)
        self.f_officer_name = ttk.Entry(row_frame2, width=25)
        self.f_officer_name.pack(side="left")

        ttk.Label(row_frame2, text="Finance Officer Email:").pack(side="left", padx=5)
        self.f_officer_email = ttk.Entry(row_frame2, width=25)
        self.f_officer_email.pack(side="left")

        ttk.Label(row_frame2, text="Finance Officer Password:").pack(side="left", padx=5)
        self.f_officer_password = ttk.Entry(row_frame2, width=25, show="*")
        self.f_officer_password.pack(side="left")

        ttk.Button(finance_officer_frame, text="Save").pack(pady=15)

    def save(self):
        # TODO: save logik
        officer_name = self.f_officer_name.get()
        officer_email = self.f_officer_email.get()
        officer_password = self.f_officer_password.get()

        if officer_name == "" or officer_password == "" or officer_email == "":
            # TODO: take the selected one
            pass
        else:
            # TODO: create new user
            pass

        messagebox.showinfo("Created Finance Officer", "Finance Officer created successfully")
        self.controller.show_frame("AdminDashboard")
