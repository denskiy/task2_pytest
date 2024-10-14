import pytest
import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

# SERVER = os.getenv('SERVER')
# DATABASE = os.getenv('DATABASE')
# UID = os.getenv('UID')
# PWD = os.getenv('PWD')

SERVER = 'EPAMYERW01C7\\SQLEXPRESS'
DATABASE = 'TRN'
UID = 'LastUser'
PWD = 'NewLastPassword17'

@pytest.fixture(scope='module')
def db_conn():
    conn = pymssql.connect(server=SERVER, user=UID, password=PWD, database=DATABASE)
    yield conn


def test_primary_key_integrity_employees(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(DISTINCT employee_id) AS distinct_ids,
                   COUNT(*) AS total_rows
            FROM hr.Employees
        """)
        result = cursor.fetchone()
        assert result[0] == result[1], "Employee_id should be unique and not null"


def test_salary_range_employees(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) AS out_of_range
            FROM hr.Employees
            WHERE salary < 1000 OR salary > 100000
        """)
        result = cursor.fetchone()
        assert result[0] == 0, "All salaries should be between $1,500 and $100,000"


def test_foreign_key_constraints_dependents(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) AS orphans
            FROM hr.Dependents d
            WHERE NOT EXISTS (
                SELECT 1 FROM hr.Employees e
                WHERE e.employee_id = d.employee_id
            )
        """)
        result = cursor.fetchone()
        assert result[0] == 0, "All dependents should reference a valid employee"


def test_dependent_names_completeness(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) AS incomplete_names
            FROM hr.Dependents
            WHERE first_name IS NULL OR last_name IS NULL OR LEN(first_name) = 0 OR LEN(last_name) = 0
        """)
        result = cursor.fetchone()
        assert result[0] == 0, "All dependents should have non-null and non-empty first and last names"


def test_region_id_values_countries(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(DISTINCT c.region_id) AS total_regions_in_countries,
                   COUNT(DISTINCT r.region_id) AS total_valid_regions
            FROM hr.Countries c
            JOIN hr.Regions r ON c.region_id = r.region_id
        """)
        result = cursor.fetchone()
        assert result[0] == result[1], "All Region IDs should exist in Regions table"


def test_country_id_uniqueness(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT country_id, COUNT(*)
            FROM hr.Countries
            GROUP BY country_id
            HAVING COUNT(*) > 1
        """)
        result = cursor.fetchall()
        assert len(result) == 0, "Country_id should be unique"
