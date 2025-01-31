# This is the ReadMe for our Virtual Club System

as a start, if you're running this in VS Code make sure that
- ``
"terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}"
  }
``

is added to your VSCode setting.json (F1 → Open User Setting (JSON))

## How to:
1. To Start the application, run the main.py file in the app folder
2. PreDefined log ins:
    - Admin login: admin@email.de, password
    - Treasurer Login: treasurer@email.de, password
    - Finance Officer Login: f.officer@email.de, password
3. The Application will initialize a sqllite3 db in the Project Directory
4. There will be predefined Departments but no History, you can add that as you please
