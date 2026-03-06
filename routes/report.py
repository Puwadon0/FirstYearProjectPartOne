from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    redirect,
    url_for,
    flash,
    session,
    abort,
)
from models.reports import Report, ReportImage
from database import db
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime


report_bp = Blueprint("report", __name__)


@report_bp.before_request
def block_unauthorized():
    if "role" not in session:
        return redirect(url_for("auth.login"))


# อัพโหลดรายงานโครงการ
@report_bp.route("/reports", methods=["GET", "POST"])
def upload_report():
    if "role" not in session:
        abort(404)

    if request.method == "POST":

        # รับข้อมูลจากฟอร์ม
        project_name = request.form.get("project_name")
        academic_year = request.form.get("academic_year")
        project_code = request.form.get("project_code")
        organization = request.form.get("organization")
        location = request.form.get("location")
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")

        start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d").date()
            if start_date_str
            else None
        )
        end_date = (
            datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        )
        report_detail = request.form.get("report_detail")

        report_file = request.files.get("report_file")
        evaluation_file = request.files.get("evaluation_file")
        images = request.files.getlist("images")

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        # บันทึกไฟล์หลัก
        report_filename = None
        if report_file and report_file.filename != "":
            filename = str(uuid.uuid4()) + "_" + secure_filename(report_file.filename)
            report_file.save(os.path.join(upload_folder, filename))
            report_filename = f"uploads/{filename}"

        evaluation_filename = None
        if evaluation_file and evaluation_file.filename != "":
            filename = (
                str(uuid.uuid4()) + "_" + secure_filename(evaluation_file.filename)
            )
            evaluation_file.save(os.path.join(upload_folder, filename))
            evaluation_filename = f"uploads/{filename}"

        # สร้าง Report object
        new_report = Report(
            project_name=project_name,
            academic_year=academic_year,
            project_code=project_code,
            organization=organization,
            location=location,
            start_date=start_date,
            end_date=end_date,
            report_file=report_filename,
            evaluation_file=evaluation_filename,
            report_detail=report_detail,
        )

        db.session.add(new_report)
        db.session.commit()  # ต้อง commit ก่อนเพื่อเอา id

        # บันทึกรูปหลายรูป
        for image in images:
            if image.filename != "":
                filename = str(uuid.uuid4()) + "_" + secure_filename(image.filename)
                image.save(os.path.join(upload_folder, filename))

                new_image = ReportImage(
                    report_id=new_report.id, image_path=f"uploads/{filename}"
                )

                db.session.add(new_image)

        db.session.commit()

        flash("upload_success")
        return redirect(url_for("report.upload_report"))

    reports = Report.query.order_by(Report.id.desc()).all()

    return render_template("upload_report.html", reports=reports)


@report_bp.route("/reports/<int:id>", methods=["GET"])
def report_detail(id):
    report = Report.query.get_or_404(id)
    return render_template("report_detail.html", report=report)


# ลบโครงการ
@report_bp.route("/reports/delete/<int:id>", methods=["POST"])
def delete_report(id):
    report = Report.query.get_or_404(id)

    ReportImage.query.filter_by(report_id=id).delete()

    db.session.delete(report)
    db.session.commit()

    return redirect(url_for("report.upload_report"))


# แก้ไขโครงการ
@report_bp.route("/reports/edit/<int:id>", methods=["GET", "POST"])
def edit_report(id):
    report = Report.query.get_or_404(id)

    if request.method == "POST":

        # ===== รับค่าจากฟอร์ม =====
        report.project_name = request.form.get("project_name")
        report.academic_year = request.form.get("academic_year")
        report.project_code = request.form.get("project_code")
        report.organization = request.form.get("organization")
        report.location = request.form.get("location")
        report.report_detail = request.form.get("report_detail")

        # ===== วันที่ =====
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")

        if start_date_str:
            report.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

        if end_date_str:
            report.end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # ===== อัปโหลดไฟล์ใหม่ =====
        report_file = request.files.get("report_file")
        evaluation_file = request.files.get("evaluation_file")
        upload_folder = current_app.config["UPLOAD_FOLDER"]

        if report_file and report_file.filename != "":
            filename = str(uuid.uuid4()) + "_" + secure_filename(report_file.filename)
            report_file.save(os.path.join(upload_folder, filename))
            report.report_file = f"uploads/{filename}"

        if evaluation_file and evaluation_file.filename != "":
            filename = (
                str(uuid.uuid4()) + "_" + secure_filename(evaluation_file.filename)
            )
            evaluation_file.save(os.path.join(upload_folder, filename))
            report.evaluation_file = f"uploads/{filename}"

        # ===== เพิ่มรูปใหม่ =====
        images = request.files.getlist("images")

        for image in images:
            if image and image.filename != "":
                filename = str(uuid.uuid4()) + "_" + secure_filename(image.filename)
                image.save(os.path.join(upload_folder, filename))

                new_image = ReportImage(
                    report_id=report.id, image_path=f"uploads/{filename}"
                )
                db.session.add(new_image)

        # ===== commit =====
        db.session.commit()

        flash("edit_success", "success")
        return render_template("edit_report.html", report=report)

    return render_template("edit_report.html", report=report)


@report_bp.route("/reports/delete-image/<int:image_id>")
def delete_image(image_id):
    image = ReportImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return redirect(request.referrer)
