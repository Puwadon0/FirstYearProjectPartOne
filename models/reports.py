from datetime import datetime
from database import db


class Report(db.Model):

    __tablename__ = "upload_reports"
    id = db.Column(db.Integer, primary_key=True)

    # -------------------------
    # 1. ข้อมูลโครงการ
    # -------------------------
    project_name = db.Column(db.String(255), nullable=False)  # ชื่อโครงการ
    academic_year = db.Column(db.String(10), nullable=False)  # ปีการศึกษา เช่น 2568
    project_code = db.Column(db.String(100), nullable=False)  # รหัสโครงการ
    organization = db.Column(db.String(255))  # หน่วยงานผู้รับผิดชอบ
    location = db.Column(db.String(255), nullable=False)  # สถานที่จัดกิจกรรม

    # -------------------------
    # 2. ระยะเวลาดำเนินโครงการ
    # -------------------------
    start_date = db.Column(db.Date, nullable=False)  # วันเริ่มโครงการ
    end_date = db.Column(db.Date, nullable=False)  # วันสิ้นสุดโครงการ

    # -------------------------
    # 3. ไฟล์รายงาน
    # (เก็บเป็นชื่อไฟล์ หรือ path)
    # -------------------------
    report_file = db.Column(db.String(255), nullable=False)  # ไฟล์รายงานหลัก
    evaluation_file = db.Column(db.String(255), nullable=False)  # ไฟล์ประเมินความพึงพอใจ

    # -------------------------
    # 4. รายละเอียดรายงาน
    # -------------------------
    report_detail = db.Column(db.Text)  # สรุปรายงาน

    # -------------------------
    # 5. สถานะการตรวจสอบ
    # -------------------------
    status = db.Column(db.String(50), default="รอเจ้าหน้าที่ตรวจสอบ")

    # -------------------------
    # 6. วันเวลาที่สร้างข้อมูล
    # -------------------------
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Report {self.project_name}>"


class ReportImage(db.Model):
    __tablename__ = "report_images"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(
        db.Integer, db.ForeignKey("upload_reports.id"), nullable=False
    )
    image_path = db.Column(db.String(255), nullable=False)
    report = db.relationship("Report", backref="images")
