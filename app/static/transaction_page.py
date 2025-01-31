"""
Lays out all the Transaction Pages
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import tkinter as tk
from tkinter import ttk, messagebox
from app.db import db_access


class TransactionPage(tk.Frame):
    """
    Base transaction Page
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


class WithdrawalPage(TransactionPage):
    """
    Withdrawal Page
    """

    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        TransactionPage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = tk.Frame(container)
        top_frame.pack(side="top", fill="both", pady=10)

        title_label = ttk.Label(top_frame, text="Make a Withdrawal!", font=("Arial", 18, "bold"))
        title_label.pack(side="left", padx=25, pady=10)

        balance_label = ttk.Label(top_frame,
                                  text=f"Current balance: {self.auth_provider.logged_in_user.departement.account.get_formatted_balance()}",
                                  font=("Arial", 18))
        balance_label.pack(side="bottom", pady=10)

        middle_frame = tk.Frame(container)
        middle_frame.pack(side="top", fill="both", pady=10)

        entry_label = ttk.Label(middle_frame, text="Enter Amount in €:", font=("Arial", 12))
        entry_label.pack(side="left", padx=25)

        self.amount_entry = ttk.Entry(middle_frame, width=25)
        self.amount_entry.pack(side="left", padx=5)

        withdrawal_button = ttk.Button(middle_frame, text="Withdraw",
                                       command=self.validate_withdrawal)
        withdrawal_button.pack(side="left", padx=10)

    def validate_withdrawal(self):
        """
        Validates the withdrawal
        :return:
        """
        input = self.amount_entry.get()

        input.replace("€", "")  # replacing symbol
        input.replace(",", ".")
        account = self.auth_provider.logged_in_user.get_departement().get_account()
        try:
            amount = int(float(input) * 100)  # convert to cents
            if amount > account.current_balance:
                messagebox.showerror("error", f"Not enough funds for this transaction!")
            else:
                account.withdraw(amount)
                messagebox.showinfo("Withdrawal successful", "Withdrawal successful")
                self.controller.go_to_dashboard()

        except ValueError:
            messagebox.showerror("error", f"{input} is not a valid number!")


class DepositPage(TransactionPage):

    """
    Deposit Page
    """

    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        TransactionPage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = tk.Frame(container)
        top_frame.pack(side="top", fill="both", pady=10)

        title_label = ttk.Label(top_frame, text="Make a Deposit!", font=("Arial", 18, "bold"))
        title_label.pack(side="left", padx=25, pady=10)

        balance_label = ttk.Label(top_frame,
                                  text=f"Current balance: {self.auth_provider.logged_in_user.departement.account.get_formatted_balance()}",
                                  font=("Arial", 18))
        balance_label.pack(side="bottom", pady=10)

        middle_frame = tk.Frame(container)
        middle_frame.pack(side="top", fill="both", pady=10)

        entry_label = ttk.Label(middle_frame, text="Enter Amount in €:", font=("Arial", 12))
        entry_label.pack(side="left", padx=25)

        self.amount_entry = ttk.Entry(middle_frame, width=25)
        self.amount_entry.pack(side="left", padx=5)

        withdrawal_button = ttk.Button(middle_frame, text="Deposit",
                                       command=self.validate_deposit)
        withdrawal_button.pack(side="left", padx=10)

    def validate_deposit(self):
        """
        Validates the deposit
        :return:
        """

        input = self.amount_entry.get()

        input.replace("€", "")  # replacing symbol
        input.replace(",", ".")

        try:
            amount = int(float(input) * 100)  # convert to cents
            self.auth_provider.logged_in_user.get_departement().get_account().deposit(amount)
            messagebox.showinfo("Deposit successful", "Deposit successful")
            self.controller.go_to_dashboard()

        except ValueError:
            messagebox.showerror("error", f"{input} is not a valid number!")


class TransferPage(TransactionPage):

    """
    Transfer Page
    """

    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        TransactionPage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = tk.Frame(container)
        top_frame.pack(side="top", fill="both", pady=10)

        ttk.Label(top_frame, text="Make a Transfer!", font=("Arial", 18, "bold")).pack(pady=15,
                                                                                       side="left")

        ttk.Label(top_frame,
                  text=f"Current balance: {self.auth_provider.logged_in_user.get_departement().get_account().get_formatted_balance()}",
                  font=("Arial", 14)).pack(side="left")

        middle_frame = tk.Frame(container)
        middle_frame.pack(side="top", fill="both", pady=10)

        ttk.Label(middle_frame, text="Enter Transfer Amount in €:").pack(side="left", pady=15,
                                                                         padx=10)

        self.amount_entry = ttk.Entry(middle_frame, width=25)
        self.amount_entry.pack(side="left", padx=15)

        ttk.Label(middle_frame, text="Select Department to receive the transfer €:").pack(
            side="left", pady=15,
            padx=0)

        departements = [departement for departement in db_access.DBAccess.get_all_departements()
                        if departement.id
                        != self.auth_provider.logged_in_user.get_departement().id]

        self.options = departements
        self.selected_option = tk.StringVar()

        self.dropdown = ttk.Combobox(middle_frame, textvariable=self.selected_option,
                                     values=self.options,
                                     state="readonly")
        self.dropdown.pack(pady=5, side="right", padx=15)
        self.dropdown.current(0)  # Set default selection

        bottom_frame = tk.Frame(container)
        bottom_frame.pack(side="top", fill="both", pady=10)

        withdrawal_button = ttk.Button(bottom_frame, text="Transfer", command=self.validate_transfer)
        withdrawal_button.pack(pady=25)

    def validate_transfer(self):
        """
        Validates the transfer
        :return:
        """
        input = self.amount_entry.get()

        input.replace("€", "")  # replacing symbol
        input.replace(",", ".")

        account = self.auth_provider.logged_in_user.get_departement().get_account()

        try:
            amount = int(float(input) * 100)  # convert to cents
        except ValueError:
            messagebox.showerror("error", f"{input} is not a valid number!")

        if amount < 0:
            messagebox.showerror("error", "Please put in a positive number")

        elif amount > account.current_balance:
            messagebox.showerror("error", "Not enough funds")

        else:
            option = self.selected_option.get()
            receiverID = \
                [dep for dep in db_access.DBAccess.get_all_departements() if dep.title == option][
                    0].id
            account.transfer(receiving_account_id=receiverID, amount=amount)
            messagebox.showinfo("Transfer successful", "Transfer successful")

            self.controller.go_to_dashboard()
