"""
DOCSTRING:

"""

import tkinter as tk
from tkinter import ttk, messagebox

from app.models.user import Treasurer, Admin, FinanceOfficer
from app.static.login_page import LoginPage
from app.static.dashboard_page import DashboardPage, AdminDashboard, TreasurerDashboard, \
    FinancialOfficerDashboard
from app.static.transaction_page import TransactionPage, WithdrawalPage, DepositPage, TransferPage
from app.auth_provider import AuthProvider, auth_provider
from app.static.create_pages import CreateDepartementPage, CreateFinanceOfficerPage
from app.models.club import Club

LARGEFONT = ("Verdana", 35)


class TkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self)

        self.logged_in_user = None
        self.title("Multi-Page App")
        self.geometry("800x600")

        self.auth_provider = auth_provider

        self.club = Club.from_db()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["LoginPage"] = LoginPage(parent=container, controller=self,
                                             auth_provider=self.auth_provider)
        self.frames["LoginPage"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """
        Shows a specific frame
        :param page_name:
        :return:
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def validate_login(self, email, password):
        """
        Validates log in and then redirects to the corresponding page
        :param email:
        :param password:
        :return:
        """
        user = self.auth_provider.check_auth(email, password)
        if user:
            self.logged_in_user = user
            messagebox.showinfo("Login Successful", f"Welcome {email}!")
            if type(self.auth_provider.logged_in_user) is Treasurer:
                print("is treasurer")
                self.frames["TreasurerDashboard"] = TreasurerDashboard(
                    parent=self.frames["LoginPage"].master, controller=self,
                    auth_provider=self.auth_provider)
                self.frames["TreasurerDashboard"].grid(row=0, column=0, sticky="nsew")
                self.show_frame("TreasurerDashboard")
            if type(self.auth_provider.logged_in_user) is Admin:
                self.frames["AdminDashboard"] = AdminDashboard(
                    parent=self.frames["LoginPage"].master, controller=self,
                    auth_provider=self.auth_provider)
                self.frames["AdminDashboard"].grid(row=0, column=0, sticky="nsew")
                self.show_frame("AdminDashboard")
            if type(self.auth_provider.logged_in_user) is FinanceOfficer:
                self.frames["FinancialOfficerDashboard"] = FinancialOfficerDashboard(
                    parent=self.frames["LoginPage"].master, controller=self,
                    auth_provider=self.auth_provider)
                self.frames["FinancialOfficerDashboard"].grid(row=0, column=0, sticky="nsew")
                self.show_frame("FinancialOfficerDashboard")

        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def show_transaction_page(self, transaction_type: str):
        """
        Shows the corresponding transaction page
        :param transaction_type:
        :return:
        """

        if transaction_type == "withdrawal":
            self.frames["WithdrawalPage"] = WithdrawalPage(
                parent=self.frames["LoginPage"].master, controller=self,
                auth_provider=self.auth_provider)
            self.frames["WithdrawalPage"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("WithdrawalPage")

        if transaction_type == "deposit":
            self.frames["DepositPage"] = DepositPage(
                parent=self.frames["LoginPage"].master, controller=self,
                auth_provider=self.auth_provider)
            self.frames["DepositPage"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("DepositPage")

        if transaction_type == "transfer":
            self.frames["TransferPage"] = TransferPage(
                parent=self.frames["LoginPage"].master, controller=self,
                auth_provider=self.auth_provider)
            self.frames["TransferPage"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("TransferPage")

    def show_create_page(self, create_type: str):
        """
        Shows the create page for the create_type
        :param create_type:
        :return:
        """

        if create_type == "departement":
            self.frames["CreateDepartementPage"] = CreateDepartementPage(
                parent=self.frames["LoginPage"].master, controller=self,
                auth_provider=self.auth_provider)
            self.frames["CreateDepartementPage"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("CreateDepartementPage")

        if create_type == "f_officer":
            self.frames["CreateFinanceOfficerPage"] = CreateFinanceOfficerPage(
                parent=self.frames["LoginPage"].master, controller=self,
                auth_provider=self.auth_provider)
            self.frames["CreateFinanceOfficerPage"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("CreateFinanceOfficerPage")
