from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from database import db
from models.qa_question import Question
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from datetime import datetime
import random
import string

qa_bp = Blueprint("qa", __name__)


def generate_code():
    return "QA-" + "".join(random.choices(string.digits, k=5))


# ------------------ ROUTES ------------------
# แสดงคำถาม (เฉพาะที่ตอบแล้ว)
@qa_bp.route("/qa/questions", methods=["GET"])
def list_questions():

    questions = Question.query.order_by(
        desc(Question.is_faq),  # FAQ ขึ้นก่อน
        desc(Question.view_count),  # แล้วค่อยดู view
        desc(Question.created_at),  # กัน view เท่ากัน
    ).all()

    return render_template("qa.html", questions=questions)


# สร้างคำถามใหม่
@qa_bp.route("/qa/questions", methods=["POST"])
def create_question():

    title = request.form.get("title")

    while True:
        try:
            code = generate_code()

            q = Question(
                code=code,
                question=title,
                answer=None,
                category="ทั่วไป",
                is_faq=False,
                view_count=0,
                status="pending",
            )

            db.session.add(q)
            db.session.commit()
            break

        except IntegrityError:
            db.session.rollback()

    return redirect(url_for("qa.list_questions"))


# หน้าตอบคำถาม
@qa_bp.route("/qa/answer", methods=["GET"])
def qa_answer_page():
    questions = Question.query.order_by(
        Question.view_count.desc(),  # วิวมากสุดก่อน
        Question.created_at.desc(),
    ).all()

    return render_template("qa_answer.html", questions=questions)


# ตอบคำถาม (ใช้ code แทน id)
@qa_bp.route("/qa/questions/<string:code>/answer", methods=["POST"])
def answer_question(code):

    q = Question.query.filter_by(code=code).first_or_404()

    if request.is_json:
        data = request.get_json()
        answer = data.get("answer")
    else:
        answer = request.form.get("answer")

    q.answer = answer
    q.status = "published"
    q.answered_at = datetime.now()

    db.session.commit()

    if not request.is_json:
        return redirect(url_for("qa.qa_answer_page"))

    return jsonify({"message": "Answer added", "code": code, "answer": answer})


# ลบคำถาม
@qa_bp.route("/qa/questions/<string:code>/delete", methods=["POST"])
def delete_question(code):

    q = Question.query.filter_by(code=code).first_or_404()

    db.session.delete(q)
    db.session.commit()

    return redirect(url_for("qa.qa_answer_page"))


# เพิ่ม view
@qa_bp.route("/qa/questions/<string:code>/view", methods=["POST"])
def add_view(code):

    q = Question.query.filter_by(code=code).first_or_404()

    q.view_count += 1

    # auto popular
    if q.view_count >= 50:
        q.is_faq = True

    db.session.commit()

    return jsonify(
        {"message": "view counted", "view_count": q.view_count, "is_faq": q.is_faq}
    )
