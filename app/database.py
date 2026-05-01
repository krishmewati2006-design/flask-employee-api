'''

'''
import sqlite3

employees = [
    {"name": "Rohit", "department": "Engineering", "salary": 75000},
    {"name": "Priya", "department": "HR", "salary": 42000},
    {"name": "Aman", "department": "Engineering", "salary": 91000},
    {"name": "Neha", "department": "Marketing", "salary": 38000},
    {"name": "Karan", "department": "Engineering", "salary": 55000}
]
def get_db_connection():
    connection = sqlite3.connect('employees.db')
    return connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               department TEXT NOT NULL,
               salary INTEGER
               )
''')


query = "INSERT INTO employees (name, department, salary) VALUES (:name, :department, :salary)"

cursor.execute("SELECT COUNT(*) from employees")
count = cursor.fetchone()[0]
if count == 0:
    cursor.executemany(query, employees)
 
cursor.execute("SELECT * from employees")

fetch = cursor.fetchall()

for index, employee, depart, sal in fetch:
    print(f"{index}. {employee} | {depart} | ₹{sal}")

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL
               )
''')

users_query = "INSERT INTO users (username, password) VALUES (:username, :password)"
conn.commit()

cursor.close()

