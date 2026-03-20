from database import db


class Place(db.Model):
    __bind_key__ = "resources"
    __tablename__ = "place"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    officer_name = db.Column(db.String(255))
    officer_phone = db.Column(db.String(20))
    status = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(255))

    equipments = db.relationship(
        "PlaceEquipment", back_populates="place", cascade="all, delete-orphan"
    )
