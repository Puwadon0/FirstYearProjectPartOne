from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# ตั้งค่าฐานข้อมูล SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ubu_calendar.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# สร้าง Model ตารางกิจกรรม
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)  # เก็บรูปแบบ dd/mm/yyyy
    end_date = db.Column(db.String(10), nullable=False)
    event_type = db.Column(db.String(50))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)


# สร้างฐานข้อมูล
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


# หน้าสำหรับดูข้อมูลในฐานข้อมูล (SQLite Viewer)
@app.route("/admin")
def admin_viewer():
    events = Event.query.all()
    return render_template("admin.html", events=events)


# API สำหรับบันทึกกิจกรรม
@app.route("/api/save_event", methods=["POST"])
def save_event():
    data = request.json
    new_event = Event(
        title=data["title"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        event_type=data["type"],
        location=data["location"],
        description=data["description"],
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "บันทึกเรียบร้อย!"})


# เพิ่มต่อจากฟังก์ชัน save_event ใน app.py
@app.route("/api/get_events")
def get_events():
    events = Event.query.all()
    event_list = []
    for e in events:
        # กำหนดสีตามประเภทกิจกรรมเพื่อให้เข้ากับคำอธิบายสี
        color = "#28a745"  # กิจกรรม (เขียว)
        if e.event_type == "ประชุม":
            color = "#ffc107"  # เหลือง
        elif e.event_type == "กำหนดส่ง":
            color = "#dc3545"  # แดง

        event_list.append(
            {
                "title": e.title,
                "start": datetime.strptime(e.start_date, "%d/%m/%Y").strftime(
                    "%Y-%m-%d"
                ),
                "end": datetime.strptime(e.end_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
                "backgroundColor": color,
                "borderColor": color,
                "extendedProps": {"location": e.location, "description": e.description},
            }
        )
    return jsonify(event_list)


# API สำหรับลบข้อมูล
@app.route("/api/delete_event/<int:id>", methods=["POST"])
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for("admin_viewer"))


if __name__ == "__main__":
    app.run(debug=True)
