from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from database import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.String(20), unique=True, nullable=False)  # รหัสนักศึกษา
    first_name = db.Column(db.String(100), nullable=False)  # ชื่อจริง
    faculty = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)  # สาขา
    year = db.Column(db.Integer, nullable=False)  # ชั้นปี
    email = db.Column(db.String(120), unique=True, nullable=False)  # อีเมล
    phone = db.Column(db.String(20), nullable=False)  # เบอร์โทร

    password = db.Column(db.String(255), nullable=False)  # รหัสผ่าน (hash)

    role = db.Column(db.String(20), nullable=False, default="student")
    last_login = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Bangkok")),
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Bangkok")),
    )

    def update_last_login(self):
        self.last_login = datetime.now(ZoneInfo("Asia/Bangkok"))
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "first_name": self.first_name,
            "faculty": self.faculty,
            "major": self.major,
            "year": self.year,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else "-"
            ),
        }

    def __repr__(self):
        return f"<Student {self.student_id} - {self.first_name}>"
