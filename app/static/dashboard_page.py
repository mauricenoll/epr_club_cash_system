"""
Defines the Dashboard Pages
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import os.path
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from app.db.db_access import DBAccess
import logging

logger = logging.getLogger("system_logger")

MEDFONT = ("Verdana", 18)


class DashboardPage(tk.Frame):
    """
    Base Dashboard page
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
        style.configure("Custom.TButton", background="white", foreground="black", font=("Arial", 14))

        logout_button = ttk.Button(top_bar_frame, text="LogOut",
                                   style="Custom.TButton", command=self.controller.log_out)
        logout_button.pack(side="left", padx=15, pady=10)


class AdminDashboard(DashboardPage):
    """
    Admins can:
        -> create/delete User
        -> create/delete Departement (-> create Account)
        -> save current status
    """

    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        DashboardPage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Top frame for department selection and actions
        departement_frame = tk.Frame(container)
        departement_frame.pack(side="left", fill="both", pady=10, padx=15)
        self.dep_frame = departement_frame

        ttk.Label(departement_frame, text="Departements", font=("Arial", 18, "bold")).pack(pady=5)

        # Row frame for dropdown and export button
        row_frame = tk.Frame(departement_frame)
        row_frame.pack(pady=5)

        button_row_frame = tk.Frame(departement_frame)
        button_row_frame.pack(pady=5)

        # Button below the dropdown row
        ttk.Button(button_row_frame, text="Create new Departement",
                   command=self.create_departement).pack(pady=20, padx=20, side="left")

        ttk.Button(button_row_frame, text="Export current Department Status",
                   command=AdminDashboard.save_history).pack(pady=20, padx=20, side="left")

        # Right side

        user_frame = tk.Frame(container)
        user_frame.pack(side="right", fill="both", pady=10, padx=15)
        self.user_frame = user_frame

        ttk.Label(user_frame, text="Users", font=("Arial", 18, "bold")).pack(pady=5)

        user_row = tk.Frame(user_frame)
        user_row.pack(pady=5)

        ttk.Button(user_row, text="Create Financial Officer",
                   command=self.create_finance_officer).pack(side="right", padx=20)

    @staticmethod
    def save_history():
        """
        Saves the history to a specific folder chosen by the user
        :return:
        """
        selected_folder = tkinter.filedialog.askdirectory(
            title="Select Directory to save current status")

        if selected_folder:
            for index, data in enumerate(DBAccess.export_current_status()):

                file = os.path.join(selected_folder, data.get("filename", "unnamed.txt"))
                with open(file, "w", encoding="utf-8") as status_file:
                    status_file.write(f"Current Balance: {data["data"]["current_balance"]}€")
                    for transaction in data["data"]["transactions"]:
                        status_file.write("\n" + str(transaction))

    def create_departement(self):
        """
        Navigates to create department
        :return:
        """
        self.controller.show_create_page("departement")

    def create_finance_officer(self):
        """
                Navigates to create finance officer
                :return:
                """
        self.controller.show_create_page("f_officer")


