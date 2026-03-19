from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    url_for,
    redirect,
    send_from_directory,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
from routes.admin import admin_bp
from database import db
from routes.auth import auth_bp
from routes.clubs import clubs_bp
from models.user import Student
from models.officer import Officer
from models.admin import Admin
from models.equipment import Equipment
from models.place import Place
from models.place_equipment import PlaceEquipment
from models.qa_question import Question
from routes.resources_manager import register_resources_routes
from routes.resources_review import resources_bp
from routes.qa import qa_bp

app = Flask(__name__)

# ===== CONFIGURATION =====
app.secret_key = "ubu-science-secret-key-2026"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# SQLAlchemy สำหรับ Event และ News
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ubu_engage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLite3 สำหรับ activities (สร้างกิจกรรม)
DB_PATH_ACTIVITY = "create_activity.db"

# SQLite3 สำหรับ expenses และ registrations (ระบบภูวดล)
DB_PATH_MAIN = "database.db"

# SQLite3 สำหรับ Q&A แลt ข้อมูลสถานที่และอุปกรณ์
app.config["SQLALCHEMY_BINDS"] = {
    "resources": "sqlite:///resources.db",
    "qa": "sqlite:///qa.db",
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

os.makedirs(app.instance_path, exist_ok=True)

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(clubs_bp)

# Q&A and Resources
register_resources_routes(app)
app.register_blueprint(resources_bp)
app.register_blueprint(qa_bp)


# ===== DATABASE HELPERS =====


def get_activity_db():
    conn = sqlite3.connect(DB_PATH_ACTIVITY, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def get_main_db():
    conn = sqlite3.connect(DB_PATH_MAIN, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_activity_db():
    with get_activity_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                act_id          TEXT PRIMARY KEY,
                act_name        TEXT,
                act_datetime    TEXT,
                act_location    TEXT,
                act_address     TEXT,
                act_cost        REAL,
                act_status      TEXT DEFAULT 'pending',
                act_file        TEXT,
                act_detail      TEXT,
                act_steps       TEXT,
                act_QA          TEXT,
                act_created_by  TEXT,
                act_phone       TEXT,
                act_department  TEXT,
                act_fiscal_year TEXT,
                act_std         INTEGER,
                act_other       INTEGER,
                act_comment     TEXT
            )
        """
        )
        new_columns = [
            ("act_address", "TEXT"),
            ("act_steps", "TEXT"),
            ("act_phone", "TEXT"),
            ("act_department", "TEXT"),
            ("act_fiscal_year", "TEXT"),
            ("act_std", "INTEGER"),
            ("act_other", "INTEGER"),
            ("act_comment", "TEXT"),
        ]
        for col_name, col_type in new_columns:
            try:
                conn.execute(f"ALTER TABLE activities ADD COLUMN {col_name} {col_type}")
            except:
                pass


def init_main_db():
    conn = get_main_db()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            act_ref_id TEXT,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            filename TEXT
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            student_id TEXT NOT NULL,
            act_ref_id TEXT
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS act_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """
    )

    existing = conn.execute("SELECT COUNT(*) as c FROM act_list").fetchone()
    if existing["c"] == 0:
        conn.executemany(
            "INSERT INTO act_list (name) VALUES (?)",
            [
                ("กิจกรรมรับน้องใหม่",),
                ("กิจกรรมวันวิทยาศาสตร์",),
                ("กิจกรรมอาสาพัฒนาชุมชน",),
            ],
        )

    conn.commit()
    conn.close()


# ===== SQLALCHEMY MODELS =====


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)
    event_type = db.Column(db.String(50))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), default="default_news.png")
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# สร้างตารางทั้งหมดตอนเริ่มโปรแกรม
with app.app_context():
    db.create_all()
    init_activity_db()
    init_main_db()


# ===== CONTEXT PROCESSOR =====
# inject current_role and current_user to all templates automatically
@app.context_processor
def inject_user():
    return {
        "current_role": session.get("role", None),
        "current_user": session.get("identifier", None),
    }


# ===== FRONTEND ROUTES =====


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/calendar")
def calendar_page():
    return render_template("index.html")


@app.route("/news")
def news_page():
    return render_template("news.html")


@app.route("/create-activity")
def create_activity_page():
    return render_template("create_activity.html")


