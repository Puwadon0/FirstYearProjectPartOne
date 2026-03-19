from database import db


class PlaceEquipment(db.Model):
    __bind_key__ = "resources"
    __tablename__ = "place_equipment"

    id = db.Column(db.Integer, primary_key=True)

    place_id = db.Column(db.Integer, db.ForeignKey("place.id"), nullable=False)

    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1)

    place = db.relationship("Place", back_populates="equipments")
    equipment = db.relationship("Equipment")
