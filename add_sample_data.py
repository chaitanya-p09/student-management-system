import sqlite3

DATABASE = "students.db"

students = [
    ("Rahul Kumar", "rahul@gmail.com", "B.Tech", "2"),
    ("Priya Sharma", "priya@gmail.com", "B.Tech", "3"),
    ("Kiran Reddy", "kiran@gmail.com", "B.Tech", "4"),
    ("Anjali Rao", "anjali@gmail.com", "B.Tech", "1"),
    ("Arjun Patel", "arjun@gmail.com", "B.Tech", "3"),
    ("Sneha Singh", "sneha@gmail.com", "B.Tech", "2"),
    ("Vikram Das", "vikram@gmail.com", "B.Tech", "4"),
    ("Divya Reddy", "divya@gmail.com", "B.Tech", "1"),
    ("Rohit Kumar", "rohit@gmail.com", "B.Tech", "3"),
    ("Meena Devi", "meena@gmail.com", "B.Tech", "2"),
    ("Suresh Babu", "suresh@gmail.com", "B.Tech", "4"),
    ("Kavya Rao", "kavya@gmail.com", "B.Tech", "1"),
    ("Naveen Kumar", "naveen@gmail.com", "B.Tech", "3"),
    ("Pooja Sharma", "pooja@gmail.com", "B.Tech", "2"),
    ("Manoj Reddy", "manoj@gmail.com", "B.Tech", "4"),
    ("Akhil Kumar", "akhil@gmail.com", "B.Tech", "1"),
    ("Harsha Rao", "harsha@gmail.com", "B.Tech", "3"),
    ("Lakshmi Devi", "lakshmi@gmail.com", "B.Tech", "2"),
    ("Sai Krishna", "saikrishna@gmail.com", "B.Tech", "4"),
    ("Neha Reddy", "neha@gmail.com", "B.Tech", "1")
]

conn = sqlite3.connect(DATABASE)

for student in students:
    try:
        conn.execute(
            """
            INSERT INTO students (name, email, course, year)
            VALUES (?, ?, ?, ?)
            """,
            student
        )
    except sqlite3.IntegrityError:
        print(f"Skipped: {student[1]} already exists")

conn.commit()
conn.close()

print("Sample students added successfully!")