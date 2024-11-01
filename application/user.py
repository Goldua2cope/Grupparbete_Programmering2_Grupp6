from flask import jsonify, request , session 
from app import app
import sqlite3

# Register a new user

def register():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')
    password = data.get('Password')

    with sqlite3.connect('blogs.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE Username= ?',(username,))
            
            if cur.fetchone():
                 return jsonify({'Error':'Username already exists.'})
        
            try:
                cur.execute('''INSERT INTO users (Username, Password) VALUES (? , ?)''', (username, password))
                con.commit()
                return jsonify({'Message': 'User successfully created.'}), 201
            except sqlite3.IntegrityError:
                return jsonify({'Error': 'Invalid data.'}) , 400

# Login 

def login():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')
    password = data.get('Password')

    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()
    # Find if username, password match a specific user
        cur.execute('''SELECT Username, Password FROM users 
                Where Username = ? AND Password = ?''', (username, password))
        user = cur.fetchone()
    
    # check if user exists
        if user:
            session['username'] = username
            return jsonify({'Message': 'Welcome! You are now logged in.'}), 200
        else:
            return jsonify({'Error': 'Wrong credentials.'}), 404
    
def logout():
    # Save received json data in variables
    if 'username' in session:
        session.pop('username', None) 
        return jsonify({'Message': 'You are now logged out.'}), 200
    else: 
        return jsonify({'Error': 'You are not logged in.'}), 400
