from datetime import datetime
from database import db
import random
import string


class Question(db.Model):
    __bind_key__ = "qa"
    __tablename__ = "qa_questions"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(10), unique=True, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")

    category = db.Column(db.String(100))

    is_faq = db.Column(db.Boolean, default=False)

    view_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)

    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    answered_at = db.Column(db.DateTime)
