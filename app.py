# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

users = {}  # In-memory user storage

def load_users():
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split(',')
                users[username] = password

def save_user(username, password):
    with open('users.txt', 'a') as f:
        f.write(f"{username},{password}\n")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists. Try logging in."
        else:
            users[username] = password
            save_user(username, password)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('secured'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/secured')
def secured():
    if 'username' in session:
        return f"Welcome {session['username']}! This is a secured page."
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    load_users()
    app.run(debug=True)
