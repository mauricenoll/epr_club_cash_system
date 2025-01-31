"""
Lays out the Login Page Gui
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"


import tkinter as tk
from tkinter import ttk
import logging

LARGEFONT = ("Verdana", 35)

logger = logging.getLogger("system_logger")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller, auth_provider):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.auth_provider = auth_provider

        self.controller.title("Virtual Club System")

        # label of frame Layout 2
        label = ttk.Label(self, text="Login", font=LARGEFONT)

        label.grid(row=0, column=4, padx=10, pady=10)

        email_label = ttk.Label(self, text="Email:")
        email_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Text input field for email
        self.email_input = tk.Entry(self, width=25)
        self.email_input.grid(row=1, column=4, padx=10, pady=10)

        password_label = ttk.Label(self, text="Password:")
        password_label.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        # Text input field for email
        self.password_input = tk.Entry(self, width=25, show="*")
        self.password_input.grid(row=2, column=4, padx=10, pady=10)

        login_btn = ttk.Button(self, text="Login", command=self.authenticate_user)

        login_btn.grid(row=4, column=4, padx=10, pady=10)

    def authenticate_user(self):
        email = self.email_input.get()
        password = self.password_input.get()

        self.controller.validate_login(email, password)
