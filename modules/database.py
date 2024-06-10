import sqlite3

def initialize_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('student_info_system.db')
        cursor = conn.cursor()

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

        # Create the courses table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                course_description TEXT,
                instructor TEXT
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
            ('Math 101', 'Introduction to Mathematics', 'Dr. John Doe'),
            ('Physics 101', 'Introduction to Physics', 'Dr. Jane Smith'),
            ('Chemistry 101', 'Introduction to Chemistry', 'Dr. Emily Johnson'),
            # Add more courses as needed
        ]

        cursor.executemany("INSERT INTO courses (course_name, course_description, instructor) VALUES (?, ?, ?)", predefined_courses)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database initialization completed successfully.")
    except sqlite3.Error as e:
        print("Database initialization failed:", e)

if __name__ == "__main__":
    initialize_database()
