import sqlite3

DATABASE = "students.db"

conn = sqlite3.connect(DATABASE)

# Get all students in ascending ID order
students = conn.execute(
    "SELECT id FROM students ORDER BY id ASC"
).fetchall()

# Sample attendance dates
dates = [
    "2026-09-01",
    "2026-09-02",
    "2026-09-03",
    "2026-09-04",
    "2026-09-05"
]

# Add attendance for every student
for student in students:

    student_id = student[0]

    for index, date in enumerate(dates):

        # Alternate Present and Absent
        if (student_id + index) % 5 == 0:
            status = "Absent"
        else:
            status = "Present"

        # Avoid duplicate attendance
        existing = conn.execute(
            """
            SELECT id
            FROM attendance
            WHERE student_id = ? AND date = ?
            """,
            (student_id, date)
        ).fetchone()

        if existing:
            continue

        conn.execute(
            """
            INSERT INTO attendance
            (student_id, date, status)
            VALUES (?, ?, ?)
            """,
            (student_id, date, status)
        )

conn.commit()
conn.close()

print("Sample attendance records added successfully!")
