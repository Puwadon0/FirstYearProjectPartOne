from flask import Blueprint, request, jsonify
from database import db
from models.user import Student
from models.club import ClubMember

clubs_bp = Blueprint("clubs", __name__, url_prefix="/clubs")


# เพิ่มสมาชิกสโมสร
@clubs_bp.route("/add", methods=["POST"])
def add_club_member():

    data = request.get_json()

    student_id = data.get("student_id")
    position = data.get("position")

    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return jsonify({"error": "ไม่พบนักศึกษา"}), 404

    existing = ClubMember.query.filter_by(student_id=student_id).first()
    if existing:
        return jsonify({"error": "นักศึกษานี้เป็นสโมสรอยู่แล้ว"}), 400

    new_member = ClubMember(student_id=student_id, position=position)

    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "เพิ่มสมาชิกสโมสรสำเร็จ"})


@clubs_bp.route("/all")
def get_club_members():
    members = ClubMember.query.all()
    return jsonify([m.to_dict() for m in members])


@clubs_bp.route("/all")
def get_clubs():

    members = ClubMember.query.all()

    result = []

    for m in members:
        s = m.student

        result.append(
            {
                "student_id": s.student_id,
                "first_name": s.first_name,
                "faculty": s.faculty,
                "major": s.major,
                "year": s.year,
                "email": s.email,
                "phone": s.phone,
                "last_login": (
                    s.last_login.strftime("%Y-%m-%d %H:%M") if s.last_login else None
                ),
                "position": m.position,
            }
        )

    return jsonify(result)


@clubs_bp.route("/remove/<student_id>", methods=["DELETE"])
def remove_club_member(student_id):

    member = ClubMember.query.filter_by(student_id=student_id).first()

    if not member:
        return jsonify({"error": "ไม่พบสมาชิกสโมสร"}), 404

    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": "นำออกจากสโมสรเรียบร้อย"})
