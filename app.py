from flask import Flask, request, render_template

# สร้างแอปพลิเคชัน Flask
app = Flask(__name__)

# -------------------------
# 1. ระบบสมาชิก (Login / Register) ผู้ดูแล เขษมศักดิ์ แก่นทน
# -------------------------

# สมัครสมาชิก (แสดงฟอร์มหรือรับข้อมูลสมัครสมาชิก)
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    # ทำหน้าที่บันทึกข้อมูลผู้ใช้ใหม่เข้าสู่ระบบ
    pass

# เข้าสู่ระบบ
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    # ตรวจสอบข้อมูลผู้ใช้และสร้าง session
    pass

# ออกจากระบบ
@app.route("/auth/logout", methods=["POST"])
def logout():
    # ลบ session และออกจากระบบ
    pass


# -------------------------
#  จัดการกิจกรรม (ผู้ดูแล: สราวดี บุญภูมิ)
# -------------------------

# แสดงรายการกิจกรรมทั้งหมด
@app.route("/activities", methods=["GET"])
def list_activities():
    # ดึงข้อมูลกิจกรรมทั้งหมดจากฐานข้อมูล
    pass

# เพิ่มกิจกรรมใหม่เข้าสู่ระบบ
@app.route("/activities", methods=["POST"])
def create_activity():
    # รับข้อมูลกิจกรรมจากผู้ใช้และบันทึกลงฐานข้อมูล
    pass

# แสดงรายละเอียดกิจกรรมตามรหัส id
@app.route("/activities/<int:id>", methods=["GET"])
def activity_detail(id):
    # ดึงข้อมูลกิจกรรมเฉพาะรายการตาม id
    pass

# แก้ไขข้อมูลกิจกรรม
@app.route("/activities/<int:id>", methods=["PUT"])
def update_activity(id):
    # อัปเดตข้อมูลกิจกรรมตาม id
    pass

# อนุมัติกิจกรรม
@app.route("/activities/<int:id>/approve", methods=["PATCH"])
def approve_activity(id):
    # เปลี่ยนสถานะกิจกรรมเป็น "อนุมัติ"
    pass


# -------------------------
#  จัดการเอกสาร (ผู้ดูแล: ธวัลรัตน์ โชติบุญ)
# -------------------------

# แสดงรายการเอกสารทั้งหมด
@app.route("/documents", methods=["GET"])
def list_documents():
    # ดึงข้อมูลเอกสารทั้งหมด
    pass

# สร้างเอกสารใหม่
@app.route("/documents", methods=["POST"])
def create_document():
    # บันทึกข้อมูลเอกสารใหม่เข้าสู่ระบบ
    pass

# ดูรายละเอียดเอกสารตาม id
@app.route("/documents/<int:id>", methods=["GET"])
def document_detail(id):
    # แสดงรายละเอียดเอกสารเฉพาะรายการ
    pass

# อนุมัติเอกสาร
@app.route("/documents/<int:id>/approve", methods=["PATCH"])
def approve_document(id):
    # เปลี่ยนสถานะเอกสารเป็น "อนุมัติ"
    pass


# -------------------------
# 6. รับสมัครจิตอาสา ผู้ดูแล ปรมินทร์ ศักดิ์สยาม
# -------------------------

# แสดงรายชื่อผู้สมัครจิตอาสา
@app.route("/volunteers", methods=["GET"])
def list_volunteers():
    # ดึงข้อมูลผู้สมัครทั้งหมด
    pass

# สมัครเป็นจิตอาสา
@app.route("/volunteers", methods=["POST"])
def apply_volunteer():
    # บันทึกข้อมูลผู้สมัครจิตอาสา
    pass


# -------------------------
# 7. ลงทะเบียนเข้าร่วมกิจกรรม ผู้ดูแล สหรัถ สะเดาว์
# -------------------------

# ลงทะเบียนเข้าร่วมกิจกรรม
@app.route("/registrations", methods=["POST"])
def register_activity():
    # บันทึกข้อมูลการลงทะเบียนและแนบลิงก์ประเมิน
    pass

# ดูรายละเอียดการลงทะเบียน
@app.route("/registrations/<int:id>", methods=["GET"])
def registration_detail(id):
    # แสดงข้อมูลการลงทะเบียนตาม id
    pass


