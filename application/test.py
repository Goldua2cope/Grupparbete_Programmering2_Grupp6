from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')
    password = data.get('Password')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()

    # Insert new user if username doesn't already exists
    try:
        cur.execute('INSERT INTO users (Username, Password, Logged_in) VALUES (?, ?, ?)', (username, password, 0))
        con.commit()
        con.close()
        return jsonify({'Message': 'User successfully created.'}), 201
    except sqlite3.IntegrityError:
        con.close()
        return jsonify({'Error': 'Username already exists.'}), 400

# Login 
@app.route('/login', methods=['POST'])
def login():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')
    password = data.get('Password')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()

    # Find if username, password match a specific user
    cur.execute('''SELECT Username, Password FROM users 
                Where Username = ? AND Password = ?''', (username, password))

    # If exists, change loging status in db
    if cur.fetchone():
        cur.execute('''UPDATE users 
                    SET Logged_in = 1
                    Where Username = ?''', (username,))
        con.commit()
        con.close()
        return jsonify({'Message': 'Welcome! You are now logged in.'}), 200
    else:
        con.close()
        return jsonify({'Error': 'Wrong credentials.'}), 404
    
@app.route('/logout', methods=['POST'])
def logout():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()

    # Check if user is logged in
    cur.execute('''SELECT Logged_in FROM users 
                Where Username = ?''', (username,))
    
    # If match is a tuple (1,0) which means logged in
    if cur.fetchone() == (1,):
        cur.execute('''UPDATE users 
                    SET Logged_in = 0
                    Where Username = ?''', (username,))
        con.commit()
        con.close()
        return jsonify({'Message': 'You are now logged out.'}), 200
    else: 
        return jsonify({'Error': 'You are not logged in.'}), 400