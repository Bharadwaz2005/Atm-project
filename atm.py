from database import Database

class ATM:
    def __init__(self):
        self.db = Database()

    def create_account(self):
        print("\n========== CREATE ACCOUNT ==========")
        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        account = input("Create account number: ").strip()
        if not account.isdigit() or len(account) < 6:
            print("Account number must contain at least 6 digits.")
            return
        account = int(account)
        if self.db.get_account(account):
            print("Account number already exists.")
            return
        pin = input("Create 4-digit PIN: ").strip()
        if len(pin) != 4 or not pin.isdigit():
            print("PIN must contain exactly 4 digits.")
            return
        try:
            balance = float(input("Enter initial deposit: ₹"))
            if balance < 0:
                print("Initial deposit cannot be negative.")
                return
        except ValueError:
            print("Enter a valid amount.")
            return
        if self.db.create_account(account, name, pin, balance):
            print("\nAccount created successfully.")
            print(f"Account Number: {account}")
        else:
            print("Account creation failed.")

    def login(self):
        print("\n========== LOGIN ==========")
        account = input("Enter account number: ").strip()
        if not account.isdigit():
            print("Invalid account number.")
            return None
        account = int(account)
        data = self.db.get_account(account)
        if not data:
            print("Account not found.")
            return None
        for attempt in range(3):
            pin = input("Enter PIN: ").strip()
            if pin == data[2]:
                print(f"\nWelcome, {data[1]}!")
                return account
            remaining = 2 - attempt
            if remaining > 0:
                print(f"Incorrect PIN. Attempts left: {remaining}")
        print("Login failed.")
        return None

    def check_balance(self, account):
        data = self.db.get_account(account)
        if data:
            print(f"\nAvailable Balance: ₹{data[3]:.2f}")

    def deposit(self, account):
        try:
            amount = float(input("Enter deposit amount: ₹"))
            if amount <= 0:
                print("Enter a valid amount.")
                return
            data = self.db.get_account(account)
            new_balance = data[3] + amount
            self.db.update_balance(account, new_balance)
            self.db.add_transaction(account, "Deposit", amount)
            print(f"₹{amount:.2f} deposited successfully.")
            print(f"New Balance: ₹{new_balance:.2f}")
        except ValueError:
            print("Enter a valid amount.")

    def withdraw(self, account):
        try:
            amount = float(input("Enter withdrawal amount: ₹"))
            data = self.db.get_account(account)
            if amount <= 0:
                print("Enter a valid amount.")
                return
            if amount % 100 != 0:
                print("Amount must be a multiple of ₹100.")
                return
            # The database is updated only after all withdrawal checks pass.
            if amount > data[3]:
                print("Insufficient balance.")
                return
            new_balance = data[3] - amount
            self.db.update_balance(account, new_balance)
            self.db.add_transaction(account, "Withdrawal", amount)
            print(f"Please collect ₹{amount:.2f}")
            print(f"Remaining Balance: ₹{new_balance:.2f}")
        except ValueError:
            print("Enter a valid amount.")

    def transfer(self, account):
        receiver = input("Enter receiver account number: ").strip()
        if not receiver.isdigit():
            print("Invalid account number.")
            return
        receiver = int(receiver)
        if receiver == account:
            print("Cannot transfer money to your own account.")
            return
        sender_data = self.db.get_account(account)
        receiver_data = self.db.get_account(receiver)
        if not receiver_data:
            print("Receiver account not found.")
            return
        try:
            amount = float(input("Enter transfer amount: ₹"))
            if amount <= 0:
                print("Enter a valid amount.")
                return
            if amount > sender_data[3]:
                print("Insufficient balance.")
                return
            print(f"Receiver Name: {receiver_data[1]}")
            confirm = input("Confirm transfer? (y/n): ").strip().lower()
            if confirm != "y":
                print("Transfer cancelled.")
                return
            sender_balance = sender_data[3] - amount
            receiver_balance = receiver_data[3] + amount
            self.db.update_balance(account, sender_balance)
            self.db.update_balance(receiver, receiver_balance)
            self.db.add_transaction(account, f"Transfer to {receiver}", amount)
            self.db.add_transaction(receiver, f"Received from {account}", amount)
            print(f"₹{amount:.2f} transferred successfully.")
        except ValueError:
            print("Enter a valid amount.")

    def mini_statement(self, account):
        transactions = self.db.get_transactions(account)
        print("\n========== MINI STATEMENT ==========")
        if not transactions:
            print("No transactions found.")
            return
        for transaction in transactions:
            transaction_type = transaction[0]
            amount = transaction[1]
            date = transaction[2]
            print(f"{date} | {transaction_type} | ₹{amount:.2f}")

    def change_pin(self, account):
        data = self.db.get_account(account)
        old_pin = input("Enter current PIN: ").strip()
        if old_pin != data[2]:
            print("Incorrect current PIN.")
            return
        new_pin = input("Enter new 4-digit PIN: ").strip()
        if len(new_pin) != 4 or not new_pin.isdigit():
            print("PIN must contain exactly 4 digits.")
            return
        if new_pin == old_pin:
            print("New PIN must be different from the old PIN.")
            return
        confirm_pin = input("Confirm new PIN: ").strip()
        if new_pin != confirm_pin:
            print("PINs do not match.")
            return
        self.db.update_pin(account, new_pin)
        print("PIN changed successfully.")

    def menu(self, account):
        while True:
            print("\n========== ATM MENU ==========")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. Mini Statement")
            print("6. Change PIN")
            print("7. Logout")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.check_balance(account)
            elif choice == "2":
                self.deposit(account)
            elif choice == "3":
                self.withdraw(account)
            elif choice == "4":
                self.transfer(account)
            elif choice == "5":
                self.mini_statement(account)
            elif choice == "6":
                self.change_pin(account)
            elif choice == "7":
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Try again.")

    def start(self):
        while True:
            print("\n********************************")
            print("        PYTHON ATM SYSTEM")
            print("********************************")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.create_account()
            elif choice == "2":
                account = self.login()
                if account:
                    self.menu(account)
            elif choice == "3":
                self.db.close()
                print("Thank you for using the ATM.")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    atm = ATM()
    atm.start()
