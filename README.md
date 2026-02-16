# UBU Science Engage System

## 📌 Project Description
UBU Science Engage System is a web-based activity and volunteer management system.

The system consists of a Backend API developed with Flask and a Frontend developed using HTML, CSS, and JavaScript with Tailwind CSS and Bootstrap frameworks.

The system includes:
- Authentication
- Activity management
- Document review
- Volunteer registration
- Finance tracking
- Reporting system
- Dashboard overview
- Q&A system

Each team member maintains at least 2 routes as required.

---

# Tech Stack

## Frontend
- HTML5
- CSS3
- JavaScript (Vanilla JS)
- Tailwind CSS
- Bootstrap 5

## Backend
- Language: Python
- Framework: Flask
- Database: SQLite, SQLAlchemy (ORM)
- Version Control: Git & GitHub

---

# ⚙ Installation Guide

## 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/ubu-engage.git
cd ubu-engage
```

---

## 2️⃣ Backend Setup

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Environment

Windows:
```bash
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Backend Server
```bash
python app.py
```

Backend runs at:
```
http://127.0.0.1:5000/
```

---

## 3️⃣ Frontend Setup

Frontend is static-based.

Just open:
```
frontend/index.html
```

Or use Live Server (VS Code recommended).

---

# 📂 Project Structure

```
ubu-engage/
│
├── app.py
├── routes/
│   ├── auth_routes.py
│   ├── activity_routes.py
│   ├── document_routes.py
│   ├── volunteer_routes.py
│   ├── finance_routes.py
│   ├── upload_routes.py
│   ├── dashboard_routes.py
│   ├── report_routes.py
│   ├── resource_routes.py
│   ├── pr_routes.py
│   ├── calendar_routes.py
│   ├── qa_routes.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── css/
│   ├── js/
│
├── models/
├── requirements.txt
└── README.md
```

---

# 🚀 API Routes & Maintainers

| No | Route | Method | Description | Maintainer |
|----|--------|--------|------------|------------|
| 1 | /login | POST | User login | นาย A |
| 2 | /register | POST | User register | นาย A |
| 3 | /activities | POST | Create activity | นาย B |
| 4 | /activities/check | GET | Check activity | นาย B |
| 5 | /documents | POST | Manage documents | นาย C |
| 6 | /documents/review | PUT | Review documents | นาย C |
| 7 | /volunteer/apply | POST | Volunteer registration | นาย D |
| 8 | /activities/register | POST | Register activity (attach evaluation link) | นาย D |
| 9 | /finance | POST | Record expense | นาย E |
| 10 | /upload | POST | Upload files | นาย E |
| 11 | /dashboard | GET | Dashboard overview | นาย F |
| 12 | /reports/upload | POST | Upload project report | นาย F |
| 13 | /resources | GET | Location & equipment aggregation | นาย G |
| 14 | /announcements | POST | Public relations | นาย G |
| 15 | /calendar | GET | Activity calendar | นาย H |
| 16 | /qa | GET/POST | Q&A club & students | นาย H |

> ✅ Each team member is responsible for at least 2 routes.

---

# 🖥 Frontend Pages Overview

| Page | Description |
|------|------------|
| login.html | Login / Register |
| dashboard.html | Dashboard overview |
| activity.html | Create & check activity |
| document.html | Document management |
| volunteer.html | Volunteer registration |
| finance.html | Expense recording |
| calendar.html | Activity calendar |
| qa.html | Q&A page |

---

# Example Flask Route (Standard Blueprint)

```python
from flask import Blueprint, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return {"message": "Login successful"}
```

---

# Notes

- Backend follows Flask Blueprint routing standard.
- Frontend uses Tailwind CSS for utility styling and Bootstrap for components.
- RESTful API structure.
- All routes are separated inside the `/routes` folder.
- Developed for academic purposes.

---

# License
Educational Project – Science Faculty
