"""
Lays out the guy for pages where something is created
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import os.path
import tkinter as tk
from tkinter import ttk, messagebox

from app.models.departement import Departement
from app.models.user import Treasurer, FinanceOfficer
from app.db import db_access

MEDFONT = ("Verdana", 18)


class CreatePage(tk.Frame):
    def __init__(self, parent, controller, auth_provider):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.auth_provider = auth_provider

        top_bar_frame = tk.Frame(self, bg="black", height=60)
        top_bar_frame.pack(side="top", fill="x")

        style = ttk.Style()
        style.configure("Custom.TButton", background="white", foreground="black",
                        font=("Arial", 14))

        logout_button = ttk.Button(top_bar_frame, text="LogOut",
                                   style="Custom.TButton", command=self.controller.log_out)
        logout_button.pack(side="left", padx=15, pady=10)

        dashboard_btn = ttk.Button(top_bar_frame, text="Back to Dashboard",
                                   style="Custom.TButton", command=self.controller.go_to_dashboard)
        dashboard_btn.pack(side="right", padx=15, pady=10)


class CreateDepartementPage(CreatePage):

    def __init__(self, parent, controller, auth_provider):
        CreatePage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        departement_frame = tk.Frame(container)
        departement_frame.pack(side="top", fill="both", pady=10)
        self.dep_frame = departement_frame

        ttk.Label(departement_frame, text="Create a new Departement",
                  font=("Arial", 18, "bold")).pack(
            pady=5)

        departement_name_frame = tk.Frame(departement_frame)
        departement_name_frame.pack(pady=15)

        ttk.Label(departement_name_frame, text="Enter new department name:").pack(side="left")

        self.dep_name_entry = ttk.Entry(departement_name_frame, width=30)
        self.dep_name_entry.pack(side="left")

        new_treasurer_column = tk.Frame(departement_frame)
        self.new_treasurer_column = new_treasurer_column
        self.new_treasurer_column.pack()

        ttk.Label(new_treasurer_column, text="Treasurer Name:").pack(side="left", padx=10)
        self.treasurer_name_entry = ttk.Entry(new_treasurer_column, width=25)
        self.treasurer_name_entry.pack(side="left")

        row2 = tk.Frame(departement_frame)
        row2.pack(pady=10)

        ttk.Label(row2, text="Treasurer Email:").pack(side="left", padx=10)
        self.treasurer_email_entry = ttk.Entry(row2, width=25)
        self.treasurer_email_entry.pack(side="left")

        row3 = tk.Frame(departement_frame)
        row3.pack(pady=10)

        ttk.Label(row3, text="Treasurer Password:").pack(side="left", padx=10)
        self.treasurer_password_entry = ttk.Entry(row3, width=25, show="*")
        self.treasurer_password_entry.pack(side="left")

        ttk.Button(departement_frame, text="Save new departement",
                   command=self.save_departement).pack(pady=10, side="bottom")

    def save_departement(self):
        """
        Saves a new departement
        :return:
        """
        dep_name = self.dep_name_entry.get()

        treasurer_name = self.treasurer_name_entry.get()
        treasurer_email = self.treasurer_email_entry.get()
        treasurer_password = self.treasurer_password_entry.get()

        if dep_name == "" or treasurer_name == "" or treasurer_email == "" or treasurer_password == "":
            messagebox.showerror("Error", "please enter something into every entry!")
        else:
            try:
                departement = Departement.from_user_input(dep_name)
                try:
                    Treasurer.from_user_input(treasurer_name, treasurer_email, treasurer_password,
                                              departement)
                    messagebox.showinfo("Created Departement", "Departement created successfully")
                    self.controller.go_to_dashboard()
                except db_access.DuplicateInsertException:
                    messagebox.showerror("Error", "Treasurer email already taken!")
            except db_access.DuplicateInsertException:
                messagebox.showerror("Error", "Department Name already exists!")


class CreateFinanceOfficerPage(CreatePage):

    def __init__(self, parent, controller, auth_provider):
        CreatePage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        finance_officer_frame = tk.Frame(container)
        finance_officer_frame.pack(side="top", fill="both", pady=10)
        self.dep_frame = finance_officer_frame

        ttk.Label(finance_officer_frame, text="Create new Finance Officer",
                  font=("Arial", 18, "bold")).pack(
            pady=5)

        row_frame2 = tk.Frame(finance_officer_frame)
        row_frame2.pack(pady=15)

        ttk.Label(row_frame2, text="Finance Officer Name:").pack(side="left", padx=10, pady=10)
        self.f_officer_name = ttk.Entry(row_frame2, width=25)
        self.f_officer_name.pack(side="left")

        row_frame3 = tk.Frame(finance_officer_frame)
        row_frame3.pack(pady=15)

        ttk.Label(row_frame3, text="Finance Officer Email:").pack(side="left", padx=10, pady=10)
        self.f_officer_email = ttk.Entry(row_frame3, width=25)
        self.f_officer_email.pack(side="left")

        row_frame4 = tk.Frame(finance_officer_frame)
        row_frame4.pack(pady=15)

        ttk.Label(row_frame4, text="Finance Officer Password:").pack(side="left", padx=10, pady=10)
        self.f_officer_password = ttk.Entry(row_frame4, width=25, show="*")
        self.f_officer_password.pack(side="left")

        ttk.Button(finance_officer_frame, text="Save", command=self.save).pack(pady=15)

    def save(self):
        officer_name = self.f_officer_name.get()
        officer_email = self.f_officer_email.get()
        officer_password = self.f_officer_password.get()

        if officer_name == "" or officer_password == "" or officer_email == "":
            messagebox.showerror("Information not complete",
                                 "Please enter all the fields")
        else:
            try:
                FinanceOfficer.from_user_input(
                    display_name=officer_name,
                    password=officer_password,
                    email=officer_email)
                messagebox.showinfo("Created Finance Officer",
                                    "Finance Officer created successfully")
                self.controller.go_to_dashboard()
            except db_access.DuplicateInsertException:
                messagebox.showerror("Error", "Finance Officer email already taken!")

class EditDepartmentPage(CreatePage):

    def __init__(self, parent, controller, auth_provider, department):
        CreatePage.__init__(self, parent, controller, auth_provider)

        self.department = department

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)
