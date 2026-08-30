from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE DATABASE TABLES ----------------

def init_db():
    conn = get_db_connection()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Students table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            year TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    # Academic records table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS academic_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL,
            grade TEXT NOT NULL,
            result TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()

    


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username or email already exists."

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            return redirect(url_for("dashboard"))

        return "Invalid username or password."

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    conn = get_db_connection()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_attendance = conn.execute(
        "SELECT COUNT(*) FROM attendance"
    ).fetchone()[0]

    total_academic = conn.execute(
        "SELECT COUNT(*) FROM academic_records"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_attendance=total_attendance,
        total_academic=total_academic
    )


# ---------------- ADD STUDENT ----------------

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        year = request.form["year"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO students (name, email, course, year)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, course, year)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")


# ---------------- VIEW STUDENTS ----------------

@app.route("/students")
def students():

    search = request.args.get("search", "")

    conn = get_db_connection()

    if search:

        students = conn.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ?
               OR email LIKE ?
               OR course LIKE ?
            ORDER BY id DESC
            """,
            (
                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%"
            )
        ).fetchall()

    else:

        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )

@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        year = request.form["year"]

        conn.execute(
            """
            UPDATE students
            SET name = ?, email = ?, course = ?, year = ?
            WHERE id = ?
            """,
            (name, email, course, year, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )

@app.route("/delete-student/<int:id>")
def delete_student(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    conn = get_db_connection()

    # Get all students
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    if request.method == "POST":

        student_id = request.form["student_id"]
        date = request.form["date"]
        status = request.form["status"]

        conn.execute(
            """
            INSERT INTO attendance (student_id, date, status)
            VALUES (?, ?, ?)
            """,
            (student_id, date, status)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("attendance"))

    conn.close()

    return render_template(
        "attendance.html",
        students=students
    )

@app.route("/attendance-records")
def attendance_records():

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    conn = get_db_connection()

    query = """
        SELECT
            attendance.id,
            students.name,
            students.course,
            attendance.date,
            attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        WHERE 1=1
    """

    params = []

    # Search by student name or course
    if search:
        query += """
            AND (
                students.name LIKE ?
                OR students.course LIKE ?
            )
        """

        params.extend([
            "%" + search + "%",
            "%" + search + "%"
        ])

    # Filter by attendance status
    if status:
        query += " AND attendance.status = ?"
        params.append(status)

    query += " ORDER BY attendance.date DESC"

    records = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return render_template(
        "attendance_records.html",
        records=records,
        search=search,
        status=status
    )
@app.route("/academic", methods=["GET", "POST"])
def academic():

    conn = get_db_connection()

    # Get all students
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    if request.method == "POST":

        student_id = request.form["student_id"]
        subject = request.form["subject"]
        marks = int(request.form["marks"])

        # Calculate grade and result
        if marks >= 90:
            grade = "A+"
        elif marks >= 80:
            grade = "A"
        elif marks >= 70:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 50:
            grade = "D"
        else:
            grade = "F"

        if marks >= 40:
            result = "Pass"
        else:
            result = "Fail"

        conn.execute(
            """
            INSERT INTO academic_records
            (student_id, subject, marks, grade, result)
            VALUES (?, ?, ?, ?, ?)
            """,
            (student_id, subject, marks, grade, result)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("academic_records"))

    conn.close()

    return render_template(
        "academic.html",
        students=students
    )
@app.route("/academic-records")
def academic_records():

    conn = get_db_connection()

    records = conn.execute("""
        SELECT
            academic_records.id,
            students.name,
            students.course,
            academic_records.subject,
            academic_records.marks,
            academic_records.grade,
            academic_records.result
        FROM academic_records
        JOIN students
        ON academic_records.student_id = students.id
        ORDER BY academic_records.id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "academic_records.html",
        records=records
    )

@app.route("/edit-academic/<int:id>", methods=["GET", "POST"])
def edit_academic(id):

    conn = get_db_connection()

    record = conn.execute(
        "SELECT * FROM academic_records WHERE id = ?",
        (id,)
    ).fetchone()

    if record is None:
        conn.close()
        return "Academic record not found."

    if request.method == "POST":

        subject = request.form["subject"]
        marks = int(request.form["marks"])

        # Calculate grade
        if marks >= 90:
            grade = "A+"
        elif marks >= 80:
            grade = "A"
        elif marks >= 70:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 50:
            grade = "D"
        else:
            grade = "F"

        # Calculate result
        if marks >= 40:
            result = "Pass"
        else:
            result = "Fail"

        conn.execute(
            """
            UPDATE academic_records
            SET subject = ?, marks = ?, grade = ?, result = ?
            WHERE id = ?
            """,
            (subject, marks, grade, result, id)
        )

        conn.commit()
        conn.close()

        return redirect("/academic-records")

    conn.close()

    return render_template(
        "edit_academic.html",
        record=record
    )

@app.route("/delete-academic/<int:id>")
def delete_academic(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM academic_records WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/academic-records")


@app.route("/student/<int:id>")
def student_details(id):

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if student is None:
        conn.close()
        return "Student not found."

    academic_records = conn.execute(
        """
        SELECT *
        FROM academic_records
        WHERE student_id = ?
        ORDER BY id DESC
        """,
        (id,)
    ).fetchall()

    attendance_records = conn.execute(
        """
        SELECT *
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
        """,
        (id,)
    ).fetchall()

    conn.close()

    return render_template(
        "student_details.html",
        student=student,
        academic_records=academic_records,
        attendance_records=attendance_records
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)