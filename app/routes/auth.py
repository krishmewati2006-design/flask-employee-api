from flask import Blueprint
from app.database import get_db_connection
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"Error": "Please Fill The Relevant Fields"}), 400
    
    if not isinstance(data, dict):
        return jsonify({"Error": "Invalid JSON format"}), 400
    
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({"Error": "Username Or Password Is Missing"}), 400

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

@auth.route('/login', methods=['POST'])
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

@auth.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    current_username = get_jwt_identity()
    return jsonify(logged_in_as=current_username), 200