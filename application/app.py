from flask import Flask, jsonify, request
import sqlite3
import user
import posts
import comments

app = Flask(__name__)

# Creates database with all information about user and posts
def init_db():
    con = sqlite3.connect('blogs.db')
    cursor = con.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                   User_ID INTEGER PRIMARY KEY, 
                   Username TEXT NOT NULL UNIQUE,
                   Password TEXT NOT NULL,
                   Logged_in INTEGER NOT NULL
                   )                  
''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                   Post_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   User_ID INTEGER NOT NULL, 
                   Post_title TEXT NOT NULL,
                   Description TEXT,
                   Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')      
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                   Comment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   User_ID INTEGER NOT NULL, 
                   Post_ID INTEGER NOT NULL,
                   Description TEXT NOT NULL,
                   Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(Post_ID) REFERENCES posts(Post_ID),
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')
    con.commit()
    con.close()

@app.route('/', methods=['GET'])
def home():
    return posts.home()

@app.route('/register', methods=['POST'])
def register():
    return user.register()

@app.route('/login', methods=['POST'])
def login():
    return user.login()

@app.route('/logout', methods=['POST'])
def logout():
    return user.logout()

@app.route('/post', methods=['POST'])
def add_post():
    return posts.add_post()

@app.route('/post', methods=['DELETE'])
def delete_post():
    return posts.delete_post()

@app.route('/comment', methods=['POST'])
def add_comment():
    return comments.add_comment()

@app.route('/comment', methods=['DELETE'])
def delete_comment():
    return comments.delete_comment()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
