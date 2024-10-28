from flask import Flask
import sqlite3

app = Flask(__name__)

# Creates database with all information about user and posts
def init_db():
    con = sqlite3.connect('blogs.db')
    cursor = con.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                   User_ID INTEGER PRIMARY KEY, 
                   USERNAME TEXT NOT NULL,
                   PASSWORD TEXT NOT NULL
                   )                  
''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                   Post_ID AUTO_INCREMENT PRIMARY KEY,
                   User_ID INTEGER NOT NULL, 
                   Post_title TEXT NOT NULL,
                   Description TEXT,
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')      
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                   Comment_ID AUTO_INCREMENT PRIMARY KEY,
                   USER_ID INTEGER NOT NULL, 
                   Post_ID INTEGER NOT NULL,
                   Description TEXT NOT NULL,
                   FOREIGN KEY(Post_ID) REFERENCES posts(Post_ID)
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')
    con.commit()
    con.close()

init_db()

@app.route('')

