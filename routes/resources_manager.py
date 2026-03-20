from flask import render_template, request, redirect, url_for, jsonify
from models.equipment import Equipment
from models.place import Place
from models.place_equipment import PlaceEquipment
from database import db

import os
from werkzeug.utils import secure_filename


def register_resources_routes(app):
    # Manage Page
    @app.route("/resources/manage")
    def manage_resources():

        places = Place.query.order_by(Place.name).all()
        equipments = Equipment.query.order_by(Equipment.name).all()

        return render_template(
            "resources_manager.html", places=places, equipments=equipments
        )

    # ADD PLACE
    @app.route("/add_place", methods=["POST"])
    def add_place():

        name = request.form.get("name")
        description = request.form.get("description")
        officer_name = request.form.get("officer_name")
        officer_phone = request.form.get("officer_phone")
        equipment_ids = request.form.getlist("equipments[]")
        status = bool(int(request.form.get("status")))

        image_file = request.files.get("image")

        image_path = None

        if image_file and image_file.filename != "":

            filename = secure_filename(image_file.filename)

            upload_folder = "static/uploads"
            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)

            image_file.save(filepath)

            image_path = "/" + filepath

        new_place = Place(
            name=name,
            description=description,
            officer_name=officer_name,
            officer_phone=officer_phone,
            status=status,
            image=image_path,
        )

        db.session.add(new_place)
        db.session.commit()

        # เพิ่มอุปกรณ์ + ลด stock
        for eq_id in equipment_ids:

            eq_id = int(eq_id)

            qty = int(request.form.get(f"qty_{eq_id}", 0))

            equipment = Equipment.query.get(eq_id)

            if not equipment:
                continue

            # กันใส่เกินจำนวน
            if qty > equipment.available_quantity:
                qty = equipment.available_quantity

            if qty > 0:

                # ลดจำนวนคงเหลือ
                equipment.available_quantity -= qty

                pe = PlaceEquipment(
                    place_id=new_place.id, equipment_id=eq_id, quantity=qty
                )

                db.session.add(pe)

        db.session.commit()

        return redirect(url_for("manage_resources"))

    # UPDATE PLACE
    # UPDATE PLACE
    @app.route("/places/update/<int:id>", methods=["POST"])
    def update_place(id):

        place = Place.query.get_or_404(id)

        place.name = request.form.get("name")
        place.description = request.form.get("description")
        place.officer_name = request.form.get("officer_name")
        place.officer_phone = request.form.get("officer_phone")
        place.status = bool(int(request.form.get("status", 1)))

        # ----------- รับรูปใหม่ -----------
        image_file = request.files.get("image")

        if image_file and image_file.filename != "":

            filename = secure_filename(image_file.filename)

            upload_folder = "static/uploads"
            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)

            image_file.save(filepath)

            place.image = "/" + filepath
        # ----------------------------------

        selected_ids = request.form.getlist("equipments[]")

        for eq_id in selected_ids:

            eq_id = int(eq_id)
            qty = int(request.form.get(f"qty_{eq_id}", 0))

            equipment = Equipment.query.get(eq_id)

            relation = PlaceEquipment.query.filter_by(
                place_id=id, equipment_id=eq_id
            ).first()

            if relation:

                diff = qty - relation.quantity
                equipment.available_quantity -= diff

                relation.quantity = qty

            else:

                if equipment.available_quantity >= qty:

                    equipment.available_quantity -= qty

                    new_relation = PlaceEquipment(
                        place_id=id, equipment_id=eq_id, quantity=qty
                    )

                    db.session.add(new_relation)

        db.session.commit()

        return redirect(url_for("manage_resources"))

    # DELETE PLACE
    @app.route("/places/delete/<int:id>", methods=["POST"])
    def delete_place(id):

        place = Place.query.get_or_404(id)

        db.session.delete(place)
        db.session.commit()

        return redirect(url_for("manage_resources"))

    # ADD EQUIPMENT
    @app.route("/equipment/add", methods=["POST"])
    def add_equipment():

        equipment = Equipment(
            code=request.form.get("code"),
            name=request.form.get("name"),
            category=request.form.get("category"),
            total_quantity=request.form.get("total_quantity"),
            available_quantity=request.form.get("available_quantity"),
            department=request.form.get("department"),
        )

        db.session.add(equipment)
        db.session.commit()

        return redirect(url_for("manage_resources"))

    # UPDATE EQUIPMENT
    @app.route("/equipment/update/<int:id>", methods=["POST"])
    def update_equipment(id):

        equipment = Equipment.query.get_or_404(id)

        equipment.code = request.form.get("code")
        equipment.name = request.form.get("name")
        equipment.category = request.form.get("category")
        equipment.total_quantity = request.form.get("total_quantity")
        equipment.available_quantity = request.form.get("available_quantity")
        equipment.department = request.form.get("department")

        db.session.commit()

        return redirect(url_for("manage_resources"))

    # DELETE EQUIPMENT
    @app.route("/equipment/delete/<int:id>", methods=["POST"])
    def delete_equipment(id):

        equipment = Equipment.query.get_or_404(id)

        # ลบ relation ก่อน
        PlaceEquipment.query.filter_by(equipment_id=id).delete(
            synchronize_session=False
        )

        # ลบ equipment
        db.session.delete(equipment)

        db.session.commit()

        return redirect(url_for("manage_resources"))

    # ADD EQUIPMENT TO PLACE
    @app.route("/place/add_equipment", methods=["POST"])
    def add_equipment_to_place():

        place_id = int(request.form.get("place_id"))
        equipment_id = int(request.form.get("equipment_id"))
        quantity = int(request.form.get("quantity"))

        relation = PlaceEquipment(
            place_id=place_id, equipment_id=equipment_id, quantity=quantity
        )

        db.session.add(relation)
        db.session.commit()

        return redirect(url_for("manage_resources"))

    # API: GET PLACES FOR REVIEW PAGE
    @app.route("/api/places")
    def api_places():

        places = Place.query.all()

        data = []

        for p in places:

            equipments = []

            for pe in p.equipments:
                if pe.equipment:  # เช็คก่อนว่า equipment ยังอยู่
                    equipments.append(
                        {"name": pe.equipment.name, "quantity": pe.quantity}
                    )

            data.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "status": p.status,
                    "image": p.image,
                    "officer_name": p.officer_name,
                    "officer_phone": p.officer_phone,
                    "equipments": equipments,
                }
            )

        return jsonify(data)

    # API EQUIPMENTS
    @app.route("/api/equipments")
    def api_equipments():

        equipments = Equipment.query.all()

        data = []

        for e in equipments:

            data.append(
                {
                    "code": e.code,
                    "name": e.name,
                    "category": e.category,
                    "total_quantity": e.total_quantity,
                    "available_quantity": e.available_quantity,
                    "department": e.department,
                }
            )

        return jsonify(data)
