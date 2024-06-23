import sqlite3
import unittest

def initialize_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('student_info_system.db')
        cursor = conn.cursor()

        # Drop existing tables if needed for clean slate (optional)
        print("Dropping existing tables if they exist...")
        cursor.execute('DROP TABLE IF EXISTS students')
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS courses')
        cursor.execute('DROP TABLE IF EXISTS enrollments')
        cursor.execute('DROP TABLE IF EXISTS accommodations')
        cursor.execute('DROP TABLE IF EXISTS books')
        cursor.execute('DROP TABLE IF EXISTS test_scores')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                major TEXT NOT NULL,
                gender TEXT NOT NULL,
                region TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                score INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')

        predefined_students = [
            ('John Doe', 22, 'IT', 'Male', 'North'),
            ('Jane Smith', 21, 'Literature', 'Female', 'South'),
            ('Michael Brown', 23, 'English', 'Male', 'East'),
            ('Emily Davis', 20, 'Art', 'Female', 'West'),
            ('Chris Johnson', 24, 'Biology', 'Male', 'North'),
            ('Jessica Taylor', 22, 'Physics', 'Female', 'South'),
            ('Daniel Martinez', 21, 'Chemistry', 'Male', 'East')
        ]

        cursor.executemany("INSERT INTO students (name, age, major, gender, region) VALUES (?, ?, ?, ?, ?)", predefined_students)

        predefined_scores = [
            (1, 85), (1, 90), (2, 88), (2, 75), (3, 92), (3, 89),
            (4, 95), (4, 80), (5, 85), (5, 87), (6, 90), (6, 85), 
            (7, 88), (7, 82)
        ]

        cursor.executemany("INSERT INTO test_scores (student_id, score) VALUES (?, ?)", predefined_scores)


    
        # Create the users table if it doesn't exist
        print("Creating users table...")
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
        print("Creating courses table...")
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
        print("Creating enrollments table...")
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
        print("Creating accommodations table...")
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
        print("Creating books table...")
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
        print("Inserting predefined courses...")
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
        print("Inserting predefined accommodations...")
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
        print("Inserting predefined books...")
        predefined_books = [
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
        
# Function to get a database connection
def get_connection():
    return sqlite3.connect('student_info_system.db')

class TestStudentDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the database for testing (assuming initialize_database is in database.py)
        initialize_database()

    def setUp(self):
        # Set up a clean slate for each test
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Clean up after each test
        self.conn.rollback()  # Rollback changes to leave the database state unchanged
        self.conn.close()

    # Test cases for students table
    def test_insert_student(self):
        # Test inserting a student into the database
        self.cursor.execute("INSERT INTO students (name, age, major, gender, region) VALUES (?, ?, ?, ?, ?)", ('John Wick', 25, 'Math', 'Male', 'West'))
        self.conn.commit()
        
        # Check if the student was inserted correctly
        self.cursor.execute("SELECT * FROM students WHERE name=?", ('John Wick',))
        student = self.cursor.fetchone()
        self.assertIsNotNone(student)
        self.assertEqual(student[1], 'John Wick')
        self.assertEqual(student[2], 25)
        self.assertEqual(student[3], 'Math')
        self.assertEqual(student[4], 'Male')
        self.assertEqual(student[5], 'West')

    def test_delete_student(self):
        # Test deleting a student from the database
        self.cursor.execute("DELETE FROM students WHERE id=?", (1,))
        self.conn.commit()
        
        # Check if the student was deleted
        self.cursor.execute("SELECT * FROM students WHERE id=?", (1,))
        student = self.cursor.fetchone()
        self.assertIsNone(student)

    # Test cases for test_scores table
    def test_update_score(self):
        # Test updating a student's test score
        self.cursor.execute("UPDATE test_scores SET score=? WHERE id=?", (90, 1))
        self.conn.commit()
        
        # Check if the score was updated correctly
        self.cursor.execute("SELECT * FROM test_scores WHERE id=?", (1,))
        score = self.cursor.fetchone()
        self.assertIsNotNone(score)
        self.assertEqual(score[2], 90)

    def test_delete_score(self):
        # Test deleting a score from the database
        self.cursor.execute("DELETE FROM test_scores WHERE id=?", (2,))
        self.conn.commit()
        
        # Check if the score was deleted
        self.cursor.execute("SELECT * FROM test_scores WHERE id=?", (2,))
        score = self.cursor.fetchone()
        self.assertIsNone(score)

    # Test cases for users table
    def test_insert_user(self):
        # Test inserting a user into the database
        self.cursor.execute("INSERT INTO users (full_name, student_id, gender, password, address) VALUES (?, ?, ?, ?, ?)", ('Eve Johnson', 'E54321', 'Female', 'password3', '789 Elm St'))
        self.conn.commit()
        
        # Check if the user was inserted correctly
        self.cursor.execute("SELECT * FROM users WHERE full_name=?", ('Eve Johnson',))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], 'Eve Johnson')
        self.assertEqual(user[2], 'E54321')
        self.assertEqual(user[3], 'Female')
        self.assertEqual(user[4], 'password3')
        self.assertEqual(user[5], '789 Elm St')

    def test_update_user_password(self):
        # Test updating user password
        self.cursor.execute("UPDATE users SET password=? WHERE id=?", ('newpassword', 1))
        self.conn.commit()
        
        # Retrieve the updated user information
        self.cursor.execute("SELECT * FROM users WHERE id=?", (1,))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        
        # Ensure that the password has been updated correctly
        self.assertEqual(user[4], 'newpassword')

    # Test cases for courses table
    def test_insert_course(self):
        # Test inserting a course into the database
        self.cursor.execute("INSERT INTO courses (course_code, course_name, instructor, credits, status) VALUES (?, ?, ?, ?, ?)", ('ENG101', 'English 101', 'Dr. Michael Smith', 3, 'active'))
        self.conn.commit()
        
        # Check if the course was inserted correctly
        self.cursor.execute("SELECT * FROM courses WHERE course_code=?", ('ENG101',))
        course = self.cursor.fetchone()
        self.assertIsNotNone(course)
        self.assertEqual(course[1], 'ENG101')
        self.assertEqual(course[2], 'English 101')
        self.assertEqual(course[3], 'Dr. Michael Smith')
        self.assertEqual(course[4], 3)
        self.assertEqual(course[5], 'active')

    def test_delete_course(self):
        # Test deleting a course from the database
        self.cursor.execute("DELETE FROM courses WHERE id=?", (1,))
        self.conn.commit()
        
        # Check if the course was deleted
        self.cursor.execute("SELECT * FROM courses WHERE id=?", (1,))
        course = self.cursor.fetchone()
        self.assertIsNone(course)

    # Test cases for enrollments table
    def test_insert_enrollment(self):
        # Test inserting an enrollment into the database
        self.cursor.execute("INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (?, ?, ?)", (1, 1, '2023-06-01'))
        self.conn.commit()
        
        # Check if the enrollment was inserted correctly
        self.cursor.execute("SELECT * FROM enrollments WHERE id=?", (self.cursor.lastrowid,))
        enrollment = self.cursor.fetchone()
        self.assertIsNotNone(enrollment)
        self.assertEqual(enrollment[1], 1)
        self.assertEqual(enrollment[2], 1)
        self.assertEqual(enrollment[3], '2023-06-01')

    # Test cases for accommodations table
    def test_insert_accommodation(self):
        # Test inserting an accommodation into the database
        self.cursor.execute("INSERT INTO accommodations (roomNo, location, type, floor, status) VALUES (?, ?, ?, ?, ?)", ('D101', 'East Wing', 'Single', 1, 'Book'))
        self.conn.commit()
        
        # Check if the accommodation was inserted correctly
        self.cursor.execute("SELECT * FROM accommodations WHERE roomNo=?", ('D101',))
        accommodation = self.cursor.fetchone()
        self.assertIsNotNone(accommodation)
        self.assertEqual(accommodation[1], 'D101')
        self.assertEqual(accommodation[2], 'East Wing')
        self.assertEqual(accommodation[3], 'Single')
        self.assertEqual(accommodation[4], 1)
        self.assertEqual(accommodation[5], 'Book')

    def test_delete_accommodation(self):
        # Test deleting an accommodation from the database
        self.cursor.execute("DELETE FROM accommodations WHERE id=?", (1,))
        self.conn.commit()
        
        # Check if the accommodation was deleted
        self.cursor.execute("SELECT * FROM accommodations WHERE id=?", (1,))
        accommodation = self.cursor.fetchone()
        self.assertIsNone(accommodation)

   

if __name__ == '__main__':
    initialize_database()
    unittest.main()
