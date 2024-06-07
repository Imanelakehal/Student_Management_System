import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

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

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE full_name = %s", (full_name,))
            user = cur.fetchone()
            cur.close()

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
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (full_name, student_id, gender, password) VALUES (%s, %s, %s, %s)", (full_name, student_id, gender, hashed_password))
            mysql.connection.commit()
            cur.close()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Passwords do not match'})

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
