from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

#Configuration for secret key (required for session managment)
app.config['SECRET_KEY'] = 'imane'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Process the login form
        username = request.form['Username']
        password = request.form['Password']
        #Authentication logic
        return redirect(url_for('dashboard'))
    return render_template('/templates/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('/templates/dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)