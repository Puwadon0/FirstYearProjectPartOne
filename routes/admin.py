from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from datetime import datetime
from functools import wraps
from models.user import Student
from models.club import ClubMember
from models.officer import Officer
from models.admin import Admin

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session or session.get("role") != "admin":
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


# แสดงหน้าแดชบอร์ดสำหรับผู้ดูแลระบบ
@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    return render_template("admin.html")


# สร้างผู้ใช้นักศึกษาใหม่
@admin_bp.route("/create-student", methods=["POST"])
def create_student():
    try:
        data = request.get_json()

        student_id = (data.get("student_id") or "").strip()
        first_name = (data.get("first_name") or "").strip()
        faculty = (data.get("faculty") or "").strip()
        major = (data.get("major") or "").strip()
        year = data.get("year")
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        password = data.get("password")
        role = data.get("role", "student")

        if not student_id or not password:
            return jsonify({"error": "กรุณากรอกรหัสนักศึกษาและรหัสผ่าน"}), 400

        if Student.query.filter_by(student_id=student_id).first():
            return jsonify({"error": "รหัสนักศึกษานี้มีอยู่แล้ว!"}), 400

        if email and Student.query.filter_by(email=email).first():
            return jsonify({"error": "อีเมลนี้มีอยู่แล้ว!"}), 400

        hashed_password = generate_password_hash(password)

        new_student = Student(
            student_id=student_id,
            first_name=first_name,
            faculty=faculty,
            major=major,
            year=year,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role,
        )

        db.session.add(new_student)
        db.session.commit()

        return jsonify({"message": "สร้างนักศึกษาสำเร็จ!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"เกิดข้อผิดพลาด: {str(e)}"}), 500


# ดึงข้อมูลผู้ใช้ตามบทบาท
@admin_bp.route("/get-users/<role>", methods=["GET"])
def get_users_by_role(role):

    if role == "student":
        users = Student.query.filter_by(role="student").all()

    elif role == "club":
        members = ClubMember.query.all()
        users = [m.student for m in members]

    elif role == "officer":
        users = Officer.query.all()

    else:
        return jsonify({"error": "role ไม่ถูกต้อง!"}), 400

    return jsonify([u.to_dict() for u in users])


# ลบนักศึกษา
@admin_bp.route("/delete-user/<student_id>", methods=["DELETE"])
def delete_user(student_id):

    user = Student.query.filter_by(student_id=student_id).first()

    if not user:
        return jsonify({"error": "ไม่พบผู้ใช้"}), 404

    member = ClubMember.query.filter_by(student_id=student_id).first()
    if member:
        db.session.delete(member)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "ลบผู้ใช้นักศึกษาสำเร็จ!"})


# แก้ไขข้อมูลนักศึกษา
@admin_bp.route("/update-user/<student_id>", methods=["PUT"])
def update_user(student_id):

    user = Student.query.filter_by(student_id=student_id).first()

    if not user:
        return jsonify({"error": "ไม่พบผู้ใช้"}), 404

    data = request.get_json()

    user.faculty = data.get("faculty")
    user.major = data.get("major")
    user.year = data.get("year")
    user.email = data.get("email")
    user.phone = data.get("phone")

    db.session.commit()

    if "position" in data:
        member = ClubMember.query.filter_by(student_id=student_id).first()
        if member:
            member.position = data.get("position")
            db.session.commit()

    return jsonify({"message": "แก้ไขข้อมูลสำเร็จ!"})


# สร้างเจ้าหน้าที่ใหม่
@admin_bp.route("/create-officer", methods=["POST"])
def create_officer():
    data = request.json

    if (
        not data.get("officer_id")
        or not data.get("full_name")
        or not data.get("password")
    ):
        return jsonify({"error": "กรอกข้อมูลไม่ครบ"}), 400

    existing_officer = Officer.query.filter_by(officer_id=data["officer_id"]).first()

    if existing_officer:
        return jsonify({"error": "รหัสเจ้าหน้าที่นี้มีอยู่แล้ว"}), 400

    hashed_password = generate_password_hash(data["password"])

    officer = Officer(
        officer_id=data["officer_id"],
        full_name=data["full_name"],
        department=data.get("department"),
        email=data.get("email"),
        phone=data.get("phone"),
        password=hashed_password,
    )

    db.session.add(officer)
    db.session.commit()

    return jsonify({"message": "สร้างเจ้าหน้าที่เรียบร้อย!"}), 201


# แก้ไขเจ้าหน้าที่
@admin_bp.route("/update-officer/<officer_id>", methods=["PUT"])
def update_officer(officer_id):

    officer = Officer.query.filter_by(officer_id=officer_id).first()

    if not officer:
        return jsonify({"error": "ไม่พบเจ้าหน้าที่"}), 404

    data = request.get_json()

    officer.full_name = data.get("full_name")
    officer.department = data.get("department")
    officer.email = data.get("email")
    officer.phone = data.get("phone")

    db.session.commit()

    return jsonify({"message": "แก้ไขเจ้าหน้าที่สำเร็จ"})


@admin_bp.route("/admin-logout")
def admin_logout():
    session.clear()
    return redirect(url_for("auth.login"))
