import sqlite3
import random

conn = sqlite3.connect("students.db")

students = conn.execute(
    "SELECT id FROM students ORDER BY id ASC"
).fetchall()

subjects = [
    "Python",
    "Database Management",
    "Web Development"
]

for student in students:
    student_id = student[0]

    for subject in subjects:
        marks = random.randint(55, 95)

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

        result = "Pass" if marks >= 40 else "Fail"

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

print("Academic records added successfully!")