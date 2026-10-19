# Bank Account Simulator: Create an OOP-based program to simulate bank account operations 
# (deposit, withdrawal, check balance) with error handling for invalid operations. 
# Make sure to use CRUD operations with MySQL to persist data, instead of just runtime.


import mysql.connector as connector

class BankAccount:
    def __init__(self):
        self.con = connector.connect(host='localhost', port='3306', user='root', password='Zig11Dhw@ni', database='bankAccount')

        query = """
        CREATE TABLE IF NOT EXISTS bank_account (
            accountId INT PRIMARY KEY,
            accountHolder VARCHAR(200),
            balance DECIMAL(12, 2) DEFAULT 0.00
        )
        """
        cursor = self.con.cursor()
        cursor.execute(query)
        print("Bank Account Table Created")

    # Create Account
    def create_account(self, accountId, accountHolder, balance):
        if not accountHolder.strip():
            print("Account holder name cannot be empty")
            return

        if balance < 0:
            print("Opening balance cannot be negative")
            return

        query = """
        INSERT INTO bank_account (accountId, accountHolder, balance)
        VALUES (%s, %s, %s)
        """
        cursor = self.con.cursor()

        try:
            cursor.execute(query, (accountId, accountHolder, balance))
            self.con.commit()
            print("Bank Account Created Successfully")

        except connector.Error as e:
            self.con.rollback()
            print("Error:", e)

    # Fetch All Accounts
    def fetch_all_accounts(self):
        query = "SELECT * FROM bank_account"
        cursor = self.con.cursor()
        cursor.execute(query)

        for row in cursor:
            print("Account ID:", row[0])
            print("Account Holder:", row[1])
            print("Balance:", row[2])
            print("----------------------------")

    # Fetch Specific Account
    def fetch_account(self, accountId):
        query = "SELECT * FROM bank_account WHERE accountId = %s"
        cursor = self.con.cursor()
        cursor.execute(query, (accountId,))

        row = cursor.fetchone()

        if row:
            print("Account ID:", row[0])
            print("Account Holder:", row[1])
            print("Balance:", row[2])
        else:
            print("Account Not Found")

    # Deposit Money
    def deposit(self, accountId, amount):
        if amount <= 0:
            print("Deposit amount must be greater than zero")
            return

        query = """
        UPDATE bank_account
        SET balance = balance + %s
        WHERE accountId = %s
        """

        cursor = self.con.cursor()
        cursor.execute(query, (amount, accountId))

        if cursor.rowcount == 0:
            print("Account Not Found")
        else:
            self.con.commit()
            print("Money Deposited Successfully")

    # Withdraw Money
    def withdraw(self, accountId, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero")
            return

        query = """
        UPDATE bank_account
        SET balance = balance - %s
        WHERE accountId = %s AND balance >= %s
        """

        cursor = self.con.cursor()
        cursor.execute(query, (amount, accountId, amount))

        if cursor.rowcount == 0:
            self.con.rollback()

            check_query = """
            SELECT balance FROM bank_account WHERE accountId = %s
            """
            cursor.execute(check_query, (accountId,))
            row = cursor.fetchone()

            if row is None:
                print("Account Not Found")
            else:
                print("Insufficient Balance")
        else:
            self.con.commit()
            print("Money Withdrawn Successfully")

    # Check Balance
    def check_balance(self, accountId):
        query = """
        SELECT accountHolder, balance
        FROM bank_account
        WHERE accountId = %s
        """

        cursor = self.con.cursor()
        cursor.execute(query, (accountId,))
        row = cursor.fetchone()

        if row:
            print("Account Holder:", row[0])
            print("Current Balance:", row[1])
        else:
            print("Account Not Found")

    # Update Account Holder
    def update_account(self, accountId, newName):
        if not newName.strip():
            print("Account holder name cannot be empty")
            return

        query = """
        UPDATE bank_account
        SET accountHolder = %s
        WHERE accountId = %s
        """

        cursor = self.con.cursor()
        cursor.execute(query, (newName, accountId))

        if cursor.rowcount == 0:
            print("Account Not Found")
        else:
            self.con.commit()
            print("Account Updated Successfully")

    # Delete Account
    def delete_account(self, accountId):
        query = "DELETE FROM bank_account WHERE accountId = %s"
        cursor = self.con.cursor()
        cursor.execute(query, (accountId,))

        if cursor.rowcount == 0:
            print("Account Not Found")
        else:
            self.con.commit()
            print("Account Deleted Successfully")


# ------------ Main Coding ------------

bank = BankAccount()

# Create Account
# bank.create_account(101, "Dhwani", 5000)
# bank.create_account(102, "Dhyey", 3000)

# Fetch All Accounts
# bank.fetch_all_accounts()

# Fetch Specific Account
# bank.fetch_account(101)

# Deposit Money
# bank.deposit(101, 1000)

# Withdraw Money
# bank.withdraw(101, 500)

# Check Balance
# bank.check_balance(101)

# Update Account Holder
# bank.update_account(101, "Dhvani")

# Delete Account
# bank.delete_account(102)

bank.con.close()