class TreasurerDashboard(DashboardPage):
    """
    Treasurer Dashboard
    """

    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        DashboardPage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        middle_frame = tk.Frame(container)
        middle_frame.pack(side="right", fill="y", padx=10)
        self.middle_frame = middle_frame

        ttk.Label(middle_frame, text="Current Balance", font=("Arial", 18, "bold")).pack(pady=5, padx=25)

        if self.auth_provider.logged_in_user is not None:
            ttk.Label(middle_frame,
                      text=f"{self.auth_provider.logged_in_user.get_departement().get_account().get_formatted_balance()}",
                      font=MEDFONT).pack(padx=25)

        ttk.Button(middle_frame, text="Withdraw", command=self.show_withdraw).pack(pady=2.5, padx=25)
        ttk.Button(middle_frame, text="Deposit", command=self.show_deposit).pack(pady=2.5, padx=25)
        ttk.Button(middle_frame, text="Transfer", command=self.show_transfer).pack(pady=2.5, padx=25)

        # Left side (Scrollable Transactions)
        left_frame = tk.Frame(container)
        left_frame.pack(side="left", fill="y", padx=10)

        ttk.Label(left_frame, text="Transaction History", font=("Arial", 18, "bold")).pack(pady=5)

        self.scrollbar = tk.Scrollbar(left_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.transaction_listbox = tk.Listbox(left_frame, yscrollcommand=self.scrollbar.set,
                                              width=60, height=10)
        self.transaction_listbox.pack(side="left", fill="y")

        self.scrollbar.config(command=self.transaction_listbox.yview)

        # Populate transactions
        self.populate_transactions()

    def populate_transactions(self):
        """Populate transaction list"""
        self.transaction_listbox.delete(0, tk.END)
        for transaction in self.auth_provider.logged_in_user.departement.account.get_history():
            self.transaction_listbox.insert(tk.END, str(transaction))

    def show_withdraw(self):
        """
        Shows withdrawal page
        :return:
        """
        self.controller.show_transaction_page("withdrawal")

    def show_deposit(self):
        """
        Shows deposit page
        :return:
        """
        self.controller.show_transaction_page("deposit")

    def show_transfer(self):
        """
        Shows transfer page
        :return:
        """
        self.controller.show_transaction_page("transfer")


class FinancialOfficerDashboard(DashboardPage):
    """
    F Officer Dashboard
    """

    def __init__(self, parent, controller, auth_provider):
        """
        Initializer
        :param parent:
        :param controller:
        :param auth_provider:
        """
        DashboardPage.__init__(self, parent, controller, auth_provider)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        dashboard_frame = tk.Frame(container)
        dashboard_frame.pack(fill="y", padx=10)
        self.dashboard_frame = dashboard_frame

        ttk.Label(dashboard_frame, text="Current Total Balance:", font=("Arial", 18, "bold")).pack(
            side="left", pady=5)
        ttk.Label(dashboard_frame,
                  text='{:,.2f}€'.format(self.controller.club.get_total_balance() / 100),
                  font=("Arial", 18)).pack(
            side="left", pady=5)

        lower_dashboard_frame = tk.Frame(container)
        lower_dashboard_frame.pack(fill="y", pady=10)
        self.lower_dashboard_frame = lower_dashboard_frame

        ttk.Label(lower_dashboard_frame, text="Select a departement:").pack(
            side="left", pady=5, padx=10)

        self.options = DBAccess.get_all_departements()
        self.selected_option = tk.StringVar()

        self.current_department = self.options[0]

        self.dropdown = ttk.Combobox(lower_dashboard_frame, textvariable=self.selected_option,
                                     values=self.options,
                                     state="readonly")
        self.dropdown.pack(pady=5, side="left", padx=10)
        self.dropdown.current(0)  # Set default selection

        ttk.Button(lower_dashboard_frame, text="Select", command=self.__update_current).pack(
            side="left")

        lowest_dashboard_frame = tk.Frame(container)
        lowest_dashboard_frame.pack(fill="y", pady=25)
        self.lowest_dashboard_frame = lowest_dashboard_frame

        balance_frame = tk.Frame(lowest_dashboard_frame)
        balance_frame.pack(fill="y", pady=5, side="right")

        ttk.Label(balance_frame, text="Current Balance:", font=("Arial", 14, "bold")).pack(
            side="left",
            pady=5)

        self.balance_label = ttk.Label(balance_frame,
                                       text=self.current_department.get_balance_overview(),
                                       font=("Arial", 18))

        self.balance_label.pack(side="left", pady=5)

        history_frame = tk.Frame(lowest_dashboard_frame)
        history_frame.pack(fill="y", pady=5, side="left")
        self.history_frame = history_frame

        ttk.Label(history_frame, text=f"Transaction History for {self.current_department.title}", font=("Arial", 14, "bold")).pack(pady=5)

        self.scrollbar = tk.Scrollbar(history_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.transaction_listbox = tk.Listbox(history_frame, yscrollcommand=self.scrollbar.set,
                                              width=60, height=25)
        self.transaction_listbox.pack(side="left", fill="y")
        self.scrollbar.config(command=self.transaction_listbox.yview)

        # Populate transactions
        self.populate_transactions()

    def populate_transactions(self):
        """Populate transaction list"""
        self.transaction_listbox.delete(0, tk.END)
        for transaction in self.current_department.get_account().get_history():
            self.transaction_listbox.insert(tk.END, str(transaction))

    def __update_current(self):
        """Updates the currently selected department for balance calculations."""

        selected_dept_name = self.selected_option.get()

        logger.info(f"selecting department {selected_dept_name}")

        # Find the corresponding department object
        self.current_department = next(
            (dept for dept in DBAccess.get_all_departements() if dept.title == selected_dept_name),
            None
        )
        self.balance_label.configure(text=self.current_department.get_balance_overview())
        self.populate_transactions()
