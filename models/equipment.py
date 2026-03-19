from database import db


class Equipment(db.Model):
    __bind_key__ = "resources"
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    total_quantity = db.Column(db.Integer)
    available_quantity = db.Column(db.Integer)
    department = db.Column(db.String(255))
