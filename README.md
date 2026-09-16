Python ATM Project
This is a simple ATM project made using Python. It allows users to create an account, log in, check balance, deposit money, withdraw money, and view transactions.
The project uses a separate Python file for the ATM program, a database connection file, and a JSON file to store user data.
Project Files
ATM-Project/
│
├── atm.py
├── database.py
├── database.json
└── README.md
1. atm.py
Main Python program. It contains the ATM operations and user menu.
2. database.py
Handles reading and saving user data in the database.
3. database.json
Stores the account details and transaction data.
Requirements
Python 3
Any code editor (VS Code, PyCharm, Notepad++, etc.)
No extra Python libraries are required.
How to Run
Step 1: Install Python
Download and install Python 3 on your computer.
Check if Python is installed:
python --version
or:
python3 --version
Step 2: Download the Project
Download or clone this project from GitHub.
git clone YOUR_GITHUB_REPOSITORY_LINK
Then open the project folder.
Step 3: Check the Files
Make sure these files are in the same folder:
atm.py
database.py
database.json
Step 4: Run the Program
Open the terminal inside the project folder and run:
python atm.py
If your system uses python3, run:
python3 atm.py
Step 5: Use the ATM
Follow the options shown on the screen.
You can:
Create an account
Login
Check balance
Deposit money
Withdraw money
View transactions
Logout
Exit
Database
The project uses database.json to store the account information.
When you create an account or make a transaction, the data is saved in the JSON file.
Example
===== ATM =====

1. Create Account
2. Login
3. Exit

Enter your choice:
After logging in, you can access the ATM menu and perform different operations.
Important
Keep atm.py, database.py, and database.json in the same folder.
Do not delete database.json, because it contains the stored account data.
Project Purpose
This project was created to practice Python programming, functions, file handling, JSON data, database-style operations, and menu-based programs.
Author
Bharadhwaj K
