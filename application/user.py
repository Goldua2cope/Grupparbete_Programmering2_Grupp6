from flask import jsonify, request , session 
import sqlite3

# Register a new user

def register():
     # Save received json data in variables
    data = request.get_json(silent=True)
    if data is None:
        return  jsonify({'Error':'Null value.'})
    username = data.get('Username')
    password = data.get('Password')

    if not username or not password: #if it's wrong spelling
        return jsonify({'Error': 'Username and Password are required.'}), 400

    with sqlite3.connect('blogs.db') as con:
            cur = con.cursor()
            user =cur.execute('SELECT * FROM users WHERE Username= ?',(username,)).fetchone()
            
            if user:
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
    data = request.get_json(silent=True)
    if data is None:
        return  jsonify({'Error':'Null value.'})
    username = data.get('Username')
    password = data.get('Password')

    if not username or not password:
        return jsonify({'Error': 'Username and Password are required.'}) , 400

    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()

    # Find if username, password match a specific user 
        cur.execute('''SELECT User_ID, Username, Password FROM users 
                Where Username = ? AND Password = ?''', (username, password))
        user = cur.fetchone()
    
    # check if user exists
        if user: ##### in session har nu både User_ID (element[0]från table och Username-element[1])
            session['user_id'] = user[0]
            session['username'] = user[1]
            return jsonify({'Message': 'Welcome! You are now logged in.'}), 200
        else:
            return jsonify({'Error': 'Wrong credentials.'}), 404

def logout():
    # Save received json data in variables
    if 'username' in session:
        session.clear() #### jag använder inte .pop för att i session finns nu både username and user_id
       # session.pop('username', None)
        print("Session after logout:", dict(session)) #### bara för att se om session är tom, kan tas bort
        response = jsonify({'Message': 'You are now logged out.'})
        #response.set_cookie('session', '',expires=0) #https://medium.com/@sujathamudadla1213/what-is-the-use-of-cookies-in-flask-530873e068e8
        return response , 200
    else: 
        return jsonify({'Error': 'You are not logged in.'}), 400
