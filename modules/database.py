import sqlite3

def initialize_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('student_info_system.db')
        cursor = conn.cursor()

        # Drop the courses table if it exists to avoid schema conflicts
        cursor.execute('DROP TABLE IF EXISTS courses')

        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                gender TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create the courses table with additional columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT NOT NULL,
                course_name TEXT NOT NULL,
                instructor TEXT,
                credits INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        # Create the enrollments table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date DATE,
                FOREIGN KEY (student_id) REFERENCES users(id),
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        ''')

        # Insert predefined courses into the courses table
        predefined_courses = [
            ('MATH101', 'Math 101', 'Dr. John Doe', 3, 'active'),
            ('PHYS101', 'Physics 101', 'Dr. Jane Smith', 4, 'active'),
            ('CHEM101', 'Chemistry 101', 'Dr. Emily Johnson', 3, 'active'),
            ('CN4', 'Chinese_HSK4', 'Izzy', 2, 'Enroll In'),
            ('DBMS67', 'Database Management', 'Mingjie Tang & Chuan Li', 3, 'Enroll In'),
            ('SWE45', 'Software Engineering', 'Jizhe Zhou', 2, 'Enroll In'),
            ('CN102', 'Computer Networks', 'Jingyu Jang', 4, 'Enrolled')
        ]

        cursor.executemany("INSERT INTO courses (course_code, course_name, instructor, credits, status) VALUES (?, ?, ?, ?, ?)", predefined_courses)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database initialization completed successfully.")
    except sqlite3.Error as e:
        print("Database initialization failed:", e)

if __name__ == "__main__":
    initialize_database()
