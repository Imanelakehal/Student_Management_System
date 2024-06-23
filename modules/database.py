import sqlite3

def initialize_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('student_info_system.db')
        cursor = conn.cursor()

        # Drop tables if they exist to avoid schema conflicts
        
        cursor.execute('DROP TABLE IF EXISTS courses')
        cursor.execute('DROP TABLE IF EXISTS accommodations')
        cursor.execute('DROP TABLE IF EXISTS books')
        

        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                gender TEXT NOT NULL,
                password TEXT NOT NULL,
                address TEXT,
                school TEXT,
                major TEXT,
                date_of_birth TEXT,
                photo TEXT,
                social_links TEXT
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

        # Create the accommodations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accommodations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roomNo TEXT NOT NULL,
                location TEXT NOT NULL,
                type TEXT NOT NULL,
                floor INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        # Create the books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       bookId TEXT NOT NULL,
                       title TEXT NOT NULL,
                       course TEXT NOT NULL,
                       status TEXT NOT NULL
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

        # Insert predefined accommodations into the accommodations table
        predefined_accommodations = [
            ('C101', 'North Wing', 'Single', 1, 'Book'),
            ('B102', 'Jiangan Campus', 'Double', 1, 'Reserved'),
            ('A201', 'Wangjiang Campus', 'Single', 2, 'Book'),
            ('S202', 'Sushe West', 'Double', 2, 'Reserved'),
            ('P202', 'South West', 'Double', 2, 'Book'),
            ('B208', 'Jiangan Campus', 'Double', 2, 'Book'),
            ('B207', 'North Wing', 'Double', 2, 'Book'),
            ('A207', 'South Wing', 'Double', 2, 'Book')
        ]

        cursor.executemany("INSERT INTO accommodations (roomNo, location, type, floor, status) VALUES (?, ?, ?, ?, ?)", predefined_accommodations)
        
        # Insert predefined books into the books table
        predefined_books= [
            ('C408','Computer Networks 9th Edition', 'Computer Networks','Book'),
            ('B407','Probability and statistics 7th Edition', 'Mathematics','Not Available'),
            ('C404','Computer Architecture 9th Edition', 'Computer Architecture','Book'),
            ('B405','The song of Achilles', 'Literature','Book'),
            ('A408','A man Called Ove', 'Novel','Book'),
            ('E407','Crime and Punishment', 'Literature','Book'),
            ('W409','Database management basics', 'DBMS','Book'),
            ('Z508','Neural Networks', 'Machine Learning','Not Available ')
        ]

        cursor.executemany('INSERT INTO books (bookId, title, course, status) VALUES(?,?,?,?)', predefined_books)
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database initialization completed successfully.")
    except sqlite3.Error as e:
        print("Database initialization failed:", e)

if __name__ == "__main__":
    initialize_database()
