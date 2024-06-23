import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_bcrypt import Bcrypt
from datetime import datetime
from config import Config
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)

def calculate_age(date_of_birth):
    # Convert date_of_birth to datetime object if needed
    dob = datetime.strptime(date_of_birth, '%Y-%m-%d')  # Example format; adjust as per your date format
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def get_db_connection():
    conn = sqlite3.connect('student_info_system.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            full_name = request.form['username']
            password = request.form['password']

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE full_name = ?", (full_name,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                stored_password = user['password']
                password_matches = bcrypt.check_password_hash(stored_password, password)

                if password_matches:
                    session['username'] = full_name
                    session['user_id'] = user['id']  # Set the user ID in session
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'error', 'message': 'Invalid password'})
            else:
                return jsonify({'status': 'error', 'message': 'User not found. Please register.'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'An error occurred. Please try again.'})
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the registration form data
        full_name = request.form['full_name']
        student_id = request.form['student_id']
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Add your registration logic here
        if password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (full_name, student_id, gender, password) VALUES (?, ?, ?, ?)", (full_name, student_id, gender, hashed_password))
            conn.commit()
            cur.close()
            conn.close()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
@app.route('/courses')
def index():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    total_courses = conn.execute('SELECT COUNT(*) FROM courses').fetchone()[0]
    total_enrolled = conn.execute("SELECT COUNT(*) FROM courses WHERE status='Enrolled'").fetchone()[0]
    conn.close()
    return render_template('courses.html', courses=courses, total_courses=total_courses, total_enrolled=total_enrolled)

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    course_id = data.get('course_id')

    try:
        conn = get_db_connection()
        conn.execute("UPDATE courses SET status = 'Enrolled' WHERE id = ?", (course_id,))
        conn.commit()
        conn.close()
        return jsonify(status='success')
    except sqlite3.Error as e:
        return jsonify(status='error', message=str(e))

@app.route('/drop_course', methods=['POST'])
def drop_course():
    data = request.json
    course_id = data.get('course_id')

    logging.debug(f"Dropping course with ID: {course_id}")

    try:
        conn = get_db_connection()
        conn.execute("UPDATE courses SET status = 'Available' WHERE id = ?", (course_id,))
        conn.commit()
        conn.close()
        logging.debug(f"Successfully dropped course with ID: {course_id}")
        return jsonify(status='success')
    except sqlite3.Error as e:
        logging.error(f"Error dropping course {course_id}: {e}")
        return jsonify(status='error', message=str(e))
    
@app.route('/get_accommodation/<int:accommodation_id>', methods=['GET'])
def get_accommodation(accommodation_id):
    conn = get_db_connection()
    accommodation = conn.execute('SELECT * FROM accommodations WHERE id = ?', (accommodation_id,)).fetchone()
    conn.close()

    if accommodation is None:
        return jsonify(status='error', message='Accommodation not found')

    try:
        # Ensure all expected fields are present in the fetched accommodation record
        id = accommodation['id']
        roomNo = accommodation['roomNo']
        location = accommodation['location']
        type = accommodation['type']
        floor = accommodation['floor']
    except KeyError as e:
        # Handle missing keys in accommodation record
        return jsonify(status='error', message=f'Missing key in accommodation record: {str(e)}')

    return jsonify(
        id=id,
        roomNo=roomNo,
        location=location,
        type=type,
        floor=floor
    )

