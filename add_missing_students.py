import sqlite3

conn = sqlite3.connect("students.db")

students = [
    (2, "Aarav Kumar", "aarav@gmail.com", "B.Tech", "1"),
    (3, "Ishitha Rao", "ishitha@gmail.com", "B.Tech", "2"),
    (4, "Varun Reddy", "varun@gmail.com", "B.Tech", "3"),
    (5, "Keerthi Sharma", "keerthi@gmail.com", "B.Tech", "4"),
    (6, "Aditya Kumar", "aditya@gmail.com", "B.Tech", "2"),
    (7, "Sanjana Rao", "sanjana@gmail.com", "B.Tech", "3")
]

for student in students:
    conn.execute(
        """
        INSERT INTO students (id, name, email, course, year)
        VALUES (?, ?, ?, ?, ?)
        """,
        student
    )

conn.commit()
conn.close()

print("Students with IDs 2-7 added successfully!")