# -------------------------
# 8. บันทึกค่าใช้จ่าย ผู้ดูแล สหรัถ สะเดาว์
# -------------------------

# เพิ่มรายการค่าใช้จ่าย
@app.route("/expenses", methods=["POST"])
def create_expense():
    # บันทึกข้อมูลค่าใช้จ่ายของโครงการ
    pass

# แสดงรายการค่าใช้จ่ายทั้งหมด
@app.route("/expenses", methods=["GET"])
def list_expenses():
    # ดึงข้อมูลค่าใช้จ่ายทั้งหมด
    pass


# -------------------------
# 9. อัปโหลดไฟล์ ผู้ดูแล ปรมินทร์ ศักดิ์สยาม
# -------------------------

# อัปโหลดไฟล์เข้าสู่ระบบ
@app.route("/uploads", methods=["POST"])
def upload_file():
    # รับไฟล์จากผู้ใช้และบันทึกลงระบบ
    pass


# -------------------------
# 10. แดชบอร์ด ผู้ดูแล ทุกคน
# -------------------------

# แสดงภาพรวมข้อมูลสถิติของระบบ
@app.route("/dashboard", methods=["GET"])
def dashboard():
    # แสดงข้อมูลสรุป เช่น จำนวนกิจกรรม ผู้สมัคร ฯลฯ
    pass


# -------------------------
# 11. อัปโหลดรายงานโครงการ ผู้ดูแล สหรัถ สะเดาว์
# -------------------------

# อัปโหลดรายงานโครงการ
@app.route("/reports", methods=["POST"])
def upload_report():
    # บันทึกรายงานโครงการเข้าสู่ระบบ
    pass

# ดูรายละเอียดรายงานโครงการ
@app.route("/reports/<int:id>", methods=["GET"])
def report_detail(id):
    # แสดงรายงานโครงการตาม id
    pass


# -------------------------
# 12. จัดการสถานที่และอุปกรณ์ (ผู้ดูแล: ณัฐดนัย ทองสรรค์)
# -------------------------

# แสดงรายการสถานที่และอุปกรณ์
@app.route("/resources", methods=["GET"])
def list_resources():
    # ดึงข้อมูลทรัพยากรทั้งหมด
    pass

# เพิ่มข้อมูลสถานที่หรืออุปกรณ์
@app.route("/resources", methods=["POST"])
def create_resource():
    # บันทึกข้อมูลทรัพยากรใหม่
    pass


# -------------------------
# 13. ประชาสัมพันธ์ ผู้ดูแล ภูวดล จันทร์ดี
# -------------------------

# แสดงรายการประกาศประชาสัมพันธ์
@app.route("/announcements", methods=["GET"])
def list_announcements():
    # ดึงข้อมูลประกาศทั้งหมด
    pass

# สร้างประกาศใหม่
@app.route("/announcements", methods=["POST"])
def create_announcement():
    # บันทึกประกาศประชาสัมพันธ์
    pass


# -------------------------
# 14. ปฏิทินกิจกรรม ผู้ดูแล ภูวดล จันทร์ดี
# -------------------------

# แสดงปฏิทินกิจกรรมทั้งหมด
@app.route("/calendar", methods=["GET"])
def view_calendar():
    # แสดงข้อมูลกิจกรรมในรูปแบบปฏิทิน
    pass

# เพิ่มกิจกรรมลงในปฏิทิน
@app.route("/calendar/events", methods=["POST"])
def create_calendar_event():
    # บันทึกกิจกรรมลงในปฏิทิน
    pass


# -------------------------
# 15. ระบบถาม-ตอบ (Q&A) สโมสรกับนักศึกษา ผู้ดูแล ณัฐดนัย ทองสรรค์
# -------------------------

# แสดงคำถามทั้งหมด
@app.route("/qa/questions", methods=["GET"])
def list_questions():
    # ดึงรายการคำถามจากนักศึกษา
    pass

# สร้างคำถามใหม่
@app.route("/qa/questions", methods=["POST"])
def create_question():
    # บันทึกคำถามใหม่เข้าสู่ระบบ
    pass

# ตอบคำถามตาม id
@app.route("/qa/questions/<int:id>/answer", methods=["POST"])
def answer_question(id):
    # บันทึกคำตอบของสโมสร
    pass


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    # รันเซิร์ฟเวอร์ในโหมด debug สำหรับพัฒนา
    app.run(debug=True)