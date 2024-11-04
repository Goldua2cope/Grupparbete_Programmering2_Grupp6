from flask import jsonify
import sqlite3

def register(username, password):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO users (Username, Password) VALUES (? , ?)''', 
                    (username, password))
        con.commit()
   
def check_credentials(username, password):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        return cur.execute('''SELECT Username, Password FROM users 
                Where Username = ? AND Password = ?''', 
                (username, password)).fetchone()

def check_status(user_id):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        user_status = cur.execute('SELECT Status FROM users WHERE User_ID = ?', 
                           (user_id,)).fetchone()
        return user_status[0]

def get_user_id(username):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        user_id = cur.execute('SELECT User_ID from users WHERE Username = ?', 
                           (username,)).fetchone()
        return user_id[0]

def change_status(user_id, value):
    with sqlite3.connect('blogg_data.db') as con: 
        cur = con.cursor()
        cur.execute('UPDATE users SET Status = ? WHERE User_ID = ?',
                    (value, user_id))
        con.commit()

def check_login(session):
    print(session)
    if 'username' in session and check_status(session['user_id']) == 1:
        return True
    return False
