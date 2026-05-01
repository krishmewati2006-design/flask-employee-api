from flask import Blueprint
from app.database import get_db_connection
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
import sqlite3
employees = Blueprint('employees', __name__)

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


@employees.route('/employees', methods=['GET'])
@jwt_required()
def read_json():
    try:
        content = read_employees()
        return jsonify(content)
    
    except sqlite3.OperationalError:
        return jsonify({"error": "Operational Error."}), 404


@employees.route('/employees/<name>', methods=['GET'])
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
            

@employees.route('/employees', methods=['POST'])
@jwt_required()
def add_new_employee():
    data_in = request.get_json(silent=True)

    if data_in is None:
        return jsonify({"Error": "NO DATA FOUND"}), 404
    
    if not isinstance(data_in, dict):
        return jsonify({"Error": "Invalid JSON format"}), 400
    
    name = data_in.get('name')
    department = data_in.get('department')
    salary = data_in.get('salary')

    if name is None or department is None or salary is None:
        return jsonify({"Error": "Please Fill Every Field"}), 400

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

@employees.route('/employees/<name>', methods=['DELETE'])
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
    
@employees.route('/employees/<name>', methods=['PUT'])
@jwt_required()
def update_salary(name):
    data_in = request.get_json(silent=True)
    if data_in is None:
        return jsonify({"Error": "NO DATA FOUND"}), 404
    
    if not isinstance(data_in, dict):
        return jsonify({"Error": "Invalid JSON format"}), 400
    
    salary = data_in.get('salary')

    if salary is None:
        return jsonify({"Error": "Please Fill Out The Salary Amount"}), 400
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