""" ไม่ใช้แล้ว ใช้ใน models/auth.py แทน
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if session.get("role"):
        return redirect("/")

    error = None
    identifier = ""

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "").strip()

        user = None
        role = None

        # เช็ค Student
        user = Student.query.filter_by(student_id=identifier).first()
        if user and check_password_hash(user.password, password):
            role = "student"

        # เช็ค Officer
        if not user:
            user = Officer.query.filter_by(officer_id=identifier).first()
            if user and check_password_hash(user.password, password):
                role = "officer"

        # เช็ค Admin
        if not user:
            user = Admin.query.filter_by(username=identifier).first()
            if user and check_password_hash(user.password, password):
                role = "admin"

        # login สำเร็จ
        if user and role:
            session["role"] = role
            session["identifier"] = identifier

            if role == "admin":
                session["admin_id"] = identifier
                return redirect("/admin/dashboard")

            return redirect("/")

        else:
            error = "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"

    return render_template("login.html", error=error, identifier=identifier)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")"""


@app.route("/club_status_activity")
def club_status_activity():
    with get_activity_db() as conn:
        activities = conn.execute(
            "SELECT * FROM activities ORDER BY act_id DESC"
        ).fetchall()
    return render_template("club_status_ativity.html", activities=activities)


@app.route("/officer")
def officer_status_activity():
    with get_activity_db() as conn:
        activities = conn.execute(
            """
            SELECT * FROM activities
            ORDER BY
                CASE act_status
                    WHEN 'resubmitted' THEN 1
                    WHEN 'pending' THEN 2
                    WHEN 'revision_needed' THEN 3
                    WHEN 'approved' THEN 4
                    WHEN 'finished' THEN 5
                    WHEN 'rejected' THEN 6
                    ELSE 7
                END, act_id DESC
        """
        ).fetchall()
    return render_template("officer_status_activity.html", activities=activities)


@app.route("/finish/<act_id>")
def finish_activity(act_id):
    with get_activity_db() as conn:
        conn.execute(
            'UPDATE activities SET act_status = "finished" WHERE act_id = ?', (act_id,)
        )
    return redirect(url_for("officer_status_activity"))


@app.route("/doc/<act_id>")
def view_doc(act_id):
    with get_activity_db() as conn:
        act = conn.execute(
            "SELECT * FROM activities WHERE act_id = ?", (act_id,)
        ).fetchone()
    return render_template("doc.html", act=act)


@app.route("/request_revision/<act_id>", methods=["POST"])
def request_revision(act_id):
    comment = request.form.get("comment")
    with get_activity_db() as conn:
        conn.execute(
            """
            UPDATE activities 
            SET act_status = 'revision_needed', act_comment = ? 
            WHERE act_id = ?
        """,
            (comment, act_id),
        )
    return redirect(url_for("officer_status_activity"))


# ===== ACTIVITY REGISTER ROUTES (ระบบลงทะเบียนกิจกรรม) =====


@app.route("/activity/register", methods=["GET", "POST"])
def activity_register():
    conn = get_main_db()

    if request.method == "POST":
        fullname = request.form.get("fullname")
        student_id = request.form.get("student_id")
        act_id = request.form.get("activity_id")  # ใช้ act_id จาก create_activity.db

        conn.execute(
            "INSERT INTO registrations (fullname, student_id, act_ref_id) VALUES (?, ?, ?)",
            (fullname, student_id, act_id),
        )
        conn.commit()

    result = conn.execute("SELECT COUNT(*) as count FROM registrations").fetchone()
    conn.close()

    # ดึงกิจกรรมที่ approved จาก create_activity.db
    with get_activity_db() as act_conn:
        activities = act_conn.execute(
            "SELECT act_id, act_name, act_datetime, act_location FROM activities WHERE act_status = 'approved' ORDER BY act_id DESC"
        ).fetchall()

    return render_template(
        "activity_register.html", count=result["count"], activities=activities
    )


@app.route("/activity/list")
def activity_list():
    conn = get_main_db()
    registrations = conn.execute(
        "SELECT id, fullname, student_id, act_ref_id FROM registrations ORDER BY id DESC"
    ).fetchall()
    conn.close()

    # ดึงชื่อกิจกรรมจาก create_activity.db มา map
    with get_activity_db() as act_conn:
        acts = act_conn.execute("SELECT act_id, act_name FROM activities").fetchall()
    act_map = {a["act_id"]: a["act_name"] for a in acts}

    # แปลง registrations เป็น list of dict พร้อมชื่อกิจกรรม
    reg_list = []
    for r in registrations:
        reg_list.append(
            {
                "id": r["id"],
                "fullname": r["fullname"],
                "student_id": r["student_id"],
                "activity_name": act_map.get(r["act_ref_id"], "-"),
            }
        )

    return render_template("activity_list.html", registrations=reg_list)


# ===== EXPENSE ROUTES (ระบบบันทึกรายจ่าย) =====


