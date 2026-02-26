from datetime import datetime
from database import db


class ClubMember(db.Model):
    __tablename__ = "club_members"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.String(20), db.ForeignKey("students.student_id"), nullable=False
    )

    position = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)

    student = db.relationship("Student", backref="club_members")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student.student_id,
            "first_name": self.student.first_name,
            "faculty": self.student.faculty,
            "major": self.student.major,
            "year": self.student.year,
            "email": self.student.email,
            "phone": self.student.phone,
            "last_login": (
                self.student.last_login.strftime("%Y-%m-%d %H:%M")
                if self.student.last_login
                else None
            ),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "position": self.position,
        }
