from flask import Flask, request, render_template

app = Flask(__name__)

# -------------------------
# 1. Auth (Login / Register)
# -------------------------
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    pass
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    pass
@app.route("/auth/logout", methods=["POST"])
def logout():
    pass
# -------------------------
# 2-3. Activities
# -------------------------
@app.route("/activities", methods=["GET"])
def list_activities():
    pass
@app.route("/activities", methods=["POST"])
def create_activity():
    pass
@app.route("/activities/<int:id>", methods=["GET"])
def activity_detail(id):
    pass
@app.route("/activities/<int:id>", methods=["PUT"])
def update_activity(id):
    pass
@app.route("/activities/<int:id>/approve", methods=["PATCH"])
def approve_activity(id):
    pass
# -------------------------
# 4-5. Documents
# -------------------------
@app.route("/documents", methods=["GET"])
def list_documents():
    pass

@app.route("/documents", methods=["POST"])
def create_document():
    pass

@app.route("/documents/<int:id>", methods=["GET"])
def document_detail(id):
    pass

@app.route("/documents/<int:id>/approve", methods=["PATCH"])
def approve_document(id):
    pass
# -------------------------
# 6. Volunteers
# -------------------------
@app.route("/volunteers", methods=["GET"])
def list_volunteers():
    pass

@app.route("/volunteers", methods=["POST"])
def apply_volunteer():
    pass
# -------------------------
# 7. Registrations
# -------------------------
@app.route("/registrations", methods=["POST"])
def register_activity():
    pass

@app.route("/registrations/<int:id>", methods=["GET"])
def registration_detail(id):
    pass
# -------------------------
# 8. Expenses
# -------------------------
@app.route("/expenses", methods=["POST"])
def create_expense():
    pass

@app.route("/expenses", methods=["GET"])
def list_expenses():
    pass
# -------------------------
# 9. Upload
# -------------------------
@app.route("/uploads", methods=["POST"])
def upload_file():
    pass
# -------------------------
# 10. Dashboard
# -------------------------
@app.route("/dashboard", methods=["GET"])
def dashboard():
    pass
# -------------------------
# 11. Project Reports
# -------------------------
@app.route("/reports", methods=["POST"])
def upload_report():
    pass
@app.route("/reports/<int:id>", methods=["GET"])
def report_detail(id):
    pass
# -------------------------
# 12. Resources (สถานที่ / อุปกรณ์)
# -------------------------
@app.route("/resources", methods=["GET"])
def list_resources():
    pass

@app.route("/resources", methods=["POST"])
def create_resource():
    pass
# -------------------------
# 13. Announcements
# -------------------------
@app.route("/announcements", methods=["GET"])
def list_announcements():
    pass

@app.route("/announcements", methods=["POST"])
def create_announcement():
    pass
# -------------------------
# 14. Calendar
# -------------------------
@app.route("/calendar", methods=["GET"])
def view_calendar():
    pass
@app.route("/calendar/events", methods=["POST"])
def create_calendar_event():
    pass
# -------------------------
# 15. Q&A
# -------------------------
@app.route("/qa/questions", methods=["GET"])
def list_questions():
    pass
@app.route("/qa/questions", methods=["POST"])
def create_question():
    pass
@app.route("/qa/questions/<int:id>/answer", methods=["POST"])
def answer_question(id):
    pass
# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)