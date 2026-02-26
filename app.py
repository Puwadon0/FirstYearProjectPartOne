from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # table expenses
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            filename TEXT
        )
    """)

    # table registrations
    conn.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            student_id TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# สร้าง database ตอนเริ่มโปรแกรม
init_db()


@app.route("/")
def home():
    pass


@app.route("/activity/register", methods=["GET", "POST"])
def activity_register():

    conn = get_db_connection()

    if request.method == "POST":

        fullname = request.form.get("fullname")
        student_id = request.form.get("student_id")

        conn.execute(
            "INSERT INTO registrations (fullname, student_id) VALUES (?, ?)",
            (fullname, student_id)
        )

        conn.commit()

    # นับจำนวนทั้งหมด
    result = conn.execute(
        "SELECT COUNT(*) as count FROM registrations"
    ).fetchone()

    conn.close()

    count = result["count"]

    return render_template(
        "activity_register.html",
        count=count
    )



@app.route("/activity/list")
def activity_list():

    conn = get_db_connection()

    registrations = conn.execute(
        "SELECT * FROM registrations ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "activity_list.html",
        registrations=registrations
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/expense/create", methods=["GET", "POST"])
def expense_create():

    if request.method == "POST":

        item = request.form.get("item")
        amount = request.form.get("amount")

        receipt = request.files.get("receipt")

        filename = None

        if receipt and receipt.filename != "":
            filename = receipt.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            receipt.save(filepath)

        # INSERT DATABASE
        conn = get_db_connection()

        conn.execute(
            "INSERT INTO expenses (item, amount, filename) VALUES (?, ?, ?)",
            (item, amount, filename)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("expense_list"))

    return render_template("expense_create.html")
# หน้าแสดงผล
@app.route("/expense/list")
def expense_list():

    conn = get_db_connection()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    result = conn.execute(
        "SELECT SUM(amount) as total FROM expenses"
    ).fetchone()

    conn.close()

    total = result["total"] if result["total"] else 0

    return render_template(
        "expense_list.html",
        expenses=expenses,
        total=total
    )

if __name__ == "__main__":
    app.run(debug=True)