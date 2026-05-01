'''
Add a GET /me route that returns the currently logged in user's username. It should be protected — only accessible with a valid token. The token already contains the user's identity.
Look up get_jwt_identity() from flask_jwt_extended. That's your only hint. Go ahead.
'''
from database import get_db_connection
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import sqlite3

employees = [
    {"name": "Rohit", "department": "Engineering", "salary": 75000},
    {"name": "Priya", "department": "HR", "salary": 42000},
    {"name": "Aman", "department": "Engineering", "salary": 91000},
    {"name": "Neha", "department": "Marketing", "salary": 38000},
    {"name": "Karan", "department": "Engineering", "salary": 55000}
]

def read_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * from employees")
    fetch = cursor.fetchall()
    result = []
    for index, employee, depart, sal in fetch:
        new_list = {
            "sno": index,
            "name": employee,
            "department": depart,
            "salary": sal
        }
        result.append(new_list)
    conn.close()
    return result

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "4b625f696e70e96dbb229f258194e39b834453e65d4cb3f502df566bba29d430" 
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    users = cursor.execute("SELECT * from users WHERE username = ?", (username,)).fetchone()
    
    if users:
        conn.close()
        return jsonify({"msg": "User already exists"}), 409
    
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    return jsonify({"Success": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * from users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
       token = create_access_token(identity=username)
       return jsonify(access_token=token), 200

    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    current_username = get_jwt_identity()
    return jsonify(logged_in_as=current_username), 200

@app.route('/employees', methods=['GET'])
@jwt_required()
def read_json():
    try:
        content = read_employees()
        return jsonify(content)
    
    except sqlite3.OperationalError:
        return jsonify({"error": "Operational Error."}), 404


@app.route('/employees/<name>', methods=['GET'])
@jwt_required()
def employee_name(name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM employees WHERE LOWER(name) = LOWER(?)',(name,))
        fetch = cursor.fetchone()
        conn.close()
        if fetch is None:
            return jsonify({"Error": f"Employee {name} Not Found"}), 404
        else:
            index, employee, depart, sal = fetch
            emp_dict = {
                "sno": index,
            "name": employee,
            "department": depart,
            "salary": sal
            }
            return jsonify(emp_dict)
        
    except sqlite3.OperationalError:
        return jsonify({"error": "Operational Error."}), 404
            

@app.route('/employees', methods=['POST'])
@jwt_required()
def add_new_employee():
    data_in = request.get_json()

    if data_in is None:
        return jsonify({"Error": "NO DATA FOUND"}), 404
    
    name = data_in['name']
    department = data_in['department']
    salary = data_in['salary']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE LOWER(name) = LOWER(?)',(name,))
        fetch = cursor.fetchone()
        if fetch is None:
            cursor.execute('INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)', (name, department, salary))
        else:
            return jsonify({"Error": "Employee Already Exists."}), 404

        conn.commit()

        return jsonify({"Success": "Employee Added Successfully"}), 200
        
    except sqlite3.OperationalError:
        return jsonify({"error": "Operational Error."}), 404
    finally:
        conn.close()

@app.route('/employees/<name>', methods=['DELETE'])
@jwt_required()
def remove_employee(name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE LOWER(name) = LOWER(?)',(name,))
        fetch = cursor.fetchone()
        if fetch is None:
            return jsonify({"error": f"Employee '{name}' not found."}), 404
        else:
            cursor.execute('DELETE FROM employees WHERE LOWER(name) = LOWER(?)',(name,))
        
        conn.commit()
        return jsonify({'message': f'Success: Employee {name} removed.'}), 200
        
    except sqlite3.OperationalError:
        return jsonify({"error": "Operational Error."}), 404
    finally:
        conn.close()
    
@app.route('/employees/<name>', methods=['PUT'])
@jwt_required()
def update_salary(name):
    data_in = request.get_json()
    if data_in is None:
        return jsonify({"Error": "NO DATA FOUND"}), 404
    salary = data_in['salary']
    try:
        conn = get_db_connection()
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM employees WHERE LOWER(name) = LOWER(?)',(name,))
        fetch = cursor.fetchone()
        if fetch is None:
            return jsonify({"error": "Employee not found."}), 404
        else:
            cursor.execute("UPDATE employees SET salary = ? WHERE LOWER(name) = LOWER(?)", (salary, name))
        
        conn.commit()
        return jsonify({'Success': f'{name} Salary Has Been Updated.'}), 200
        
    except sqlite3.OperationalError:
        return jsonify({"error": "Operational Error."}), 404
    finally:
        conn.close()
    

if __name__ == '__main__':
    app.run(debug=True)