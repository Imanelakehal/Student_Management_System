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
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.check_password_hash(user[2], password):  # Assuming password is in the 2nd column
                session['username'] = username
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid password'})
        else:
            return jsonify({'status': 'error', 'message': 'User not found. Please register.'})

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
