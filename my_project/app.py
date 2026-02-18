from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ตั้งค่าฐานข้อมูลและระบบอัปโหลด
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ubu_engage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Model ตารางกิจกรรม
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(10), nullable=False) 
    end_date = db.Column(db.String(10), nullable=False)
    event_type = db.Column(db.String(50))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

# Model ตารางข่าวประชาสัมพันธ์
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), default='default_news.png')
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news')
def news_page():
    return render_template('news.html')

# --- API ข่าวประชาสัมพันธ์ ---
@app.route('/api/get_news')
def get_news():
    news_items = News.query.order_by(News.created_at.desc()).all()
    output = []
    for n in news_items:
        output.append({
            'id': n.id,
            'title': n.title,
            'content': n.content,
            'image_url': url_for('static', filename='uploads/' + n.image_filename),
            'is_pinned': n.is_pinned,
            'date': n.created_at.strftime('%d/%m/%Y')
        })
    return jsonify(output)

@app.route('/api/save_news', methods=['POST'])
def save_news():
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('image')
        filename = 'default_news.png'
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"news_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_news = News(title=title, content=content, image_filename=filename)
        db.session.add(new_news)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/toggle_pin/<int:id>', methods=['POST'])
def toggle_pin(id):
    news_item = News.query.get(id)
    if news_item:
        news_item.is_pinned = not news_item.is_pinned
        db.session.commit()
        return jsonify({"status": "success", "is_pinned": news_item.is_pinned})
    return jsonify({"status": "error"}, 404)

@app.route('/api/delete_news/<int:id>', methods=['DELETE'])
def delete_news(id):
    news_item = News.query.get(id)
    if news_item:
        if news_item.image_filename != 'default_news.png':
            try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], news_item.image_filename))
            except: pass
        db.session.delete(news_item)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}, 404)

# --- API กิจกรรม ---
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
        end_date=data['end_date'] if data['end_date'] else data['start_date'],
        event_type=data['type'], location=data['location'], description=data['description']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)