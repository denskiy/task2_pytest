# TRN Database Validation Tests


## Overview
This project includes automated data validation tests for the TRN database using Pytest, ensuring the integrity and validity of data across various tables like employees, dependents, and countries.


## Prerequisites
Python 3.8 or newer
SQL Server (local setup or cloud instance)
Access to TRN database with configured tables


## Installation
Set up a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For UNIX/Linux/MacOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```


## Configuration
Environment Setup: Copy .env.example to a new file and rename it to .env. Update this file with your database credentials and other necessary details:
```bash
cp .env.example .env
# Now edit .env with your specific configurations
```
Ensure to replace placeholder values in .env with actual data:
```bash
SERVER='your_actual_server'
DATABASE='TRN'
USERNAME='your_actual_username'
PASSWORD='your_actual_password'
```
Database Connection: The project will use the information in .env to connect to your SQL Server. Ensure the credentials match your database settings.


## Running Tests
Execute the tests using the following command:
```bash
pytest
```

## Report Generation
To generate an HTML report after test execution using pytest-html, use:
```bash
pytest --html=report.html
```


## Troubleshooting
If issues arise:
Review console errors.
Ensure .env configurations are valid.
Confirm appropriate SQL Server user permissions.