@app.route("/expense/create", methods=["GET", "POST"])
def expense_create():
    # ดึงกิจกรรมที่ approved มาให้เลือก
    with get_activity_db() as act_conn:
        activities = act_conn.execute(
            "SELECT act_id, act_name, act_cost FROM activities WHERE act_status = 'approved' ORDER BY act_id DESC"
        ).fetchall()

    if request.method == "POST":
        act_ref_id = request.form.get("act_ref_id")
        item = request.form.get("item")
        amount = request.form.get("amount")
        receipt = request.files.get("receipt")

        filename = None
        if receipt and receipt.filename != "":
            filename = secure_filename(receipt.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            receipt.save(filepath)

        conn = get_main_db()
        conn.execute(
            "INSERT INTO expenses (act_ref_id, item, amount, filename) VALUES (?, ?, ?, ?)",
            (act_ref_id, item, amount, filename),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("expense_list"))

    return render_template("expense_create.html", activities=activities)


@app.route("/expense/list")
def expense_list():
    conn = get_main_db()
    expenses = conn.execute("SELECT * FROM expenses ORDER BY id DESC").fetchall()
    conn.close()

    # ดึงข้อมูลกิจกรรมทั้งหมดมา map
    with get_activity_db() as act_conn:
        acts = act_conn.execute(
            "SELECT act_id, act_name, act_cost FROM activities WHERE act_status = 'approved'"
        ).fetchall()
    act_map = {
        a["act_id"]: {"name": a["act_name"], "budget": a["act_cost"] or 0} for a in acts
    }

    # คำนวณยอดใช้จริงแยกตามกิจกรรม
    summary = {}
    for e in expenses:
        aid = e["act_ref_id"] or "ไม่ระบุ"
        if aid not in summary:
            act_info = act_map.get(aid, {"name": "ไม่ระบุกิจกรรม", "budget": 0})
            summary[aid] = {
                "act_id": aid,
                "act_name": act_info["name"],
                "budget": act_info["budget"],
                "used": 0,
            }
        summary[aid]["used"] += e["amount"] or 0

    # คำนวณคงเหลือ
    for k in summary:
        summary[k]["remaining"] = summary[k]["budget"] - summary[k]["used"]

    total_all = sum(e["amount"] or 0 for e in expenses)

    return render_template(
        "expense_list.html",
        expenses=expenses,
        act_map=act_map,
        summary=list(summary.values()),
        total_all=total_all,
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ===== API ROUTES (Events & News) =====


@app.route("/api/get_events")
def get_events():
    events = Event.query.all()
    event_list = []
    for e in events:
        color = "#28a745"
        if e.event_type == "ประชุม":
            color = "#ffc107"
        elif e.event_type == "กำหนดส่ง":
            color = "#dc3545"
        try:
            f_start = datetime.strptime(e.start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            f_end = datetime.strptime(e.end_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            continue
        event_list.append(
            {
                "id": e.id,
                "title": e.title,
                "start": f_start,
                "end": f_end,
                "backgroundColor": color,
                "borderColor": color,
                "extendedProps": {
                    "location": e.location,
                    "description": e.description,
                    "type": e.event_type,
                },
            }
        )
    return jsonify(event_list)


@app.route("/api/save_event", methods=["POST"])
def save_event():
    data = request.json
    new_event = Event(
        title=data["title"],
        start_date=data["start_date"],
        end_date=data["end_date"] if data.get("end_date") else data["start_date"],
        event_type=data["type"],
        location=data["location"],
        description=data["description"],
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"status": "success"})


@app.route("/api/save_news", methods=["POST"])
def save_news():
    title = request.form.get("title")
    content = request.form.get("content")
    file = request.files.get("image")
    filename = "default_news.png"
    if file and file.filename != "":
        filename = secure_filename(
            f"news_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        )
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    new_news = News(title=title, content=content, image_filename=filename)
    db.session.add(new_news)
    db.session.commit()
    return jsonify({"status": "success"})


@app.route("/api/get_news")
def get_news():
    news_items = News.query.order_by(News.created_at.desc()).all()
    return jsonify(
        [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "image_url": url_for("static", filename="uploads/" + n.image_filename),
                "is_pinned": n.is_pinned,
                "date": n.created_at.strftime("%d/%m/%Y"),
            }
            for n in news_items
        ]
    )


@app.route("/api/toggle_pin/<int:id>", methods=["POST"])
def toggle_pin(id):
    news = News.query.get(id)
    if not news:
        return jsonify({"status": "error"}), 404
    news.is_pinned = not news.is_pinned
    db.session.commit()
    return jsonify({"status": "success"})


@app.route("/api/delete_news/<int:id>", methods=["DELETE"])
def delete_news(id):
    item = News.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404


@app.route("/api/delete_event_json/<int:id>", methods=["DELETE"])
def delete_event_json(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404


# ===== ACTIVITY MANAGEMENT API (sqlite3) =====


@app.route("/api/save-activity", methods=["POST"])
def save_activity():
    project_file = request.files.get("project_file")
    filename = (
        secure_filename(project_file.filename)
        if project_file and project_file.filename
        else ""
    )
    if project_file and filename:
        project_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    activity_date = request.form.get("activityDate", "")
    date_time = f"{activity_date} {request.form.get('startTime', '')}-{request.form.get('endTime', '')}"
    amounts = request.form.getlist("budget_amount[]")
    total_cost = sum(float(a) for a in amounts if a) if amounts else 0
    unique_suffix = uuid.uuid4().hex[:6].upper()
    act_id = f"ACT_{activity_date.replace('-', '')}_{unique_suffix}"

    with get_activity_db() as conn:
        conn.execute(
            """
            INSERT INTO activities (
                act_id, act_name, act_datetime, act_location, act_address,
                act_cost, act_status, act_file, act_detail, act_steps,
                act_QA, act_created_by, act_phone, act_department,
                act_fiscal_year, act_std, act_other
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                act_id,
                request.form.get("activityName"),
                date_time,
                request.form.get("location"),
                request.form.get("address"),
                total_cost,
                "pending",
                filename,
                request.form.get("objective"),
                request.form.get("steps"),
                request.form.get("notes"),
                request.form.get("responsiblePerson"),
                request.form.get("phone"),
                request.form.get("department"),
                request.form.get("fiscalYear"),
                int(request.form.get("participant_std") or 0),
                int(request.form.get("participant_other") or 0),
            ),
        )
    return redirect(url_for("club_status_activity"))


@app.route("/approve/<act_id>")
def approve_activity(act_id):
    with get_activity_db() as conn:
        conn.execute(
            'UPDATE activities SET act_status = "approved" WHERE act_id = ?', (act_id,)
        )
    return redirect(url_for("officer_status_activity"))


@app.route("/reject/<act_id>")
def reject_activity(act_id):
    with get_activity_db() as conn:
        conn.execute(
            'UPDATE activities SET act_status = "rejected" WHERE act_id = ?', (act_id,)
        )
    return redirect(url_for("officer_status_activity"))


@app.route("/edit/<act_id>", methods=["POST"])
def edit_activity(act_id):
    project_file = request.files.get("project_file")
    filename = None
    if project_file and project_file.filename:
        filename = secure_filename(project_file.filename)
        project_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    with get_activity_db() as conn:
        if filename:
            conn.execute(
                """
                UPDATE activities SET
                    act_name=?, act_datetime=?, act_location=?, act_address=?,
                    act_cost=?, act_detail=?, act_steps=?, act_QA=?,
                    act_created_by=?, act_phone=?, act_department=?,
                    act_fiscal_year=?, act_std=?, act_other=?, act_file=?,
                    act_status='resubmitted', act_comment=NULL
                WHERE act_id=?
            """,
                (
                    request.form.get("activityName"),
                    request.form.get("activityDatetime"),
                    request.form.get("location"),
                    request.form.get("address"),
                    float(request.form.get("cost") or 0),
                    request.form.get("objective"),
                    request.form.get("steps"),
                    request.form.get("notes"),
                    request.form.get("responsiblePerson"),
                    request.form.get("phone"),
                    request.form.get("department"),
                    request.form.get("fiscalYear"),
                    int(request.form.get("participant_std") or 0),
                    int(request.form.get("participant_other") or 0),
                    filename,
                    act_id,
                ),
            )
        else:
            conn.execute(
                """
                UPDATE activities SET
                    act_name=?, act_datetime=?, act_location=?, act_address=?,
                    act_cost=?, act_detail=?, act_steps=?, act_QA=?,
                    act_created_by=?, act_phone=?, act_department=?,
                    act_fiscal_year=?, act_std=?, act_other=?,
                    act_status='resubmitted', act_comment=NULL
                WHERE act_id=?
            """,
                (
                    request.form.get("activityName"),
                    request.form.get("activityDatetime"),
                    request.form.get("location"),
                    request.form.get("address"),
                    float(request.form.get("cost") or 0),
                    request.form.get("objective"),
                    request.form.get("steps"),
                    request.form.get("notes"),
                    request.form.get("responsiblePerson"),
                    request.form.get("phone"),
                    request.form.get("department"),
                    request.form.get("fiscalYear"),
                    int(request.form.get("participant_std") or 0),
                    int(request.form.get("participant_other") or 0),
                    act_id,
                ),
            )
    return redirect(url_for("club_status_activity"))


@app.route("/delete/<act_id>")
def delete_activity(act_id):
    with get_activity_db() as conn:
        conn.execute("DELETE FROM activities WHERE act_id = ?", (act_id,))
    return redirect(url_for("club_status_activity"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
