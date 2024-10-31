from flask import jsonify, request
import sqlite3

# TODO: KOLLA HUR SESSIONS FUNGERAR FÖR ATT SPÅRA VILKEN ANVÄNDARE ÄR INLOGGAD

# Register a new user
def register():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')
    password = data.get('Password')

    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()

    # Insert new user if username doesn't already exists
        try:
            cur.execute('INSERT INTO users (Username, Password, Logged_in) VALUES (?, ?, ?)', (username, password, 0))
            con.commit()
            return jsonify({'Message': 'User successfully created.'}), 201
        except sqlite3.OperationalError:
            return jsonify({'Error': 'Username already exists.'}), 400
        except sqlite3.IntegrityError:
            return jsonify({'Error': 'You need to give a valid "Username" and "Password".'})

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

    # If exists, change loging status in db
        if cur.fetchone():
            cur.execute('''UPDATE users 
                        SET Logged_in = 1
                        Where Username = ?''', (username,))
            con.commit()
            return jsonify({'Message': 'Welcome! You are now logged in.'}), 200
        else:
            return jsonify({'Error': 'Wrong credentials.'}), 404
    
def logout():
    # Save received json data in variables
    data = request.get_json()
    username = data.get('Username')

    with sqlite3.connect('blogs.db') as con:
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
            return jsonify({'Message': 'You are now logged out.'}), 200
        else: 
            return jsonify({'Error': 'You are not logged in.'}), 400