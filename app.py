from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'users.db'


# Function to get DB connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Home page: Login or Register
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
            return redirect(url_for('register'))

    return render_template('register.html')


# Dashboard for logged-in users
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))


# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
