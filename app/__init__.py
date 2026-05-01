from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from app.routes.employees import employees
from app.routes.auth import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    jwt = JWTManager(app)
    
    app.register_blueprint(employees)
    app.register_blueprint(auth)
    
    return app