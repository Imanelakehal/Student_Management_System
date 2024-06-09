import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('student_info_system.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    student_id TEXT NOT NULL,
    gender TEXT NOT NULL
)
''')

# Create Courses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    description TEXT,
    credits INTEGER NOT NULL
)
''')

# Create Enrollments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and tables initialized.")
