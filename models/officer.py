from datetime import datetime
from database import db
from sqlalchemy.sql import func


class Officer(db.Model):
    __tablename__ = "officers"

    id = db.Column(db.Integer, primary_key=True)

    officer_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "officer_id": self.officer_id,
            "full_name": self.full_name,
            "department": self.department,
            "email": self.email,
            "phone": self.phone,
            "last_login": (
                self.last_login.strftime("%Y-%m-%d %H:%M:%S")
                if self.last_login
                else None
            ),
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else None
            ),
        }
