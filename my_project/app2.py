from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# --- 1. การตั้งค่าระบบ (Configuration) ---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ตั้งค่าฐานข้อมูลหลัก (SQLAlchemy) สำหรับ Event และ News
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ubu_engage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ตั้งค่าฐานข้อมูลสำหรับระบบสร้างกิจกรรม (sqlite3)
DB_PATH_ACTIVITY = 'create_activity.db'

# --- 2. ฟังก์ชันจัดการฐานข้อมูลกิจกรรม (sqlite3) ---
def get_db():
    conn = sqlite3.connect(DB_PATH_ACTIVITY, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_activity_db():
    with get_db() as conn:
        conn.execute('''
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
                act_other       INTEGER
            )
        ''')
        # ตรวจสอบการเพิ่ม Column ใหม่ป้องกัน Error
        new_columns = [
            ("act_address", "TEXT"), ("act_steps", "TEXT"), ("act_phone", "TEXT"),
            ("act_department", "TEXT"), ("act_fiscal_year", "TEXT"),
            ("act_std", "INTEGER"), ("act_other", "INTEGER"),
        ]
        for col_name, col_type in new_columns:
            try: conn.execute(f'ALTER TABLE activities ADD COLUMN {col_name} {col_type}')
            except: pass

# --- 3. โมเดลฐานข้อมูล (SQLAlchemy) สำหรับ Event และ News ---
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
    image_filename = db.Column(db.String(255), default='default_news.png')
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# สร้างตารางทั้งหมดตอนเริ่มโปรแกรม
with app.app_context():
    db.create_all()
    init_activity_db()

# --- 4. เส้นทางหน้าเว็บ (Frontend Routes) ---

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/calendar')
def calendar_page():
    return render_template('index.html')

@app.route('/news')
def news_page():
    return render_template('news.html')

@app.route('/create-activity') # เปลี่ยนจาก '/' เดิมของสโมสร
def create_activity_page():
    return render_template('create_activity.html')

@app.route('/club_status_activity')
def club_status_activity():
    with get_db() as conn:
        activities = conn.execute('SELECT * FROM activities ORDER BY act_id DESC').fetchall()
    return render_template('club_status_ativity.html', activities=activities)

@app.route('/officer')
def officer_status_activity():
    with get_db() as conn:
        activities = conn.execute('''
            SELECT * FROM activities 
            ORDER BY 
                CASE act_status 
                    WHEN 'pending' THEN 1 WHEN 'approved' THEN 2 
                    WHEN 'finished' THEN 3 WHEN 'rejected' THEN 4 ELSE 5 
                END, act_id DESC
        ''').fetchall()
    return render_template('officer_status_activity.html', activities=activities)

# --- 5. ระบบ API สำหรับกิจกรรมและข่าวสาร (SQLAlchemy) ---

@app.route('/api/get_events')
def get_events():
    events = Event.query.all()
    event_list = []
    for e in events:
        color = "#28a745"
        if e.event_type == "ประชุม": color = "#ffc107"
        elif e.event_type == "กำหนดส่ง": color = "#dc3545"
        try:
            f_start = datetime.strptime(e.start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            f_end = datetime.strptime(e.end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        except: continue
        event_list.append({
            'id': e.id, 'title': e.title, 'start': f_start, 'end': f_end,
            'backgroundColor': color, 'borderColor': color,
            'extendedProps': {'location': e.location, 'description': e.description, 'type': e.event_type}
        })
    return jsonify(event_list)

@app.route('/api/save_event', methods=['POST'])
def save_event():
    data = request.json
    new_event = Event(
        title=data['title'], start_date=data['start_date'],
        end_date=data['end_date'] if data.get('end_date') else data['start_date'],
        event_type=data['type'], location=data['location'], description=data['description']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/save_news', methods=['POST'])
def save_news():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files.get('image')
    filename = 'default_news.png'
    if file and file.filename != '':
        filename = secure_filename(f"news_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_news = News(title=title, content=content, image_filename=filename)
    db.session.add(new_news)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/get_news')
def get_news():
    news_items = News.query.order_by(News.created_at.desc()).all()
    return jsonify([{
        'id': n.id, 'title': n.title, 'content': n.content,
        'image_url': url_for('static', filename='uploads/' + n.image_filename),
        'is_pinned': n.is_pinned, 'date': n.created_at.strftime('%d/%m/%Y')
    } for n in news_items])

# --- 6. ระบบ API สำหรับการจัดการคำขอ (sqlite3) ---

@app.route('/api/save-activity', methods=['POST'])
def save_activity():
    project_file = request.files.get('project_file')
    filename = secure_filename(project_file.filename) if project_file and project_file.filename else ""
    if project_file and filename:
        project_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    activity_date = request.form.get('activityDate', '')
    date_time = f"{activity_date} {request.form.get('startTime', '')}-{request.form.get('endTime', '')}"
    amounts = request.form.getlist('budget_amount[]')
    total_cost = sum(float(a) for a in amounts if a) if amounts else 0
    unique_suffix = uuid.uuid4().hex[:6].upper()
    act_id = f"ACT_{activity_date.replace('-', '')}_{unique_suffix}"

    with get_db() as conn:
        conn.execute('''
            INSERT INTO activities (
                act_id, act_name, act_datetime, act_location, act_address,
                act_cost, act_status, act_file, act_detail, act_steps,
                act_QA, act_created_by, act_phone, act_department,
                act_fiscal_year, act_std, act_other
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            act_id, request.form.get('activityName'), date_time, request.form.get('location'),
            request.form.get('address'), total_cost, 'pending', filename, request.form.get('objective'),
            request.form.get('steps'), request.form.get('notes'), request.form.get('responsiblePerson'),
            request.form.get('phone'), request.form.get('department'), request.form.get('fiscalYear'),
            int(request.form.get('participant_std') or 0), int(request.form.get('participant_other') or 0),
        ))
    return redirect(url_for('club_status_activity'))

@app.route('/approve/<act_id>')
def approve_activity(act_id):
    with get_db() as conn:
        conn.execute('UPDATE activities SET act_status = "approved" WHERE act_id = ?', (act_id,))
    return redirect(url_for('officer_status_activity'))

@app.route('/reject/<act_id>')
def reject_activity(act_id):
    with get_db() as conn:
        conn.execute('UPDATE activities SET act_status = "rejected" WHERE act_id = ?', (act_id,))
    return redirect(url_for('officer_status_activity'))

@app.route('/delete-news/<int:id>', methods=['DELETE'])
def delete_news(id):
    item = News.query.get(id)
    if item:
        db.session.delete(item); db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

@app.route('/api/delete_event_json/<int:id>', methods=['DELETE'])
def delete_event_json(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event); db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)