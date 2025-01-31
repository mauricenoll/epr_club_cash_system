import tkinter as tk
from tkinter import ttk, messagebox
from app.auth_provider import AuthProvider
from app.db.db_access import get_departements


class TransactionPage(tk.Frame):

    def __init__(self, parent, controller, auth_provider):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.auth_provider = auth_provider


class WithdrawalPage(TransactionPage):

    def __init__(self, parent, controller, auth_provider):
        TransactionPage.__init__(self, parent, controller, auth_provider)

        title_label = ttk.Label(self, text="Make a Withdrawal!", font=("Arial", 18))
        title_label.grid(row=1, column=1, pady=15)

        balance_label = ttk.Label(self,
                                  text=f"Current balance: {self.auth_provider.logged_in_user.departement.account.get_formatted_balance()}",
                                  font=("Arial", 14))
        balance_label.grid(row=2, column=1, pady=15)

        entry_label = ttk.Label(self, text="Amount in €:")
        entry_label.grid(row=3, column=0, pady=15, padx=4, sticky="w")

        self.amount_entry = ttk.Entry(self, width=25, )
        self.amount_entry.grid(row=3, column=1, pady=15, padx=4, sticky="w")

        withdrawal_button = ttk.Button(self, text="Withdraw", command=self.validate_withdrawal)
        withdrawal_button.grid(row=5, column=1)

    def validate_withdrawal(self):
        input = self.amount_entry.get()

        input.replace("€", "")  # replacing symbol
        input.replace(",", ".")
        account = self.auth_provider.logged_in_user.departement.account
        try:
            amount = int(float(input) * 100)  # convert to cents
            if amount > account.current_balance:
                messagebox.showerror("error", f"Not enough funds for this transaction!")
            else:
                account.withdraw(amount)
                messagebox.showinfo("Withdrawal successful", "Withdrawal successful")
                self.controller.show_frame("TreasurerDashboard")

        except ValueError:
            messagebox.showerror("error", f"{input} is not a valid number!")


class DepositPage(TransactionPage):

    def __init__(self, parent, controller, auth_provider):
        TransactionPage.__init__(self, parent, controller, auth_provider)

        title_label = ttk.Label(self, text="Make a Deposit!", font=("Arial", 18))
        title_label.grid(row=1, column=1, pady=15)

        balance_label = ttk.Label(self,
                                  text=f"Current balance: {self.auth_provider.logged_in_user.departement.account.get_formatted_balance()}",
                                  font=("Arial", 14))
        balance_label.grid(row=2, column=1, pady=15)

        entry_label = ttk.Label(self, text="Amount in €:")
        entry_label.grid(row=3, column=0, pady=15, padx=4, sticky="w")

        self.amount_entry = ttk.Entry(self, width=25, )
        self.amount_entry.grid(row=3, column=1, pady=15, padx=4, sticky="w")

        withdrawal_button = ttk.Button(self, text="Deposit", command=self.validate_deposit)
        withdrawal_button.grid(row=5, column=1)

    def validate_deposit(self):
        input = self.amount_entry.get()

        input.replace("€", "")  # replacing symbol
        input.replace(",", ".")

        try:
            amount = int(float(input) * 100)  # convert to cents
            self.auth_provider.logged_in_user.departement.account.deposit(amount)
            messagebox.showinfo("Deposit successful", "Deposit successful")
            self.controller.show_frame("TreasurerDashboard")

        except ValueError:
            messagebox.showerror("error", f"{input} is not a valid number!")


class TransferPage(TransactionPage):

    def __init__(self, parent, controller, auth_provider):
        TransactionPage.__init__(self, parent, controller, auth_provider)

        ttk.Label(self, text="Make a Transfer!", font=("Arial", 18)).pack()

        ttk.Label(self,
                  text=f"Current balance: {self.auth_provider.logged_in_user.departement.account.get_formatted_balance()}",
                  font=("Arial", 14)).pack()

        ttk.Label(self, text="Amount in €:").pack()

        self.amount_entry = ttk.Entry(self, width=25)
        self.amount_entry.pack()

        self.options = get_departements()
        self.selected_option = tk.StringVar()

        self.dropdown = ttk.Combobox(self, textvariable=self.selected_option, values=self.options,
                                     state="readonly")
        self.dropdown.pack(pady=5)
        self.dropdown.current(0)  # Set default selection

        withdrawal_button = ttk.Button(self, text="Transfer", command=self.validate_transfer)
        withdrawal_button.pack()

    def validate_transfer(self):
        input = self.amount_entry.get()

        input.replace("€", "")  # replacing symbol
        input.replace(",", ".")

        account = self.auth_provider.logged_in_user.departement.account

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
            receiverID = [dep for dep in get_departements() if dep.title == option][0].id
            account.transfer(receivingAccountID=receiverID, amount=amount)
            messagebox.showinfo("Transfer successful", "Transfer successful")
            self.controller.show_frame("TreasurerDashboard")
