from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_PATH = 'create_activity.db'

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
        new_columns = [
            ("act_address",     "TEXT"),
            ("act_steps",       "TEXT"),
            ("act_phone",       "TEXT"),
            ("act_department",  "TEXT"),
            ("act_fiscal_year", "TEXT"),
            ("act_std",         "INTEGER"),
            ("act_other",       "INTEGER"),
        ]
        for col_name, col_type in new_columns:
            try:
                conn.execute(f'ALTER TABLE activities ADD COLUMN {col_name} {col_type}')
            except Exception:
                pass 

#สโม 
@app.route('/')
def index():
    return render_template('create_activity.html')

@app.route('/api/save-activity', methods=['POST'])
def save_activity():
    project_file = request.files.get('project_file')
    filename = secure_filename(project_file.filename) if project_file and project_file.filename else ""

    if project_file and filename:
        project_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    activity_date = request.form.get('activityDate', '')
    start_time    = request.form.get('startTime', '')
    end_time      = request.form.get('endTime', '')
    date_time     = f"{activity_date} {start_time}-{end_time}"

    amounts    = request.form.getlist('budget_amount[]')
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
            act_id,
            request.form.get('activityName'),
            date_time,
            request.form.get('location'),
            request.form.get('address'),
            total_cost,
            'pending',
            filename,
            request.form.get('objective'),
            request.form.get('steps'),
            request.form.get('notes'),
            request.form.get('responsiblePerson'),
            request.form.get('phone'),
            request.form.get('department'),
            request.form.get('fiscalYear'),
            int(request.form.get('participant_std') or 0),
            int(request.form.get('participant_other') or 0),
        ))

    return redirect(url_for('club_status_activity'))

@app.route('/club_status_activity')
def club_status_activity():
    with get_db() as conn:
        activities = conn.execute(
            'SELECT * FROM activities ORDER BY act_id DESC'
        ).fetchall()
    return render_template('club_status_ativity.html', activities=activities)

@app.route('/edit/<act_id>', methods=['POST'])
def edit_activity(act_id):
    project_file = request.files.get('project_file')
    new_filename = None

    if project_file and project_file.filename:
        new_filename = secure_filename(project_file.filename)
        project_file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    with get_db() as conn:
        if new_filename:
            conn.execute('''
                UPDATE activities SET
                    act_name       = ?,
                    act_datetime   = ?,
                    act_location   = ?,
                    act_cost       = ?,
                    act_file       = ?,
                    act_detail     = ?,
                    act_QA         = ?,
                    act_created_by = ?
                WHERE act_id = ?
            ''', (
                request.form.get('activityName'),
                request.form.get('activityDatetime'),
                request.form.get('location'),
                float(request.form.get('cost') or 0),
                new_filename,
                request.form.get('objective'),
                request.form.get('notes'),
                request.form.get('responsiblePerson'),
                act_id
            ))
        else:
            conn.execute('''
                UPDATE activities SET
                    act_name       = ?,
                    act_datetime   = ?,
                    act_location   = ?,
                    act_cost       = ?,
                    act_detail     = ?,
                    act_QA         = ?,
                    act_created_by = ?
                WHERE act_id = ?
            ''', (
                request.form.get('activityName'),
                request.form.get('activityDatetime'),
                request.form.get('location'),
                float(request.form.get('cost') or 0),
                request.form.get('objective'),
                request.form.get('notes'),
                request.form.get('responsiblePerson'),
                act_id
            ))

    return redirect(url_for('club_status_activity'))

@app.route('/delete/<act_id>')
def delete_activity(act_id):
    with get_db() as conn:
        row = conn.execute(
            'SELECT act_file FROM activities WHERE act_id = ?', (act_id,)
        ).fetchone()

        if row and row['act_file']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], row['act_file'])
            if os.path.exists(file_path):
                os.remove(file_path)

        conn.execute('DELETE FROM activities WHERE act_id = ?', (act_id,))

    return redirect(url_for('club_status_activity'))


# เพิ่ม Route สำหรับจัดการกิจกรรมที่สำเร็จ (Optional)
@app.route('/finish/<act_id>')
def finish_activity(act_id):
    with get_db() as conn:
        conn.execute(
            'UPDATE activities SET act_status = "finished" WHERE act_id = ?', (act_id,)
        )
    return redirect(url_for('officer_status_activity'))

# ปรับ Route หลักของ Officer ให้ดึงข้อมูลมาทั้งหมดเพื่อรอ JS กรอง
@app.route('/officer')
def officer_status_activity():
    with get_db() as conn:
        # ดึงมาทั้งหมด โดยเรียงลำดับความสำคัญ (Pending ขึ้นก่อน)
        activities = conn.execute('''
            SELECT * FROM activities 
            ORDER BY 
                CASE act_status 
                    WHEN 'pending' THEN 1 
                    WHEN 'approved' THEN 2 
                    WHEN 'finished' THEN 3
                    WHEN 'rejected' THEN 4
                    ELSE 5 
                END, act_id DESC
        ''').fetchall()
    return render_template('officer_status_activity.html', activities=activities)

@app.route('/approve/<act_id>')
def approve_activity(act_id):
    with get_db() as conn:
        conn.execute(
            'UPDATE activities SET act_status = "approved" WHERE act_id = ?', (act_id,)
        )
    return redirect(url_for('officer_status_activity'))

@app.route('/reject/<act_id>')
def reject_activity(act_id):
    with get_db() as conn:
        conn.execute(
            'UPDATE activities SET act_status = "rejected" WHERE act_id = ?', (act_id,)
        )
    return redirect(url_for('officer_status_activity'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)