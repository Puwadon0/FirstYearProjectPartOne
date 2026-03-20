from flask import Flask, render_template, request, session, redirect, url_for, Blueprint

resources_bp = Blueprint("resources", __name__)


# แสดงรายการสถานที่และอุปกรณ์
@resources_bp.route("/resources", methods=["GET"])
def list_resources():
    return render_template("resources_review.html")  # แสดงหน้าแหล่งข้อมูล
