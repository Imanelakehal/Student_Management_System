import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)

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

            print(f"Received login attempt for full_name: {full_name}")
            print(f"Entered password (raw): {password}")

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE full_name = ?", (full_name,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                print(f"User found in database: {user}")
                stored_password = user['password']  # Accessing dictionary key
                print(f"Stored password hash: {stored_password}")

                # Check the password using bcrypt
                password_matches = bcrypt.check_password_hash(stored_password, password)
                print(f"Password matches: {password_matches}")

                if password_matches:
                    session['username'] = full_name
                    print("Password matches, login successful")
                    return jsonify({'status': 'success'})
                else:
                    print("Invalid password")
                    return jsonify({'status': 'error', 'message': 'Invalid password'})
            else:
                print("User not found")
                return jsonify({'status': 'error', 'message': 'User not found. Please register.'})
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'status': 'error', 'message': 'An error occurred. Please try again.'})
    else:  # Handle GET requests
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

if __name__ == '__main__':
    app.run(debug=True)
