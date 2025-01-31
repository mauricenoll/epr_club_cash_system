"""
Lays out the Login Page Gui
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"


import tkinter as tk
from tkinter import ttk
import logging

LARGEFONT = ("Verdana", 24, "bold")

logger = logging.getLogger("system_logger")


class LoginPage(tk.Frame):
    """
    Login Page
    """
    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.auth_provider = auth_provider

        self.controller.title("Virtual Club System")

        # Configure grid to center widgets
        self.grid_columnconfigure(0, weight=1)  # Left padding
        self.grid_columnconfigure(1, weight=1)  # Center content
        self.grid_columnconfigure(2, weight=1)  # Right padding

        # Title Label
        label = ttk.Label(self, text="Login", font=LARGEFONT)
        label.grid(row=0, column=1, pady=10)

        # Email Label & Input
        email_label = ttk.Label(self, text="Email:")
        email_label.grid(row=1, column=1, pady=5)

        self.email_input = tk.Entry(self, width=30)
        self.email_input.grid(row=2, column=1, pady=5)

        # Password Label & Input
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(row=3, column=1, pady=5)

        self.password_input = tk.Entry(self, width=30, show="*")
        self.password_input.grid(row=4, column=1, pady=5)

        # Login Button
        login_btn = ttk.Button(self, text="Login", command=self.authenticate_user)
        login_btn.grid(row=5, column=1, pady=10)

    def authenticate_user(self):
        """
        Authenticates the User
        :return:
        """

        email = self.email_input.get()
        password = self.password_input.get()

        logger.info("validating login")

        self.controller.validate_login(email, password)