@app.route('/update_accommodation', methods=['POST'])
def update_accommodation():
    data = request.json
    logging.debug(f"Received data for update: {data}")
    accommodation_id = data.get('accommodation_id')
    room_number = data.get('roomNo')
    location = data.get('location')
    type_ = data.get('type')  # rename variable to avoid conflict with Python keyword
    floor = data.get('floor')

    if not all([accommodation_id, room_number, location, type_, floor]):
        logging.error("Missing data in the update request")
        return jsonify(status='error', message='Missing data'), 400

    conn = None
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE accommodations
            SET roomNo = ?, location = ?, type = ?, floor = ?
            WHERE id = ?
        ''', (room_number, location, type_, floor, accommodation_id))
        conn.commit()
        logging.debug("Accommodation updated successfully")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return jsonify(status='error', message=str(e))
    finally:
        if conn:
            conn.close()
    return jsonify(status='success')
@app.route('/cancel_accommodation', methods=['POST'])
def cancel_accommodation():
    data = request.json
    accommodation_id = data.get('accommodation_id')

    try:
        conn = get_db_connection()
        conn.execute('UPDATE accommodations SET status = "Available" WHERE id = ?', (accommodation_id,))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify(status='error', message=str(e))
    finally:
        conn.close()
    return jsonify(status='success')

@app.route('/book_accommodation', methods=['POST'])
def book_accommodation():
    data = request.json
    accommodation_id = data.get('accommodation_id')

    try:
        conn = get_db_connection()
        conn.execute("UPDATE accommodations SET status = 'Reserved' WHERE id = ?", (accommodation_id,))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify(status='error', message=str(e))
    finally:
        conn.close()
    return jsonify(status='success')

@app.route('/accommodations')
def accommodations():
    try:
        conn = get_db_connection()
        accommodations = conn.execute('SELECT * FROM accommodations').fetchall()
    except sqlite3.Error as e:
        flash('Error fetching accommodations: ' + str(e), 'error')
        return redirect(url_for('dashboard'))
    finally:
        conn.close()

    return render_template('accomodation.html', accommodations=accommodations)

@app.route('/book_book', methods=['POST'])
def book_book():
    data = request.json
    book_id = data.get('book_id')

    try:
        conn = get_db_connection()
        # Update the status of the book to 'Booked'
        conn.execute("UPDATE books SET status = 'Booked' WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return jsonify(status='success')
    except sqlite3.Error as e:
        return jsonify(status='error', message=str(e))


def get_books():
    try:
        conn = get_db_connection()
        books = conn.execute('SELECT * FROM books').fetchall()
        conn.close()
        return books
    except sqlite3.Error as e:
        print(f"Error fetching books: {e}")
        return None

@app.route('/books')
def books():
    books = get_books()
    if books is not None:
        return render_template('books.html', books=books)
    else:
        flash('Error fetching books.','error')
        return redirect(url_for('dashboard'))
    
@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = sqlite3.connect('student_info_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return "User not found", 404

    user_data = {
        'full_name': user[1],
        'student_id': user[2],
        'gender': user[3],
        'password': user[4],
        'address': user[5],
        'school': user[6],
        'major': user[7],
        'date_of_birth': user[8],
        'photo': user[9],
        'social_links': user[10],
    }

    return render_template('profile.html', user=user_data)

# Route to handle profile update
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    full_name = request.form['full_name']
    student_id = request.form['student_id']
    gender = request.form['gender']
    password = request.form['password']
    address = request.form['address']
    school = request.form['school']
    major = request.form['major']
    date_of_birth = request.form['date_of_birth']
    photo = request.form['photo']
    social_links = request.form['social_links']

    conn = sqlite3.connect('student_info_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET full_name = ?, student_id = ?, gender = ?, password = ?, address = ?, school = ?, major = ?, date_of_birth = ?, photo = ?, social_links = ?
        WHERE id = ?
    ''', (full_name, student_id, gender, password, address, school, major, date_of_birth, photo, social_links, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('profile'))

# Mock student data
students = [
    {"name": "John Doe", "age": 22, "major": "IT"},
    {"name": "Jane Smith", "age": 21, "major": "Literature"},
    {"name": "Michael Brown", "age": 23, "major": "English"},
    {"name": "Emily Davis", "age": 20, "major": "Art"},
    # Add more students as needed
]
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/api/students')
def get_students():
    return jsonify(students)

@app.route('/api/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [student for student in students if student['id'] != student_id]
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Starting Flask app, navigate to http://127.0.0.1:5000/")
    app.run(debug=True)
