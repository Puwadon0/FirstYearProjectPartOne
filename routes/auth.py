from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import Student
from database import db
from datetime import datetime
from sqlalchemy import or_, func
from zoneinfo import ZoneInfo
from models.club import ClubMember
from models.officer import Officer
from models.admin import Admin


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# REGISTER
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        first_name = request.form.get("first_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        role = request.form.get("role")

        if password != confirm_password:
            return render_template("register.html", error="รหัสผ่านไม่ตรงกัน")

        if Student.query.filter_by(email=email).first():
            return render_template("register.html", error="อีเมลนี้ถูกใช้งานแล้ว")

        if role == "student":
            student_id = request.form.get("student_id")
            faculty = request.form.get("faculty")
            major = request.form.get("major")
            year = request.form.get("year")

            if not student_id:
                return render_template("register.html", error="กรุณากรอกรหัสนักศึกษา")

            if Student.query.filter_by(student_id=student_id).first():
                return render_template("register.html", error="รหัสนักศึกษานี้ถูกใช้งานแล้ว")

            hashed_password = generate_password_hash(password)

            new_student = Student(
                first_name=first_name,
                email=email,
                phone=phone,
                password=hashed_password,
                student_id=student_id,
                faculty=faculty,
                major=major,
                year=year,
            )

            db.session.add(new_student)
            db.session.commit()

            return render_template("register.html", success=True)

        if role == "club":
            return render_template("register.html", error="ระบบสโมสรยังไม่เปิดใช้งาน")

    return render_template("register.html")


# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "").strip()

        if not identifier or not password:
            return render_template(
                "login.html",
                error="กรุณากรอกข้อมูลให้ครบ",
                identifier=identifier,
            )

        # =========================
        # เช็ค ADMIN ก่อนเลย
        # =========================
        admin = Admin.query.filter(
            func.lower(Admin.username) == identifier.lower()
        ).first()

        if admin:
            if check_password_hash(admin.password, password):
                session.clear()
                session["admin_id"] = admin.id
                session["role"] = "admin"
                return redirect(url_for("admin.admin_dashboard"))
            else:
                return render_template(
                    "login.html",
                    error="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!",
                    identifier=identifier,
                )

        # =========================
        # เช็ค Student / Officer (ของเดิมคุณ)
        # =========================

        user = None

        if "@" in identifier:
            user = Student.query.filter(
                func.lower(Student.email) == identifier.lower()
            ).first()

            if not user:
                user = Officer.query.filter(
                    func.lower(Officer.email) == identifier.lower()
                ).first()
        else:
            user = Student.query.filter_by(student_id=identifier).first()

        if not user:
            return render_template(
                "login.html",
                error="ไม่พบผู้ใช้นี้ในระบบ!",
                identifier=identifier,
            )

        if not check_password_hash(user.password, password):
            return render_template(
                "login.html",
                error="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!",
                identifier=identifier,
            )

        # Login สำเร็จ
        session.clear()
        session["user_id"] = user.id
        session["identifier"] = identifier

        if isinstance(user, Officer):
            session["role"] = "officer"
            session["officer_id"] = user.officer_id

        elif isinstance(user, Student):
            club_member = ClubMember.query.filter_by(student_id=user.student_id).first()

            if club_member:
                session["role"] = "club"
            else:
                session["role"] = "student"

            session["student_id"] = user.student_id

        user.last_login = datetime.now(ZoneInfo("Asia/Bangkok"))
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("login.html")


# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))
