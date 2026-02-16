# UBU Science Engage System

##  Project Description
This project is a RESTful Web API developed as a team assignment.
The system demonstrates route structure according to framework standards.
Each team member is responsible for maintaining at least 2 routes.

---

##  Tech Stack

- Backend: Python
- Framework: Flask
- Database: SQLite
- Version Control: Git + GitHub
- Environment: Python Virtual Environment (venv)

---

##  Installation Guide

### 1️ Clone Repository
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2️ Create Virtual Environment
```bash
python -m venv venv
```

### 3️ Activate Virtual Environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac / Linux**
```bash
source venv/bin/activate
```

### 4️ Install Required Packages
```bash
pip install -r requirements.txt
```

### 5️ Run Application
```bash
python app.py
```

Server will run at:
```
http://127.0.0.1:5000/
```

---

##  Project Structure

```
project-name/
│
├── app.py
├── routes/
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── product_routes.py
│   ├── order_routes.py
│
├── models/
│   └── user_model.py
│
├── requirements.txt
└── README.md
```

---

##  API Routes & Maintainers

| Route | Method | Description | Maintainer |
|-------|--------|------------|------------|
| /login | POST | User login | นาย A |
| /register | POST | User registration | นาย A |
| /users | GET | Get all users | นาย B |
| /profile | GET | Get user profile | นาย B |
| /products | GET | Get product list | นาย C |
| /products | POST | Create product | นาย C |
| /orders | GET | Get order list | นาย D |
| /checkout | POST | Create order | นาย D |

>  Each team member maintains at least 2 routes.

---

##  Framework Route Standard Example

Example (Flask Blueprint):

```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return {"message": "Login successful"}
```

In `app.py`:

```python
from flask import Flask
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
```

---





##  Notes

- All routes are structured under `/routes` directory.
- The project follows standard Flask routing conventions.
- GitHub is used for version control and collaboration.
- Every member contributes to at least 2 routes as required.

---

## License

This project is developed for educational purposes.


