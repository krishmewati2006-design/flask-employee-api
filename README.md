# Flask Employee API

A RESTful Employee Management API built using Flask, SQLite, and JWT Authentication.

This project demonstrates backend development concepts including CRUD operations, authentication, API structuring, database integration, and deployment.

---

## Features

- Employee CRUD Operations
- JWT Authentication
- SQLite Database Integration
- RESTful API Architecture
- Flask Blueprints
- Input Validation
- JSON Responses
- Environment Variable Support
- Deployment Ready
- Modular Project Structure

---

## Tech Stack

### Backend
- Python
- Flask
- Flask-JWT-Extended
- SQLite
- SQLAlchemy

### Tools & Deployment
- Git & GitHub
- Render
- Postman

---

## Live API

https://flask-employee-api.onrender.com

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/krishmewati2006-design/flask-employee-api.git
cd flask-employee-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python run.py
```

or

```bash
flask run
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register new user |
| POST | `/login` | Login and receive JWT token |

---

### Employees

| Method | Endpoint | Description |
|---|---|---|
| GET | `/employees` | Get all employees |
| GET | `/employees/<name>` | Get employee by name |
| POST | `/employees` | Create employee |
| PUT | `/employees/<name>` | Update employee |
| DELETE | `/employees/<name>` | Delete employee |

---

## Example JSON

### Create Employee

```json
{
  "name": "John Doe",
  "position": "Backend Developer",
  "salary": 50000
}
```

---

## Project Structure

```bash
flask-employee-api/
│
├── app/
│   ├── routes/
│   ├── models/
│   ├── auth/
│   ├── __init__.py
│
├── instance/
├── migrations/
├── requirements.txt
├── run.py
├── .env
└── README.md
```

---

## What I Learned

This project helped me understand:

- REST API Design
- JWT Authentication
- Flask Blueprints
- Database Relationships
- CRUD Operations
- API Testing with Postman
- Backend Deployment
- Clean Backend Architecture

---

## Author

Krish Mewati

GitHub:
https://github.com/krishmewati2006-design

---

## License

This project is open-source and available under the MIT License.